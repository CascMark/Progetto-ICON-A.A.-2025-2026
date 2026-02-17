import os
import sys
import owlready2 as owl

# Importiamo i moduli personalizzati
# Assicurati che ml_module.py, prolog_module.py, bayes_module.py, csp_module.py siano in src/
from ml_module import DiseasePredictorML
from prolog_module import GardenLogic
from bayes_module import crea_rete_diagnosi
from csp_module import GardenCSP

# --- CONFIGURAZIONE PERCORSI ---
# Rendiamo il codice portabile su qualsiasi computer (Windows/Mac/Linux)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))       # Cartella src/
ROOT_DIR = os.path.dirname(BASE_DIR)                        # Cartella del progetto
DATA_DIR = os.path.join(ROOT_DIR, 'data')
KB_DIR = os.path.join(ROOT_DIR, 'knowledge_base')

class SmartGardenSystem:
    def __init__(self):
        print("\n" + "="*50)
        print("   AVVIO SISTEMA SMART GARDEN (KBS INTEGRATO)")
        print("="*50)
        
        # 1. Caricamento Dataset e Training ML (Capitoli 2-3)
        # Usa il dataset coerente generato dall'Ontologia
        print(" [1/4] Addestramento Modello Machine Learning...", end=" ")
        try:
            csv_path = os.path.join(DATA_DIR, 'dataset_integrato.csv')
            if not os.path.exists(csv_path):
                raise FileNotFoundError("Esegui prima 'generate_dataset.py' per creare il CSV!")
            
            self.ml_engine = DiseasePredictorML(csv_path)
            print("OK.")
        except Exception as e:
            print(f"\n [ERRORE ML] {e}")
            self.ml_engine = None

        # 2. Caricamento Knowledge Base Prolog (Capitolo 5)
        print(" [2/4] Caricamento Motore Logico (Prolog)...", end=" ")
        try:
            kb_path = os.path.join(KB_DIR, 'kb.pl')
            # Fix per Windows: Prolog richiede slash normali '/'
            kb_path = kb_path.replace('\\', '/')
            
            if not os.path.exists(kb_path):
                # Se non trova kb.pl, prova kb (1).pl come fallback
                kb_path = os.path.join(KB_DIR, 'kb (1).pl').replace('\\', '/')
            
            self.logic_engine = GardenLogic(kb_path)
            print("OK.")
        except Exception as e:
            print(f"\n [ERRORE PROLOG] {e}")
            self.logic_engine = None

        # 3. Caricamento Ontologia OWL (Struttura Dati)
        print(" [3/4] Caricamento Ontologia OWL...", end=" ")
        try:
            onto_path = os.path.join(KB_DIR, 'Ontologia.owx')
            self.onto = owl.get_ontology(onto_path).load()
            print("OK.")
        except Exception as e:
            print(f"\n [ERRORE ONTOLOGIA] {e}")
            self.onto = None

        # 4. Inizializzazione Rete Bayesiana (Capitolo 4)
        print(" [4/4] Configurazione Rete Bayesiana...", end=" ")
        try:
            self.bayes_net = crea_rete_diagnosi()
            print("OK.")
        except Exception as e:
            print(f"\n [ERRORE BAYES] {e}")
            self.bayes_net = None

    def analizza_caso(self, nome_pianta, nome_sintomo):
        """
        Esegue il ciclo completo: ML -> Prolog -> Bayes -> CSP
        """
        print(f"\n\n{'='*60}")
        print(f" ANALISI CASO: {nome_pianta} | SINTOMO: {nome_sintomo}")
        print(f"{'='*60}")

        if not self.ml_engine:
            print("Errore critico: Modello ML non caricato.")
            return

        # --- STEP 1: MACHINE LEARNING (Predizione) ---
        malattia_predetta, confidenza = self.ml_engine.predici_malattia(nome_pianta, nome_sintomo)
        
        print(f"\n[1] MACHINE LEARNING (Classificazione Random Forest)")
        print(f" -> Diagnosi Statistica: {malattia_predetta}")
        print(f" -> Confidenza: {confidenza*100:.2f}%")

        # --- STEP 2: PROLOG (Logica e Trattamento) ---
        print(f"\n[2] PROLOG (Motore Inferenziale)")
        if self.logic_engine:
            # Cerca la cura
            cure = self.logic_engine.ottieni_trattamento(malattia_predetta)
            if cure:
                print(f" -> Trattamento dedotto dalla KB: {cure}")
            else:
                print(f" -> Nessuna regola di trattamento trovata per '{malattia_predetta}'")
            
            # Verifica consistenza logica
            conferme = self.logic_engine.verifica_diagnosi_logica(nome_pianta, nome_sintomo)
            if conferme:
                print(f" -> Consistenza logica verificata: Regola esistente per {conferme}")
        else:
            print(" -> Modulo Prolog non attivo.")

        # --- STEP 3: RETE BAYESIANA (Gestione Incertezza) ---
        # Si attiva solo per sintomi ambigui noti
        if nome_sintomo in ["Foglie_Gialle", "Macchie_Fogliari"]:
            print(f"\n[3] RETE BAYESIANA (Diagnosi Probabilistica)")
            if self.bayes_net:
                try:
                    # Esempio: calcoliamo probabilità per Carenza Ferro
                    res = self.bayes_net.query(variables=['Carenza_Ferro'], evidence={'Foglie_Gialle': 1})
                    prob = res.values[1]
                    print(f" -> Probabilità 'Carenza_Ferro' dato il sintomo: {prob*100:.2f}%")
                except Exception as e:
                    print(f" -> Errore inferenza: {e}")
            else:
                print(" -> Modulo Bayesiano non attivo.")

        # --- STEP 4: CSP (Ottimizzazione Spaziale) ---
        print(f"\n[4] CSP (Constraint Satisfaction Problem)")
        if self.onto:
            # Definiamo un ambiente virtuale per il test
            ambiente_balcone = {
                "Vaso_A (Soleggiato)": {"luce": 9, "umidita": 0.5},
                "Vaso_B (Ombreggiato)": {"luce": 5, "umidita": 0.8},
                "Vaso_C (Interno)":    {"luce": 7, "umidita": 0.6}
            }
            
            print(f" -> Ricerca posizione ottimale per: {nome_pianta}")
            try:
                # Grazie al dataset rigenerato, i nomi coincidono! Nessuna mappa necessaria.
                solver = GardenCSP([nome_pianta], ambiente_balcone, self.onto)
                soluzione = solver.solve()
                
                if soluzione:
                    pos = soluzione[nome_pianta]
                    condizioni = ambiente_balcone[pos]
                    print(f" -> SUCCESSO! Posiziona in: '{pos}'")
                    print(f"    (Dati ambientali: Luce {condizioni['luce']}h, Umidità {condizioni['umidita']})")
                else:
                    print(" -> FALLIMENTO: Nessuna posizione disponibile soddisfa i requisiti biologici.")
            except Exception as e:
                print(f" -> Errore CSP: {e}")
        else:
            print(" -> Ontologia non caricata, impossibile eseguire CSP.")

# --- ESECUZIONE ---
if __name__ == "__main__":
    app = SmartGardenSystem()

    # TEST FINALE
    # Usiamo nomi in Italiano, coerenti con l'Ontologia e il nuovo CSV generato
    # Modifica questi valori per testare casi diversi
    pianta_test = "Basilico_Genovese"
    sintomo_test = "Foglie_Gialle"
    
    app.analizza_caso(pianta_test, sintomo_test)