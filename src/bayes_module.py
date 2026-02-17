from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def crea_rete_diagnosi():
    # Modello: Carenza_Ferro, Afidi e Cocciniglia causano Foglie_Gialle [cite: 22, 26, 27]
    model = DiscreteBayesianNetwork([
        ('Carenza_Ferro', 'Foglie_Gialle'),
        ('Afidi', 'Foglie_Gialle'),
        ('Cocciniglia', 'Foglie_Gialle')
    ])

    # Definizione probabilità (CPT) basate su frequenze osservate
    cpd_ferro = TabularCPD(variable='Carenza_Ferro', variable_card=2, values=[[0.8], [0.2]])
    cpd_afidi = TabularCPD(variable='Afidi', variable_card=2, values=[[0.85], [0.15]])
    cpd_cocciniglia = TabularCPD(variable='Cocciniglia', variable_card=2, values=[[0.9], [0.1]])

    cpd_sintomo = TabularCPD(
        variable='Foglie_Gialle', variable_card=2,
        values=[
            [0.99, 0.40, 0.30, 0.10, 0.20, 0.05, 0.05, 0.01], # False
            [0.01, 0.60, 0.70, 0.90, 0.80, 0.95, 0.95, 0.99]  # True
        ],
        evidence=['Carenza_Ferro', 'Afidi', 'Cocciniglia'],
        evidence_card=[2, 2, 2]
    )

    model.add_cpds(cpd_ferro, cpd_afidi, cpd_cocciniglia, cpd_sintomo)
    return VariableElimination(model)