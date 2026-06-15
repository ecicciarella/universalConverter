"""Base class for all operation panels."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from gui.theme import *


class BasePanel(tk.Frame):
    title = "Operazione"
    description = ""

    def __init__(self, parent):
        super().__init__(parent, bg=BG_MEDIUM)
        self._build_header()
        self._build_body()

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------

    def _build_header(self):
        hdr = tk.Frame(self, bg=BG_LIGHT, padx=30, pady=20)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text=self.title, font=FONT_TITLE, bg=BG_LIGHT, fg=WHITE).pack(anchor="w")
        if self.description:
            tk.Label(hdr, text=self.description, font=FONT_BODY, bg=BG_LIGHT, fg=TEXT_DIM).pack(anchor="w", pady=(4, 0))

    # ------------------------------------------------------------------
    # Body  – subclasses call helpers below inside _build_body()
    # ------------------------------------------------------------------

    def _build_body(self):
        self.body = tk.Frame(self, bg=BG_MEDIUM, padx=30, pady=20)
        self.body.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _label(self, parent, text, **kw):
        return tk.Label(parent, text=text, font=FONT_BODY, bg=BG_MEDIUM, fg=TEXT, **kw)

    def _entry(self, parent, textvariable, width=50):
        return tk.Entry(parent, textvariable=textvariable, width=width,
                        bg=BG_DARK, fg=TEXT, insertbackground=TEXT,
                        relief=tk.FLAT, font=FONT_BODY)

    def _button(self, parent, text, command, color=ACCENT, fg=WHITE):
        btn = tk.Button(parent, text=text, command=command,
                        bg=color, fg=fg, activebackground=ACCENT2,
                        activeforeground=WHITE, font=FONT_BODY,
                        relief=tk.FLAT, padx=12, pady=6, cursor="hand2")
        return btn

    def _file_row(self, parent, label_text, var, filetypes=None, save=False, row=0):
        """One row: label + entry + browse button."""
        filetypes = filetypes or [("Tutti i file", "*.*")]
        self._label(parent, label_text).grid(row=row, column=0, sticky="w", pady=4, padx=(0, 10))
        e = self._entry(parent, var, width=45)
        e.grid(row=row, column=1, sticky="ew", pady=4)

        def browse():
            if save:
                p = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=filetypes[0][1])
            else:
                p = filedialog.askopenfilename(filetypes=filetypes)
            if p:
                var.set(p)

        self._button(parent, "Sfoglia", browse, color=BG_LIGHT).grid(row=row, column=2, padx=(8, 0), pady=4)
        parent.columnconfigure(1, weight=1)

    def _status_bar(self, parent):
        frame = tk.Frame(parent, bg=BG_DARK, padx=10, pady=6)
        frame.pack(fill=tk.X, side=tk.BOTTOM)
        var = tk.StringVar(value="Pronto.")
        lbl = tk.Label(frame, textvariable=var, font=FONT_SMALL, bg=BG_DARK, fg=TEXT_DIM, anchor="w")
        lbl.pack(fill=tk.X)
        return var

    def _progress(self, parent):
        pb = ttk.Progressbar(parent, mode="indeterminate", length=400)
        return pb

    def _run_in_thread(self, fn, on_done=None, on_error=None):
        """Run fn() in background thread; call on_done/on_error on main thread."""
        def _target():
            try:
                result = fn()
                self.after(0, lambda: on_done(result) if on_done else None)
            except Exception as exc:
                self.after(0, lambda: on_error(exc) if on_error else messagebox.showerror("Errore", str(exc)))
        threading.Thread(target=_target, daemon=True).start()

    @staticmethod
    def _pdf_types():
        return [("File PDF", "*.pdf"), ("Tutti i file", "*.*")]

    @staticmethod
    def _image_types():
        return [("Immagini", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"), ("Tutti i file", "*.*")]
