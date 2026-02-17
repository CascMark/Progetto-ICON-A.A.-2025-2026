from sklearn.cluster import KMeans
import numpy as np

class UnsupervisedModels:
    def __init__(self, n_clusters=3):
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.centroids = None

    def train(self, X_env):
        """
        X_env: Solo dati ambientali (Umidità, Temp, Luce)
        """
        self.kmeans.fit(X_env)
        self.centroids = self.kmeans.cluster_centers_
        
        # Analisi automatica dei cluster (per dare un nome sensato)
        print(" [K-MEANS] Analisi dei Cluster generati:")
        for i, center in enumerate(self.centroids):
            # center[0]=Umidita, center[1]=Temp, center[2]=Luce
            print(f"   - Cluster {i}: Umidità {center[0]:.2f}, Temp {center[1]:.1f}°C, Luce {center[2]:.1f}h")

    def predict_cluster(self, input_env):
        cluster_id = self.kmeans.predict(input_env)[0]
        
        # Logica semplice per dare un nome al cluster basato sul centroide
        # (Nota: questo è un'euristica basata sui dati medi)
        centroid = self.centroids[cluster_id]
        umid_media = centroid[0]
        
        descrizione = f"Cluster {cluster_id}"
        if umid_media < 0.4:
            descrizione = "Ambiente Secco/Arido"
        elif umid_media > 0.7:
            descrizione = "Ambiente Umido/Tropicale"
        else:
            descrizione = "Ambiente Temperato/Standard"
            
        return descrizione