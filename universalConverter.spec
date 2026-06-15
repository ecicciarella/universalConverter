# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

SP = os.path.join(os.getcwd(), 'venv', 'Lib', 'site-packages')

# Icon is kept in assets/ which is git-ignored. Falls back to None so the
# build works for anyone cloning the repo without that folder.
_icon_path = os.path.join(os.getcwd(), 'assets', 'icon.ico')
APP_ICON = _icon_path if os.path.isfile(_icon_path) else None

datas = []

# reportlab — fonts and graphics data
datas += collect_data_files('reportlab')

# weasyprint — CSS user-agent stylesheet
datas += collect_data_files('weasyprint')

# pdfminer — cmap data (used by pdfplumber)
datas += collect_data_files('pdfminer')

# pdf2docx templates / data
datas += collect_data_files('pdf2docx')

# Pillow — plugin data
datas += collect_data_files('PIL')

hidden = [
    # core
    'pypdf',
    'pypdf._crypt_filters',
    'pypdf.filters',
    # reportlab
    'reportlab',
    'reportlab.pdfgen',
    'reportlab.pdfgen.canvas',
    'reportlab.lib',
    'reportlab.lib.colors',
    'reportlab.lib.pagesizes',
    'reportlab.lib.units',
    'reportlab.graphics',
    'reportlab.graphics.barcode',
    # PIL
    'PIL',
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    # office
    'docx',
    'docx.oxml',
    'pptx',
    'pptx.util',
    'openpyxl',
    'openpyxl.workbook',
    # pdf tools
    'pdfplumber',
    'pdfminer',
    'pdfminer.high_level',
    'pdfminer.layout',
    'pdf2docx',
    'img2pdf',
    # optional (gracefully absent at runtime if binaries missing)
    'pytesseract',
    'pdf2image',
    'weasyprint',
    # win32
    'win32com',
    'win32com.client',
    'win32api',
    'pywintypes',
    # tkinter (usually auto-detected, listed for safety)
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    # gui modules
    'gui',
    'gui.app',
    'gui.sidebar',
    'gui.theme',
    'gui.panels',
    'gui.panels.registry',
    'gui.panels.base_panel',
    'gui.panels.organize_panels',
    'gui.panels.optimize_panels',
    'gui.panels.convert_to_panels',
    'gui.panels.convert_from_panels',
    'gui.panels.edit_panels',
    'gui.panels.security_panels',
    'ops',
    'ops.pdf_ops',
]

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'pandas', 'IPython', 'jupyter'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,          # onedir mode: faster startup
    name='UniversalPDFConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,                  # no black console window
    icon=APP_ICON,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='UniversalPDFConverter',
)
