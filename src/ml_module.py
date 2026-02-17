import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

class DiseasePredictorML:
    def __init__(self, csv_path):
        # Carichiamo il dataset (che ora è già pulito e coerente!)
        self.data = pd.read_csv(csv_path)
        
        # Colonne attese: Pianta, Sintomo_Visibile, Diagnosi_Lab
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.le_pianta = LabelEncoder()
        self.le_sintomo = LabelEncoder()
        self.le_diagnosi = LabelEncoder()
        
        self._train_model()

    def _train_model(self):
        # Encoding diretto, senza dizionari o 'if' complessi
        X = pd.DataFrame()
        X['Pianta'] = self.le_pianta.fit_transform(self.data['Pianta'])
        X['Sintomo'] = self.le_sintomo.fit_transform(self.data['Sintomo_Visibile'])
        y = self.le_diagnosi.fit_transform(self.data['Diagnosi_Lab'])

        self.model.fit(X, y)
        print(" -> [ML] Modello addestrato su dataset coerente.")

    def predici_malattia(self, nome_pianta, nome_sintomo):
        try:
            p_code = self.le_pianta.transform([nome_pianta])[0]
            s_code = self.le_sintomo.transform([nome_sintomo])[0]
            
            pred = self.model.predict([[p_code, s_code]])[0]
            malattia = self.le_diagnosi.inverse_transform([pred])[0]
            conf = max(self.model.predict_proba([[p_code, s_code]])[0])
            
            return malattia, conf
        except ValueError:
            return "Dato sconosciuto (non presente nel training set)", 0.0