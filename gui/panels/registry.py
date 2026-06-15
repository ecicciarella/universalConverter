"""Maps operation keys to their panel classes."""
from gui.panels.organize_panels import (
    MergePanel, SplitPanel, RemovePagesPanel,
    ExtractPagesPanel, OrganizePagesPanel, ScanToPDFPanel,
)
from gui.panels.optimize_panels import CompressPanel, RepairPanel, OCRPanel
from gui.panels.convert_to_panels import (
    JpgToPDFPanel, WordToPDFPanel, PptxToPDFPanel, ExcelToPDFPanel, HtmlToPDFPanel,
)
from gui.panels.convert_from_panels import (
    PDFToJpgPanel, PDFToWordPanel, PDFToPptxPanel, PDFToExcelPanel, PDFToPdfAPanel,
)
from gui.panels.edit_panels import (
    RotatePanel, PageNumbersPanel, WatermarkPanel,
    CropPanel, EditPDFPanel, FormsPanel,
)
from gui.panels.security_panels import (
    UnlockPanel, ProtectPanel, SignPanel, RedactPanel, ComparePanel,
)

PANEL_MAP = {
    "merge":          MergePanel,
    "split":          SplitPanel,
    "remove_pages":   RemovePagesPanel,
    "extract_pages":  ExtractPagesPanel,
    "organize_pages": OrganizePagesPanel,
    "scan_to_pdf":    ScanToPDFPanel,
    "compress":       CompressPanel,
    "repair":         RepairPanel,
    "ocr":            OCRPanel,
    "jpg_to_pdf":     JpgToPDFPanel,
    "word_to_pdf":    WordToPDFPanel,
    "pptx_to_pdf":    PptxToPDFPanel,
    "excel_to_pdf":   ExcelToPDFPanel,
    "html_to_pdf":    HtmlToPDFPanel,
    "pdf_to_jpg":     PDFToJpgPanel,
    "pdf_to_word":    PDFToWordPanel,
    "pdf_to_pptx":    PDFToPptxPanel,
    "pdf_to_excel":   PDFToExcelPanel,
    "pdf_to_pdfa":    PDFToPdfAPanel,
    "rotate":         RotatePanel,
    "page_numbers":   PageNumbersPanel,
    "watermark":      WatermarkPanel,
    "crop":           CropPanel,
    "edit_pdf":       EditPDFPanel,
    "forms":          FormsPanel,
    "unlock":         UnlockPanel,
    "protect":        ProtectPanel,
    "sign":           SignPanel,
    "redact":         RedactPanel,
    "compare":        ComparePanel,
}


def get_panel(key: str):
    return PANEL_MAP.get(key)
