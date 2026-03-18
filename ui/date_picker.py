"""
DatePickerDialog - ttkbootstrap版カレンダー日付選択
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import datetime
import calendar

DAYS_JP  = ["月","火","水","木","金","土","日"]
SAT_FG   = "#5B9BD5"
SUN_FG   = "#E05252"

def week_fg(col):
    if col == 5: return SAT_FG
    if col == 6: return SUN_FG
    return None  # デフォルト色


class DatePickerDialog(ttk.Toplevel):
    def __init__(self, parent, initial_date=None):
        super().__init__(parent)
        self.withdraw()
        self.result  = None
        today        = datetime.date.today()
        self._date   = initial_date or today
        self._view_y = self._date.year
        self._view_m = self._date.month

        self.title("日付を選択")
        self.resizable(False, False)
        self.grab_set()
        self.transient(parent)
        self.geometry("310x290")

        # アイコン設定
        import sys, os
        base = sys._MEIPASS if getattr(sys, "frozen", False) else \
               os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ico = os.path.join(base, "assets", "icon.ico")
        if os.path.exists(ico):
            try: self.iconbitmap(ico)
            except Exception: pass

        self._build()
        self._draw()
        self._center(parent)

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width()  // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"+{pw-self.winfo_width()//2}+{ph-self.winfo_height()//2}")
        self.deiconify()

    def _build(self):
        nav = ttk.Frame(self)
        nav.pack(fill="x", padx=12, pady=(12, 6))
        ttk.Button(nav, text="◀", bootstyle="outline-secondary",
                   width=3, command=self._prev).pack(side="left")
        self.nav_label = ttk.Label(nav, text="",
                                   font=("Yu Gothic UI", 12, "bold"), width=14,
                                   anchor="center")
        self.nav_label.pack(side="left", expand=True)
        ttk.Button(nav, text="▶", bootstyle="outline-secondary",
                   width=3, command=self._next).pack(side="right")

        days_row = ttk.Frame(self)
        days_row.pack(fill="x", padx=12)
        for i, d in enumerate(DAYS_JP):
            fg = week_fg(i)
            lbl = ttk.Label(days_row, text=d,
                            font=("Yu Gothic UI", 9, "bold"), width=4,
                            anchor="center")
            if fg:
                lbl.config(foreground=fg)
            lbl.grid(row=0, column=i)
            days_row.columnconfigure(i, weight=1)

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(fill="x", padx=12, pady=(0, 12))

    def _draw(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        y, m = self._view_y, self._view_m
        self.nav_label.config(text=f"{y}年 {m}月")
        today     = datetime.date.today()
        first_dow = datetime.date(y, m, 1).weekday()
        days_in_m = calendar.monthrange(y, m)[1]

        slot = 0
        for r in range(6):
            for c in range(7):
                do = slot - first_dow
                if 0 <= do < days_in_m:
                    d    = datetime.date(y, m, do+1)
                    sel  = (d == self._date)
                    tod  = (d == today)
                    fg   = week_fg(c)

                    if sel:
                        btn = ttk.Button(
                            self.grid_frame, text=str(d.day),
                            bootstyle="primary", width=3,
                            command=lambda dt=d: self._select(dt)
                        )
                    elif tod:
                        btn = ttk.Button(
                            self.grid_frame, text=str(d.day),
                            bootstyle="outline-primary", width=3,
                            command=lambda dt=d: self._select(dt)
                        )
                    else:
                        btn = ttk.Button(
                            self.grid_frame, text=str(d.day),
                            bootstyle="link", width=3,
                            command=lambda dt=d: self._select(dt)
                        )
                    if fg and not sel:
                        try: btn.config(foreground=fg)
                        except Exception: pass
                    btn.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                    self.grid_frame.columnconfigure(c, weight=1)
                else:
                    ttk.Label(self.grid_frame, text="", width=3
                              ).grid(row=r, column=c)
                slot += 1

    def _prev(self):
        if self._view_m == 1: self._view_m=12; self._view_y-=1
        else: self._view_m-=1
        self._draw()

    def _next(self):
        if self._view_m == 12: self._view_m=1; self._view_y+=1
        else: self._view_m+=1
        self._draw()

    def _select(self, d):
        self.result = d
        self.destroy()
