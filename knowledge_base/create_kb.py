import os

# --- CONFIGURAZIONE PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
KB_DIR = os.path.join(ROOT_DIR, "knowledge_base")

# Assicuriamoci che la cartella esista
if not os.path.exists(KB_DIR):
    os.makedirs(KB_DIR)

OUTPUT_FILE = os.path.join(KB_DIR, "kb.pl")

print(f"--- GENERATORE KNOWLEDGE BASE PROLOG ---")
print(f"File destinazione: {OUTPUT_FILE}")

# --- CONTENUTO DELLA KNOWLEDGE BASE ---
# Qui definiamo le regole che Prolog deve conoscere.
# Usiamo i Nomi Semplici (Basilico, Pomodoro...)

prolog_content = """% =======================================================
%  KNOWLEDGE BASE PROLOG - SMART GARDEN
%  Generato automaticamente da src/create_kb.py
% =======================================================

% --- 1. REGOLE DI TRATTAMENTO ---
% Sintassi: trattamento('Malattia', 'Cura').

trattamento('Afidi', 'Olio_di_Neem').
trattamento('Carenza_Ferro', 'Chelato_di_Ferro').
trattamento('Peronospora', 'Rame_Metallo').
trattamento('Ruggine', 'Fungicida_Rameico').
trattamento('Stress_Idrico', 'Regolazione_Irrigazione').
trattamento('Oidio', 'Zolfo_Bagnabile').
trattamento('Muffa_Bianca', 'Zolfo_Bagnabile').
trattamento('Virosi', 'Rimozione_Pianta_Infetta').
trattamento('Carenza_Nutrienti', 'Concime_NPK_Liquido').

% Casi speciali
trattamento('Sano', 'Nessuna_Azione_Richiesta').
trattamento('Nessuna', 'Monitoraggio_Preventivo').

% Fallback: Se la malattia non è in lista
trattamento(X, 'Consultare_Agronomo') :- 
    \+ trattamento(X, _).


% --- 2. REGOLE DI DIAGNOSI LOGICA ---
% Sintassi: diagnosi('Pianta', 'Sintomo', 'Malattia').
% Queste regole rappresentano la conoscenza "da manuale".

diagnosi('Basilico', 'Foglie_Gialle', 'Afidi').
diagnosi('Pomodoro', 'Macchie_Fogliari', 'Peronospora').
diagnosi('Lattuga', 'Foglie_Secche', 'Stress_Idrico').
diagnosi('Rosa', 'Muffa_Bianca', 'Oidio').
diagnosi('Peperone', 'Macchie_Fogliari', 'Virosi').

% Regola generica
diagnosi(_, _, 'In_Analisi_Approfondita').
"""

# --- SCRITTURA FILE ---
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(prolog_content)
    print(" -> [SUCCESSO] File 'kb.pl' creato correttamente!")
    print("    Ora il sistema Prolog ha le regole aggiornate.")
except Exception as e:
    print(f" -> [ERRORE] Impossibile scrivere il file: {e}")