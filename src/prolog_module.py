from pyswip import Prolog

class GardenLogic:
    def __init__(self, kb_path):
        self.prolog = Prolog()
        # Carichiamo il file .pl del tuo compagno
        # Nota: assicurati che i percorsi nel file .pl non diano conflitti
        self.prolog.consult(kb_path)

    def ottieni_trattamento(self, malattia):
        # Interroga la regola trattamento(Malattia, Cura) presente in kb.pl
        query = f"trattamento('{malattia}', Cura)"
        try:
            risultati = list(self.prolog.query(query))
            curas = [res['Cura'] for res in risultati]
            return list(set(curas)) # Rimuove duplicati
        except Exception as e:
            print(f"Errore Prolog: {e}")
            return []
            
    def verifica_diagnosi_logica(self, pianta, sintomo):
        # Interroga la regola diagnosi(Pianta, Sintomo, Malattia)
        query = f"diagnosi('{pianta}', '{sintomo}', Malattia)"
        risultati = list(self.prolog.query(query))
        return [res['Malattia'] for res in risultati]