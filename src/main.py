import os
import sys
import warnings
import random

warnings.filterwarnings("ignore")

# --- CONFIGURAZIONE PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

if os.path.basename(BASE_DIR) == "src":
    ROOT_DIR = os.path.dirname(BASE_DIR)
else:
    ROOT_DIR = BASE_DIR

GUI_DIR = os.path.join(ROOT_DIR, "gui")
if os.path.exists(GUI_DIR):
    sys.path.insert(0, GUI_DIR)

# --- IMPORT MODULI PROGETTO ---
from garden_ml_engine import GardenMLEngine 
from owlready2 import get_ontology, default_world

# 1. IMPORTIAMO IL NUOVO REPORTER
try:
    from validation_reporter import ValidationReporter
except ImportError:
    ValidationReporter = None

try:
    from prolog_module import GardenLogic
except ImportError:
    GardenLogic = None

try:
    from csp_module import GardenCSP
except ImportError:
    GardenCSP = None

try:
    from bayes_module import crea_rete_diagnosi
    from pgmpy.inference import VariableElimination
except ImportError:
    crea_rete_diagnosi = None

class SmartGardenSystem:
    def __init__(self):
        print("\n" + "="*60)
        print("   AVVIO SISTEMA SMART GARDEN (INTEGRATED AI v4.0)")
        print("="*60)

        self.root_dir = ROOT_DIR
        self.model_dir = os.path.join(self.root_dir, 'models')
        self.kb_path = os.path.join(self.root_dir, 'knowledge_base', 'kb.pl')
        self.onto_path = os.path.join(self.root_dir, 'knowledge_base', 'Ontologia_Completa.owx')
        self.csv_path = os.path.join(self.root_dir, 'data', 'piante_dataset.csv')
        
        # Inizializziamo l'engine ML e il Reporter
        self.ml_engine = GardenMLEngine() 
        if ValidationReporter:
            self.reporter = ValidationReporter(self.model_dir)
        else:
            self.reporter = None

        print(" [1/4] Connessione a SWI-Prolog...")
        if GardenLogic and os.path.exists(self.kb_path):
            try:
                self.logic_engine = GardenLogic(self.kb_path)
            except Exception as e:
                print(f" [ERRORE PROLOG] {e}")
                self.logic_engine = None
        else:
            self.logic_engine = None

        print(" [2/4] Caricamento Ontologia OWL...")
        try:
            default_world.ontologies.clear()
            self.onto = get_ontology(self.onto_path).load()
        except Exception as e:
            self.onto = None

        print(" [3/4] Configurazione Rete Bayesiana...")
        if crea_rete_diagnosi:
            try:
                self.bayes_net = crea_rete_diagnosi()
                self.bayes_infer = VariableElimination(self.bayes_net)
            except Exception:
                self.bayes_infer = None
        else:
            self.bayes_infer = None

    def analizza_caso(self, nome_pianta, nome_sintomo):
        print(f"\n\n{'='*70}")
        print(f" ANALISI CASO: {nome_pianta} | SINTOMO: {nome_sintomo}")
        print(f"{'='*70}")

        malattia_predetta = "Nessuna"
        risultati_ml = None # Variabile per salvare i risultati da passare al Reporter

        # --- STEP 1: ML ---
        print(f"\n[1] INTELLIGENZA ARTIFICIALE (Multi-Model Analysis)")
        if self.ml_engine and self.ml_engine.models_loaded:
            risultati_ml = self.ml_engine.predici_complesso(nome_pianta, nome_sintomo)
            if risultati_ml:
                malattia_rf = risultati_ml["RF"]
                conf_rf = risultati_ml["RF_Conf"]
                malattia_nn = risultati_ml["NN"]
                cluster = risultati_ml["Cluster"]
                malattia_predetta = malattia_rf

                print(f" -> Random Forest: {malattia_rf} (Confidenza: {conf_rf*100:.2f}%)")
                print(f" -> Rete Neurale:  {malattia_nn}")
                
                if malattia_rf == malattia_nn:
                    print("    (Esito: I modelli concordano -> Diagnosi ad alta affidabilità)")
                else:
                    print("    (Esito: Discrepanza rilevata. Si consiglia prevalenza al modello RF)")
                
                print(f" -> K-Means:   {cluster}")

        # --- STEP 2: PROLOG ---
        print(f"\n[2] PROLOG (Motore Inferenziale Reale)")
        if self.logic_engine:
            cure = self.logic_engine.ottieni_trattamento(malattia_predetta)
            if cure:
                print(f" -> Trattamento suggerito (dalla KB): {cure}")
            try:
                diagnosi_logica = self.logic_engine.verifica_diagnosi_logica(nome_pianta, nome_sintomo)
                if diagnosi_logica:
                    print(f" -> Controllo Consistenza KB: La letteratura suggerisce '{diagnosi_logica[0]}'")
            except: pass

        # --- STEP 3: BAYES ---
        print(f"\n[3] RETE BAYESIANA (Analisi Probabilistica)")
        if self.bayes_infer:
            try:
                q = self.bayes_infer.query(variables=['Malattia'], evidence={'Sintomo': nome_sintomo})
                for i, val in enumerate(q.values):
                     if val > 0.10: 
                        print(f"    * Probabilità '{q.state_names['Malattia'][i]}': {val*100:.2f}%")
            except: pass

        # --- STEP 4: CSP ---
        print(f"\n[4] CSP (Constraint Satisfaction Problem)")
        if self.onto and GardenCSP:
            ambiente_balcone = {
                "Vaso_Sole":   {"luce": 9.5, "umidita": 0.4},
                "Vaso_Ombra":  {"luce": 4.0, "umidita": 0.8},
                "Vaso_Interno": {"luce": 7.0, "umidita": 0.6},
                "Vaso_Serra":   {"luce": 8.0, "umidita": 0.9}
            }
            try:
                candidates = self.onto.search(iri=f"*{nome_pianta}*")
                pianta_target = random.choice(candidates).name if candidates else nome_pianta 
                
                solver = GardenCSP([pianta_target], ambiente_balcone, self.onto)
                soluzione = solver.solve()
                
                if soluzione:
                    vaso_scelto = soluzione[pianta_target]
                    dati_vaso = ambiente_balcone[vaso_scelto]
                    print(f" -> Individuo rappresentativo selezionato: {pianta_target}")
                    print(f" -> SUCCESSO! Posizione ottimale trovata: '{vaso_scelto}'")
                    print(f"    (Dati ambientali: Luce {dati_vaso['luce']}h, Umidità {dati_vaso['umidita']})")
            except: pass

        # --- STEP 5: VALIDAZIONE ---
        print(f"\n[5] VALIDAZIONE SCIENTIFICA")
        if self.reporter:
            # Passiamo i risultati ML (risultati_ml) per calcolare il consenso dinamico
            print(self.reporter.get_formatted_report(risultati_ml))
        else:
            print(" -> Modulo ValidationReporter non caricato.")


if __name__ == "__main__":
    try:
        import tkinter as tk
        try:
            from gui import GreenLeafGui
        except ImportError:
            sys.path.append(os.path.join(ROOT_DIR, "gui"))
            from gui import GreenLeafGui

        root = tk.Tk()
        app = GreenLeafGui(root)
        root.mainloop()
    except Exception as e:
        print(f"Fallback testuale attivato. L'ERRORE FATALE E': {e}")
        import traceback
        traceback.print_exc()