import os
import random
import pandas as pd
import owlready2 as owl

# --- CONFIGURAZIONE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONTO_PATH = os.path.join(BASE_DIR, "knowledge_base", "Ontologia.owx")
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "dataset_integrato.csv")

# Carichiamo l'ontologia
print(f"Caricamento ontologia da: {ONTO_PATH}")
onto = owl.get_ontology(ONTO_PATH).load()

# --- ESTRAZIONE VOCABOLARIO DALL'ONTOLOGIA ---
# Cerchiamo gli individui reali definiti nel file .owx
# Nota: Adattare le query in base a come si chiamano le tue classi in Protégé
# Esempio: onto.Pianta.instances() restituisce [ontologia.Basilico_Genovese, ...]

def get_clean_names(owl_class):
    return [i.name for i in owl_class.instances()]

# Recuperiamo le liste di nomi validi
# Se le tue classi si chiamano diversamente (es. 'Plant' invece di 'Pianta'), modifica qui
try:
    lista_piante = get_clean_names(onto.Pianta)
    lista_sintomi = get_clean_names(onto.Sintomo)
    lista_malattie = get_clean_names(onto.Avversita) # o Malattia
except AttributeError:
    print("ERRORE: I nomi delle classi nello script non corrispondono a quelli nell'Ontologia.")
    print("Verifica se in Protégé hai usato 'Pianta', 'Plant', 'Sintomo' o 'Symptom'.")
    exit()

print(f"Piante trovate: {lista_piante}")
print(f"Sintomi trovati: {lista_sintomi}")

# --- GENERAZIONE DATI SINTETICI ---
data = []
num_samples = 1000

for _ in range(num_samples):
    # Scelta casuale della pianta
    pianta = random.choice(lista_piante)
    
    # Simulazione sensori (valori casuali realistici)
    temp = round(random.uniform(15.0, 35.0), 1)
    umidita = round(random.uniform(0.1, 1.0), 2) # Scala 0-1
    ph = round(random.uniform(5.5, 7.5), 1)
    luce = random.randint(4, 12)
    
    # Logica di base per assegnare Sintomi e Malattie coerenti
    # (Per il ML, creiamo pattern riconoscibili)
    
    if umidita < 0.3:
        # Caso Secco -> Rischio Stress Idrico o Parassiti
        stato = "Malato"
        sintomo = "Foglie_Gialle" if "Foglie_Gialle" in lista_sintomi else random.choice(lista_sintomi)
        malattia = "Afidi" if "Afidi" in lista_malattie else random.choice(lista_malattie)
    elif umidita > 0.8:
        # Caso Umido -> Rischio Funghi
        stato = "Malato"
        sintomo = "Macchie_Fogliari" if "Macchie_Fogliari" in lista_sintomi else random.choice(lista_sintomi)
        malattia = "Oidio" if "Oidio" in lista_malattie else random.choice(lista_malattie)
    else:
        # Caso Sano
        stato = "Sano"
        sintomo = "Nessuno"
        malattia = "Nessuna"

    # Aggiungiamo rumore casuale (il mondo reale non è perfetto)
    if random.random() < 0.1:
        sintomo = random.choice(lista_sintomi)

    row = {
        "Pianta": pianta,             # Coincide con l'Ontologia (es. Basilico_Genovese)
        "Temperatura": temp,
        "Umidita": umidita,
        "pH_Terreno": ph,
        "Ore_Luce": luce,
        "Sintomo_Visibile": sintomo,  # Coincide con l'Ontologia (es. Foglie_Gialle)
        "Diagnosi_Lab": malattia,     # Coincide con l'Ontologia (es. Afidi)
        "Stato_Salute": stato
    }
    data.append(row)

# --- SALVATAGGIO ---
df = pd.DataFrame(data)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Dataset generato con successo: {OUTPUT_CSV}")
print(df.head())