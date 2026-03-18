"""
TaskPlovo - アプリケーションコア
"""
import sys
import os
import json
import winreg
import threading

APP_NAME      = "TaskPlovo"
APP_VERSION   = "1.06"
STARTUP_KEY   = r"Software\Microsoft\Windows\CurrentVersion\Run"

def get_exe_path():
    if getattr(sys, 'frozen', False):
        return sys.executable
    return os.path.abspath(sys.argv[0])

def get_data_dir():
    appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
    d = os.path.join(appdata, "TaskPlovo")
    os.makedirs(d, exist_ok=True)
    return d


class TaskPlovoApp:
    def __init__(self):
        self.data_dir    = get_data_dir()
        self.config_path = os.path.join(self.data_dir, "config.json")
        self.config      = self._load_config()
        self.root        = None
        self.tray_icon   = None

    def _load_config(self):
        defaults = {
            "startup_enabled": True,
            "close_to_tray":   True,
            "app_mode":        "dark",
            "language":        "ja",
        }
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    defaults.update(json.load(f))
            except Exception:
                pass
        return defaults

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def set_startup(self, enabled: bool):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY,
                                 0, winreg.KEY_SET_VALUE)
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ,
                                  f'"{get_exe_path()}"')
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[startup] {e}")

    # ── トレイアイコン ────────────────────────────────────
    def _build_tray(self):
        try:
            import pystray
            from PIL import Image
        except ImportError:
            return

        # icon.png が存在すればそれを使う、なければフォールバック
        import sys, os
        if getattr(sys, 'frozen', False):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base, "assets", "icon.png")

        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((64, 64), Image.LANCZOS)
        else:
            # フォールバック：シンプルな青四角
            from PIL import ImageDraw
            img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            dd  = ImageDraw.Draw(img)
            dd.rounded_rectangle([4, 4, 60, 60], radius=12, fill="#1565C0")

        menu = pystray.Menu(
            pystray.MenuItem("TaskPlovo を開く", self._show_window, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("終了", self._quit),
        )
        self.tray_icon = pystray.Icon(APP_NAME, img, APP_NAME, menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def _show_window(self, *_):
        if self.root:
            self.root.after(0, lambda: (
                self.root.deiconify(),
                self.root.lift(),
                self.root.focus_force()
            ))

    def _hide_window(self):
        self.root.withdraw()

    def _quit(self, *_):
        if self.tray_icon:
            self.tray_icon.stop()
        if self.root:
            self.root.after(0, self.root.destroy)

    def _on_close(self):
        if self.config.get("close_to_tray") and self.tray_icon:
            self._hide_window()
        else:
            self._quit()

    def run(self):
        if self.config.get("startup_enabled", True):
            self.set_startup(True)

        import ttkbootstrap as ttk
        from data.task_store import TaskStore
        from ui.main_window  import MainWindow

        store = TaskStore(os.path.join(self.data_dir, "tasks.json"))

        theme = "darkly" if self.config.get("app_mode", "dark") == "dark" else "flatly"
        self.root = ttk.Window(themename=theme)
        self.root.withdraw()
        self.root.title(APP_NAME)
        self.root.geometry("1280x800")
        self.root.minsize(960, 640)

        win = MainWindow(self.root, store, self.config, self)
        win.pack(fill="both", expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_tray()
        self.root.deiconify()

        # ttkbootstrap の初期化完了後にアイコンを設定（上書きされないよう遅延）
        self.root.after(100, self._set_window_icon)

        self.root.mainloop()

    def _set_window_icon(self):
        """ウィンドウ左上アイコンを icon.ico から設定"""
        import sys, os
        if getattr(sys, 'frozen', False):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base, "assets", "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"[icon] {e}")
