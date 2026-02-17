from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def crea_rete_diagnosi():
    """
    Costruisce una Rete Bayesiana COMPLETA per il giardino.
    Copre 4 scenari principali:
    1. Giallo -> Carenza o Afidi
    2. Macchie -> Peronospora o Ruggine
    3. Secco -> Stress Idrico
    4. Bianco -> Oidio (Muffa)
    """
    # 1. Definizione Struttura (Grafo)
    model = DiscreteBayesianNetwork([
        # Ramo Foglie Gialle
        ('Carenza_Ferro', 'Foglie_Gialle'),
        ('Afidi', 'Foglie_Gialle'),
        
        # Ramo Macchie
        ('Peronospora', 'Macchie_Fogliari'),
        ('Ruggine', 'Macchie_Fogliari'),
        
        # Ramo Secco
        ('Stress_Idrico', 'Foglie_Secche'),
        
        # Ramo Muffa
        ('Oidio', 'Muffa_Bianca')
    ])

    # 2. Probabilità a Priori (Le cause esistono nel giardino?)
    # Valori bassi (0.1/0.2) perché le malattie non sono sempre presenti
    cpd_ferro = TabularCPD(variable='Carenza_Ferro', variable_card=2, values=[[0.8], [0.2]])
    cpd_afidi = TabularCPD(variable='Afidi', variable_card=2, values=[[0.7], [0.3]])
    
    cpd_perono = TabularCPD(variable='Peronospora', variable_card=2, values=[[0.8], [0.2]])
    cpd_ruggine = TabularCPD(variable='Ruggine', variable_card=2, values=[[0.9], [0.1]])
    
    cpd_stress = TabularCPD(variable='Stress_Idrico', variable_card=2, values=[[0.6], [0.4]]) # Più comune
    
    cpd_oidio = TabularCPD(variable='Oidio', variable_card=2, values=[[0.8], [0.2]])

    # 3. Probabilità Condizionate (Se ho la malattia, quanto è probabile il sintomo?)
    
    # Sintomo: Foglie_Gialle (Dipende da Ferro e Afidi)
    cpd_giallo = TabularCPD(
        variable='Foglie_Gialle', variable_card=2,
        values=[
            [0.99, 0.40, 0.30, 0.05], # False (Sintomo assente)
            [0.01, 0.60, 0.70, 0.95]  # True (Sintomo presente)
        ],
        evidence=['Carenza_Ferro', 'Afidi'], evidence_card=[2, 2]
    )

    # Sintomo: Macchie_Fogliari (Dipende da Peronospora e Ruggine)
    cpd_macchie = TabularCPD(
        variable='Macchie_Fogliari', variable_card=2,
        values=[
            [0.99, 0.30, 0.40, 0.05], 
            [0.01, 0.70, 0.60, 0.95]  
        ],
        evidence=['Peronospora', 'Ruggine'], evidence_card=[2, 2]
    )

    # Sintomo: Foglie_Secche (Dipende da Stress_Idrico)
    cpd_secche = TabularCPD(
        variable='Foglie_Secche', variable_card=2,
        values=[[0.95, 0.10], [0.05, 0.90]], # Se c'è stress, 90% foglie secche
        evidence=['Stress_Idrico'], evidence_card=[2]
    )

    # Sintomo: Muffa_Bianca (Dipende da Oidio)
    cpd_bianca = TabularCPD(
        variable='Muffa_Bianca', variable_card=2,
        values=[[0.99, 0.05], [0.01, 0.95]], # Oidio causa quasi sempre muffa bianca
        evidence=['Oidio'], evidence_card=[2]
    )

    # 4. Aggiunta al modello
    model.add_cpds(cpd_ferro, cpd_afidi, cpd_perono, cpd_ruggine, cpd_stress, cpd_oidio,
                   cpd_giallo, cpd_macchie, cpd_secche, cpd_bianca)
    
    if model.check_model():
        return VariableElimination(model)
    else:
        raise ValueError("Errore nella definizione della Rete Bayesiana Completa")