# Universal PDF Converter

A fully offline, cross-platform PDF toolbox with a dark-themed GUI — covering every major PDF operation you'd normally need a web service for.

> **Co-authored with [Claude Sonnet 4.6](https://www.anthropic.com/claude) (Anthropic)**

---

## Features

30 operations across 6 categories:

| Category | Operations |
|---|---|
| **Organize PDF** | Merge, Split, Remove Pages, Extract Pages, Reorder Pages, Scan to PDF |
| **Optimize PDF** | Compress, Repair, OCR |
| **Convert TO PDF** | JPG → PDF, Word → PDF, PowerPoint → PDF, Excel → PDF, HTML → PDF |
| **Convert FROM PDF** | PDF → JPG, PDF → Word, PDF → PowerPoint, PDF → Excel, PDF → PDF/A |
| **Edit PDF** | Rotate, Add Page Numbers, Add Watermark, Crop, Add Text Overlay, Read Form Fields |
| **PDF Security** | Unlock, Protect (password), Sign (image stamp), Redact (black-box), Compare |

Everything runs **locally** — no files are uploaded anywhere.

---

## Project Structure

```
universalConverter/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── universalConverter.spec      # PyInstaller build spec
├── gui/
│   ├── app.py                   # Main window (sidebar + content area)
│   ├── sidebar.py               # Left navigation bar
│   ├── theme.py                 # Colors, fonts, category definitions
│   └── panels/
│       ├── base_panel.py        # Base class with shared UI helpers
│       ├── organize_panels.py   # Merge, Split, Remove/Extract/Reorder pages, Scan
│       ├── optimize_panels.py   # Compress, Repair, OCR
│       ├── convert_to_panels.py # *→PDF conversions
│       ├── convert_from_panels.py # PDF→* conversions
│       ├── edit_panels.py       # Rotate, Watermark, Page numbers, Crop, Edit, Forms
│       ├── security_panels.py   # Unlock, Protect, Sign, Redact, Compare
│       └── registry.py          # Maps operation keys to panel classes
└── ops/
    └── pdf_ops.py               # All 30 PDF backend functions
```

---

## Dependencies

### Core (required)

| Package | Purpose |
|---|---|
| `pypdf` | Page manipulation, encryption, metadata |
| `reportlab` | PDF generation, overlays, watermarks, page numbers |
| `Pillow` | Image handling |
| `python-docx` | Read/write Word documents |
| `python-pptx` | Read/write PowerPoint files |
| `openpyxl` | Read/write Excel files |
| `img2pdf` | Lossless image → PDF |
| `pdf2docx` | PDF → Word conversion |
| `pdfplumber` | Table/text extraction from PDF |

### Optional (enhanced features)

| Package | Feature unlocked |
|---|---|
| `pytesseract` + **Tesseract binary** | OCR PDF |
| `pdf2image` + **Poppler binary** | PDF → JPG, PDF → PowerPoint |
| `weasyprint` | HTML → PDF |
| `pywin32` | High-quality Word/Excel/PowerPoint → PDF via MS Office COM (Windows only) |

Install all at once:

```bash
pip install pypdf Pillow reportlab python-docx python-pptx openpyxl img2pdf pdf2docx pdfplumber pytesseract pdf2image weasyprint pywin32
```

### External binaries (optional, system-level)

- **Tesseract OCR** — required for *OCR PDF*
  - Windows: [UB Mannheim installer](https://github.com/UB-Mannheim/tesseract/wiki) → add install folder to PATH
  - macOS: `brew install tesseract tesseract-lang`
  - Linux: `sudo apt install tesseract-ocr tesseract-ocr-ita`

- **Poppler** — required for *PDF → JPG* and *PDF → PowerPoint*
  - Windows: [oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases) → add `bin\` to PATH
  - macOS: `brew install poppler`
  - Linux: `sudo apt install poppler-utils`

---

## Running from Source

### 1. Clone the repository

```bash
git clone https://github.com/ecicciarella/universalConverter.git
cd universalConverter
```

### 2. Create and activate a virtual environment

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch

```bash
python main.py
```

---

## Running the Portable Executable (Windows)

A pre-built portable build for Windows is available in the [Releases](https://github.com/ecicciarella/universalConverter/releases) section.

1. Download and extract `UniversalPDFConverter_portable.zip`
2. Open the extracted folder
3. Double-click **`UniversalPDFConverter.exe`**

No Python installation required. The folder is fully self-contained — copy it anywhere or put it on a USB drive.

> **Note:** Tesseract and Poppler still need to be installed at the system level for OCR and PDF→image features, even when using the executable.

### Building the executable yourself

With the virtual environment active:

```powershell
pip install pyinstaller
pyinstaller universalConverter.spec --clean
```

Output will be in `dist\UniversalPDFConverter\`.

---

## Usage Tips

- **Merge PDF**: add files in the desired order using the list, reorder with the ↑/↓ buttons
- **Split PDF**: set *pages per file* to `1` to extract every page as a separate PDF
- **OCR PDF**: set the language field to match your document (e.g. `ita`, `eng`, `ita+eng`)
- **Watermark**: opacity `0.15`–`0.3` gives a subtle result; `45°` angle is the classic diagonal
- **Redact**: searches for the exact string (case-insensitive) and draws black boxes over every match — the underlying text is also removed from the content stream
- **Compare**: text-based diff — reports which page numbers differ between two PDFs
- **Sign**: uses an image file (PNG with transparency works best) stamped onto the chosen page at the specified coordinates (points, origin = bottom-left)

---

## License

MIT

---

## Credits

Built by **Enrico Cicciarella**, co-authored with **Claude Sonnet 4.6** by [Anthropic](https://www.anthropic.com).
