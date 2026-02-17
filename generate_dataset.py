import os
import random
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "dataset_integrato.csv")

print(f"--- GENERATORE DATASET (NOMI SEMPLICI) ---")

# USIAMO I NOMI SEMPLICI: "Basilico", "Pomodoro", "Lattuga", "Rosa"
SCENARI = {
    "Basilico": {
        "Foglie_Gialle": ["Afidi", "Carenza_Ferro"],
        "Sano": ["Nessuna"]
    },
    "Pomodoro": {
        "Macchie_Fogliari": ["Peronospora", "Ruggine"],
        "Sano": ["Nessuna"]
    },
    "Lattuga": {
        "Foglie_Secche": ["Stress_Idrico"], 
        "Sano": ["Nessuna"]
    },
    "Rosa": {
        "Muffa_Bianca": ["Oidio"],          
        "Macchie_Fogliari": ["Ruggine"],
        "Sano": ["Nessuna"]
    },
    "Peperone": {
         "Macchie_Fogliari": ["Virosi"],
         "Sano": ["Nessuna"]
    }
}

data = []
num_samples = 3000

for _ in range(num_samples):
    pianta = random.choice(list(SCENARI.keys()))
    is_malata = random.choice([True, False])
    
    if is_malata:
        sintomi_malati = [s for s in SCENARI[pianta].keys() if s != "Sano"]
        if not sintomi_malati: continue
        
        sintomo = random.choice(sintomi_malati)
        malattia = random.choice(SCENARI[pianta][sintomo])
        
        if "Stress_Idrico" in malattia:
            umidita = round(random.uniform(0.0, 0.25), 2)
        elif "Muffa" in sintomo or "Oidio" in malattia or "Peronospora" in malattia:
            umidita = round(random.uniform(0.80, 0.99), 2)
        else:
            umidita = round(random.uniform(0.40, 0.70), 2)
    else:
        sintomo = "Nessuno"
        malattia = "Nessuna"
        umidita = round(random.uniform(0.40, 0.60), 2)

    row = {
        "Pianta": pianta,
        "Sintomo_Visibile": sintomo,
        "Diagnosi_Lab": malattia,
        "Umidita": umidita,
        "Temperatura": round(random.uniform(15.0, 35.0), 1),
        "pH_Terreno": round(random.uniform(5.5, 7.5), 1),
        "Ore_Luce": random.randint(4, 12)
    }
    data.append(row)

df = pd.DataFrame(data)
df.to_csv(OUTPUT_CSV, index=False)
print(f"[SUCCESSO] Dataset 'dataset_integrato.csv' rigenerato con nomi semplici.")