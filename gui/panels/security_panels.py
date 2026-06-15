import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from gui.panels.base_panel import BasePanel
from gui.theme import *
import ops.pdf_ops as pdf


class UnlockPanel(BasePanel):
    title = "Unlock PDF"
    description = "Rimuovi la password di apertura da un PDF protetto."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)

        self._label(grid, "Password:").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        self.pwd_var = tk.StringVar()
        pwd_entry = self._entry(grid, self.pwd_var, 30)
        pwd_entry.config(show="*")
        pwd_entry.grid(row=2, column=1, sticky="w")

        self._button(b, "Sblocca PDF", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        pwd = self.pwd_var.get()
        if not inp or not out:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Sblocco in corso…")
        self._run_in_thread(
            lambda: pdf.unlock_pdf(inp, out, pwd),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"PDF sbloccato:\n{r}")),
            on_error=lambda e: (self.status.set(f"Errore: {e}"),
                                messagebox.showerror("Errore", str(e)))
        )


class ProtectPanel(BasePanel):
    title = "Protect PDF"
    description = "Proteggi un PDF con password."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)

        self._label(grid, "Password utente:").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        self.upwd_var = tk.StringVar()
        up_entry = self._entry(grid, self.upwd_var, 30)
        up_entry.config(show="*")
        up_entry.grid(row=2, column=1, sticky="w")

        self._label(grid, "Password proprietario\n(opzionale):").grid(row=3, column=0, sticky="w", pady=4, padx=(0, 10))
        self.opwd_var = tk.StringVar()
        op_entry = self._entry(grid, self.opwd_var, 30)
        op_entry.config(show="*")
        op_entry.grid(row=3, column=1, sticky="w")

        self._button(b, "Proteggi PDF", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        upwd = self.upwd_var.get()
        opwd = self.opwd_var.get() or None
        if not inp or not out or not upwd:
            messagebox.showwarning("Attenzione", "Compila tutti i campi obbligatori.")
            return
        self.status.set("Protezione in corso…")
        self._run_in_thread(
            lambda: pdf.protect_pdf(inp, out, upwd, opwd),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"PDF protetto:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class SignPanel(BasePanel):
    title = "Sign PDF"
    description = "Applica una firma visiva (immagine) su una pagina del PDF."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)
        self.sig_var = tk.StringVar()
        self._file_row(grid, "Immagine firma (PNG/JPG):", self.sig_var,
                       [("Immagini", "*.png *.jpg *.jpeg"), ("Tutti", "*.*")], row=2)

        for i, (lbl, attr, default) in enumerate([
            ("Pagina:", "pg_var", "1"),
            ("X (pt):", "x_var", "50"),
            ("Y (pt):", "y_var", "50"),
            ("Larghezza (pt):", "w_var", "150"),
            ("Altezza (pt):",   "h_var", "50"),
        ]):
            row = i + 3
            self._label(grid, lbl).grid(row=row, column=0, sticky="w", pady=2, padx=(0, 10))
            var = tk.StringVar(value=default)
            setattr(self, attr, var)
            self._entry(grid, var, 10).grid(row=row, column=1, sticky="w")

        self._button(b, "Applica Firma", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out, sig = self.in_var.get(), self.out_var.get(), self.sig_var.get()
        if not inp or not out or not sig:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        try:
            pg = int(self.pg_var.get())
            x  = float(self.x_var.get())
            y  = float(self.y_var.get())
            w  = float(self.w_var.get())
            h  = float(self.h_var.get())
        except ValueError:
            pg, x, y, w, h = 1, 50, 50, 150, 50
        self.status.set("Apposizione firma…")
        self._run_in_thread(
            lambda: pdf.sign_pdf(inp, out, sig, pg, x, y, w, h),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"Salvato:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class RedactPanel(BasePanel):
    title = "Redact PDF"
    description = "Oscura (nero) le occorrenze di testo nel PDF.\nRichiede pdfplumber."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.in_var = tk.StringVar()
        self._file_row(grid, "File PDF:", self.in_var, self._pdf_types(), row=0)
        self.out_var = tk.StringVar()
        self._file_row(grid, "Output:", self.out_var, self._pdf_types(), save=True, row=1)

        self._label(grid, "Testo da oscurare:").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 10))
        self.search_var = tk.StringVar()
        self._entry(grid, self.search_var, 40).grid(row=2, column=1, sticky="w")

        self._button(b, "Oscura Testo", self._run, ACCENT).pack(pady=(16, 0), anchor="w")
        self.status = self._status_bar(self)

    def _run(self):
        inp, out = self.in_var.get(), self.out_var.get()
        search = self.search_var.get()
        if not inp or not out or not search:
            messagebox.showwarning("Attenzione", "Compila tutti i campi.")
            return
        self.status.set("Oscuramento in corso…")
        self._run_in_thread(
            lambda: pdf.redact_pdf(inp, out, search),
            on_done=lambda r: (self.status.set(f"Completato: {r}"),
                               messagebox.showinfo("Fatto", f"PDF redatto:\n{r}")),
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )


class ComparePanel(BasePanel):
    title = "Compare PDF"
    description = "Confronta due PDF e mostra le differenze testuali pagina per pagina."

    def _build_body(self):
        super()._build_body()
        b = self.body
        grid = tk.Frame(b, bg=BG_MEDIUM)
        grid.pack(fill=tk.X)

        self.a_var = tk.StringVar()
        self._file_row(grid, "PDF A:", self.a_var, self._pdf_types(), row=0)
        self.b_var = tk.StringVar()
        self._file_row(grid, "PDF B:", self.b_var, self._pdf_types(), row=1)

        self._button(b, "Confronta", self._run, ACCENT).pack(pady=(16, 0), anchor="w")

        self._label(b, "Risultato:").pack(anchor="w", pady=(12, 2))
        self.result_box = scrolledtext.ScrolledText(b, height=10, bg=BG_DARK, fg=TEXT,
                                                    font=FONT_MONO, relief=tk.FLAT)
        self.result_box.pack(fill=tk.BOTH, expand=True)
        self.status = self._status_bar(self)

    def _run(self):
        a, b_ = self.a_var.get(), self.b_var.get()
        if not a or not b_:
            messagebox.showwarning("Attenzione", "Seleziona entrambi i file.")
            return
        self.status.set("Confronto in corso…")

        def _show(result):
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, f"Pagine PDF A: {result['pages_a']}\n")
            self.result_box.insert(tk.END, f"Pagine PDF B: {result['pages_b']}\n")
            if result["identical"]:
                self.result_box.insert(tk.END, "\n✔ I due PDF sono identici (testualmente).\n")
            else:
                self.result_box.insert(tk.END,
                    f"\n✖ Differenze trovate nelle pagine: {result['differing_pages']}\n")
            self.status.set("Confronto completato.")

        self._run_in_thread(
            lambda: pdf.compare_pdfs(a, b_),
            on_done=_show,
            on_error=lambda e: self.status.set(f"Errore: {e}")
        )
