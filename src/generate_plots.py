import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

from sklearn.preprocessing import LabelEncoder, StandardScaler, label_binarize
from sklearn.model_selection import learning_curve, train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression # <--- NUOVO IMPORT
from sklearn.metrics import silhouette_score

# --- CONFIGURAZIONE PATH ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "src" else SCRIPT_DIR
DATASET_PATH = os.path.join(ROOT_DIR, "data", "piante_dataset.csv")
PLOTS_DIR = os.path.join(ROOT_DIR, "plots")

os.makedirs(PLOTS_DIR, exist_ok=True)

def load_and_preprocess():
    df = pd.read_csv(DATASET_PATH)
    
    le_fam = LabelEncoder()
    df['Famiglia_Encoded'] = le_fam.fit_transform(df['Famiglia'].fillna("Sconosciuta"))
    
    le_sint = LabelEncoder()
    df['Sintomo_Encoded'] = le_sint.fit_transform(df['Sintomi_Visivi'].fillna("Nessuno"))
    
    X = df[['Famiglia_Encoded', 'Sintomo_Encoded', 'Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale', 'PH_Suolo']]
    y = df['Diagnosi_Reale']
    
    le_target = LabelEncoder()
    y_encoded = le_target.fit_transform(y)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y_encoded, le_target.classes_, df

def plot_kmeans_evaluation(df):
    """Genera il grafico del Gomito e del Silhouette Score"""
    print("Generazione K-Means Plots...")
    scaler = StandardScaler()
    X_env = scaler.fit_transform(df[['Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale']])
    
    inertias = []
    silhouettes = []
    K_range = range(2, 11)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(X_env)
        inertias.append(kmeans.inertia_)
        silhouettes.append(silhouette_score(X_env, labels))
        
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(K_range, inertias, marker='o', color='navy')
    ax1.set_title('Metodo del Gomito per K-Means')
    ax1.set_xlabel('Numero di Cluster (k)')
    ax1.set_ylabel('Inertia')
    ax1.grid(True)
    
    ax2.plot(K_range, silhouettes, marker='o', color='green')
    ax2.set_title('Silhouette Score per K-Means')
    ax2.set_xlabel('Numero di Cluster (k)')
    ax2.set_ylabel('Silhouette Score')
    ax2.grid(True)
    
    plt.savefig(os.path.join(PLOTS_DIR, '01_kmeans_evaluation.png'), bbox_inches='tight')
    plt.close()

def plot_learning_curves(X, y):
    """Genera le Learning Curves per 4 Modelli (inclusa Logistic Regression)"""
    print("Generazione Learning Curves...")
    
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "SVM (Kernel RBF)": SVC(kernel='rbf', random_state=42),
        "Naive Bayes": GaussianNB(),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }
    
    plt.figure(figsize=(14, 8))
    
    colors = ['blue', 'green', 'red', 'purple']
    
    for (name, model), color in zip(models.items(), colors):
        train_sizes, train_scores, test_scores = learning_curve(
            model, X, y, cv=5, n_jobs=-1, 
            train_sizes=np.linspace(0.1, 1.0, 10), scoring='accuracy'
        )
        
        train_mean = np.mean(train_scores, axis=1)
        test_mean = np.mean(test_scores, axis=1)
        
        plt.plot(train_sizes, train_mean, '--', color=color, label=f'{name} (Train)')
        plt.plot(train_sizes, test_mean, '-', color=color, label=f'{name} (Validation)')
        
    plt.title('Confronto delle Curve di Apprendimento (Learning Curves)')
    plt.xlabel('Numero di Campioni nel Training Set')
    plt.ylabel('Accuratezza')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, '02_learning_curves.png'), bbox_inches='tight')
    plt.close()

def plot_confusion_and_roc(X, y, classes):
    """Genera Matrici di Confusione e Curve ROC multi-classe per 4 Modelli"""
    print("Generazione Matrici di Confusione e Curve ROC...")
    
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "SVM": SVC(kernel='rbf', probability=True, random_state=42),
        "Naive Bayes": GaussianNB(),
        "Logistic_Regression": LogisticRegression(max_iter=1000, random_state=42)
    }
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    y_test_bin = label_binarize(y_test, classes=range(len(classes)))
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_probs = model.predict_proba(X_test)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # 1. Matrice di Confusione
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax1, 
                    xticklabels=classes, yticklabels=classes)

        display_name = name.replace('_', ' ')
        ax1.set_title(f'Matrice di Confusione: {display_name}')
        ax1.set_ylabel('Classe Reale')
        ax1.set_xlabel('Classe Predetta')
        
        # 2. Curva ROC (Micro-Averaging per multi-classe)
        fpr, tpr, _ = roc_curve(y_test_bin.ravel(), y_probs.ravel())
        roc_auc = auc(fpr, tpr)
        
        ax2.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        ax2.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        ax2.set_xlim([0.0, 1.0])
        ax2.set_ylim([0.0, 1.05])
        ax2.set_xlabel('FPR (False Positive Rate)')
        ax2.set_ylabel('TPR (True Positive Rate)')
        ax2.set_title(f'ROC Curve: {display_name}')
        ax2.legend(loc="lower right")
        ax2.grid(True)
        
     
        filename = f'03_{name.lower()}_eval.png'
        plt.savefig(os.path.join(PLOTS_DIR, filename), bbox_inches='tight')
        plt.close()
    

def plot_pie_charts(df):
    """Genera i grafici a torta per Diagnosi Reali e Distribuzione Cluster"""
    print("Generazione Grafici a Torta (Distribuzione)...")
    
    # 1. Calcolo distribuzione etichette reali (Diagnosi)
    dist_reale = df['Diagnosi_Reale'].value_counts()
    
    # 2. Esecuzione K-Means per trovare la distribuzione dei cluster climatici (k=3)
    scaler = StandardScaler()
    X_env = scaler.fit_transform(df[['Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale']])
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_labels = kmeans.fit_predict(X_env)
    
    # Contiamo quanti elementi ci sono in ogni cluster
    unique, counts = np.unique(cluster_labels, return_counts=True)
    dist_cluster = dict(zip(unique, counts))
    
    # --- Disegno dei grafici ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Torta 1: Etichette Reali
    ax1.pie(dist_reale.values, labels=dist_reale.index, autopct='%1.1f%%', 
            startangle=140, colors=sns.color_palette("Set2", len(dist_reale)))
    ax1.set_title("Distribuzione delle Patologie Reali\n(Dal Dataset Ontologico)")
    
    # Torta 2: Cluster K-Means
    labels_cluster = [f"Profilo Climatico {k}" for k in dist_cluster.keys()]
    ax2.pie(dist_cluster.values(), labels=labels_cluster, autopct='%1.1f%%', 
            startangle=140, colors=sns.color_palette("pastel"))
    ax2.set_title("Distribuzione dei Cluster Ambientali\n(K-Means con k=3)")
    
    plt.savefig(os.path.join(PLOTS_DIR, '04_pie_charts_distribution.png'), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("--- AVVIO GENERATORE DI GRAFICI PER DOCUMENTAZIONE ---")
    X, y, classes, df = load_and_preprocess()
    
    plot_kmeans_evaluation(df)
    plot_learning_curves(X, y)
    plot_confusion_and_roc(X, y, classes)
    plot_pie_charts(df)
    
    print(f"[SUCCESSO] Tutti i grafici sono stati salvati nella cartella: {PLOTS_DIR}")