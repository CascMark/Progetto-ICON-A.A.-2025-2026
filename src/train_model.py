import os
import pandas as pd
import numpy as np
import joblib
import json
import warnings

from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.metrics import roc_auc_score

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "src" else SCRIPT_DIR
DATASET_PATH = os.path.join(ROOT_DIR, "data", "piante_dataset.csv") 
MODEL_DIR = os.path.join(ROOT_DIR, "models")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

os.makedirs(MODEL_DIR, exist_ok=True)

def train_and_validate():
    print("============================================================")
    print("   AZIONE 3: 10-FOLD CV CON METRICHE AVANZATE (F1, AUC, P)")
    print("============================================================")
    
    if not os.path.exists(DATASET_PATH):
        print(f"[ERRORE] Dataset non trovato: {DATASET_PATH}")
        return
    df = pd.read_csv(DATASET_PATH)

    le_fam = LabelEncoder()
    df['Famiglia_Encoded'] = le_fam.fit_transform(df['Famiglia'].fillna("Sconosciuta"))
    
    le_sint = LabelEncoder()
    df['Sintomo_Encoded'] = le_sint.fit_transform(df['Sintomi_Visivi'].fillna("Nessuno"))
    
    X = df[['Famiglia_Encoded', 'Sintomo_Encoded', 'Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale', 'PH_Suolo']]
    y = df['Diagnosi_Reale']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Neural Network": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42),
        "SVM (Kernel RBF)": SVC(kernel='rbf', probability=True, random_state=42),
        "Naive Bayes": GaussianNB(),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }

    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    scoring = ['accuracy', 'f1_weighted', 'precision_weighted']
    metrics_dict = {}
    
    print(f"{'Algoritmo':<18} | {'Acc':<6} | {'Var':<6} | {'Dev':<6} | {'F1':<6} | {'AVG(P)':<6} | {'AUC':<6}")
    print("-" * 70)

    X_tr, X_te, y_tr, y_te = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    for name, model in models.items():
        cv_results = cross_validate(model, X_scaled, y, cv=cv, scoring=scoring)
        
        acc_array = cv_results['test_accuracy']
        acc_mean = np.mean(acc_array)
        acc_var = np.var(acc_array)
        acc_std = np.std(acc_array)
        
        f1_mean = np.mean(cv_results['test_f1_weighted'])
        prec_mean = np.mean(cv_results['test_precision_weighted'])
        
        try:
            model_temp = type(model)(**model.get_params())
            model_temp.fit(X_tr, y_tr)
            y_probs = model_temp.predict_proba(X_te)
            auc_val = roc_auc_score(y_te, y_probs, multi_class='ovo')
        except:
            auc_val = -1.0 

        metrics_dict[name] = {
            "Accuratezza": float(acc_mean),
            "Varianza": float(acc_var),
            "Deviazione": float(acc_std),
            "F1-score": float(f1_mean),
            "AVG(P)": float(prec_mean),
            "AUC": float(auc_val)
        }
        
        auc_str = f"{auc_val:.3f}" if auc_val >= 0 else "//"
        print(f"{name:<18} | {acc_mean:.3f} | {acc_var:.3f} | {acc_std:.3f} | {f1_mean:.3f} | {prec_mean:.3f} | {auc_str:<6}")

    rf = models["Random Forest"].fit(X_scaled, y)
    nn = models["Neural Network"].fit(X_scaled, y)
    scaler_env = StandardScaler()
    X_env = scaler_env.fit_transform(df[['Ore_Luce', 'Umidita_Ottimale', 'Temperatura_Ottimale']])
    kmeans = KMeans(n_clusters=3, random_state=42).fit(X_env)

    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics_dict, f, indent=4)
        
    joblib.dump(rf, os.path.join(MODEL_DIR, "model_rf.pkl"))
    joblib.dump(nn, os.path.join(MODEL_DIR, "model_nn.pkl"))
    joblib.dump(kmeans, os.path.join(MODEL_DIR, "model_kmeans.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    joblib.dump(le_fam, os.path.join(MODEL_DIR, "le_famiglia.pkl"))
    joblib.dump(le_sint, os.path.join(MODEL_DIR, "le_sintomo.pkl"))
    joblib.dump(scaler_env, os.path.join(MODEL_DIR, "scaler_env.pkl"))
    
    print("\n[SUCCESSO] Modelli e Metriche Avanzate salvati correttamente!")

if __name__ == "__main__":
    train_and_validate()