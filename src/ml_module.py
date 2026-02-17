import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class DiseasePredictorML:
    def __init__(self, csv_path):
        try:
            self.data = pd.read_csv(csv_path)
            
            # --- CORREZIONE 1: PULIZIA COLONNE ---
            # Rimuoviamo spazi vuoti dai nomi delle colonne (es. " Plant " -> "Plant")
            self.data.columns = self.data.columns.str.strip()
            
            # Stampiamo le colonne trovate per debug
            print(f" [DEBUG] Colonne trovate nel CSV: {self.data.columns.tolist()}")
            
            # Se le colonne sono minuscole, le rinominiamo per uniformità
            self.data.rename(columns={'plant': 'Plant', 'symptom': 'Symptom', 'disease': 'Disease'}, inplace=True)
            
            # Verifica finale
            required_cols = {'Plant', 'Symptom', 'Disease'}
            if not required_cols.issubset(self.data.columns):
                raise ValueError(f"Il CSV deve contenere le colonne: {required_cols}")

            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.le_plant = LabelEncoder()
            self.le_symptom = LabelEncoder()
            self.le_disease = LabelEncoder()
            self._train_model()
            
        except Exception as e:
            print(f" ERRORE INIZIALIZZAZIONE ML: {e}")
            raise e

    def _train_model(self):
        # Preparazione dati come nel file del tuo compagno
        X = self.data[['Plant', 'Symptom']].copy()
        y = self.data['Disease']

        # Encoding: Trasforma stringhe in numeri
        X['Plant'] = self.le_plant.fit_transform(X['Plant'])
        X['Symptom'] = self.le_symptom.fit_transform(X['Symptom'])
        y_encoded = self.le_disease.fit_transform(y)

        # Addestramento
        self.model.fit(X, y_encoded)
        print(" -> Modello ML (Random Forest) addestrato sul dataset CSV.")

    def predici_malattia(self, nome_pianta, nome_sintomo):
        try:
            # Trasformiamo l'input dell'utente nei numeri che il modello capisce
            plant_code = self.le_plant.transform([nome_pianta])[0]
            symptom_code = self.le_symptom.transform([nome_sintomo])[0]
            
            # Predizione
            pred_code = self.model.predict([[plant_code, symptom_code]])[0]
            malattia_predetta = self.le_disease.inverse_transform([pred_code])[0]
            
            # Recuperiamo la confidenza (probabilità)
            confidenza = max(self.model.predict_proba([[plant_code, symptom_code]])[0])
            return malattia_predetta, confidenza
        except ValueError:
            return "Sconosciuto (Dati non nel dataset)", 0.0