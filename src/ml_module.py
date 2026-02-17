import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

class SmartGardenML:
    def __init__(self, dataset_path):
        self.data = pd.read_csv(dataset_path)
        # Placeholder per il modello supervisionato
        self.model = RandomForestClassifier()
    
    def clustering_piante(self):
        # Esegue K-Means per raggruppare piante con esigenze simili (Cap. 2)
        # Basato su richiedeOreLuce e haLivelloUmiditaOttimale 
        X = self.data[['luce', 'umidita']]
        kmeans = KMeans(n_clusters=3, n_init=10)
        return kmeans.fit_predict(X)

    def predici_salute(self, nuovi_dati):
        # Classificazione dello stato (Cap. 3)
        # In un caso reale, qui useresti il modello addestrato sul dataset [cite: 1]
        if nuovi_dati['umidita'] < 0.3:
            return "Rischio_Malattia"
        return "Sano"