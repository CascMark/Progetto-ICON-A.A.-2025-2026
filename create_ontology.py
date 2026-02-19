import os
import random
from owlready2 import *

# --- 1. CONFIGURAZIONE PERCORSI (FIX UNIVERSALE) ---
# Otteniamo la posizione esatta di questo file script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Logica intelligente: se siamo in 'src', saliamo di uno. Se siamo già in root, restiamo lì.
if os.path.basename(SCRIPT_DIR) == "src":
    ROOT_DIR = os.path.dirname(SCRIPT_DIR)
else:
    ROOT_DIR = SCRIPT_DIR

KB_DIR = os.path.join(ROOT_DIR, "knowledge_base")

# Creiamo la cartella se non esiste
if not os.path.exists(KB_DIR):
    os.makedirs(KB_DIR)

OUTPUT_FILE = os.path.join(KB_DIR, "Ontologia_Completa.owx")
IRI_BASE = "http://www.semanticweb.org/smartgarden/ontologia#"
NUM_ISTANZE = 500  # Generiamo 500 piante per avere un dataset serio

print(f"--- CREAZIONE ONTOLOGIA (V4.1 - FIX PERCORSI) ---")
print(f"1. Script eseguito da: {SCRIPT_DIR}")
print(f"2. Root Progetto rilevata: {ROOT_DIR}")
print(f"3. File Output: {OUTPUT_FILE}")

# Creazione Ontologia
onto = get_ontology(IRI_BASE)

with onto:
    # --- 2. GERARCHIA DELLE CLASSI (TASSONOMIA ESTESA) ---
    class Pianta(Thing): pass
    
    class Solanaceae(Pianta): pass   # Pomodoro, Peperone, Melanzana
    class Cucurbitaceae(Pianta): pass # Zucchina, Cetriolo
    class Lamiaceae(Pianta): pass     # Basilico, Menta
    class Rosaceae(Pianta): pass      # Rosa, Fragola
    
    class Sintomo(Thing): pass
    class Malattia(Thing): pass

    # --- 3. PROPRIETÀ DATI (FEATURES) ---
    class richiedeOreLuce(DataProperty, FunctionalProperty):
        domain = [Pianta]
        range = [float] 

    class haLivelloUmiditaOttimale(DataProperty, FunctionalProperty):
        domain = [Pianta]
        range = [float] 

    class haPHOttimale(DataProperty, FunctionalProperty):
        domain = [Pianta]
        range = [float]

    class haTemperaturaOttimale(DataProperty, FunctionalProperty):
        domain = [Pianta]
        range = [float]

    # --- 4. PROPRIETÀ OGGETTO ---
    class presenta(ObjectProperty):
        domain = [Pianta]
        range = [Sintomo]

    class affettaDa(ObjectProperty, FunctionalProperty):
        domain = [Pianta]
        range = [Malattia]
        
    class compatibileCon(ObjectProperty, SymmetricProperty):
        domain = [Pianta]
        range = [Pianta]

    # --- 5. POPOLAMENTO T-BOX (Concetti Base) ---
    giallo = Sintomo("Foglie_Gialle")
    macchie = Sintomo("Macchie_Fogliari")
    secco = Sintomo("Foglie_Secche")
    muffa = Sintomo("Muffa_Bianca")
    arricciate = Sintomo("Foglie_Arricciate")
    marciume = Sintomo("Marciume_Apicale")
    ragnatele = Sintomo("Ragnatele")

    sano = Malattia("Sano")
    afidi = Malattia("Infestazione_Afidi")
    peronospora = Malattia("Peronospora")
    oidio = Malattia("Oidio")
    botrite = Malattia("Botrite")
    ragnetto = Malattia("Ragnetto_Rosso")
    stress = Malattia("Stress_Idrico")

    # --- 6. GENERATORE PROCEDURALE DI DATASET (A-BOX) ---
    templates = [
        (Solanaceae, "Pomodoro", 8.0, 10.0, 0.5, 0.7, [peronospora, afidi, marciume]),
        (Solanaceae, "Peperone", 7.0, 9.0, 0.4, 0.6, [afidi, oidio]),
        (Cucurbitaceae, "Zucchina", 6.0, 9.0, 0.6, 0.8, [oidio, muffa]),
        (Lamiaceae, "Basilico", 5.0, 8.0, 0.5, 0.7, [peronospora, stress]),
        (Lamiaceae, "Menta", 4.0, 6.0, 0.7, 0.9, [ragnetto, afidi]),
        (Rosaceae, "Rosa", 6.0, 8.0, 0.4, 0.6, [oidio, ragnetto]),
        (Rosaceae, "Fragola", 7.0, 9.0, 0.6, 0.8, [botrite, muffa])
    ]

    print(f"Generazione simulata di {NUM_ISTANZE} piante in corso...")

    for i in range(NUM_ISTANZE):
        template = random.choice(templates)
        cls_obj, nome_base, l_min, l_max, u_min, u_max, mal_list = template
        
        nome_istanza = f"{nome_base}_{i:03d}"
        pianta = cls_obj(nome_istanza)
        
        pianta.richiedeOreLuce = round(random.uniform(l_min, l_max), 2)
        pianta.haLivelloUmiditaOttimale = round(random.uniform(u_min, u_max), 2)
        pianta.haTemperaturaOttimale = round(random.uniform(15.0, 30.0), 1)
        pianta.haPHOttimale = round(random.uniform(6.0, 7.5), 1)
        
        if random.random() < 0.3:
            malattia_scelta = random.choice(mal_list)
            pianta.affettaDa = malattia_scelta
            
            if malattia_scelta == afidi:
                pianta.presenta.extend([arricciate, giallo])
            elif malattia_scelta == oidio:
                pianta.presenta.append(muffa)
            elif malattia_scelta == peronospora:
                pianta.presenta.extend([macchie, secco])
            elif malattia_scelta == ragnetto:
                pianta.presenta.append(ragnatele)
            elif malattia_scelta == botrite:
                pianta.presenta.extend([marciume, muffa])
            elif malattia_scelta == stress:
                pianta.presenta.append(secco)
        else:
            pianta.affettaDa = sano

try:
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    onto.save(file=OUTPUT_FILE)
    print(f"[SUCCESSO] Ontologia salvata correttamente in:")
    print(f">>> {OUTPUT_FILE}")
except Exception as e:
    print(f"[ERRORE] Impossibile salvare: {e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Salviamo l'ontologia usando semplicemente la variabile 'onto' (senza self)
onto.save(file=os.path.join(BASE_DIR, 'knowledge_base', 'Ontologia_Aggiornata.owl'), format="rdfxml")