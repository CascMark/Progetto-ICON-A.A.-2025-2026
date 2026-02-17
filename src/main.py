import os
import sys
import warnings

# --- CONFIGURAZIONE SISTEMA ---
# Filtriamo i warning di sistema (es. sklearn version mismatch) per un output pulito
warnings.filterwarnings("ignore")

# Assicuriamo che Python veda la cartella corrente come package
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# --- IMPORT MODULI PROGETTO ---
from garden_ml_engine import GardenMLEngine
from prolog_module import GardenLogic
from csp_module import GardenCSP
from bayes_module import crea_rete_diagnosi
from owlready2 import get_ontology

class SmartGardenSystem:
    def __init__(self):
        print("\n" + "="*60)
        print("   AVVIO SISTEMA SMART GARDEN (INTEGRATED AI v2.0)")
        print("="*60)

        # 1. Configurazione Percorsi
        self.root_dir = os.path.dirname(BASE_DIR)
        self.kb_path = os.path.join(self.root_dir, 'knowledge_base', 'kb.pl')
        self.onto_path = os.path.join(self.root_dir, 'knowledge_base', 'Ontologia_Completa.owx')
        self.csv_path = os.path.join(self.root_dir, 'data', 'dataset_integrato.csv')

        # 2. Caricamento ed Addestramento ML (Supervisionato + Non Supervisionato)
        print(" [1/4] Avvio Machine Learning Engine (Multi-Model)...")
        self.ml_engine = GardenMLEngine(self.csv_path)
        self.ml_engine.addestra()

        # 3. Caricamento Prolog (Motore Inferenziale)
        print(" [2/4] Connessione a SWI-Prolog...")
        self.logic_engine = GardenLogic(self.kb_path)

        # 4. Caricamento Ontologia (Knowledge Graph)
        print(" [3/4] Caricamento Ontologia OWL...")
        try:
            self.onto = get_ontology(self.onto_path).load()
        except Exception as e:
            print(f" [ERRORE ONTOLOGIA] {e}")
            self.onto = None

        # 5. Caricamento Rete Bayesiana (Probabilistico)
        print(" [4/4] Configurazione Rete Bayesiana...")
        try:
            self.bayes_net = crea_rete_diagnosi()
            print(" -> Rete Bayesiana pronta.")
        except Exception as e:
            print(f" [ERRORE BAYES] {e}")
            self.bayes_net = None

    def analizza_caso(self, nome_pianta, nome_sintomo):
        """
        Esegue la pipeline completa: ML Avanzato -> Prolog -> Bayes -> CSP
        """
        print(f"\n\n{'='*70}")
        print(f" ANALISI CASO: {nome_pianta} | SINTOMO: {nome_sintomo}")
        print(f"{'='*70}")

        malattia_predetta = "Nessuna"

        # --- STEP 1: INTELLIGENZA ARTIFICIALE AVANZATA ---
        print(f"\n[1] INTELLIGENZA ARTIFICIALE (Multi-Model Analysis)")
        
        if self.ml_engine:
            # Richiamiamo la predizione complessa che include RF, NN e K-Means
            risultati = self.ml_engine.predici_complesso(nome_pianta, nome_sintomo)
            
            if risultati:
                malattia_rf = risultati["RF"]
                conf_rf = risultati["RF_Conf"]
                malattia_nn = risultati["NN"]
                cluster = risultati["Cluster"]
                
                # Scegliamo Random Forest come diagnosi principale (generalmente più robusto sui dati tabulari)
                malattia_predetta = malattia_rf

                print(f" -> [Supervisionato] Random Forest: {malattia_rf} (Confidenza: {conf_rf*100:.2f}%)")
                print(f" -> [Supervisionato] Rete Neurale:  {malattia_nn}")
                
                # Confronto tra modelli (Model Selection logic)
                if malattia_rf == malattia_nn:
                    print("    (Esito: I modelli concordano -> Diagnosi ad alta affidabilità)")
                else:
                    print(f"    (Esito: Discrepanza rilevata. Si consiglia prevalenza al modello RF)")
                
                # Risultato Clustering (Non supervisionato)
                print(f" -> [Non Supervisionato] K-Means:   {cluster}")
                print("    (La pianta è stata profilata automaticamente in questo cluster climatico)")
            else:
                print(" -> Errore: Dati insufficienti per una predizione ML.")

        
        # --- STEP 2: PROLOG (Logica e Trattamenti) ---
        print(f"\n[2] PROLOG (Motore Inferenziale Reale)")
        if self.logic_engine:
            # A. Otteniamo la cura per la malattia diagnosticata dal ML
            cure = self.logic_engine.ottieni_trattamento(malattia_predetta)
            if cure:
                print(f" -> Trattamento suggerito (dalla KB): {cure}")
            else:
                print(f" -> Nessun trattamento trovato in KB per '{malattia_predetta}'")
                
            # B. Verifica consistenza logica (Regola ontologica pura)
            diagnosi_logica = self.logic_engine.verifica_diagnosi_logica(nome_pianta, nome_sintomo)
            if diagnosi_logica:
                print(f" -> Controllo Consistenza KB: La letteratura suggerisce '{diagnosi_logica[0]}'")
                if diagnosi_logica[0] != malattia_predetta:
                    print("    (Nota: Il sistema ha rilevato una variazione rispetto al caso teorico standard)")


        # --- STEP 3: RETE BAYESIANA (Probabilità Condizionata) ---
        print(f"\n[3] RETE BAYESIANA (Analisi Probabilistica)")
        if self.bayes_net:
            # Mappa dinamica: Sintomo -> Quali cause indagare nel grafo?
            indagini = {
                "Foglie_Gialle": ["Carenza_Ferro", "Afidi"],
                "Macchie_Fogliari": ["Peronospora", "Ruggine"],
                "Foglie_Secche": ["Stress_Idrico"],
                "Muffa_Bianca": ["Oidio"]
            }
            
            cause = indagini.get(nome_sintomo, [])
            if cause:
                print(f" -> Calcolo probabilità cause per sintomo '{nome_sintomo}':")
                for causa in cause:
                    try:
                        # Query alla rete bayesiana
                        res = self.bayes_net.query(variables=[causa], evidence={nome_sintomo: 1})
                        prob = res.values[1] # Indice 1 = True (Evento verificato)
                        print(f"    * Probabilità '{causa}': {prob*100:.2f}%")
                    except Exception:
                        pass
            else:
                print(" -> Sintomo non presente nel grafo causale (Analisi saltata).")


        # --- STEP 4: CSP (Posizionamento Ottimale) ---
        print(f"\n[4] CSP (Constraint Satisfaction Problem)")
        if self.onto:
            # Definiamo l'ambiente disponibile sul balcone
            ambiente_balcone = {
                "Vaso_Sole":   {"luce": 9, "umidita": 0.5}, # Tanto sole, secco
                "Vaso_Ombra":  {"luce": 4, "umidita": 0.8}, # Poca luce, umido
                "Vaso_Interno": {"luce": 7, "umidita": 0.6}, # Equilibrato
                "Vaso_Serra":   {"luce": 8, "umidita": 0.9}  # Luce e molto umido
            }
            
            try:
                # Creiamo e risolviamo il problema dei vincoli
                solver = GardenCSP([nome_pianta], ambiente_balcone, self.onto)
                soluzione = solver.solve()
                
                if soluzione:
                    vaso_scelto = soluzione[nome_pianta]
                    dati_vaso = ambiente_balcone[vaso_scelto]
                    print(f" -> SUCCESSO! Posizione ottimale trovata: '{vaso_scelto}'")
                    print(f"    (Dati ambientali: Luce {dati_vaso['luce']}h, Umidità {dati_vaso['umidita']})")
                else:
                    print(" -> ATTENZIONE: Nessun vaso soddisfa i requisiti biologici della pianta.")
            except Exception as e:
                print(f" -> Errore durante il calcolo CSP: {e}")
        else:
            print(" -> Ontologia non caricata, impossibile posizionare la pianta.")

# --- ESECUZIONE TEST ---
if __name__ == "__main__":
    # Istanziamo il sistema
    app = SmartGardenSystem()

    print("\n" + "*"*70)
    print("   TEST FINALE GIARDINO (Complete Pipeline)")
    print("*"*70)

    # Scenari di test usando i Nomi Semplici
    casi_di_test = [
        ("Basilico", "Foglie_Gialle"),      # Test combinato Afidi/Carenza
        ("Pomodoro", "Macchie_Fogliari"),   # Test conflitto ML (Ruggine) vs Prolog (Peronospora)
        ("Lattuga",  "Foglie_Secche"),      # Test ML deterministico (Stress Idrico)
        ("Rosa",     "Muffa_Bianca"),       # Test Oidio
        ("Peperone", "Macchie_Fogliari")    # Test Virosi
    ]

    for pianta, sintomo in casi_di_test:
        app.analizza_caso(pianta, sintomo)