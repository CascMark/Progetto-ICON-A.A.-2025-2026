import pandas as pd
import os
import warnings
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# IMPORTIAMO I NUOVI MODULI
from ml_supervised import SupervisedModels
from ml_unsupervised import UnsupervisedModels

warnings.filterwarnings("ignore")

class GardenMLEngine:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        
        # Inizializza i sottomoduli
        self.supervised = SupervisedModels()
        self.unsupervised = UnsupervisedModels()
        
        # Preprocessing Tools
        self.le_pianta = LabelEncoder()
        self.le_sintomo = LabelEncoder()
        self.le_malattia = LabelEncoder()
        self.scaler = StandardScaler() # Fondamentale per Reti Neurali e K-Means
        
        self.feature_names = ['Pianta_Encoded', 'Sintomo_Encoded', 'Umidita', 'Temperatura', 'Ore_Luce']

    def addestra(self):
        if not os.path.exists(self.csv_path):
            print(f" [ERROR] CSV mancante: {self.csv_path}")
            return

        print(" [ML ENGINE] Caricamento e preprocessing dataset...")
        df = pd.read_csv(self.csv_path)

        # 1. Encoding
        df['Pianta_Encoded'] = self.le_pianta.fit_transform(df['Pianta'])
        df['Sintomo_Encoded'] = self.le_sintomo.fit_transform(df['Sintomo_Visibile'])
        df['Malattia_Encoded'] = self.le_malattia.fit_transform(df['Diagnosi_Lab'])

        # 2. Preparazione Dati
        X = df[self.feature_names]
        y = df['Malattia_Encoded']
        
        # 3. Scaling (Standardizzazione)
        # Trasforma i dati per avere media 0 e deviazione standard 1
        X_scaled = self.scaler.fit_transform(X)

        # 4. Split Train/Test
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # --- ADDESTRAMENTO SUPERVISIONATO ---
        acc_rf, acc_nn = self.supervised.train(X_train, y_train, X_test, y_test)
        print(f" [SUPERVISED] Random Forest Accuracy: {acc_rf*100:.2f}%")
        print(f" [SUPERVISED] Neural Network Accuracy: {acc_nn*100:.2f}%")

        # --- ADDESTRAMENTO NON SUPERVISIONATO (K-MEANS) ---
        # Usiamo solo le colonne ambientali (indici 2, 3, 4 di X_scaled)
        # Umidita, Temperatura, Ore_Luce
        X_env = X_scaled[:, 2:] 
        self.unsupervised.train(X_env)

    def predici_complesso(self, nome_pianta, nome_sintomo):
        try:
            # Encoding Input
            if nome_pianta not in self.le_pianta.classes_: return None
            
            p_code = self.le_pianta.transform([nome_pianta])[0]
            s_code = self.le_sintomo.transform([nome_sintomo])[0]
            
            # Valori simulati (Sensori)
            umid, temp, luce = 0.6, 25.0, 8

            # Creazione Input
            input_raw = pd.DataFrame([[p_code, s_code, umid, temp, luce]], columns=self.feature_names)
            input_scaled = self.scaler.transform(input_raw)

            # 1. Chiediamo al modulo Supervisionato
            idx_rf, prob_rf, idx_nn = self.supervised.predict(input_scaled)
            
            malattia_rf = self.le_malattia.inverse_transform([idx_rf])[0]
            malattia_nn = self.le_malattia.inverse_transform([idx_nn])[0]

            # 2. Chiediamo al modulo Non Supervisionato (solo dati ambientali)
            input_env = input_scaled[:, 2:]
            cluster_desc = self.unsupervised.predict_cluster(input_env)

            return {
                "RF": malattia_rf,
                "RF_Conf": prob_rf,
                "NN": malattia_nn,
                "Cluster": cluster_desc
            }
        except Exception as e:
            print(f"Errore predizione: {e}")
            return None