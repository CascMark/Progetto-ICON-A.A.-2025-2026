from constraint import Problem, AllDifferentConstraint

class GardenCSP:
    def __init__(self, piante_da_posizionare, ambiente_balcone, onto):
        """
        piante_da_posizionare: Lista di nomi di piante (es. ['Basilico_Genovese'])
        ambiente_balcone: Dizionario { 'Vaso_A': {'luce': 8, 'umidita': 0.5}, ... }
        onto: L'ontologia caricata con owlready2
        """
        self.problem = Problem()
        self.piante = piante_da_posizionare
        self.ambiente = ambiente_balcone
        self.onto = onto

        vasi_disponibili = list(ambiente_balcone.keys())
        
        for pianta in self.piante:
            self.problem.addVariable(pianta, vasi_disponibili)

        # VINCOLO 1: Ogni pianta in un vaso diverso
        if len(self.piante) > 1:
            self.problem.addConstraint(AllDifferentConstraint(), self.piante)

        # VINCOLO 2: Esigenze Biologiche (Luce e Umidità)
        for nome_pianta in self.piante:
            individuo_pianta = onto.search_one(iri=f"*{nome_pianta}")
            
            if individuo_pianta:
                # --- GESTIONE ROBUSTA DATI (FIX INT/LIST) ---
                req_luce = individuo_pianta.richiedeOreLuce
                target_luce = req_luce[0] if isinstance(req_luce, list) else req_luce
                
                req_umid = individuo_pianta.haLivelloUmiditaOttimale
                target_umid = req_umid[0] if isinstance(req_umid, list) else req_umid
                
                if target_luce is None: target_luce = 5
                if target_umid is None: target_umid = 0.5

                def check_bio(vaso_scelto, t_luce=target_luce, t_umid=target_umid):
                    dati_vaso = self.ambiente[vaso_scelto]
                    # Tolleranza: Accettiamo il vaso se i valori sono vicini
                    luce_ok = abs(dati_vaso['luce'] - t_luce) <= 3       
                    umid_ok = abs(dati_vaso['umidita'] - t_umid) <= 0.3 
                    return luce_ok and umid_ok

                self.problem.addConstraint(check_bio, [nome_pianta])

    def solve(self):
        """
        Restituisce la prima soluzione valida trovata.
        """
        soluzione = self.problem.getSolution()
        return soluzione