import os
import owlready2 as owl
from pyswip import Prolog
from ml_module import SmartGardenML
from bayes_module import crea_rete_diagnosi
from csp_module import GardenCSP

# Caricamento KB
base_path = os.path.dirname(os.path.abspath(__file__))
onto_path = os.path.join(base_path, "..", "knowledge_base", "Ontologia.owx")
onto = owl.get_ontology(onto_path).load()

# Integrazione Prolog [cite: 1]
prolog = Prolog()
prolog.consult(os.path.join(base_path, "..", "knowledge_base", "kb.pl"))

def sistema_esperto_integrato(nome_pianta, dati_sensore):
    print(f"\n--- MONITORAGGIO SMART GARDEN: {nome_pianta} ---")
    
    # 1. ML: Rilevamento Anomalia
    ml = SmartGardenML(os.path.join(base_path, "..", "data", "dataset.csv"))
    stato = ml.predici_salute(dati_sensore)
    
    if stato == "Rischio_Malattia":
        # 2. ONTOLOGIA: Recupero sintomi [cite: 4, 23]
        pianta = onto.search_one(iri=f"*{nome_pianta}")
        sintomi = [s.name for s in pianta.presenta] # [cite: 23]
        
        if "Foglie_Gialle" in sintomi:
            # 3. BAYES: Diagnosi Incerta [cite: 22, 27]
            infer = crea_rete_diagnosi()
            res = infer.query(variables=['Carenza_Ferro'], evidence={'Foglie_Gialle': 1})
            prob = res.values[1]
            print(f"[Diagnosi] Probabilità Carenza Ferro: {prob*100:.1f}%")
            
            # 4. PROLOG: Regola di Contagio [cite: 1]
            if list(prolog.query(f"pericolo_contagio('{nome_pianta}', 'Pomodoro_San_Marzano')")):
                print("[Prolog] ATTENZIONE: Rischio contagio per piante vicine!")

if __name__ == "__main__":
    # Esempio per Basilico 
    test_dati = {'umidita': 0.15, 'luce': 8}
    sistema_esperto_integrato("Basilico_Genovese", test_dati)