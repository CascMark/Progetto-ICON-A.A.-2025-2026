import os
import joblib
import pandas as pd
import numpy as np

class GardenMLEngine:
    def __init__(self, csv_path_ignored=None):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(BASE_DIR) == "src":
            ROOT_DIR = os.path.dirname(BASE_DIR)
        else:
            ROOT_DIR = BASE_DIR
            
        MODEL_DIR = os.path.join(ROOT_DIR, "models")
        
        print(" [ML ENGINE] Caricamento modelli pre-addestrati...")
        try:
            self.rf = joblib.load(os.path.join(MODEL_DIR, "model_rf.pkl"))
            self.nn = joblib.load(os.path.join(MODEL_DIR, "model_nn.pkl"))
            self.kmeans = joblib.load(os.path.join(MODEL_DIR, "model_kmeans.pkl"))
            
            self.scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
            self.le_famiglia = joblib.load(os.path.join(MODEL_DIR, "le_famiglia.pkl"))
            self.scaler_env = joblib.load(os.path.join(MODEL_DIR, "scaler_env.pkl"))
            
            self.models_loaded = True
            print(" -> Modelli caricati: RF, NN, K-Means.")
        except Exception as e:
            print(f" [ERRORE] Impossibile caricare i modelli: {e}")
            print(" -> Assicurati di aver eseguito 'python src/train_model.py'!")
            self.models_loaded = False

    def addestra(self):
        print(" [INFO] I modelli sono già pre-addestrati e caricati da file.")
        pass

    def predici_complesso(self, nome_pianta, nome_sintomo):
        if not self.models_loaded:
            return None

        try:
            famiglia_map = {
                "Basilico": "Lamiaceae", "Menta": "Lamiaceae",
                "Pomodoro": "Solanaceae", "Peperone": "Solanaceae", "Melanzana": "Solanaceae",
                "Zucchina": "Cucurbitaceae", "Cetriolo": "Cucurbitaceae",
                "Rosa": "Rosaceae", "Fragola": "Rosaceae"
            }
            famiglia_str = famiglia_map.get(nome_pianta, "Solanaceae") # Default

            luce = 8.0
            umidita = 0.6
            temp = 25.0
            ph = 7.0

            try:
                fam_encoded = self.le_famiglia.transform([famiglia_str])[0]
            except:
                fam_encoded = 0 
            
            input_df = pd.DataFrame([[fam_encoded, luce, umidita, temp, ph]], 
                                    columns=['Famiglia_Encoded', 'Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale', 'PH_Suolo'])
            
            X_input = self.scaler.transform(input_df)

            pred_rf = self.rf.predict(X_input)[0]
            prob_rf = np.max(self.rf.predict_proba(X_input))
            
            pred_nn = self.nn.predict(X_input)[0]

            input_env = pd.DataFrame([[luce, umidita, temp]], columns=['Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale'])
            X_env_scaled = self.scaler_env.transform(input_env)
            cluster_id = self.kmeans.predict(X_env_scaled)[0]
            
            descrizioni_cluster = {
                0: "Clima A (Prob. Secco/Soleggiato)",
                1: "Clima B (Prob. Umido/Ombroso)",
                2: "Clima C (Prob. Temperato/Neutro)"
            }
            cluster_desc = descrizioni_cluster.get(cluster_id, f"Cluster {cluster_id}")

            return {
                "RF": pred_rf,
                "RF_Conf": prob_rf,
                "NN": pred_nn,
                "Cluster": cluster_desc
            }

        except Exception as e:
            print(f" [ERRORE PREDIZIONE] {e}")
            return None