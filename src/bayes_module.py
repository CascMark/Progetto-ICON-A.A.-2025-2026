import sys

# Gestione compatibilità versioni pgmpy
try:
    from pgmpy.models import DiscreteBayesianNetwork
except ImportError:
    try:
        from pgmpy.models import BayesianNetwork as DiscreteBayesianNetwork
    except ImportError:
        from pgmpy.models import BayesianModel as DiscreteBayesianNetwork

from pgmpy.factors.discrete import TabularCPD

def crea_rete_diagnosi():
    """
    Costruisce la Rete Bayesiana per il calcolo delle probabilità.
    Corretto per gestire la matrice delle probabilità trasposta.
    """
    
    # 1. STRUTTURA: Malattia -> Sintomo
    model = DiscreteBayesianNetwork([
        ('Malattia', 'Sintomo')
    ])

    # --- DEFINIZIONE STATI ---
    malattie = [
        'Afidi', 'Botrite', 'Carenza_Calcio', 'Carenza_Ferro', 'Oidio', 
        'Peronospora', 'Ragnetto_Rosso', 'Ruggine', 'Sano', 'Stress_Idrico', 'Virosi'
    ]

    sintomi = [
        'Foglie_Arricciate', 'Foglie_Gialle', 'Foglie_Secche', 'Macchie_Fogliari', 
        'Marciume_Apicale', 'Muffa_Bianca', 'Nessuna', 'Ragnatele'
    ]

    # --- 2. PROBABILITÀ A PRIORI (MALATTIA) ---
    p_sano = 0.20
    p_altre = (1.0 - p_sano) / 10  # 0.08
    
    values_malattia = [
        [p_altre], [p_altre], [p_altre], [p_altre], [p_altre], [p_altre], 
        [p_altre], [p_altre], [p_sano], [p_altre], [p_altre]
    ]

    cpd_malattia = TabularCPD(
        variable='Malattia', variable_card=len(malattie),
        values=values_malattia,
        state_names={'Malattia': malattie}
    )

    # --- 3. PROBABILITÀ CONDIZIONATA (SINTOMO | MALATTIA) ---
    # Qui inseriamo i dati COME LI HAI SCRITTI TU (per Malattia),
    # perché è più leggibile per l'essere umano.
    # Poi li trasponiamo via codice per pgmpy.
    
    # Ordine Sintomi interno a ogni lista: 
    # [Arricciate, Gialle, Secche, Macchie, Marciume, Muffa, Nessuna, Ragnatele]
    
    dati_per_malattia = [
        # 1. Afidi
        [0.60, 0.30, 0.00, 0.00, 0.00, 0.00, 0.10, 0.00], 
        # 2. Botrite
        [0.00, 0.00, 0.00, 0.05, 0.00, 0.90, 0.05, 0.00], 
        # 3. Carenza_Calcio
        [0.00, 0.00, 0.00, 0.00, 0.95, 0.00, 0.05, 0.00], 
        # 4. Carenza_Ferro
        [0.00, 0.95, 0.00, 0.00, 0.00, 0.00, 0.05, 0.00], 
        # 5. Oidio
        [0.00, 0.05, 0.00, 0.00, 0.00, 0.90, 0.05, 0.00], 
        # 6. Peronospora
        [0.00, 0.05, 0.00, 0.90, 0.00, 0.00, 0.05, 0.00], 
        # 7. Ragnetto_Rosso
        [0.00, 0.10, 0.00, 0.00, 0.00, 0.00, 0.05, 0.85], 
        # 8. Ruggine
        [0.00, 0.00, 0.00, 0.95, 0.00, 0.00, 0.05, 0.00], 
        # 9. Sano
        [0.01, 0.01, 0.01, 0.01, 0.00, 0.00, 0.96, 0.00], 
        # 10. Stress_Idrico
        [0.10, 0.00, 0.85, 0.00, 0.00, 0.00, 0.05, 0.00], 
        # 11. Virosi
        [0.70, 0.00, 0.00, 0.25, 0.00, 0.00, 0.05, 0.00], 
    ]

    # --- TRASPOSIZIONE AUTOMATICA ---
    # La funzione zip(*lista) gira la matrice: le righe diventano colonne.
    # Ora pgmpy riceverà: [[Tutte le prob di Arricciate], [Tutte le prob di Gialle], ...]
    values_sintomi_transposed = list(map(list, zip(*dati_per_malattia)))

    cpd_sintomo = TabularCPD(
        variable='Sintomo', variable_card=len(sintomi),
        values=values_sintomi_transposed, # Usiamo la matrice girata
        evidence=['Malattia'],
        evidence_card=[len(malattie)],
        state_names={
            'Malattia': malattie,
            'Sintomo': sintomi
        }
    )

    model.add_cpds(cpd_malattia, cpd_sintomo)
    
    # Verifica validità (ora la somma delle colonne farà 1.0 e non darà errore)
    if not model.check_model():
        raise ValueError("Errore modello: Le probabilità non sommano a 1.")
        
    return model