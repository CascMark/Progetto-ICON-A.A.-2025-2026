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

        # Variabili: Le piante
        # Dominio: I vasi disponibili (es. 'Vaso_A', 'Vaso_B')
        vasi_disponibili = list(ambiente_balcone.keys())
        
        # Aggiungiamo le variabili al problema
        for pianta in self.piante:
            self.problem.addVariable(pianta, vasi_disponibili)

        # VINCOLO 1: Ogni pianta in un vaso diverso
        # Correzione: Usiamo AllDifferentConstraint() e passiamo la lista delle variabili come secondo argomento
        if len(self.piante) > 1:
            self.problem.addConstraint(AllDifferentConstraint(), self.piante)

        # VINCOLO 2: Esigenze Biologiche (Luce e Umidità)
        for nome_pianta in self.piante:
            # Cerchiamo la pianta nell'ontologia
            individuo_pianta = onto.search_one(iri=f"*{nome_pianta}")
            
            if individuo_pianta:
                # --- GESTIONE ROBUSTA DATI (FIX INT/LIST) ---
                # Recuperiamo Luce
                req_luce = individuo_pianta.richiedeOreLuce
                # Se è una lista (vecchio owlready), prendiamo il primo elemento. Se è un numero, lo usiamo così com'è.
                target_luce = req_luce[0] if isinstance(req_luce, list) else req_luce
                
                # Recuperiamo Umidità
                req_umid = individuo_pianta.haLivelloUmiditaOttimale
                target_umid = req_umid[0] if isinstance(req_umid, list) else req_umid
                
                # Valori di default se mancano nell'ontologia
                if target_luce is None: target_luce = 5
                if target_umid is None: target_umid = 0.5

                # Definiamo la funzione di controllo (closure)
                # Serve per "congelare" i valori di target_luce e target_umid per questa specifica pianta
                def check_bio(vaso_scelto, t_luce=target_luce, t_umid=target_umid):
                    dati_vaso = self.ambiente[vaso_scelto]
                    # Tolleranza: Accettiamo il vaso se i valori sono vicini
                    luce_ok = abs(dati_vaso['luce'] - t_luce) <= 3       # Tolleranza +/- 3 ore
                    umid_ok = abs(dati_vaso['umidita'] - t_umid) <= 0.3  # Tolleranza +/- 30%
                    return luce_ok and umid_ok

                # Aggiungiamo il vincolo unario (solo su questa variabile)
                self.problem.addConstraint(check_bio, [nome_pianta])

    def solve(self):
        """
        Restituisce la prima soluzione valida trovata.
        """
        soluzione = self.problem.getSolution()
        return soluzione