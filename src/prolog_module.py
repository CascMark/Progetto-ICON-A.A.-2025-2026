import os
import sys
import ctypes

# --- 1. CONFIGURAZIONE SISTEMA (DLL PROLOG) ---
# Percorso tipico su Windows. Se hai installato altrove, verifica questo path.
PROLOG_PATH = r"C:\Program Files\swipl\bin"

def configura_prolog():
    """
    Carica manualmente la DLL di Prolog per evitare crash su Windows.
    """
    if not os.path.exists(PROLOG_PATH):
        # Tentativo di fallback se il percorso standard non esiste
        print(f" [PROLOG SYSTEM] Attenzione: {PROLOG_PATH} non trovato.")
        return False

    # Aggiungiamo al PATH
    os.environ['PATH'] += ';' + PROLOG_PATH

    try:
        # Caricamento esplicito della DLL
        dll_path = os.path.join(PROLOG_PATH, "libswipl.dll")
        if os.path.exists(dll_path):
            ctypes.CDLL(dll_path)
            # print(" [PROLOG SYSTEM] Libreria 'libswipl.dll' agganciata.") # Decommenta per debug
            return True
        else:
            print(f" [PROLOG SYSTEM] DLL non trovata in: {dll_path}")
            return False
    except Exception as e:
        print(f" [PROLOG SYSTEM] Errore caricamento DLL: {e}")
        return False

# Eseguiamo la configurazione PRIMA di importare pyswip
if not configura_prolog():
    print(" [PROLOG SYSTEM] Tentativo di avvio standard (sperando nel PATH di sistema)...")

try:
    from pyswip import Prolog
except ImportError:
    print(" [ERRORE CRITICO] Libreria 'pyswip' mancante. Esegui: pip install pyswip")
    sys.exit(1)


# --- 2. CLASSE LOGICA (INTERFACCIA AI-PROLOG) ---
class GardenLogic:
    def __init__(self, kb_path):
        self.prolog = Prolog()
        self.attivo = False
        
        # Gestione path Windows/GitBash (i backslash rompono Prolog)
        self.kb_path = kb_path.replace('\\', '/')
        
        if not os.path.exists(self.kb_path):
            print(f" [ERRORE PROLOG] File KB non trovato: {self.kb_path}")
            return

        try:
            # Consultiamo il file .pl
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
        
        # Formattiamo l'input (es. 'Infestazione_Afidi')
        malattia_atom = self._formatta_per_prolog(diagnosi_ml)
        
        try:
            # Query alla regola ponte
            query_str = f"trova_cura({malattia_atom}, X)"
            risultati = list(self.prolog.query(query_str))
            
            cure = []
            for res in risultati:
                # Estraiamo la variabile X
                valore = res["X"]
                
                # Decodifica se bytes (succede con alcune versioni di pyswip)
                if isinstance(valore, bytes):
                    valore = valore.decode('utf-8')
                
                # Pulizia per la GUI (rimuove underscore)
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
            # Usiamo la tua regola classica diagnosi/3
            query_str = f"diagnosi({p_atom}, {s_atom}, Malattia)"
            risultati = list(self.prolog.query(query_str))
            
            for res in risultati:
                mal = res['Malattia']
                if isinstance(mal, bytes): mal = mal.decode('utf-8')
                suggerimenti.append(str(mal))
                
        except Exception:
            pass # Se fallisce, restituisce lista vuota senza rompere l'app
            
        return suggerimenti