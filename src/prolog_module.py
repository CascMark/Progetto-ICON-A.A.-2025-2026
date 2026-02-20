import os
import sys
import ctypes

PROLOG_PATH = r"C:\Program Files\swipl\bin"

def configura_prolog():
    """
    Carica manualmente la DLL di Prolog per evitare crash su Windows.
    """
    if not os.path.exists(PROLOG_PATH):
        print(f" [PROLOG SYSTEM] Attenzione: {PROLOG_PATH} non trovato.")
        return False

    os.environ['PATH'] += ';' + PROLOG_PATH

    try:
        dll_path = os.path.join(PROLOG_PATH, "libswipl.dll")
        if os.path.exists(dll_path):
            ctypes.CDLL(dll_path)
            return True
        else:
            print(f" [PROLOG SYSTEM] DLL non trovata in: {dll_path}")
            return False
    except Exception as e:
        print(f" [PROLOG SYSTEM] Errore caricamento DLL: {e}")
        return False

if not configura_prolog():
    print(" [PROLOG SYSTEM] Tentativo di avvio standard (sperando nel PATH di sistema)...")

try:
    from pyswip import Prolog
except ImportError:
    print(" [ERRORE CRITICO] Libreria 'pyswip' mancante. Esegui: pip install pyswip")
    sys.exit(1)


class GardenLogic:
    def __init__(self, kb_path):
        self.prolog = Prolog()
        self.attivo = False
        
        self.kb_path = kb_path.replace('\\', '/')
        
        if not os.path.exists(self.kb_path):
            print(f" [ERRORE PROLOG] File KB non trovato: {self.kb_path}")
            return

        try:
            self.prolog.consult(self.kb_path)
            self.attivo = True
            print(f" [PROLOG] Knowledge Base V4.0 caricata: {os.path.basename(self.kb_path)}")
        except Exception as e:
            print(f" [ERRORE PROLOG] Impossibile caricare KB: {e}")
            self.attivo = False

    def _formatta_per_prolog(self, testo):
        """
        Helper: Assicura che la stringa sia tra apici singoli per Prolog.
        Esempio: Infestazione_Afidi -> 'Infestazione_Afidi'
        """
        if not testo: return "'Sano'"
        clean = str(testo).strip()
        if clean.startswith("'") and clean.endswith("'"):
            return clean
        return f"'{clean}'"

    def ottieni_trattamento(self, diagnosi_ml):
        """
        Chiama la regola intelligente 'trova_cura(MalattiaML, Cura)' definita nel kb.pl.
        Questa regola gestisce automaticamente il mapping (es. Infestazione_Afidi -> Afidi)
        e il fallback (Consultare Agronomo).
        """
        if not self.attivo: return ["Modulo Prolog non attivo"]
        
        malattia_atom = self._formatta_per_prolog(diagnosi_ml)
        
        try:
            query_str = f"trova_cura({malattia_atom}, X)"
            risultati = list(self.prolog.query(query_str))
            
            cure = []
            for res in risultati:
                valore = res["X"]
                
                if isinstance(valore, bytes):
                    valore = valore.decode('utf-8')
                
                valore_leggibile = str(valore).replace("_", " ")
                cure.append(valore_leggibile)
            
            if not cure:
                return ["Nessun trattamento trovato (Errore Logico)"]
                
            return cure

        except Exception as e:
            print(f" [ERRORE QUERY PROLOG] {e}")
            return ["Errore comunicazione Prolog"]

    def verifica_diagnosi_logica(self, pianta, sintomo):
        """
        Interroga la regola 'diagnosi(Pianta, Sintomo, Malattia)' o 'verifica_consistenza'.
        Serve per il cross-check tra ML e KB.
        """
        if not self.attivo: return []
        
        p_atom = self._formatta_per_prolog(pianta)
        s_atom = self._formatta_per_prolog(sintomo)
        
        suggerimenti = []
        try:
            query_str = f"diagnosi({p_atom}, {s_atom}, Malattia)"
            risultati = list(self.prolog.query(query_str))
            
            for res in risultati:
                mal = res['Malattia']
                if isinstance(mal, bytes): mal = mal.decode('utf-8')
                suggerimenti.append(str(mal))
                
        except Exception:
            pass
            
        return suggerimenti