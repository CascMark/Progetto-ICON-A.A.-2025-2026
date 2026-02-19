import tkinter as tk
from tkinter import ttk
import os
import sys
import threading
import io

# --- CONFIGURAZIONE PATH ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, ROOT_DIR)

# --- IMPORT BACKEND E ROVER ---
from main import SmartGardenSystem

# Prova a importare la classe del Rover (assicurati che il file si chiami rover_tab.py e sia nella stessa cartella o in src)
try:
    from rover_tab import RoverTab
except ImportError:
    RoverTab = None

# ══════════════════════════════════════════════════════════════════
#  COSTANTI DI STILE
# ══════════════════════════════════════════════════════════════════
BG_DARK      = "#021f02"
BG_PANEL     = "#0a3d0a"
BG_CARD      = "#0f5c0f"
ACCENT_GREEN = "#2ecc71"
ACCENT_LIGHT = "#d4f7d4"
TEXT_WHITE   = "#ffffff"
TEXT_MUTED   = "#a8d8a8"
BTN_COLOR    = "#1a7a1a"
BTN_HOVER    = "#238c23"
ERROR_COLOR  = "#e74c3c"
WARN_COLOR   = "#f39c12"

FONT_TITLE   = ("Georgia", 52, "bold")
FONT_HEADING = ("Georgia", 13, "bold")
FONT_LABEL   = ("Courier", 10)
FONT_MONO    = ("Courier", 10)
FONT_BTN     = ("Georgia", 11, "bold")
FONT_STATUS  = ("Courier", 9)


# ══════════════════════════════════════════════════════════════════
#  CLASSE PRINCIPALE GUI
# ══════════════════════════════════════════════════════════════════
class GreenLeafGui:
    
    PIANTE  = [
        "Basilico", "Pomodoro", "Lattuga", "Rosa", "Peperone", 
        "Fragola", "Zucchina", "Menta"
    ]
    SINTOMI = [
        "Foglie_Gialle", "Macchie_Fogliari", "Foglie_Secche", 
        "Muffa_Bianca", "Foglie_Arricciate", "Marciume_Apicale", "Ragnatele"
    ]

    # I tuoi tab testuali standard
    TAB_INFO = [
        ("🤖  ML",      "Risultati Machine Learning (Random Forest, Rete Neurale, K-Means)"),
        ("🧠  Prolog",  "Motore Inferenziale — Trattamenti dalla Knowledge Base"),
        ("📊  Bayes",   "Rete Bayesiana — Probabilità delle Cause"),
        ("🌿  CSP",     "Constraint Satisfaction — Posizione Ottimale nel Giardino"),
        ("📈  Validazione", "Validazione Scientifica — 10-Fold CV e Consensus"),
    ]

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Green Leaf — Giardino Intelligente")
        self.root.geometry("1050x700") # Leggermente più grande per contenere bene la griglia del Rover
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)

        # Tenta di massimizzare la finestra all'avvio (funziona su Windows)
        try:
            self.root.state('zoomed')
        except:
            pass
    
        self.system = None
        self.status_var = tk.StringVar(value="⏳  Avvio sistema in corso…")
        self.result_texts: dict[str, tk.Text] = {}

        self._build_header()
        self._build_input_section()
        self._build_results_section()
        self._build_status_bar()

        threading.Thread(target=self._load_system, daemon=True).start()

    def _load_system(self):
        try:
            self.system = SmartGardenSystem()
            self.root.after(0, lambda: self.status_var.set("✅  Sistema pronto. Seleziona pianta e sintomo, poi premi Analizza."))
            self.root.after(0, lambda: self.btn_analizza.config(state="normal"))
        except Exception as e:
            self.root.after(0, lambda err=e: self.status_var.set(f"❌  Errore caricamento: {err}"))

    def _build_header(self):
        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", pady=(30, 0))

        tk.Label(header, text="🌿 Green Leaf", font=FONT_TITLE, bg=BG_DARK, fg=ACCENT_GREEN).pack()
        tk.Label(header, text="Sistema AI per la diagnosi e cura del giardino", font=("Georgia", 11, "italic"), bg=BG_DARK, fg=TEXT_MUTED).pack(pady=(2, 20))
        tk.Frame(self.root, bg=ACCENT_GREEN, height=2).pack(fill="x", padx=30)

    def _build_input_section(self):
        container = tk.Frame(self.root, bg=BG_PANEL, pady=18, padx=25)
        container.pack(fill="x", padx=30, pady=14)

        tk.Label(container, text="INSERISCI I DATI", font=FONT_HEADING, bg=BG_PANEL, fg=ACCENT_LIGHT).grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 10))

        tk.Label(container, text="Pianta:", font=FONT_LABEL, bg=BG_PANEL, fg="#ffffff").grid(row=1, column=0, sticky="w", padx=(0, 6))
        self.pianta_var = tk.StringVar(value=self.PIANTE[0])
        self._styled_combo(container, self.pianta_var, self.PIANTE).grid(row=1, column=1, padx=(0, 20))

        tk.Label(container, text="Sintomo:", font=FONT_LABEL, bg=BG_PANEL, fg="#ffffff").grid(row=1, column=2, sticky="w", padx=(0, 6))
        self.sintomo_var = tk.StringVar(value=self.SINTOMI[0])
        self._styled_combo(container, self.sintomo_var, self.SINTOMI, width=20).grid(row=1, column=3, padx=(0, 20))

        self.btn_analizza = tk.Button(
            container, text="🔍  Analizza", font=FONT_BTN, bg=BTN_COLOR, fg=TEXT_WHITE,
            activebackground=BTN_HOVER, activeforeground=TEXT_WHITE, relief="flat",
            cursor="hand2", padx=14, pady=6, state="disabled", command=self._run_analysis,
        )
        self.btn_analizza.grid(row=1, column=4)

    def _styled_combo(self, parent, variable, values, width=14):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Green.TCombobox", fieldbackground=BG_CARD, background=BG_CARD, foreground=TEXT_WHITE,
                        selectbackground=ACCENT_GREEN, selectforeground=BG_DARK, bordercolor=ACCENT_GREEN, arrowcolor=ACCENT_GREEN)
        return ttk.Combobox(parent, textvariable=variable, values=values, width=width, state="readonly", style="Green.TCombobox", font=FONT_MONO)

    def _build_results_section(self):
        container = tk.Frame(self.root, bg=BG_DARK)
        container.pack(fill="both", expand=True, padx=30, pady=(0, 5))

        style = ttk.Style()
        style.configure("Green.TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("Green.TNotebook.Tab", background=BG_PANEL, foreground=TEXT_MUTED, padding=[12, 5], font=FONT_HEADING)
        style.map("Green.TNotebook.Tab", background=[("selected", BG_CARD)], foreground=[("selected", ACCENT_GREEN)])

        notebook = ttk.Notebook(container, style="Green.TNotebook")
        notebook.pack(fill="both", expand=True)

        # 1. CREA I TAB DI TESTO CLASSICI
        for tab_name, tab_desc in self.TAB_INFO:
            frame = tk.Frame(notebook, bg=BG_CARD)
            notebook.add(frame, text=tab_name)

            tk.Label(frame, text=tab_desc, font=("Courier", 9, "italic"), bg=BG_CARD, fg="#c8e8c8", anchor="w").pack(fill="x", padx=10, pady=(6, 2))
            tk.Frame(frame, bg=ACCENT_GREEN, height=1).pack(fill="x", padx=10)

            txt = tk.Text(frame, bg=BG_CARD, fg=TEXT_WHITE, font=FONT_MONO, relief="flat", padx=12, pady=8,
                          state="disabled", wrap="word", insertbackground=ACCENT_GREEN, selectbackground=ACCENT_GREEN, selectforeground=BG_DARK)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
            txt.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            txt.pack(fill="both", expand=True, padx=(10, 0), pady=8)

            txt.tag_configure("header",  foreground="#4ded8f",  font=("Courier", 10, "bold"))
            txt.tag_configure("ok",      foreground="#e8ffe8")
            txt.tag_configure("warn",    foreground="#ffd27f")
            txt.tag_configure("error",   foreground="#ff6b6b")
            txt.tag_configure("muted",   foreground="#b8ddb8")
            txt.tag_configure("value",   foreground="#ffffff", font=("Courier", 10, "bold"))

            self.result_texts[tab_name] = txt
            self._write_to_tab(tab_name, "In attesa di un'analisi…\n", "muted")

        # 2. INTEGRAZIONE DEL NUOVO TAB ROVER A*
        tab_rover_frame = tk.Frame(notebook, bg=BG_DARK) # Sfondo scuro per matchare la dashboard
        notebook.add(tab_rover_frame, text="🚜  Rover A*")
        
        if RoverTab:
            # Passiamo il frame del tab direttamente alla classe del Rover
            self.rover_app = RoverTab(tab_rover_frame)
        else:
            tk.Label(tab_rover_frame, text="⚠️ Modulo 'rover_tab.py' non trovato nella cartella.", 
                     font=FONT_HEADING, bg=BG_DARK, fg=ERROR_COLOR).pack(pady=50)

    def _build_status_bar(self):
        bar = tk.Frame(self.root, bg="#010e01", pady=4)
        bar.pack(fill="x", side="bottom")
        tk.Label(bar, textvariable=self.status_var, font=FONT_STATUS, bg="#010e01", fg="#c0e0c0", anchor="w", padx=12).pack(fill="x")

    def _run_analysis(self):
        if not self.system:
            self.status_var.set("⚠️  Sistema non ancora pronto.")
            return

        self.btn_analizza.config(state="disabled")
        self.status_var.set("⏳  Analisi in corso…")

        for name in self.result_texts:
            self._clear_tab(name)

        pianta  = self.pianta_var.get()
        sintomo = self.sintomo_var.get()

        threading.Thread(target=self._do_analysis, args=(pianta, sintomo), daemon=True).start()

    def _do_analysis(self, pianta: str, sintomo: str):
        try:
            buf = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buf

            self.system.analizza_caso(pianta, sintomo)

            sys.stdout = old_stdout
            output = buf.getvalue()

            self.root.after(0, lambda: self._parse_and_display(output, pianta, sintomo))

        except Exception as e:
            sys.stdout = old_stdout if 'old_stdout' in dir() else sys.stdout
            self.root.after(0, lambda err=e: self.status_var.set(f"❌  Errore caricamento: {err}"))

        finally:
            self.root.after(0, lambda: self.btn_analizza.config(state="normal"))
            self.root.after(0, lambda: self.status_var.set(f"✅  Analisi completata per: {pianta} / {sintomo}"))

    def _parse_and_display(self, output: str, pianta: str, sintomo: str):
        lines = output.splitlines()

        blocks = {"ml": [], "prolog": [], "bayes": [], "csp": [], "val": []}
        current = None

        for line in lines:
            if "[1] INTELLIGENZA ARTIFICIALE" in line:
                current = "ml"
            elif "[2] PROLOG" in line:
                current = "prolog"
            elif "[3] RETE BAYESIANA" in line:
                current = "bayes"
            elif "[4] CSP" in line:
                current = "csp"
            elif "[5] VALIDAZIONE" in line:
                current = "val"

            if current:
                blocks[current].append(line)

        tab_map = {
            "ml":     "🤖  ML",
            "prolog": "🧠  Prolog",
            "bayes":  "📊  Bayes",
            "csp":    "🌿  CSP",
            "val":    "📈  Validazione",
        }

        for key, tab_name in tab_map.items():
            self._clear_tab(tab_name)
            self._write_to_tab(tab_name, f"📋  {pianta}  ›  {sintomo}\n\n", "header")
            for line in blocks[key]:
                self._format_line(tab_name, line)

    def _format_line(self, tab_name: str, line: str):
        if not line.strip():
            self._write_to_tab(tab_name, "\n")
            return
        low = line.lower()
        if "errore" in low or "error" in low or "attenzione" in low:
            tag = "error"
        elif "successo" in low or "pronto" in low or "concordano" in low or "unanime" in low:
            tag = "ok"
        elif "discrepanza" in low or "nota" in low or "variazione" in low:
            tag = "warn"
        elif line.strip().startswith("[") or line.strip().startswith("="):
            tag = "header"
        elif line.strip().startswith("->") or line.strip().startswith("*") or "|" in line:
            tag = "value"
        else:
            tag = "ok"

        self._write_to_tab(tab_name, line + "\n", tag)

    def _write_to_tab(self, tab_name: str, text: str, tag: str = "ok"):
        txt = self.result_texts.get(tab_name)
        if txt:
            txt.config(state="normal")
            txt.insert("end", text, tag)
            txt.see("end")
            txt.config(state="disabled")

    def _clear_tab(self, tab_name: str):
        txt = self.result_texts.get(tab_name)
        if txt:
            txt.config(state="normal")
            txt.delete("1.0", "end")
            txt.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = GreenLeafGui(root)
    root.mainloop()