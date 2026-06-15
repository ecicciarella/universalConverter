import tkinter as tk
from tkinter import filedialog, messagebox
from gui.panels.base_panel import BasePanel
from gui.theme import *
import ops.pdf_ops as pdf


# ──────────────────────────────────────────────
# Merge
# ──────────────────────────────────────────────

class MergePanel(BasePanel):
    title = "Merge PDF"
    description = "Unisci più file PDF in un unico documento."

    def _build_body(self):
        super()._build_body()
        b = self.body
        self._label(b, "File PDF da unire (in ordine):").pack(anchor="w")

        self.listbox = tk.Listbox(b, bg=BG_DARK, fg=TEXT, font=FONT_BODY,
                                  selectmode=tk.EXTENDED, height=8, relief=tk.FLAT)
        self.listbox.pack(fill=tk.X, pady=(4, 8))

        btn_row = tk.Frame(b, bg=BG_MEDIUM)
        btn_row.pack(fill=tk.X)
        self._button(btn_row, "+ Aggiungi", self._add_files, BG_LIGHT).pack(side=tk.LEFT, padx=(0, 6))
        self._button(btn_row, "Rimuovi sel.", self._remove_sel, BG_DARK).pack(side=tk.LEFT, padx=(0, 6))
        self._button(btn_row, "↑ Su",  lambda: self._move(-1), BG_DARK).pack(side=tk.LEFT, padx=(0, 6))
        self._button(btn_row, "↓ Giù", lambda: self._move(1),  BG_DARK).pack(side=tk.LEFT)

        sep = tk.Frame(b, bg=BG_DARK, height=1)
        sep.pack(fill=tk.X, pady=12)

        out_row = tk.Frame(b, bg=BG_MEDIUM)
        out_row.pack(fill=tk.X)
        self.out_var = tk.StringVar()
        self._file_row(out_row, "Output:", self.out_var,
                       filetypes=self._pdf_types(), save=True, row=0)

        self._button(b, "Unisci PDF", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _add_files(self):
        paths = filedialog.askopenfilenames(filetypes=self._pdf_types())
        for p in paths:
            self.listbox.insert(tk.END, p)

    def _remove_sel(self):
        for i in reversed(self.listbox.curselection()):
            self.listbox.delete(i)

    def _move(self, direction):
        sel = list(self.listbox.curselection())
        if not sel:
            return
        if direction == -1 and sel[0] == 0:
            return
        if direction == 1 and sel[-1] == self.listbox.size() - 1:
            return
        for i in sel[::direction]:
            j = i + direction
            a, b_ = self.listbox.get(i), self.listbox.get(j)
            self.listbox.delete(i)
            self.listbox.insert(i, b_)
            self.listbox.delete(j)
            self.listbox.insert(j, a)
            self.listbox.selection_set(j)

    def _run(self):
        paths = list(self.listbox.get(0, tk.END))
        out = self.out_var.get()
        if len(paths) < 2:
            messagebox.showwarning("Attenzione", "Aggiungi almeno 2 file PDF.")
            return
        if not out:
            messagebox.showwarning("Attenzione", "Specifica il file di output.")
            return
        self.status.set("Unione in corso…")
        self._run_in_thread(
            lambda: pdf.merge_pdfs(paths, out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"PDF unito:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


# ──────────────────────────────────────────────
# Split
# ──────────────────────────────────────────────

class SplitPanel(BasePanel):
    title = "Split PDF"
    description = "Dividi un PDF in più file."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)

        self._label(grid, "Pagine per file:").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 10))
        self.pages_var = tk.StringVar(value="1")
        self._entry(grid, self.pages_var, 10).grid(row=1, column=1, sticky="w", pady=4)

        self._label(grid, "Cartella output:").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        self.out_var = tk.StringVar()
        e = self._entry(grid, self.out_var, 45)
        e.grid(row=2, column=1, sticky="ew", pady=4)

        def pick_dir():
            d = filedialog.askdirectory()
            if d:
                self.out_var.set(d)

        self._button(grid, "Sfoglia", pick_dir, BG_LIGHT).grid(row=2, column=2, padx=(8, 0))

        self._button(b, "Dividi PDF", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp = self.in_var.get()
        out = self.out_var.get()
        try:
            ppf = int(self.pages_var.get())
        except ValueError:
            messagebox.showwarning("Attenzione", "Inserisci un numero intero di pagine.")
            return
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Divisione in corso…")
        self._run_in_thread(
            lambda: pdf.split_pdf(inp, out, ppf),
            on_done=lambda r: (self.status.set(f"Creati {len(r)} file."),
                               messagebox.showinfo("Fatto", f"Creati {len(r)} file in:\n{out}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


# ──────────────────────────────────────────────
# Remove Pages
# ──────────────────────────────────────────────

class RemovePagesPanel(BasePanel):
    title = "Remove Pages"
    description = "Rimuovi pagine specifiche da un PDF."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)

        self._label(grid, "Pagine da rimuovere\n(es. 1,3,5-7):").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 10))
        self.pages_var = tk.StringVar()
        self._entry(grid, self.pages_var, 30).grid(row=1, column=1, sticky="w", pady=4)

        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=2)

        self._button(b, "Rimuovi Pagine", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _parse_pages(self, text):
        pages = []
        for part in text.split(","):
            part = part.strip()
            if "-" in part:
                a, z = part.split("-", 1)
                pages.extend(range(int(a), int(z) + 1))
            elif part:
                pages.append(int(part))
        return pages

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        try:
            pages = self._parse_pages(self.pages_var.get())
        except ValueError:
            messagebox.showwarning("Formato", "Formato pagine non valido (es. 1,3,5-7).")
            return
        self.status.set("Rimozione in corso…")
        self._run_in_thread(
            lambda: pdf.remove_pages(inp, out, pages),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


# ──────────────────────────────────────────────
# Extract Pages
# ──────────────────────────────────────────────

class ExtractPagesPanel(BasePanel):
    title = "Extract Pages"
    description = "Estrai pagine selezionate in un nuovo PDF."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)

        self._label(grid, "Pagine da estrarre\n(es. 2,4,6-10):").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 10))
        self.pages_var = tk.StringVar()
        self._entry(grid, self.pages_var, 30).grid(row=1, column=1, sticky="w", pady=4)

        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=2)

        self._button(b, "Estrai Pagine", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _parse_pages(self, text):
        pages = []
        for part in text.split(","):
            part = part.strip()
            if "-" in part:
                a, z = part.split("-", 1)
                pages.extend(range(int(a), int(z) + 1))
            elif part:
                pages.append(int(part))
        return pages

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        try:
            pages = self._parse_pages(self.pages_var.get())
        except ValueError:
            messagebox.showwarning("Formato", "Formato pagine non valido.")
            return
        self.status.set("Estrazione in corso…")
        self._run_in_thread(
            lambda: pdf.extract_pages(inp, out, pages),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


# ──────────────────────────────────────────────
# Organize (reorder) pages
# ──────────────────────────────────────────────

class OrganizePagesPanel(BasePanel):
    title = "Organize PDF"
    description = "Riordina le pagine di un PDF."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)

        self._label(grid, "Nuovo ordine pagine\n(es. 3,1,2,4):").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 10))
        self.order_var = tk.StringVar()
        self._entry(grid, self.order_var, 40).grid(row=1, column=1, sticky="w", pady=4)

        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=2)

        self._button(b, "Riordina Pagine", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        try:
            order = [int(x.strip()) for x in self.order_var.get().split(",")]
        except ValueError:
            messagebox.showwarning("Formato", "Inserisci numeri separati da virgola.")
            return
        self.status.set("Riordinamento in corso…")
        self._run_in_thread(
            lambda: pdf.reorder_pages(inp, out, order),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


# ──────────────────────────────────────────────
# Scan to PDF
# ──────────────────────────────────────────────

class ScanToPDFPanel(BasePanel):
    title = "Scan to PDF"
    description = "Converti immagini scansionate in un PDF."

    def _build_body(self):
        super()._build_body()
        b = self.body
        self._label(b, "Immagini (nell'ordine delle pagine):").pack(anchor="w")

        self.listbox = tk.Listbox(b, bg=BG_DARK, fg=TEXT, font=FONT_BODY,
                                  selectmode=tk.EXTENDED, height=8, relief=tk.FLAT)
        self.listbox.pack(fill=tk.X, pady=(4, 8))

        btn_row = tk.Frame(b, bg=BG_MEDIUM)
        btn_row.pack(fill=tk.X)
        self._button(btn_row, "+ Aggiungi", self._add, BG_LIGHT).pack(side=tk.LEFT, padx=(0, 6))
        self._button(btn_row, "Rimuovi", self._remove, BG_DARK).pack(side=tk.LEFT)

        sep = tk.Frame(b, bg=BG_DARK, height=1)
        sep.pack(fill=tk.X, pady=12)

        out_row = tk.Frame(b, bg=BG_MEDIUM)
        out_row.pack(fill=tk.X)
        self.out_var = tk.StringVar()
        self._file_row(out_row, "Output PDF:", self.out_var, self._pdf_types(), save=True, row=0)

        self._button(b, "Crea PDF", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _add(self):
        paths = filedialog.askopenfilenames(filetypes=self._image_types())
        for p in paths:
            self.listbox.insert(tk.END, p)

    def _remove(self):
        for i in reversed(self.listbox.curselection()):
            self.listbox.delete(i)

    def _run(self):
        images = list(self.listbox.get(0, tk.END))
        out = self.out_var.get()
        if not images or not out:
            messagebox.showwarning("Attenzione", "Aggiungi immagini e specifica l'output.")
            return
        self.status.set("Conversione in corso…")
        self._run_in_thread(
            lambda: pdf.images_to_pdf(images, out),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"PDF creato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )
