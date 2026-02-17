from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def crea_rete_diagnosi():
    """
    Costruisce la Rete Bayesiana per la diagnosi differenziale.
    Struttura: Carenza_Ferro, Afidi, Cocciniglia -> Foglie_Gialle
    """
    # 1. Definizione Struttura (Grafo)
    model = DiscreteBayesianNetwork([
        ('Carenza_Ferro', 'Foglie_Gialle'),
        ('Afidi', 'Foglie_Gialle'),
        ('Cocciniglia', 'Foglie_Gialle')
    ])

    # 2. Definizione Probabilità a Priori (P(Causa))
    # Valori ipotetici basati sulla frequenza nel giardino
    cpd_ferro = TabularCPD(variable='Carenza_Ferro', variable_card=2, values=[[0.8], [0.2]])
    cpd_afidi = TabularCPD(variable='Afidi', variable_card=2, values=[[0.85], [0.15]])
    cpd_cocciniglia = TabularCPD(variable='Cocciniglia', variable_card=2, values=[[0.9], [0.1]])

    # 3. Probabilità Condizionata (CPT) - P(Sintomo | Cause)
    # Sintomo: Foglie_Gialle
    cpd_sintomo = TabularCPD(
        variable='Foglie_Gialle', variable_card=2,
        values=[
            # False (Sintomo assente) per le 8 combinazioni
            [0.99, 0.40, 0.30, 0.10, 0.20, 0.05, 0.05, 0.01], 
            # True (Sintomo presente)
            [0.01, 0.60, 0.70, 0.90, 0.80, 0.95, 0.95, 0.99]  
        ],
        evidence=['Carenza_Ferro', 'Afidi', 'Cocciniglia'],
        evidence_card=[2, 2, 2]
    )

    # 4. Aggiunta al modello e verifica
    model.add_cpds(cpd_ferro, cpd_afidi, cpd_cocciniglia, cpd_sintomo)
    
    if model.check_model():
        return VariableElimination(model)
    else:
        raise ValueError("Errore nella definizione del modello Bayesiano")