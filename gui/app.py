"""Main application window."""
import tkinter as tk
from tkinter import ttk
from gui.theme import *
from gui.sidebar import Sidebar
from gui.panels.registry import get_panel


def _configure_ttk_styles():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("TProgressbar", troughcolor=BG_DARK, background=ACCENT,
                    bordercolor=BG_DARK, lightcolor=ACCENT, darkcolor=ACCENT2)
    style.configure("TScrollbar", background=BG_MEDIUM, troughcolor=BG_DARK,
                    bordercolor=BG_DARK, arrowcolor=TEXT_DIM)


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Universal PDF Converter")
        self.root.geometry("1150x760")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG_DARK)
        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        _configure_ttk_styles()
        self._build_ui()

    # ------------------------------------------------------------------

    def _build_ui(self):
        self.sidebar = Sidebar(self.root, self._show_panel)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.content = tk.Frame(self.root, bg=BG_MEDIUM)
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._current_panel = None
        # Show welcome screen on startup
        self._show_welcome()

    def _show_welcome(self):
        if self._current_panel:
            self._current_panel.destroy()
        frame = tk.Frame(self.content, bg=BG_MEDIUM)
        frame.pack(fill=tk.BOTH, expand=True)
        self._current_panel = frame

        tk.Label(frame, text="Universal PDF Converter",
                 font=("Segoe UI", 26, "bold"), bg=BG_MEDIUM, fg=WHITE).pack(pady=(80, 10))
        tk.Label(frame,
                 text="Seleziona un'operazione dalla barra laterale per iniziare.",
                 font=FONT_BODY, bg=BG_MEDIUM, fg=TEXT_DIM).pack()
        tk.Label(frame,
                 text="Tutte le conversioni avvengono localmente — nessun file viene caricato online.",
                 font=FONT_SMALL, bg=BG_MEDIUM, fg=TEXT_DIM).pack(pady=(4, 0))

    def _show_panel(self, key: str):
        if self._current_panel:
            self._current_panel.destroy()
            self._current_panel = None

        panel_cls = get_panel(key)
        if panel_cls is None:
            return
        panel = panel_cls(self.content)
        panel.pack(fill=tk.BOTH, expand=True)
        self._current_panel = panel

    def run(self):
        self.root.mainloop()
