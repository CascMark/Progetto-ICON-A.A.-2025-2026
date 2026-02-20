import os
import pandas as pd
from owlready2 import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.basename(SCRIPT_DIR) == "src":
    ROOT_DIR = os.path.dirname(SCRIPT_DIR)
else:
    ROOT_DIR = SCRIPT_DIR

ONTO_PATH = os.path.join(ROOT_DIR, "knowledge_base", "Ontologia_Completa.owx")

OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "piante_dataset.csv")

def safe_get_property(prop):
    """Estrae valori puliti da proprietà funzionali o liste"""
    if prop is None: return None
    if isinstance(prop, list) and len(prop) > 0:
        return prop[0]
    if not isinstance(prop, list):
        return prop
    return None

def genera_dataset_da_ontologia():
    print("--- GENERAZIONE DATASET (V4.2 - FIX PATH & RELOAD) ---")
    print(f"1. Cerco ontologia in: {ONTO_PATH}")
    
    if not os.path.exists(ONTO_PATH):
        print(f"[ERRORE FATALE] File non trovato!")
        print(f"Verifica che il percorso sia: {ONTO_PATH}")
        return

    try:
        default_world.ontologies.clear() 
        onto = get_ontology(ONTO_PATH).load(reload=True)
        print("-> Ontologia caricata e aggiornata.")
    except Exception as e:
        print(f"[ERRORE] Impossibile caricare l'ontologia: {e}")
        return
    
    data_rows = []
    
    piante = onto.search(type=onto.Pianta)
    print(f"-> Trovate {len(piante)} istanze di piante.")
    
    if len(piante) < 20:
        print("\n[ATTENZIONE] Trovate poche piante! Sembra ancora l'ontologia vecchia.")
        print("Suggerimento: Esegui di nuovo 'python create_ontology.py' e controlla dove salva il file.\n")

    for p in piante:
        nome = p.name
        
        famiglia = "Sconosciuta"
        for cls in p.is_a:
            if hasattr(cls, "name") and cls.name not in ["Thing", "Pianta", "NamedIndividual"]:
                famiglia = cls.name
                break
        
        luce = safe_get_property(p.richiedeOreLuce)
        umidita = safe_get_property(p.haLivelloUmiditaOttimale)
        temp = safe_get_property(p.haTemperaturaOttimale)
        ph = safe_get_property(p.haPHOttimale)
        
        malattia_obj = safe_get_property(p.affettaDa)
        malattia = malattia_obj.name if malattia_obj else "Sano"
        
        sintomi_list = [s.name for s in p.presenta]
        sintomi_str = ", ".join(sintomi_list) if sintomi_list else "Nessuno"

        data_rows.append({
            "ID_Pianta": nome,
            "Famiglia": famiglia,
            "Ore_Luce": luce,
            "Umidita_Ottimale": umidita,
            "Temperatura_Ottimale": temp,
            "PH_Suolo": ph,
            "Sintomi_Visivi": sintomi_str,
            "Diagnosi_Reale": malattia 
        })

    if data_rows:
        df = pd.DataFrame(data_rows)
        
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print(f"[INFO] Creata cartella {OUTPUT_DIR}")
        
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        print(f"\n[SUCCESSO] Dataset generato: {len(df)} righe.")
        print(f"Salvato in: {OUTPUT_FILE}")
        
        print("\nDistribuzione Famiglie:")
        print(df["Famiglia"].value_counts().head())
    else:
        print("[AVVISO] Nessun dato estratto.")

if __name__ == "__main__":
    genera_dataset_da_ontologia()