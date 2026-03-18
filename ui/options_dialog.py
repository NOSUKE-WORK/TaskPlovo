"""
OptionsDialog - i18n対応版（言語設定追加）
"""
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys, os
import i18n


class OptionsDialog(ttk.Toplevel):
    def __init__(self, parent, config: dict, app_ref):
        super().__init__(parent)
        self.withdraw()
        self.config  = config
        self.app     = app_ref

        self.title(i18n.get(config, "opt_title"))
        self.resizable(False, False)
        self.grab_set()
        self.transient(parent)
        self.geometry("460x580")

        base = sys._MEIPASS if getattr(sys,"frozen",False) else \
               os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ico = os.path.join(base, "assets", "icon.ico")
        if os.path.exists(ico):
            try: self.iconbitmap(ico)
            except Exception: pass

        self._mode_var       = tk.StringVar(value=config.get("app_mode",        "dark"))
        self._lang_var       = tk.StringVar(value=config.get("language",         "ja"))
        self._startup_var    = tk.BooleanVar(value=config.get("startup_enabled", True))
        self._close_tray_var = tk.BooleanVar(value=config.get("close_to_tray",   True))

        self._build()
        self._center(parent)

    def _t(self, key): return i18n.get(self.config, key)

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width()//2
        ph = parent.winfo_rooty() + parent.winfo_height()//2
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{pw-w//2}+{ph-h//2}")
        self.deiconify()

    def _build(self):
        mode = self.config.get("app_mode","dark")
        FG   = "#f0f0f0" if mode=="dark" else "#1a1a1a"
        FG_S = "#bbbbbb" if mode=="dark" else "#444444"

        ttk.Label(self, text=self._t("opt_title"),
                  font=("Yu Gothic UI",13,"bold"), foreground=FG
                  ).pack(anchor="w", padx=24, pady=(20,4))

        # ── アプリモード ──────────────────────────────────
        ttk.Label(self, text=self._t("opt_app_mode"),
                  font=("Yu Gothic UI",11,"bold"), foreground=FG
                  ).pack(anchor="w", padx=24, pady=(14,5))
        mode_f = ttk.Frame(self)
        mode_f.pack(fill="x", padx=20, pady=(0,4))
        inner  = ttk.Frame(mode_f)
        inner.pack(fill="x", padx=16, pady=12)
        for val, lbl_key, desc_key in [
            ("dark",  "opt_dark",  "opt_dark_desc"),
            ("light", "opt_light", "opt_light_desc"),
        ]:
            f = ttk.Frame(inner)
            f.pack(side="left", expand=True, fill="x", padx=6)
            ttk.Radiobutton(f, text=self._t(lbl_key),
                            variable=self._mode_var, value=val,
                            bootstyle="toolbutton-primary").pack(fill="x")
            ttk.Label(f, text=self._t(desc_key),
                      font=("Yu Gothic UI",8), foreground=FG_S).pack(anchor="w", padx=4)

        # ── 言語設定 ──────────────────────────────────────
        ttk.Label(self, text=self._t("opt_language"),
                  font=("Yu Gothic UI",11,"bold"), foreground=FG
                  ).pack(anchor="w", padx=24, pady=(14,5))
        lang_f = ttk.Frame(self)
        lang_f.pack(fill="x", padx=20, pady=(0,4))
        lang_inner = ttk.Frame(lang_f)
        lang_inner.pack(fill="x", padx=16, pady=12)
        for val, label in [("ja","🇯🇵 日本語"), ("en","🇺🇸 English")]:
            f = ttk.Frame(lang_inner)
            f.pack(side="left", expand=True, fill="x", padx=6)
            ttk.Radiobutton(f, text=label,
                            variable=self._lang_var, value=val,
                            bootstyle="toolbutton-primary").pack(fill="x")

        # ── 動作設定 ──────────────────────────────────────
        ttk.Label(self, text=self._t("opt_behavior"),
                  font=("Yu Gothic UI",11,"bold"), foreground=FG
                  ).pack(anchor="w", padx=24, pady=(14,5))
        sys_f = ttk.Frame(self)
        sys_f.pack(fill="x", padx=20, pady=(0,4))
        for var, text_key, desc_key in [
            (self._startup_var,    "opt_startup", "opt_startup_desc"),
            (self._close_tray_var, "opt_tray",    "opt_tray_desc"),
        ]:
            row = ttk.Frame(sys_f)
            row.pack(fill="x", padx=8, pady=5)
            ttk.Checkbutton(row, text=self._t(text_key), variable=var,
                            bootstyle="primary-round-toggle").pack(anchor="w")
            ttk.Label(row, text=self._t(desc_key),
                      font=("Yu Gothic UI",8), foreground=FG_S).pack(anchor="w", padx=28)

        # ── ボタン ────────────────────────────────────────
        btn_row = ttk.Frame(self)
        btn_row.pack(fill="x", padx=24, pady=(16,20))
        ttk.Button(btn_row, text=self._t("btn_cancel"), bootstyle="outline-secondary",
                   command=self.destroy).pack(side="right", padx=(8,0))
        ttk.Button(btn_row, text=self._t("opt_save"), bootstyle="primary",
                   command=self._save).pack(side="right")

    def _save(self):
        self.config["app_mode"]        = self._mode_var.get()
        self.config["language"]         = self._lang_var.get()
        self.config["startup_enabled"] = self._startup_var.get()
        self.config["close_to_tray"]   = self._close_tray_var.get()

        self.app.set_startup(self.config["startup_enabled"])
        self.app.save_config()

        messagebox.showinfo(self._t("opt_saved"), self._t("opt_saved_msg"), parent=self)
        self.destroy()
