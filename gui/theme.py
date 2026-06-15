BG_DARK     = "#1a1a2e"
BG_MEDIUM   = "#16213e"
BG_LIGHT    = "#0f3460"
ACCENT      = "#e94560"
ACCENT2     = "#533483"
TEXT        = "#eaeaea"
TEXT_DIM    = "#888888"
SUCCESS     = "#4caf50"
WARNING     = "#ff9800"
ERROR       = "#f44336"
WHITE       = "#ffffff"

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_HEAD   = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 9)

CATEGORIES = [
    ("ORGANIZE PDF", "organize", [
        ("Merge PDF",     "merge"),
        ("Split PDF",     "split"),
        ("Remove Pages",  "remove_pages"),
        ("Extract Pages", "extract_pages"),
        ("Organize PDF",  "organize_pages"),
        ("Scan to PDF",   "scan_to_pdf"),
    ]),
    ("OPTIMIZE PDF", "optimize", [
        ("Compress PDF",  "compress"),
        ("Repair PDF",    "repair"),
        ("OCR PDF",       "ocr"),
    ]),
    ("CONVERT TO PDF", "convert_to", [
        ("JPG to PDF",         "jpg_to_pdf"),
        ("WORD to PDF",        "word_to_pdf"),
        ("POWERPOINT to PDF",  "pptx_to_pdf"),
        ("EXCEL to PDF",       "excel_to_pdf"),
        ("HTML to PDF",        "html_to_pdf"),
    ]),
    ("CONVERT FROM PDF", "convert_from", [
        ("PDF to JPG",        "pdf_to_jpg"),
        ("PDF to WORD",       "pdf_to_word"),
        ("PDF to POWERPOINT", "pdf_to_pptx"),
        ("PDF to EXCEL",      "pdf_to_excel"),
        ("PDF to PDF/A",      "pdf_to_pdfa"),
    ]),
    ("EDIT PDF", "edit", [
        ("Rotate PDF",       "rotate"),
        ("Add Page Numbers", "page_numbers"),
        ("Add Watermark",    "watermark"),
        ("Crop PDF",         "crop"),
        ("Edit PDF",         "edit_pdf"),
        ("PDF Forms",        "forms"),
    ]),
    ("PDF SECURITY", "security", [
        ("Unlock PDF",   "unlock"),
        ("Protect PDF",  "protect"),
        ("Sign PDF",     "sign"),
        ("Redact PDF",   "redact"),
        ("Compare PDF",  "compare"),
    ]),
]
