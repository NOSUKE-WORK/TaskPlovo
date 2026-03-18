"""
TaskDialog - i18n対応版
"""
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import datetime, threading, sys, os
import i18n
from .date_picker import DatePickerDialog

PRESET_COLORS = [
    "#4F7EFF","#FF6B6B","#43D9A2","#FFB347",
    "#A78BFA","#38BDF8","#F472B6","#FBBF24",
    "#6EE7B7","#FCA5A5","#93C5FD","#C4B5FD",
]


class TaskDialog(ttk.Toplevel):
    def __init__(self, parent, store, config=None, task=None, default_start=None):
        super().__init__(parent)
        self.withdraw()
        self.store         = store
        self.task          = task
        self.default_start = default_start
        self._cfg          = config or {}

        self.title(i18n.get(self._cfg, "dlg_edit_title" if task else "dlg_add_title"))
        self.resizable(False, True)
        self.grab_set()
        self.transient(parent)
        self.geometry("500x620")

        base = sys._MEIPASS if getattr(sys,"frozen",False) else \
               os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ico = os.path.join(base, "assets", "icon.ico")
        if os.path.exists(ico):
            try: self.iconbitmap(ico)
            except Exception: pass

        self._start_date  = tk.StringVar()
        self._due_date    = tk.StringVar()
        self._due_time_h  = tk.StringVar(value="12")
        self._due_time_m  = tk.StringVar(value="00")
        self._label_color = tk.StringVar(value=PRESET_COLORS[0])

        if task:
            self._start_date.set(task.get("start_date",""))
            self._due_date.set(task.get("due_date",""))
            self._label_color.set(task.get("label_color", PRESET_COLORS[0]))
            due_time = task.get("due_time","12:00")
            parts = due_time.split(":")
            self._due_time_h.set(f"{int(parts[0]):02d}" if parts else "12")
            raw_m = int(parts[1]) if len(parts)>1 else 0
            self._due_time_m.set("30" if raw_m>=30 else "00")
        elif default_start:
            self._start_date.set(default_start.isoformat())
            self._due_date.set(default_start.isoformat())
        else:
            # メニューから開いた場合は今日の日付をデフォルトに
            today = datetime.date.today().isoformat()
            self._start_date.set(today)
            self._due_date.set(today)

        self._build()
        self._center(parent)

    def _t(self, key): return i18n.get(self._cfg, key)

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width()//2
        ph = parent.winfo_rooty() + parent.winfo_height()//2
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{pw-w//2}+{ph-h//2}")
        self.deiconify()

    def _build(self):
        canvas = tk.Canvas(self, highlightthickness=0)
        vsb    = ttk.Scrollbar(self, orient="vertical", command=canvas.yview, bootstyle="round")
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner  = ttk.Frame(canvas)
        win_id = canvas.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)),"units"))

        mode = self._cfg.get("app_mode","dark")
        FG   = "#f0f0f0" if mode=="dark" else "#1a1a1a"
        FG_S = "#bbbbbb" if mode=="dark" else "#444444"
        pad  = {"padx":24, "pady":5}

        # タイトル
        ttk.Label(inner, text=self._t("lbl_task_title"),
                  font=("Yu Gothic UI",9), foreground=FG_S
                  ).pack(anchor="w", padx=24, pady=(20,2))
        title_row = ttk.Frame(inner)
        title_row.pack(fill="x", padx=24, pady=(0,4))
        self.ent_title = ttk.Entry(title_row, font=("Yu Gothic UI",11))
        self.ent_title.pack(side="left", fill="x", expand=True)
        self.mic_btn = ttk.Button(title_row, text="🎤",
                                  bootstyle="outline-secondary",
                                  width=3, command=lambda: self._start_voice("title"))
        self.mic_btn.pack(side="left", padx=(6,0))
        self.voice_status = ttk.Label(inner, text="", font=("Yu Gothic UI",9), bootstyle="info")
        self.voice_status.pack(anchor="w", padx=24)
        if self.task: self.ent_title.insert(0, self.task.get("title",""))

        # 詳細
        detail_hdr = ttk.Frame(inner)
        detail_hdr.pack(fill="x", padx=24, pady=(8,2))
        ttk.Label(detail_hdr, text=self._t("lbl_detail"),
                  font=("Yu Gothic UI",9), foreground=FG_S).pack(side="left")
        ttk.Button(detail_hdr, text="🎤", bootstyle="outline-secondary",
                   width=3, command=lambda: self._start_voice("detail")).pack(side="right")
        self.txt_detail = tk.Text(inner, height=3, font=("Yu Gothic UI",10),
                                  relief="flat", highlightthickness=1)
        self.txt_detail.pack(fill="x", **pad)
        if self.task: self.txt_detail.insert("1.0", self.task.get("detail",""))

        # 日付
        date_row = ttk.Frame(inner)
        date_row.pack(fill="x", padx=24, pady=(6,0))
        left = ttk.Frame(date_row)
        left.pack(side="left", fill="x", expand=True, padx=(0,8))
        ttk.Label(left, text=self._t("lbl_start_date"),
                  font=("Yu Gothic UI",9), foreground=FG_S).pack(anchor="w", pady=(0,2))
        self._date_field(left, self._start_date)
        right = ttk.Frame(date_row)
        right.pack(side="left", fill="x", expand=True)
        ttk.Label(right, text=self._t("lbl_due_date"),
                  font=("Yu Gothic UI",9), foreground=FG_S).pack(anchor="w", pady=(0,2))
        self._date_field(right, self._due_date)

        # 〆時刻
        ttk.Label(inner, text=self._t("lbl_due_time"),
                  font=("Yu Gothic UI",9), foreground=FG_S
                  ).pack(anchor="w", padx=24, pady=(10,3))
        time_inner = ttk.Frame(inner)
        time_inner.pack(anchor="w", padx=24)
        ttk.Combobox(time_inner, textvariable=self._due_time_h,
                     values=[f"{h:02d}" for h in range(24)],
                     state="readonly", width=5, font=("Yu Gothic UI",11)).pack(side="left")
        ttk.Label(time_inner, text="：", font=("Yu Gothic UI",13,"bold")).pack(side="left", padx=4)
        ttk.Combobox(time_inner, textvariable=self._due_time_m,
                     values=["00","30"], state="readonly", width=5,
                     font=("Yu Gothic UI",11)).pack(side="left")
        ttk.Label(time_inner, text=self._t("lbl_time_until"),
                  font=("Yu Gothic UI",10), foreground=FG_S).pack(side="left", padx=(8,0))

        # タスクラベル色
        ttk.Label(inner, text=self._t("lbl_label_color"),
                  font=("Yu Gothic UI",9), foreground=FG_S
                  ).pack(anchor="w", padx=24, pady=(12,4))
        swatch_frame = tk.Frame(inner)
        swatch_frame.pack(anchor="w", padx=24)
        self._color_buttons = {}
        SWATCH_W, SWATCH_H = 28, 22
        for i, col in enumerate(PRESET_COLORS):
            cv = tk.Canvas(swatch_frame, width=SWATCH_W, height=SWATCH_H,
                           highlightthickness=0, cursor="hand2")
            cv.grid(row=0, column=i, padx=2, pady=2)
            rect_id = cv.create_rectangle(0, 0, SWATCH_W, SWATCH_H, fill=col, outline=col)
            cv.bind("<Button-1>", lambda e, c=col: self._pick_color(c))
            self._color_buttons[col] = (cv, rect_id, col)

        prev_row = tk.Frame(inner)
        prev_row.pack(fill="x", padx=24, pady=(6,0))
        tk.Label(prev_row, text=self._t("lbl_selected"),
                 font=("Yu Gothic UI",9), fg=FG_S).pack(side="left")
        self.color_preview = tk.Canvas(prev_row, width=40, height=20,
                                       highlightthickness=1, highlightbackground="#888888")
        self.color_preview.pack(side="left", padx=(4,0))
        self._preview_rect = self.color_preview.create_rectangle(
            0, 0, 40, 20, fill=PRESET_COLORS[0], outline=PRESET_COLORS[0])
        self.color_preview_text = tk.Label(prev_row, text="", font=("Yu Gothic UI",9), fg=FG_S)
        self.color_preview_text.pack(side="left", padx=(6,0))
        self._update_color_preview()

        # 備考
        note_hdr = ttk.Frame(inner)
        note_hdr.pack(fill="x", padx=24, pady=(12,2))
        ttk.Label(note_hdr, text=self._t("lbl_note"),
                  font=("Yu Gothic UI",9), foreground=FG_S).pack(side="left")
        ttk.Button(note_hdr, text="🎤", bootstyle="outline-secondary",
                   width=3, command=lambda: self._start_voice("note")).pack(side="right")
        self.txt_note = tk.Text(inner, height=3, font=("Yu Gothic UI",10),
                                relief="flat", highlightthickness=1)
        self.txt_note.pack(fill="x", **pad)
        if self.task: self.txt_note.insert("1.0", self.task.get("note",""))

        # ボタン
        btn_row = ttk.Frame(inner)
        btn_row.pack(fill="x", padx=24, pady=(16,20))
        ttk.Button(btn_row, text=self._t("btn_cancel"), bootstyle="outline-secondary",
                   command=self.destroy).pack(side="right", padx=(8,0))
        ttk.Button(btn_row, text=self._t("btn_save"), bootstyle="primary",
                   command=self._save).pack(side="right")
        if self.task:
            ttk.Button(btn_row, text=self._t("btn_delete"), bootstyle="outline-danger",
                       command=self._delete).pack(side="left")

    def _date_field(self, parent, var):
        row = ttk.Frame(parent)
        row.pack(fill="x")
        lbl = ttk.Label(row, textvariable=var, font=("Yu Gothic UI",10), width=14, anchor="w")
        lbl.pack(side="left", padx=8, pady=6)
        btn = ttk.Label(row, text="📅", cursor="hand2")
        btn.pack(side="right", padx=6)
        for w in (row, lbl, btn):
            w.bind("<Button-1>", lambda e, v=var: self._pick_date(v))

    def _pick_date(self, var):
        try: initial = datetime.date.fromisoformat(var.get())
        except Exception: initial = datetime.date.today()
        dlg = DatePickerDialog(self, initial_date=initial)
        self.wait_window(dlg)
        if dlg.result: var.set(dlg.result.isoformat())

    def _pick_color(self, color):
        self._label_color.set(color)
        self._update_color_preview()

    def _update_color_preview(self):
        c = self._label_color.get()
        if not c or c == "auto":
            c = PRESET_COLORS[0]
            self._label_color.set(c)
        self.color_preview.itemconfig(self._preview_rect, fill=c, outline=c)
        self.color_preview_text.config(text="")
        for col, (cv, rect_id, orig) in self._color_buttons.items():
            if col == c:
                cv.itemconfig(rect_id, outline="white")
                cv.config(highlightthickness=2, highlightbackground="white")
            else:
                cv.itemconfig(rect_id, outline=orig)
                cv.config(highlightthickness=0)

    def _start_voice(self, target="title"):
        try:
            import speech_recognition as sr
        except ImportError:
            messagebox.showwarning("Voice", self._t("voice_missing"), parent=self)
            return
        self._voice_target = target
        self.voice_status.config(text=self._t("voice_listening"))
        if target == "title": self.mic_btn.config(bootstyle="outline-danger")
        self.update()

        def run():
            recognizer = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
                result = recognizer.recognize_google(audio, language="ja-JP")
                self.after(0, lambda: self._voice_ok(result))
            except sr.WaitTimeoutError:
                self.after(0, lambda: self._voice_err(self._t("voice_timeout")))
            except sr.UnknownValueError:
                self.after(0, lambda: self._voice_err(self._t("voice_unknown")))
            except Exception as ex:
                self.after(0, lambda: self._voice_err(self._t("voice_error")+str(ex)))

        threading.Thread(target=run, daemon=True).start()

    def _voice_ok(self, text):
        target = getattr(self, "_voice_target", "title")
        if target == "title":
            self.ent_title.delete(0, "end"); self.ent_title.insert(0, text)
            self.mic_btn.config(bootstyle="outline-secondary")
        elif target == "detail": self.txt_detail.insert("end", text)
        elif target == "note":   self.txt_note.insert("end", text)
        self.voice_status.config(text=self._t("voice_ok")+text)

    def _voice_err(self, msg):
        self.voice_status.config(text=f"❌ {msg}")
        if hasattr(self,"mic_btn"): self.mic_btn.config(bootstyle="outline-secondary")

    def _save(self):
        title  = self.ent_title.get().strip()
        detail = self.txt_detail.get("1.0","end").strip()
        start  = self._start_date.get().strip()
        due    = self._due_date.get().strip()
        note   = self.txt_note.get("1.0","end").strip()
        lcolor = self._label_color.get()
        try:
            h = int(self._due_time_h.get()); m = int(self._due_time_m.get())
            due_time = f"{max(0,min(23,h)):02d}:{max(0,min(59,m)):02d}"
        except ValueError:
            due_time = "12:00"

        err = self._t("err_input")
        if not title:
            messagebox.showwarning(err, self._t("err_title_empty"), parent=self); return
        if not start:
            messagebox.showwarning(err, self._t("err_start_empty"), parent=self); return
        if not due:
            messagebox.showwarning(err, self._t("err_due_empty"),   parent=self); return
        try:
            s = datetime.date.fromisoformat(start)
            e = datetime.date.fromisoformat(due)
            if e < s:
                messagebox.showwarning(err, self._t("err_date_order"), parent=self); return
        except ValueError:
            messagebox.showwarning(err, self._t("err_date_format"), parent=self); return

        if self.task:
            self.store.update(self.task["id"], title=title, detail=detail,
                              start_date=start, due_date=due, due_time=due_time,
                              note=note, label_color=lcolor)
        else:
            self.store.add(title, detail, start, due, note,
                           label_color=lcolor, due_time=due_time)
        self.destroy()

    def _delete(self):
        if messagebox.askyesno(self._t("confirm_delete"),
                               f"「{self.task['title']}」{self._t('confirm_delete_msg')}",
                               parent=self):
            self.store.delete(self.task["id"])
            self.destroy()
