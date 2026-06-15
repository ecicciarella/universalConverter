import tkinter as tk
from tkinter import filedialog, messagebox
from gui.panels.base_panel import BasePanel
from gui.theme import *
import ops.pdf_ops as pdf


class PDFToJpgPanel(BasePanel):
    title = "PDF to JPG"
    description = "Converti ogni pagina del PDF in un'immagine JPG.\nRichiede pdf2image e Poppler nel PATH."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)

        self._label(grid, "Cartella output:").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 10))
        self.out_var = tk.StringVar()
        self._entry(grid, self.out_var, 45).grid(row=1, column=1, sticky="ew", pady=4)

        def pick_dir():
            d = filedialog.askdirectory()
            if d:
                self.out_var.set(d)

        self._button(grid, "Sfoglia", pick_dir, BG_LIGHT).grid(row=1, column=2, padx=(8, 0))

        self._label(grid, "DPI:").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        self.dpi_var = tk.StringVar(value="150")
        self._entry(grid, self.dpi_var, 10).grid(row=2, column=1, sticky="w")

        self._button(b, "Converti in JPG", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        try:
            dpi = int(self.dpi_var.get())
        except ValueError:
            dpi = 150
        self.status.set("Conversione in corso…")
        self._run_in_thread(
            lambda: pdf.pdf_to_images(inp, out, "JPEG", dpi),
            on_done=lambda r: (self.status.set(f"Creati {len(r)} file."),
                               messagebox.showinfo("Fatto", f"Creati {len(r)} file in:\n{out}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class PDFToWordPanel(BasePanel):
    title = "PDF to WORD"
    description = "Converti un PDF in documento Word (.docx).\nRichiede pdf2docx."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)
        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output (.docx):", self.out_var,
                       [("Word", "*.docx"), ("Tutti", "*.*")], save=True, row=1)
        self._button(b, "Converti in Word", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Conversione in corso (può richiedere del tempo)…")
        self._run_in_thread(
            lambda: pdf.pdf_to_word(inp, out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class PDFToPptxPanel(BasePanel):
    title = "PDF to POWERPOINT"
    description = "Converti ogni pagina PDF in una slide PPTX.\nRichiede pdf2image, python-pptx e Poppler."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)
        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output (.pptx):", self.out_var,
                       [("PowerPoint", "*.pptx"), ("Tutti", "*.*")], save=True, row=1)
        self._button(b, "Converti in PPTX", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Conversione in corso…")
        self._run_in_thread(
            lambda: pdf.pdf_to_pptx(inp, out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class PDFToExcelPanel(BasePanel):
    title = "PDF to EXCEL"
    description = "Estrai tabelle e testo da un PDF in formato Excel (.xlsx).\nRichiede pdfplumber e openpyxl."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)
        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output (.xlsx):", self.out_var,
                       [("Excel", "*.xlsx"), ("Tutti", "*.*")], save=True, row=1)
        self._button(b, "Converti in Excel", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Conversione in corso…")
        self._run_in_thread(
            lambda: pdf.pdf_to_excel(inp, out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class PDFToPdfAPanel(BasePanel):
    title = "PDF to PDF/A"
    description = "Converti un PDF in formato archiviazione PDF/A."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)
        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)
        self._button(b, "Converti in PDF/A", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Conversione in corso…")
        self._run_in_thread(
            lambda: pdf.pdf_to_pdfa(inp, out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )
