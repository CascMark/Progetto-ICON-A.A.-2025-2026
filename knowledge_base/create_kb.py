import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
KB_DIR = os.path.join(ROOT_DIR, "knowledge_base")

if not os.path.exists(KB_DIR):
    os.makedirs(KB_DIR)

OUTPUT_FILE = os.path.join(KB_DIR, "kb.pl")

print(f"--- ESPANSIONE KNOWLEDGE BASE (V3.0) ---")

prolog_content = """% =======================================================
%  KNOWLEDGE BASE PROLOG - SMART GARDEN V3.0
%  (Espansione: Fragole, Zucchine, Nuove Patologie)
% =======================================================

% --- 1. REGOLE DI TRATTAMENTO (CURE) ---
trattamento('Afidi', 'Olio_di_Neem').
trattamento('Carenza_Ferro', 'Chelato_di_Ferro').
trattamento('Carenza_Calcio', 'Integratore_Calcio').
trattamento('Peronospora', 'Rame_Metallo').
trattamento('Ruggine', 'Fungicida_Rameico').
trattamento('Stress_Idrico', 'Regolazione_Irrigazione').
trattamento('Oidio', 'Zolfo_Bagnabile').
trattamento('Muffa_Bianca', 'Zolfo_Bagnabile').
trattamento('Botrite', 'Fungicida_Antibotritico').
trattamento('Virosi', 'Rimozione_Pianta_Infetta').
trattamento('Ragnetto_Rosso', 'Acaricida_Specifico').
trattamento('Marciume_Radicale', 'Ridurre_Acqua_e_Fungicida').

% Casi speciali
trattamento('Sano', 'Nessuna_Azione_Richiesta').
trattamento('Nessuna', 'Monitoraggio_Preventivo').
trattamento(X, 'Consultare_Agronomo') :- \+ trattamento(X, _).

% --- 2. REGOLE DI DIAGNOSI LOGICA (Il Manuale Completo) ---
% Sintassi: diagnosi('Pianta', 'Sintomo', 'Malattia').

% --- BASILICO ---
diagnosi('Basilico', 'Foglie_Gialle', 'Afidi').
diagnosi('Basilico', 'Macchie_Fogliari', 'Peronospora').  % 
diagnosi('Basilico', 'Foglie_Arricciate', 'Stress_Idrico').

% --- POMODORO ---
diagnosi('Pomodoro', 'Macchie_Fogliari', 'Peronospora').
diagnosi('Pomodoro', 'Foglie_Gialle', 'Carenza_Ferro').
diagnosi('Pomodoro', 'Marciume_Apicale', 'Carenza_Calcio').
diagnosi('Pomodoro', 'Foglie_Arricciate', 'Virosi').

% --- LATTUGA ---
diagnosi('Lattuga', 'Foglie_Secche', 'Stress_Idrico').
diagnosi('Lattuga', 'Muffa_Bianca', 'Botrite').
diagnosi('Lattuga', 'Foglie_Gialle', 'Afidi').

% --- ROSA ---
diagnosi('Rosa', 'Muffa_Bianca', 'Oidio').
diagnosi('Rosa', 'Macchie_Fogliari', 'Ruggine').
diagnosi('Rosa', 'Ragnatele', 'Ragnetto_Rosso').

% --- PEPERONE ---
diagnosi('Peperone', 'Macchie_Fogliari', 'Virosi').
diagnosi('Peperone', 'Foglie_Arricciate', 'Afidi').

% --- FRAGOLA (Nuova!) ---
diagnosi('Fragola', 'Muffa_Bianca', 'Botrite').
diagnosi('Fragola', 'Macchie_Fogliari', 'Ruggine').

% --- ZUCCHINA (Nuova!) ---
diagnosi('Zucchina', 'Muffa_Bianca', 'Oidio').
diagnosi('Zucchina', 'Foglie_Gialle', 'Carenza_Nutrienti').

% --- MENTA (Nuova!) ---
diagnosi('Menta', 'Ragnatele', 'Ragnetto_Rosso').
diagnosi('Menta', 'Macchie_Fogliari', 'Ruggine').

% Regola Fallback
diagnosi(_, _, 'In_Analisi_Approfondita').
"""

try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(prolog_content)
    print(" -> [SUCCESSO] KB espansa con nuove piante e malattie.")
except Exception as e:
    print(f" -> [ERRORE] {e}")