"""Left sidebar with collapsible category groups."""
import tkinter as tk
from gui.theme import *


class Sidebar(tk.Frame):
    def __init__(self, parent, on_select):
        super().__init__(parent, bg=BG_DARK, width=220)
        self.pack_propagate(False)
        self.on_select = on_select
        self._active_key = None
        self._active_btn = None
        self._build()

    def _build(self):
        # Logo / title
        hdr = tk.Frame(self, bg=ACCENT, padx=16, pady=14)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="⬛ PDF Tools", font=("Segoe UI", 13, "bold"),
                 bg=ACCENT, fg=WHITE).pack(anchor="w")

        # Scrollable container
        canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        self.inner = tk.Frame(canvas, bg=BG_DARK)
        self.inner.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Mouse-wheel scroll
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        for cat_label, _cat_key, ops in CATEGORIES:
            self._add_category(cat_label, ops)

    def _add_category(self, label, ops):
        # Category header
        cat_frame = tk.Frame(self.inner, bg=BG_DARK)
        cat_frame.pack(fill=tk.X, pady=(8, 0))

        header = tk.Label(cat_frame, text=label, font=("Segoe UI", 8, "bold"),
                          bg=BG_DARK, fg=ACCENT, padx=16, pady=4, anchor="w")
        header.pack(fill=tk.X)

        # Operation buttons
        ops_frame = tk.Frame(self.inner, bg=BG_DARK)
        ops_frame.pack(fill=tk.X)
        for op_label, op_key in ops:
            self._add_op_button(ops_frame, op_label, op_key)

        # Separator
        sep = tk.Frame(self.inner, bg=BG_MEDIUM, height=1)
        sep.pack(fill=tk.X, padx=16, pady=(6, 0))

    def _add_op_button(self, parent, label, key):
        btn = tk.Label(parent, text=f"  {label}", font=FONT_BODY,
                       bg=BG_DARK, fg=TEXT_DIM,
                       padx=12, pady=5, anchor="w", cursor="hand2")
        btn.pack(fill=tk.X)

        def on_enter(_):
            if btn is not self._active_btn:
                btn.config(bg=BG_MEDIUM, fg=TEXT)

        def on_leave(_):
            if btn is not self._active_btn:
                btn.config(bg=BG_DARK, fg=TEXT_DIM)

        def on_click(_):
            if self._active_btn:
                self._active_btn.config(bg=BG_DARK, fg=TEXT_DIM)
            btn.config(bg=ACCENT, fg=WHITE)
            self._active_btn = btn
            self._active_key = key
            self.on_select(key)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_click)
