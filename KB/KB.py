import pandas as pd
import os
from pyswip import Prolog

class KB:
    def __init__(self, percorso_csv, percorso_pl):
        self.percorso_csv = percorso_csv
        self.percorso_pl = percorso_pl
        self.prolog = Prolog()

    def generazione_kb(self):
        """Legge il nuovo CSV arricchito e genera il file kb.pl"""
        if not os.path.exists(self.percorso_csv):
            print(f"Errore: Il file {self.percorso_csv} non esiste.")
            return

        dataset = pd.read_csv(self.percorso_csv)
        os.makedirs(os.path.dirname(self.percorso_pl), exist_ok=True)
        
        with open(self.percorso_pl, 'w', encoding='utf-8') as f:
            f.write("% --- Base di Conoscenza Green-Root (Dataset Arricchito) ---\n\n")
            
            for indice, riga in dataset.iterrows():
            
                v_score = riga['vulnerability_score']
                specie = str(riga['species']).lower().replace(" ", "_")
                malattia_tipo = str(riga['disease_type']).lower().replace(" ", "_")
                colore = str(riga['leaf_color']).lower().replace(" ", "_")
                texture = str(riga['leaf_texture']).lower().replace(" ", "_")
                
                if pd.isna(riga['spots']) or str(riga['spots']).lower() == 'none':
                    macchie = 'none'
                else:
                    macchie = str(riga['spots']).lower().replace(" ", "_")

        
                fatto = (f"data({indice}, {riga['temperature']}, {riga['humidity']}, "
                        f"{riga['rainfall']}, {riga['soil_pH']}, {riga['disease_present']}, "
                        f"{specie}, {malattia_tipo}, {colore}, {texture}, {macchie}, {v_score}).\n")
                f.write(fatto)
                
       
            f.write("\n% --- Regole Logiche ---\n")
            
     
            f.write("rischio_critico(ID) :- data(ID, _, _, _, _, _, _, _, _, _, _, VS), VS >= 6.\n")
            f.write("rischio_basso(ID) :- data(ID, _, _, _, _, _, _, _, _, _, _, VS), VS >= 3, VS < 6.\n")
            f.write("rischio_nullo(ID) :- data(ID, _, _, _, _, _, _, _, _, _, _, VS), VS < 3.\n")

            f.write("diagnosi(ID, peronospora) :- data(ID, _, _, _, _, _, potato, late_blight, brown, _, dark_spots, _).\n")

            f.write("diagnosi(ID, ruggine) :- data(ID, _, _, _, _, _, chili, leaf_rust, yellowish, dry_curled, rust_spots, _).\n")
            
            f.write("diagnosi(ID, oidio) :- data(ID, _, _, _, _, _, _, powdery_mildew, yellowish, _, white, _).\n")
            
            f.write("diagnosi(ID, carenza_nutrizionale) :- data(ID, _, _, _, _, _, citrus, nutrient_deficiency, pale_green, _, yellow_veins, _).\n")
            
            f.write("diagnosi(ID, stress_idrico) :- data(ID, _, _, _, _, _, _, water_stress, brown, dry_curled, none, _).\n")

            f.write("diagnosi(ID, infezione_virale) :- data(ID, _, _, _, _, _, _, generic_viral_infection, mottled, distorted, none, _).\n")

            f.write("pianta_sana(ID) :- data(ID, _, _, _, _, 0, _, healthy, green, normal, none, _).\n")

        print(f"KB generata con successo in {self.percorso_pl}")

    def carica_kb(self):
        try:
            path_pyswip = self.percorso_pl.replace(os.sep, '/')
            self.prolog.consult(path_pyswip)
            print("KB caricata correttamente in Prolog.")
        except Exception as e:
            print(f"Errore caricamento: {e}")

    # Metodi per le query

    def get_rischio_critico(self):
        """Esegue la query per ottenere gli elementi con rischio critico"""
        query = "rischio_critico(ID)"
        result = list(self.prolog.query(query))
        return [r["ID"] for r in result]

    def get_rischio_basso(self):
        """Esegue la query per ottenere gli elementi con rischio basso"""
        query = "rischio_basso(ID)"
        result = list(self.prolog.query(query))
        return [r["ID"] for r in result]

    def get_rischio_nullo(self):
        """Esegue la query per ottenere gli elementi con rischio nullo"""
        query = "rischio_nullo(ID)"
        result = list(self.prolog.query(query))
        return [r["ID"] for r in result]

    def get_pianta_sana(self):
        """Esegue la query per ottenere gli elementi completamente sani"""
        query = "pianta_sana(ID)"
        result = list(self.prolog.query(query))
        return [r["ID"] for r in result]

    def diagnosi_peronospora(self):
        """Query specifica per la Peronospora (late_blight)"""
        query = "diagnosi(ID, peronospora)"
        risultati = list(self.prolog.query(query))
        return [r["ID"] for r in risultati]

    def diagnosi_ruggine(self):
        """Query specifica per la ruggine (leaf_rust)"""
        query = "diagnosi(ID, ruggine)"
        risultati = list(self.prolog.query(query))
        return [r["ID"] for r in risultati]

    def diagnosi_oidio(self):
        """Query specifica per l'oidio (powdery_mildew)"""
        query = "diagnosi(ID, oidio)"
        risultati = list(self.prolog.query(query))
        return [r["ID"] for r in risultati]

    def diagnosi_carenza_nutrizionale(self):
        """Query specifica per la carenza nutrizionale (nutrient_deficiency)"""
        query = "diagnosi(ID, carenza_nutrizionale)"
        risultati = list(self.prolog.query(query))
        return [r["ID"] for r in risultati]

    def diagnosi_stress_idrico(self):
        """Query specifica per lo stress idrico (water_stress)"""
        query = "diagnosi(ID, stress_idrico)"
        risultati = list(self.prolog.query(query))
        return [r["ID"] for r in risultati]

    def diagnosi_infezione_virale(self):
        """Query specifica per l'infezione virale generic_viral_infection)"""
        query = "diagnosi(ID, infezione_virale)"
        risultati = list(self.prolog.query(query))
        return [r["ID"] for r in risultati]

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    percorso_csv = os.path.join(base_path, "..", "data", "plant_disease_set.csv")
    percorso_pl = os.path.join(base_path, "kb.pl")

    kb_manager = KB(percorso_csv, percorso_pl)
    kb_manager.generazione_kb()
    kb_manager.carica_kb()