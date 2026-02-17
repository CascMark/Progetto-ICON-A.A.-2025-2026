import os
import sys
import owlready2 as owl

# Importiamo i moduli personalizzati creati in precedenza
# Assicurati che i file ml_module.py, bayes_module.py, csp_module.py, prolog_module.py siano in src/
from ml_module import DiseasePredictorML
from prolog_module import GardenLogic
from bayes_module import crea_rete_diagnosi
from csp_module import GardenCSP

# --- CONFIGURAZIONE PERCORSI E AMBIENTE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))       # Cartella src/
ROOT_DIR = os.path.dirname(BASE_DIR)                        # Cartella principale del progetto
DATA_DIR = os.path.join(ROOT_DIR, 'data')
KB_DIR = os.path.join(ROOT_DIR, 'knowledge_base')

# --- DIZIONARIO DI TRADUZIONE (BRIDGE CSV <-> ONTOLOGIA) ---
# Il CSV usa l'inglese (es. Tomato), l'Ontologia usa l'Italiano (es. Pomodoro_San_Marzano)
# Questo dizionario permette ai due mondi di parlarsi.
MAPPA_NOMI = {
    "Tomato": "Pomodoro_San_Marzano",
    "Pepper": "Peperone",
    "Potato": "Patata",
    "Strawberry": "Fragola",
    "Yellow Leaves": "Foglie_Gialle",
    "Leaf Spot": "Macchie_Fogliari"
}

class SmartGardenSystem:
    def __init__(self):
        print("--- INIZIALIZZAZIONE SISTEMA SMART GARDEN ---")
        
        # 1. Caricamento Dataset e Training ML (Capitoli 2-3)
        print(" [1/4] Addestramento Modello Machine Learning...", end=" ")
        try:
            self.ml_engine = DiseasePredictorML(os.path.join(DATA_DIR, 'plant_disease_set.csv'))
            print("OK.")
        except Exception as e:
            print(f"ERRORE: {e}")

        # 2. Caricamento Knowledge Base Prolog (Capitolo 5)
        print(" [2/4] Caricamento Motore Logico (Prolog)...", end=" ")
        try:
            self.logic_engine = GardenLogic(os.path.join(KB_DIR, 'kb.pl'))
            print("OK.")
        except Exception as e:
            print(f"ERRORE: {e}")

        # 3. Caricamento Ontologia OWL (Struttura Dati)
        print(" [3/4] Caricamento Ontologia OWL...", end=" ")
        try:
            self.onto = owl.get_ontology(os.path.join(KB_DIR, 'Ontologia.owx')).load()
            print("OK.")
        except Exception as e:
            print(f"ERRORE: {e}")
            self.onto = None

        # 4. Inizializzazione Rete Bayesiana (Capitolo 4)
        print(" [4/4] Configurazione Rete Bayesiana...", end=" ")
        try:
            self.bayes_net = crea_rete_diagnosi()
            print("OK.")
        except Exception as e:
            print(f"ERRORE: {e}")

    def analizza_caso(self, input_pianta_csv, input_sintomo_csv):
        """
        Esegue il ciclo completo di ragionamento: ML -> Prolog -> Bayes -> CSP
        """
        print(f"\n\n{'='*60}")
        print(f" ANALISI CASO: {input_pianta_csv} con sintomo '{input_sintomo_csv}'")
        print(f"{'='*60}")

        # --- STEP 1: MACHINE LEARNING (Predizione) ---
        # Usa i dati storici (CSV) per predire la malattia più probabile
        malattia_predetta, confidenza = self.ml_engine.predici_malattia(input_pianta_csv, input_sintomo_csv)
        
        print(f"\n[MODULO ML] Analisi Statistica:")
        print(f" -> Malattia Identificata: {malattia_predetta}")
        print(f" -> Livello di Confidenza: {confidenza*100:.2f}%")

        # --- STEP 2: PROLOG (Logica e Trattamento) ---
        # Interroga la KB per trovare cure e verificare regole logiche
        print(f"\n[MODULO PROLOG] Consultazione Knowledge Base:")
        
        # Verifica 1: Esiste un trattamento codificato?
        cure = self.logic_engine.ottieni_trattamento(malattia_predetta)
        if cure:
            print(f" -> Trattamento suggerito dalla KB: {cure}")
        else:
            print(f" -> Nessun trattamento specifico trovato nelle regole logiche per '{malattia_predetta}'.")

        # Verifica 2: Regole di diagnosi incrociata
        conferme = self.logic_engine.verifica_diagnosi_logica(input_pianta_csv, input_sintomo_csv)
        if conferme:
            print(f" -> Regola logica attivata: Combinazione compatibile con {conferme}")

        # --- STEP 3: RETE BAYESIANA (Gestione Incertezza) ---
        # Se il sintomo è generico ("Yellow Leaves"), usiamo la probabilità
        if "Yellow" in input_sintomo_csv or "Gialle" in input_sintomo_csv:
            print(f"\n[MODULO BAYES] Diagnosi Probabilistica (Sintomo Ambiguo):")
            # Calcoliamo la probabilità che sia Carenza di Ferro
            try:
                risultato = self.bayes_net.query(variables=['Carenza_Ferro'], evidence={'Foglie_Gialle': 1})
                prob_ferro = risultato.values[1]
                print(f" -> Probabilità che sia 'Carenza_Ferro': {prob_ferro*100:.2f}%")
                
                risultato_afidi = self.bayes_net.query(variables=['Afidi'], evidence={'Foglie_Gialle': 1})
                prob_afidi = risultato_afidi.values[1]
                print(f" -> Probabilità che siano 'Afidi': {prob_afidi*100:.2f}%")
            except Exception as e:
                print(f" -> Impossibile eseguire inferenza bayesiana: {e}")

        # --- STEP 4: CSP (Ottimizzazione Spaziale) ---
        # Cerchiamo di posizionare la pianta nel giardino virtuale rispettando i vincoli
        print(f"\n[MODULO CSP] Ottimizzazione Spaziale:")
        
        # Traduzione nome per l'Ontologia (es. Tomato -> Pomodoro_San_Marzano)
        nome_ontologia = MAPPA_NOMI.get(input_pianta_csv, input_pianta_csv)
        
        if self.onto:
            # Creiamo una griglia giardino simulata
            ambiente_balcone = {
                "Vaso_Nord (Ombra)":   {"luce": 4, "umidita": 0.8},
                "Vaso_Sud (Sole)":     {"luce": 9, "umidita": 0.5},
                "Fioriera_Est (Mix)":  {"luce": 7, "umidita": 0.7}
            }
            
            print(f" -> Tentativo di posizionamento per: {nome_ontologia}")
            try:
                # Istanziamo il risolutore CSP
                solver = GardenCSP([nome_ontologia], ambiente_balcone, self.onto)
                soluzione = solver.solve()
                
                if soluzione:
                    pos = soluzione[nome_ontologia]
                    dati_pos = ambiente_balcone[pos]
                    print(f" -> SUCCESSO! Posizione ottimale trovata: '{pos}'")
                    print(f"    (Condizioni: Luce {dati_pos['luce']}h, Umidità {dati_pos['umidita']})")
                else:
                    print(" -> FALLIMENTO: Nessuna posizione soddisfa i vincoli biologici della pianta.")
            except Exception as e:
                print(f" -> Errore durante il calcolo CSP (probabile nome non trovato in Ontologia): {e}")
        else:
            print(" -> Ontologia non caricata, salto fase CSP.")

# --- ESECUZIONE PRINCIPALE ---
if __name__ == "__main__":
    # Avvia il sistema
    app = SmartGardenSystem()

    # --- SCENARIO DI TEST ---
    # Simuliamo un utente che ha un Pomodoro con le foglie gialle
    # Questi nomi devono esistere nel CSV del tuo compagno
    pianta_input = "Tomato" 
    sintomo_input = "Yellow Leaves"
    
    app.analizza_caso(pianta_input, sintomo_input)

    # Se vuoi testare un altro caso, scommenta qui sotto:
    # app.analizza_caso("Pepper", "Leaf Spot")