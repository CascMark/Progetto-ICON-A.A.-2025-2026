import pandas as pd
import os
from pyswip import Prolog

class KB:

    def __init__(self, percorso_csv, percorso_pl):
        """
        Inizializza il manager della Knowledge Base.
        :param percorso_csv: Percorso del file plant_disease.csv
        :param percorso_pl: Percorso dove salvare il file kb.pl
        """
        self.percorso_csv = percorso_csv
        self.percorso_pl = percorso_pl
        self.prolog = Prolog()

    def generazione_kb(self):
        """
        Legge il CSV e genera il file kb.pl rispettando fedelmente i dati
        """
        if not os.path.exists(self.percorso_csv):
            print(f"Errore: Il file {self.percorso_csv} non esiste.")
            return

        dataset = pd.read_csv(self.percorso_csv)
        
        os.makedirs(os.path.dirname(self.percorso_pl), exist_ok=True)
        
        with open(self.percorso_pl, 'w', encoding='utf-8') as f:
            
            for indice, riga in dataset.iterrows():

                temperature = riga['temperature']
                humidity = riga['humidity']
                rainfall = riga['rainfall']
                soil_pH = riga['soil_pH']
                disease_present = riga['disease_present']
                vulnerability_score = riga['vulnerability_score']

                species = str(riga['species']).lower().replace(" ", "_")
                disease_type = str(riga['disease_type']).lower().replace(" ", "_")
                leaf_color = str(riga['leaf_color']).lower().replace(" ", "_")
                leaf_texture = str(riga['leaf_texture']).lower().replace(" ", "_")
                
                if pd.isna(riga['spots']):
                    spots = 'none'
                else:
                    spots = str(riga['spots']).lower().replace(" ", "_")

                fatto = (f"data({indice}, {temperature}, {humidity}, {rainfall}, {soil_pH}, "
                        f"{disease_present}, {species}, {disease_type}, {leaf_color}, {leaf_texture}, "
                        f"{spots}, {vulnerability_score}).\n")
                
                f.write(fatto)
                
          
            # --- Regole Logiche ---
            f.write("\n% --- Regole Logiche ---\n")
            
            f.write("pianta_malata(ID) :- data(ID, _, _, _, _, 1, _, _, _, _, _, _).\n")

            f.write("rischio_critico(ID) :- data(ID, _, _, _, _, _, _, _, _, _, _, VS), VS >= 6.\n")

            f.write("rischio basso(ID) :- data(ID, _, _, _, _, _, _, _, _, _, _, VS), VS >= 3, VS < 6.\n")

            f.write("riscio_nullo(ID) :- data(ID, _, _, _, _, _, _, _, _, _, _, VS), VS < 3.\n")
                    
            f.write("diagnosi(ID, oidio) :- data(ID, _, _, _, _, _, _, _, yellowish, _, white, _).\n")

            f.write("diagnosi(ID, carenza_nutrizionale) :- data(ID, _, _, _, _, _, _, _, pale_green, _, yellow_veins, _).\n")

            f.write("diagnosi(ID, infezione_virale) :- data(ID, _, _, _, _, _, _, _, mottled, distorted, none, _).\n")

            f.write("pianta_sana(ID) :- data(ID, _, _, _, _, 0, _, healthy, green, normal, none _).\n")

        print(f"File {self.percorso_pl} generato con successo rispettando al 100% i dati del CSV.")

    def carica_kb(self):
        """Carica il file Prolog generato nel motore di inferenza."""
        try:
            self.prolog.consult(self.percorso_pl)
            print("Knowledge Base caricata correttamente in Prolog.")
        except Exception as e:
            print(f"Errore durante il caricamento della KB: {e}")

if __name__ == "__main__":

    print("--------------------- AVVIO PROCESSO DI GENERAZIONE DEL KB ---------------------")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    percorso_csv_input = os.path.join(base_path, "..", "data", "plant_disease.csv")
    percorso_pl_output = os.path.join(base_path, "kb.pl")

    print(f"Cercando il file CSV in: {percorso_csv_input}")
    
    kb_manager = KB(percorso_csv_input, percorso_pl_output)
    kb_manager.generazione_kb()
    
    print("--------------------- PROCESSO COMPLETATO ---------------------")