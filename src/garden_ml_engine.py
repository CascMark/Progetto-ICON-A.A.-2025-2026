import os
import joblib
import pandas as pd
import numpy as np

class GardenMLEngine:
    def __init__(self, csv_path_ignored=None):
        # Percorsi
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(BASE_DIR) == "src":
            ROOT_DIR = os.path.dirname(BASE_DIR)
        else:
            ROOT_DIR = BASE_DIR
            
        MODEL_DIR = os.path.join(ROOT_DIR, "models")
        
        print(" [ML ENGINE] Caricamento modelli (v2 con Sintomi)...")
        try:
            self.rf = joblib.load(os.path.join(MODEL_DIR, "model_rf.pkl"))
            self.nn = joblib.load(os.path.join(MODEL_DIR, "model_nn.pkl"))
            self.kmeans = joblib.load(os.path.join(MODEL_DIR, "model_kmeans.pkl"))
            
            self.scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
            self.le_famiglia = joblib.load(os.path.join(MODEL_DIR, "le_famiglia.pkl"))
            # Carichiamo il nuovo encoder
            self.le_sintomo = joblib.load(os.path.join(MODEL_DIR, "le_sintomo.pkl"))
            self.scaler_env = joblib.load(os.path.join(MODEL_DIR, "scaler_env.pkl"))
            
            self.models_loaded = True
            print(" -> Modelli caricati correttamente.")
        except Exception as e:
            print(f" [ERRORE] Impossibile caricare i modelli: {e}")
            self.models_loaded = False

    def addestra(self):
        pass

    def predici_complesso(self, nome_pianta, nome_sintomo):
        if not self.models_loaded:
            return None

        try:
            # 1. Preparazione Dati
            # Mapping Famiglia
            famiglia_map = {
                "Basilico": "Lamiaceae", "Menta": "Lamiaceae",
                "Pomodoro": "Solanaceae", "Peperone": "Solanaceae", "Melanzana": "Solanaceae",
                "Zucchina": "Cucurbitaceae", "Cetriolo": "Cucurbitaceae",
                "Rosa": "Rosaceae", "Fragola": "Rosaceae"
            }
            famiglia_str = famiglia_map.get(nome_pianta, "Solanaceae")
            
            # Simuliamo condizioni ambientali (o le prenderemmo dai sensori)
            luce = 8.0
            umidita = 0.6
            temp = 25.0
            ph = 7.0

            # 2. Encoding (Trasformiamo le parole in numeri per l'IA)
            try:
                fam_encoded = self.le_famiglia.transform([famiglia_str])[0]
            except:
                fam_encoded = 0
            
            # --- FIX: ENCODING SINTOMO ---
            # Se l'utente seleziona "Foglie_Gialle", dobbiamo dire all'IA il codice corrispondente.
            try:
                # Nota: Il dataset generato usa spazi o underscore? 
                # Il generatore faceva join con ", ". 
                # Se la GUI passa "Foglie_Gialle", proviamo a passarlo direttamente.
                # Se l'encoder non lo conosce (magari nel training era "Foglie_Gialle, Altro"), usiamo fallback.
                
                # Cerchiamo un match parziale se quello esatto fallisce
                if nome_sintomo in self.le_sintomo.classes_:
                     sintomo_encoded = self.le_sintomo.transform([nome_sintomo])[0]
                else:
                    # Fallback intelligente: cerchiamo la classe che contiene la stringa
                    possibili = [c for c in self.le_sintomo.classes_ if nome_sintomo in str(c)]
                    if possibili:
                        sintomo_encoded = self.le_sintomo.transform([possibili[0]])[0]
                    else:
                        sintomo_encoded = 0 # Nessuno/Sconosciuto
            except:
                sintomo_encoded = 0

            # 3. Creazione Vettore Input
            # L'ordine DEVE essere identico a quello in train_model.py
            # ['Famiglia_Encoded', 'Sintomo_Encoded', 'Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale', 'PH_Suolo']
            input_df = pd.DataFrame([[fam_encoded, sintomo_encoded, luce, umidita, temp, ph]], 
                                    columns=['Famiglia_Encoded', 'Sintomo_Encoded', 'Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale', 'PH_Suolo'])
            
            X_input = self.scaler.transform(input_df)

            # 4. Predizioni
            pred_rf = self.rf.predict(X_input)[0]
            prob_rf = np.max(self.rf.predict_proba(X_input))
            pred_nn = self.nn.predict(X_input)[0]

            # Clustering
            input_env = pd.DataFrame([[luce, umidita, temp]], columns=['Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale'])
            X_env_scaled = self.scaler_env.transform(input_env)
            cluster_id = self.kmeans.predict(X_env_scaled)[0]
            
            desc_cluster = f"Cluster {cluster_id} (Profilo Climatico Simile)"

            return {
                "RF": pred_rf,
                "RF_Conf": prob_rf,
                "NN": pred_nn,
                "Cluster": desc_cluster
            }

        except Exception as e:
            print(f" [ERRORE PREDIZIONE ML] {e}")
            return None