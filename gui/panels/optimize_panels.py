import tkinter as tk
from tkinter import messagebox
from gui.panels.base_panel import BasePanel
from gui.theme import *
import ops.pdf_ops as pdf


class CompressPanel(BasePanel):
    title = "Compress PDF"
    description = "Riduci le dimensioni del file PDF."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)
        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)
        self._button(b, "Comprimi PDF", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Compressione in corso…")
        self._run_in_thread(
            lambda: pdf.compress_pdf(inp, out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"PDF compresso:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class RepairPanel(BasePanel):
    title = "Repair PDF"
    description = "Tenta di riparare un PDF corrotto o mal formattato."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)
        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)
        self._button(b, "Ripara PDF", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Riparazione in corso…")
        self._run_in_thread(
            lambda: pdf.repair_pdf(inp, out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"PDF riparato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class OCRPanel(BasePanel):
    title = "OCR PDF"
    description = "Applica il riconoscimento testo (OCR) a un PDF scansionato.\nRichiede: pytesseract, pdf2image, Poppler e Tesseract nel PATH."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)
        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)

        self._label(grid, "Lingue OCR (es. ita+eng):").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        self.lang_var = tk.StringVar(value="ita+eng")
        self._entry(grid, self.lang_var, 20).grid(row=2, column=1, sticky="w", pady=4)

        self._button(b, "Esegui OCR", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("OCR in corso (potrebbe richiedere del tempo)…")
        lang = self.lang_var.get() or "ita+eng"
        self._run_in_thread(
            lambda: pdf.ocr_pdf(inp, out, lang),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"PDF OCR:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )
