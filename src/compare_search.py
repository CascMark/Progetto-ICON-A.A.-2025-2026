import heapq
import time
import os
import matplotlib.pyplot as plt

# --- CONFIGURAZIONE AMBIENTE ---
RIGHE = 15
COLONNE = 20
START = (1, 1)
GOAL = (13, 18)

OSTACOLI = set()
for r in range(4, 13):
    OSTACOLI.add((r, 10))
for c in range(4, 11):
    OSTACOLI.add((4, c))

# --- MOTORE DI RICERCA ---
def euristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def esegui_ricerca(usa_euristica=True):
    open_set = []
    heapq.heappush(open_set, (0, START))
    came_from = {}
    
    g_score = { (r, c): float('inf') for r in range(RIGHE) for c in range(COLONNE) }
    g_score[START] = 0
    
    nodi_espansi = 0
    start_time = time.perf_counter()

    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == GOAL:
            path_len = 0
            while current in came_from:
                current = came_from[current]
                path_len += 1
            exec_time = (time.perf_counter() - start_time) * 1000 
            return nodi_espansi, path_len, exec_time

        if current != START:
            nodi_espansi += 1

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            vicino = (current[0] + dr, current[1] + dc)
            
            if 0 <= vicino[0] < RIGHE and 0 <= vicino[1] < COLONNE and vicino not in OSTACOLI:
                tentativo_g_score = g_score[current] + 1
                
                if tentativo_g_score < g_score.get(vicino, float('inf')):
                    came_from[vicino] = current
                    g_score[vicino] = tentativo_g_score
                    
                    h_score = euristica_manhattan(vicino, GOAL) if usa_euristica else 0
                    f_score = tentativo_g_score + h_score
                    
                    if vicino not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score, vicino))
                        
    return nodi_espansi, 0, 0 # Fallimento

# --- ESECUZIONE TEST ---
print("Avvio simulazione Dijkstra (Ricerca Cieca)...")
nodi_dijkstra, path_dijkstra, time_dijkstra = esegui_ricerca(usa_euristica=False)

print("Avvio simulazione A* (Ricerca Informata)...")
nodi_astar, path_astar, time_astar = esegui_ricerca(usa_euristica=True)

# --- GENERAZIONE GRAFICO ---
labels = ['Nodi Espansi (Memoria)', 'Tempo di Esecuzione (ms)']
dijkstra_stats = [nodi_dijkstra, time_dijkstra * 10] 
astar_stats = [nodi_astar, time_astar * 10]

x = range(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 6))
rects1 = ax.bar([i - width/2 for i in x], dijkstra_stats, width, label='Dijkstra (Senza Euristica)', color='#e74c3c')
rects2 = ax.bar([i + width/2 for i in x], astar_stats, width, label='A* (Euristica Manhattan)', color='#2ecc71')

ax.set_ylabel('Quantità (Minore è meglio)')
ax.set_title('Confronto Performance Algoritmi di Navigazione\n(Lunghezza Percorso Ottimale Trovato: {} passi per entrambi)'.format(path_astar))
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_path = os.path.join(base_dir, 'plots', 'confronto_astar_dijkstra.png')
os.makedirs(os.path.dirname(save_path), exist_ok=True)
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"\nGrafico salvato con successo in: {save_path}")

plt.show()