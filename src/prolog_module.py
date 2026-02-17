import os
import sys
import ctypes

# --- CONFIGURAZIONE PERCORSO PROLOG ---
# Usiamo il percorso esatto che mi hai fornito
PROLOG_PATH = r"C:\Program Files\swipl\bin"

def configura_prolog():
    """
    Carica manualmente la DLL di Prolog dal percorso specificato.
    """
    if not os.path.exists(PROLOG_PATH):
        print(f" [ERRORE CRITICO] Il percorso {PROLOG_PATH} non esiste!")
        return False

    print(f" [SYSTEM] Configurazione Prolog su: {PROLOG_PATH}")

    # 1. Aggiungiamo al PATH di sistema (fondamentale per Windows)
    os.environ['PATH'] += ';' + PROLOG_PATH

    # 2. Carichiamo esplicitamente la libreria (il segreto per evitare crash)
    try:
        # Percorso completo della DLL
        dll_path = os.path.join(PROLOG_PATH, "libswipl.dll")
        ctypes.CDLL(dll_path)
        print(" [SYSTEM] Libreria 'libswipl.dll' agganciata correttamente.")
        return True
    except Exception as e:
        print(f" [ERRORE DLL] Impossibile caricare libswipl.dll: {e}")
        return False

# Eseguiamo la configurazione PRIMA di importare la libreria Python
if configura_prolog():
    try:
        from pyswip import Prolog
    except ImportError:
        print(" [ERRORE] Libreria 'pyswip' mancante. Fai 'pip install pyswip'")
        sys.exit(1)
else:
    print(" [ERRORE] Impossibile avviare il ponte Python-Prolog.")
    sys.exit(1)

class GardenLogic:
    def __init__(self, kb_path):
        self.prolog = Prolog()
        try:
            # Normalizziamo il percorso per Windows (backslashes -> slashes)
            kb_path = kb_path.replace('\\', '/')
            
            # Carichiamo il file .pl
            self.prolog.consult(kb_path)
            self.attivo = True
            print(f" [PROLOG] Knowledge Base caricata: {os.path.basename(kb_path)}")
        except Exception as e:
            print(f" [PROLOG ERROR] Errore caricamento KB: {e}")
            self.attivo = False

    def ottieni_trattamento(self, malattia):
        """
        Interroga Prolog: trattamento('Malattia', Cura).
        """
        if not self.attivo: return []
        
        # Pulizia stringa
        malattia = malattia.strip()
        
        # Query
        query = f"trattamento('{malattia}', Cura)"
        
        try:
            risultati = list(self.prolog.query(query))
            return [res['Cura'] for res in risultati]
        except Exception as e:
            print(f" [PROLOG QUERY ERROR] {e}")
            return []

    def verifica_diagnosi_logica(self, pianta, sintomo):
        """
        Interroga Prolog: diagnosi('Pianta', 'Sintomo', Malattia).
        """
        if not self.attivo: return []
        
        try:
            query = f"diagnosi('{pianta}', '{sintomo}', Malattia)"
            risultati = list(self.prolog.query(query))
            return [res['Malattia'] for res in risultati]
        except Exception:
            return []