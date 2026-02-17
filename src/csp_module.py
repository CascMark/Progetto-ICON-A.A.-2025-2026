import owlready2 as owl

# Funzione helper per estrarre i dati puliti dall'Ontologia
def estrai_dati_piante_da_onto(onto):
    database_piante = {}
    # Cerca tutte le sottoclassi di Pianta o individui
    # Qui cerchiamo gli individui diretti
    piante = onto.search(type=onto.Pianta)
    
    for p in piante:
        # Gestione sicura delle liste di Owlready2
        luce = p.richiedeOreLuce[0] if p.richiedeOreLuce else 0
        umidita = p.haLivelloUmiditaOttimale[0] if p.haLivelloUmiditaOttimale else 0.0
        compatibili = [c.name for c in p.compatibileCon]
        
        database_piante[p.name] = {
            "luce": luce,
            "umidita": umidita,
            "compatibili": compatibili
        }
    return database_piante

class GardenCSP:
    def __init__(self, piante_da_posizionare, posizioni_disponibili, ontologia_caricata):
        """
        :param piante_da_posizionare: Lista di nomi (IRI) delle piante (es. ['Basilico_Genovese'])
        :param posizioni_disponibili: Dizionario { 'Pos_A': {'luce': 8, ...} }
        :param ontologia_caricata: L'oggetto 'onto' di owlready2
        """
        self.piante = piante_da_posizionare
        self.posizioni_nomi = list(posizioni_disponibili.keys())
        self.posizioni_dati = posizioni_disponibili
        # Estraiamo i vincoli (Luce/Umidità/Compatibilità) dalla KB
        self.db_vincoli = estrai_dati_piante_da_onto(ontologia_caricata)

    def e_consistente(self, pianta, pos_nome, assegnamento):
        # Se la pianta non è nell'ontologia (es. nome errato nel CSV), non possiamo piazzarla
        if pianta not in self.db_vincoli:
            print(f"Warning: {pianta} non trovata nell'Ontologia CSP.")
            return False

        req_pianta = self.db_vincoli[pianta]
        dati_pos = self.posizioni_dati[pos_nome]

        # 1. VINCOLO UNARIO: Luce e Umidità
        # Tolleranza di 2 ore di luce e 0.2 di umidità
        if req_pianta['luce'] > dati_pos['luce'] + 2: 
            return False
        if abs(req_pianta['umidita'] - dati_pos['umidita']) > 0.3:
            return False

        # 2. VINCOLO BINARIO: Compatibilità con i vicini
        # (Semplificazione: tutti nel giardino sono "vicini" in questo esempio)
        for p_gia_piazzata in assegnamento:
            if p_gia_piazzata not in req_pianta['compatibili']:
                # Se NON sono esplicitamente compatibili, fallisce
                return False
        
        return True

    def solve(self, index=0, assegnamento=None):
        if assegnamento is None: assegnamento = {}
        
        # Caso base: tutte le piante sono state assegnate
        if index == len(self.piante):
            return assegnamento

        pianta_corrente = self.piante[index]
        
        # Prova tutte le posizioni nel dominio
        for pos in self.posizioni_nomi:
            # Vincolo: Una pianta per posizione (alldifferent)
            if pos not in assegnamento.values():
                if self.e_consistente(pianta_corrente, pos, assegnamento):
                    assegnamento[pianta_corrente] = pos
                    
                    # Passo ricorsivo
                    risultato = self.solve(index + 1, assegnamento)
                    if risultato: 
                        return risultato
                    
                    # Backtracking
                    del assegnamento[pianta_corrente]
        
        return None