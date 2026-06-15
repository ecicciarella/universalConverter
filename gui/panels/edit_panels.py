import tkinter as tk
from tkinter import messagebox, scrolledtext
from gui.panels.base_panel import BasePanel
from gui.theme import *
import ops.pdf_ops as pdf


class RotatePanel(BasePanel):
    title = "Rotate PDF"
    description = "Ruota le pagine di un PDF di 90°, 180° o 270°."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)

        self._label(grid, "Angolo rotazione:").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        self.angle_var = tk.StringVar(value="90")
        angle_frame = tk.Frame(grid, bg=BG_MEDIUM)
        angle_frame.grid(row=2, column=1, sticky="w")
        for a in ("90", "180", "270"):
            tk.Radiobutton(angle_frame, text=f"{a}°", variable=self.angle_var, value=a,
                           bg=BG_MEDIUM, fg=TEXT, selectcolor=BG_DARK,
                           activebackground=BG_MEDIUM, font=FONT_BODY).pack(side=tk.LEFT, padx=8)

        self._label(grid, "Pagine (vuoto = tutte)\n(es. 1,3,5-7):").grid(row=3, column=0, sticky="w", pady=4, padx=(0, 10))
        self.pages_var = tk.StringVar()
        self._entry(grid, self.pages_var, 30).grid(row=3, column=1, sticky="w")

        self._button(b, "Ruota PDF", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        angle = int(self.angle_var.get())
        raw = self.pages_var.get().strip()
        pages = None
        if raw:
            pages = []
            for part in raw.split(","):
                part = part.strip()
                if "-" in part:
                    a, z = part.split("-", 1)
                    pages.extend(range(int(a), int(z) + 1))
                else:
                    pages.append(int(part))
        self.status.set("Rotazione in corso…")
        self._run_in_thread(
            lambda: pdf.rotate_pdf(inp, out, angle, pages),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class PageNumbersPanel(BasePanel):
    title = "Add Page Numbers"
    description = "Aggiungi numeri di pagina a un PDF."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)

        self._label(grid, "Posizione:").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        self.pos_var = tk.StringVar(value="bottom-center")
        pos_menu = tk.OptionMenu(grid, self.pos_var,
                                 "bottom-center", "bottom-left", "bottom-right", "top-center")
        pos_menu.config(bg=BG_DARK, fg=TEXT, font=FONT_BODY, relief=tk.FLAT)
        pos_menu.grid(row=2, column=1, sticky="w")

        self._label(grid, "Numero iniziale:").grid(row=3, column=0, sticky="w", pady=4, padx=(0, 10))
        self.start_var = tk.StringVar(value="1")
        self._entry(grid, self.start_var, 10).grid(row=3, column=1, sticky="w")

        self._label(grid, "Dimensione font:").grid(row=4, column=0, sticky="w", pady=4, padx=(0, 10))
        self.fs_var = tk.StringVar(value="10")
        self._entry(grid, self.fs_var, 10).grid(row=4, column=1, sticky="w")

        self._button(b, "Aggiungi Numeri", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        pos = self.pos_var.get()
        try:
            start = int(self.start_var.get())
            fs = int(self.fs_var.get())
        except ValueError:
            start, fs = 1, 10
        self.status.set("Aggiunta numeri in corso…")
        self._run_in_thread(
            lambda: pdf.add_page_numbers(inp, out, pos, fs, start),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class WatermarkPanel(BasePanel):
    title = "Add Watermark"
    description = "Aggiungi una filigrana di testo diagonale al PDF."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)

        self._label(grid, "Testo filigrana:").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        self.text_var = tk.StringVar(value="CONFIDENTIAL")
        self._entry(grid, self.text_var, 30).grid(row=2, column=1, sticky="w")

        self._label(grid, "Opacità (0–1):").grid(row=3, column=0, sticky="w", pady=4, padx=(0, 10))
        self.opacity_var = tk.StringVar(value="0.3")
        self._entry(grid, self.opacity_var, 10).grid(row=3, column=1, sticky="w")

        self._label(grid, "Angolo:").grid(row=4, column=0, sticky="w", pady=4, padx=(0, 10))
        self.angle_var = tk.StringVar(value="45")
        self._entry(grid, self.angle_var, 10).grid(row=4, column=1, sticky="w")

        self._label(grid, "Dimensione font:").grid(row=5, column=0, sticky="w", pady=4, padx=(0, 10))
        self.fs_var = tk.StringVar(value="48")
        self._entry(grid, self.fs_var, 10).grid(row=5, column=1, sticky="w")

        self._button(b, "Aggiungi Filigrana", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        try:
            opacity = float(self.opacity_var.get())
            angle = float(self.angle_var.get())
            fs = int(self.fs_var.get())
        except ValueError:
            opacity, angle, fs = 0.3, 45, 48
        text = self.text_var.get() or "WATERMARK"
        self.status.set("Aggiunta filigrana…")
        self._run_in_thread(
            lambda: pdf.add_watermark(inp, out, text, opacity, angle, fs),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class CropPanel(BasePanel):
    title = "Crop PDF"
    description = "Ritaglia i margini delle pagine PDF (valori in punti, 72pt = 1 pollice)."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)

        for i, (lbl, attr, default) in enumerate([
            ("Margine sinistro (pt):", "left_var", "0"),
            ("Margine basso (pt):",    "bottom_var", "0"),
            ("Margine destro (pt):",   "right_var", "0"),
            ("Margine alto (pt):",     "top_var", "0"),
        ]):
            row = i + 2
            self._label(grid, lbl).grid(row=row, column=0, sticky="w", pady=4, padx=(0, 10))
            var = tk.StringVar(value=default)
            setattr(self, attr, var)
            self._entry(grid, var, 10).grid(row=row, column=1, sticky="w")

        self._button(b, "Ritaglia PDF", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        try:
            l = float(self.left_var.get())
            bot = float(self.bottom_var.get())
            r = float(self.right_var.get())
            t = float(self.top_var.get())
        except ValueError:
            messagebox.showwarning("Errore", "Inserisci valori numerici per i margini.")
            return
        self.status.set("Ritaglio in corso…")
        self._run_in_thread(
            lambda: pdf.crop_pdf(inp, out, l, bot, r, t),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class EditPDFPanel(BasePanel):
    title = "Edit PDF"
    description = "Aggiungi testo o overlay a un PDF tramite reportlab."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)

        self._label(grid, "Testo da aggiungere:").grid(row=2, column=0, sticky="nw", pady=4, padx=(0, 10))
        self.txt = tk.Text(grid, height=4, width=40, bg=BG_DARK, fg=TEXT,
                           insertbackground=TEXT, font=FONT_BODY, relief=tk.FLAT)
        self.txt.grid(row=2, column=1, pady=4, sticky="ew")

        for i, (lbl, attr, default) in enumerate([
            ("X (pt):", "x_var", "50"),
            ("Y (pt):", "y_var", "50"),
            ("Pagina:", "pg_var", "1"),
            ("Font size:", "fs_var", "12"),
        ]):
            row = i + 3
            self._label(grid, lbl).grid(row=row, column=0, sticky="w", pady=2, padx=(0, 10))
            var = tk.StringVar(value=default)
            setattr(self, attr, var)
            self._entry(grid, var, 10).grid(row=row, column=1, sticky="w")

        self._button(b, "Aggiungi Testo", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        import io
        from pypdf import PdfReader, PdfWriter
        from reportlab.pdfgen import canvas as rl_canvas

        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        text = self.txt.get("1.0", tk.END).strip()
        try:
            x = float(self.x_var.get())
            y = float(self.y_var.get())
            pg = int(self.pg_var.get()) - 1
            fs = int(self.fs_var.get())
        except ValueError:
            x, y, pg, fs = 50, 50, 0, 12

        def _do():
            reader = PdfReader(inp)
            writer = PdfWriter()
            for i, page in enumerate(reader.pages):
                if i == pg:
                    box = page.mediabox
                    pw, ph = float(box.width), float(box.height)
                    packet = io.BytesIO()
                    c = rl_canvas.Canvas(packet, pagesize=(pw, ph))
                    c.setFont("Helvetica", fs)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(x, y, text)
                    c.save()
                    packet.seek(0)
                    overlay = PdfReader(packet).pages[0]
                    page.merge_page(overlay)
                writer.add_page(page)
            with open(out, "wb") as f:
                writer.write(f)
            return out

        self.status.set("Modifica in corso…")
        self._run_in_thread(
            _do,
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class FormsPanel(BasePanel):
    title = "PDF Forms"
    description = "Visualizza i campi di un modulo PDF e i loro valori."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)
        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self._button(b, "Leggi Campi", self._run, ACCENT).pack(pady=(16, 0), anchor="w")

        self._label(b, "Campi trovati:").pack(anchor="w", pady=(12, 2))
        self.txt = scrolledtext.ScrolledText(b, height=12, bg=BG_DARK, fg=TEXT,
                                             font=FONT_MONO, relief=tk.FLAT)
        self.txt.pack(fill=tk.BOTH, expand=True)
        self.status = self._status_bar(self)

    def _run(self):
        inp = self.in_var.get()
        if not inp:
            messagebox.showwarning("Attenzione", "Seleziona un file PDF.")
            return
        self.status.set("Lettura campi…")

        def _do():
            data = pdf.extract_form_data(inp)
            return data

        def _show(data):
            self.txt.delete("1.0", tk.END)
            if not data:
                self.txt.insert(tk.END, "Nessun campo trovato (il PDF non è un modulo).")
            else:
                for k, v in data.items():
                    self.txt.insert(tk.END, f"{k}: {v}\n")
            self.status.set(f"Trovati {len(data)} campi.")

        self._run_in_thread(_do, on_done=_show, on_error=lambda e: self.status.set(f"Errore: {e}"))
