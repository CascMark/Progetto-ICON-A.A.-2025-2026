import os
from owlready2 import *

# --- CONFIGURAZIONE PERCORSI ---
CURRENT_DIR = os.getcwd() 
KB_DIR = os.path.join(CURRENT_DIR, "knowledge_base")

if not os.path.exists(KB_DIR):
    os.makedirs(KB_DIR)

OUTPUT_FILE = os.path.join(KB_DIR, "Ontologia_Completa.owx")
IRI_BASE = "http://www.semanticweb.org/smartgarden/ontologia#"

print(f"--- CREAZIONE ONTOLOGIA  ---")
print(f"Output: {OUTPUT_FILE}")

onto = get_ontology(IRI_BASE)

with onto:
    # Classi
    class Pianta(Thing): pass
    class Ortaggio(Pianta): pass
    class Aromatica(Pianta): pass
    class Ornamentale(Pianta): pass
    
    class Sintomo(Thing): pass
    class Avversita(Thing): pass

    # Proprietà Dati (CSP)
    class richiedeOreLuce(DataProperty, FunctionalProperty):
        domain = [Pianta]
        range = [int]

    class haLivelloUmiditaOttimale(DataProperty, FunctionalProperty):
        domain = [Pianta]
        range = [float]

    # Proprietà Oggetto
    class compatibileCon(ObjectProperty, SymmetricProperty):
        domain = [Pianta]
        range = [Pianta]

    class presenta(ObjectProperty):
        domain = [Pianta]
        range = [Sintomo]

    class colpisce(ObjectProperty):
        domain = [Avversita]
        range = [Pianta]

    # --- POPOLAMENTO INDIVIDUI (Nomi Semplici) ---
    
    # Sintomi
    giallo = Sintomo("Foglie_Gialle")
    macchie = Sintomo("Macchie_Fogliari")
    secco = Sintomo("Foglie_Secche")
    muffa = Sintomo("Muffa_Bianca")

    # Malattie
    afidi = Avversita("Afidi")
    perono = Avversita("Peronospora")
    stress = Avversita("Stress_Idrico")
    oidio = Avversita("Oidio")
    ferro = Avversita("Carenza_Ferro")

    # PIANTE (Nomi Generali)
    
    # 1. Basilico
    basilico = Aromatica("Basilico") # Non più Basilico_Genovese
    basilico.richiedeOreLuce = 6
    basilico.haLivelloUmiditaOttimale = 0.6
    basilico.presenta.append(giallo)

    # 2. Pomodoro
    pomodoro = Ortaggio("Pomodoro") # Non più Pomodoro_San_Marzano
    pomodoro.richiedeOreLuce = 9
    pomodoro.haLivelloUmiditaOttimale = 0.5
    pomodoro.presenta.append(macchie)

    # 3. Lattuga
    lattuga = Ortaggio("Lattuga") # Non più Lattuga_Romana
    lattuga.richiedeOreLuce = 5
    lattuga.haLivelloUmiditaOttimale = 0.8
    lattuga.presenta.append(secco)

    # 4. Rosa
    rosa = Ornamentale("Rosa") # Non più Rosa_Rossa
    rosa.richiedeOreLuce = 7
    rosa.haLivelloUmiditaOttimale = 0.6
    rosa.presenta.append(muffa)
    
    # 5. Peperone
    peperone = Ortaggio("Peperone")
    peperone.richiedeOreLuce = 8
    peperone.haLivelloUmiditaOttimale = 0.5

    # Compatibilità
    basilico.compatibileCon.append(pomodoro)
    basilico.compatibileCon.append(peperone)
    pomodoro.compatibileCon.append(basilico)

# --- SALVATAGGIO ---
try:
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    onto.save(file=OUTPUT_FILE)
    print(f"[SUCCESSO] Ontologia creata!")
except Exception as e:
    print(f"[ERRORE] {e}")