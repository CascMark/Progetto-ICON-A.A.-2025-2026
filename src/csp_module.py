class GardenCSP:
    def __init__(self, piante_obiettivi, posizioni_disponibili, db_onto):
        self.piante = piante_obiettivi
        self.posizioni = posizioni_disponibili
        self.db = db_onto

    def e_consistente(self, pianta, pos, assegnamento):
        # Vincolo Unario: Luce [cite: 5, 37]
        if self.db[pianta]['luce'] > self.posizioni[pos]['luce']:
            return False
        
        # Vincolo Binario: compatibileCon [cite: 4, 43]
        for p_assegnata in assegnamento:
            if p_assegnata not in self.db[pianta]['compatibili']:
                return False
        return True

    def solve(self, index=0, assegnamento=None):
        if assegnamento is None: assegnamento = {}
        if index == len(self.piante): return assegnamento
        
        pianta = self.piante[index]
        for pos in self.posizioni:
            if pos not in assegnamento.values():
                if self.e_consistente(pianta, pos, assegnamento):
                    assegnamento[pianta] = pos
                    res = self.solve(index + 1, assegnamento)
                    if res: return res
                    del assegnamento[pianta]
        return None