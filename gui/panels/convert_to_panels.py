import tkinter as tk
from tkinter import messagebox
from gui.panels.base_panel import BasePanel
from gui.theme import *
import ops.pdf_ops as pdf


class _SimpleConvertPanel(BasePanel):
    """Generic 1-input → 1-output conversion panel."""
    input_label = "File di input:"
    input_types = [("Tutti", "*.*")]
    output_types = [("File PDF", "*.pdf")]
    button_label = "Converti"
    op_func = None  # set in subclass

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)
        self.in_var = tk.StringVar()
        self._file_row(grid, self.input_label, self.in_var, self.input_types, row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self.output_types, save=True, row=1)
        self._button(b, self.button_label, self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Conversione in corso…")
        fn = self.op_func
        self._run_in_thread(
            lambda: fn(inp, out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class JpgToPDFPanel(_SimpleConvertPanel):
    title = "JPG to PDF"
    description = "Converti una o più immagini in PDF."
    input_label = "Immagine:"
    input_types = [("Immagini", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"), ("Tutti", "*.*")]
    output_types = [("File PDF", "*.pdf")]
    button_label = "Converti in PDF"

    def _build_body(self):
        super()._build_body()

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Conversione in corso…")
        self._run_in_thread(
            lambda: pdf.images_to_pdf([inp], out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class WordToPDFPanel(_SimpleConvertPanel):
    title = "WORD to PDF"
    description = "Converti un file Word (.docx) in PDF.\nMicrosoft Word installato = qualità migliore."
    input_label = "File Word (.docx):"
    input_types = [("Word", "*.docx *.doc"), ("Tutti", "*.*")]
    output_types = [("File PDF", "*.pdf")]
    button_label = "Converti in PDF"
    op_func = staticmethod(pdf.word_to_pdf)


class PptxToPDFPanel(_SimpleConvertPanel):
    title = "POWERPOINT to PDF"
    description = "Converti un file PowerPoint (.pptx) in PDF.\nRichiede Microsoft PowerPoint installato."
    input_label = "File PowerPoint (.pptx):"
    input_types = [("PowerPoint", "*.pptx *.ppt"), ("Tutti", "*.*")]
    output_types = [("File PDF", "*.pdf")]
    button_label = "Converti in PDF"
    op_func = staticmethod(pdf.pptx_to_pdf)


class ExcelToPDFPanel(_SimpleConvertPanel):
    title = "EXCEL to PDF"
    description = "Converti un file Excel (.xlsx) in PDF.\nRichiede Microsoft Excel installato."
    input_label = "File Excel (.xlsx):"
    input_types = [("Excel", "*.xlsx *.xls"), ("Tutti", "*.*")]
    output_types = [("File PDF", "*.pdf")]
    button_label = "Converti in PDF"
    op_func = staticmethod(pdf.excel_to_pdf)


class HtmlToPDFPanel(_SimpleConvertPanel):
    title = "HTML to PDF"
    description = "Converti un file HTML in PDF.\nRichiede weasyprint o pdfkit installato."
    input_label = "File HTML:"
    input_types = [("HTML", "*.html *.htm"), ("Tutti", "*.*")]
    output_types = [("File PDF", "*.pdf")]
    button_label = "Converti in PDF"
    op_func = staticmethod(pdf.html_to_pdf)
