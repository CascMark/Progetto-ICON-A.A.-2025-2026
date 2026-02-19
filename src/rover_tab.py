import tkinter as tk
from tkinter import messagebox
import heapq
import random
import os
import pandas as pd
from datetime import datetime

# --- CONFIGURAZIONI GRIGLIA E DESIGN ---
RIGHE = 15
COLONNE = 20
DIM_CELLA = 28 

BG_SIDEBAR = "#2c3e50"    
BG_MAIN = "#ecf0f1"       
BG_GRID = "#ffffff"       
COLOR_LINE = "#bdc3c7"    
COLOR_WALL = "#7f8c8d"    
COLOR_ROBOT = "#2980b9"   
COLOR_MALATA = "#e74c3c"  
COLOR_SANA = "#2ecc71"    
COLOR_ESPLORATO = "#d1f2eb"
COLOR_PERCORSO = "#f1c40f" 
COLOR_CURATA = "#9b59b6"  
COLOR_INNAFFIATA = "#3498db" 

DIAGNOSI_CURE = {
    'Sano': '💧 Manutenzione Idrica Standard',
    'Infestazione_Afidi': '🐞 Spruzzare Olio di Neem',
    'Peronospora': '🍂 Applicare Fungicida Rameico',
    'Stress_Idrico': '🏜 Regolazione del flusso idrico',
    'Muffa_Bianca': '☁ Ridurre umidità e Fungicida sistemico',
    'Oidio': '💨 Trattamento a base di Zolfo',
    'Marciume_Apicale': '🍅 Integrazione di Calcio nel suolo',
    'Botrite': '✂ Rimozione manuale e Antibotritico',
    'Ragnetto_Rosso': '🕷 Acaricida e aumento umidità fogliare'
}

class RoverTab:
    def __init__(self, parent):
        self.parent = parent # Il Frame genitore (il Tab del Notebook)
        self.parent.configure(bg=BG_MAIN)
        
        self.dataset = self.carica_dataset()
        
        # --- LAYOUT PRINCIPALE ---
        self.sidebar = tk.Frame(self.parent, bg=BG_SIDEBAR, width=280)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False) 
        
        self.main_area = tk.Frame(self.parent, bg=BG_MAIN)
        self.main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.costruisci_sidebar()
        self.costruisci_main_area()

        self.celle = {}
        self.icone_piante = {} 
        self.sfondi_piante = {}
        self.ostacoli = set()
        self.start_iniziale = (1, 1)          
        self.robot_pos = self.start_iniziale
        self.robot_icon = None 
        self.piante_info = {} 
        self.piante_da_visitare = {}
        self.piante_fallite = set() 
        
        self.rigenera_piante() 
        self.log_terminal("Sistema Rover inizializzato. Digital Twin pronto.", "green")
        
        self.canvas.bind("<Button-1>", self.click_sinistro)
        self.canvas.bind("<B1-Motion>", self.trascina_muri)
        self.canvas.bind("<Button-3>", self.rimuovi_ostacolo)
        self.canvas.bind("<B3-Motion>", self.rimuovi_ostacolo)

    def costruisci_sidebar(self):
        # Titolo più compatto
        tk.Label(self.sidebar, text="🤖 ROVER A*", font=("Segoe UI", 18, "bold"), bg=BG_SIDEBAR, fg="#f1c40f", pady=10).pack(fill=tk.X)
        tk.Label(self.sidebar, text="Automated Planning", font=("Segoe UI", 9, "italic"), bg=BG_SIDEBAR, fg="#bdc3c7").pack(fill=tk.X)
        
        tk.Frame(self.sidebar, bg="#34495e", height=2).pack(fill=tk.X, padx=20, pady=10)
        
        # Pulsanti
        self.crea_pulsante(self.sidebar, "🚀 AVVIA MISSIONE", "#e67e22", self.avvia_missione)
        self.crea_pulsante(self.sidebar, "🔄 RIGENERA SERRA", "#27ae60", self.rigenera_piante)
        
        tk.Frame(self.sidebar, bg="#34495e", height=2).pack(fill=tk.X, padx=20, pady=10)
        
        # Controlli sintetizzati
        tk.Label(self.sidebar, text="CONTROLLI:", font=("Segoe UI", 10, "bold"), bg=BG_SIDEBAR, fg="white", anchor="w").pack(fill=tk.X, padx=20, pady=(0,5))
        istruzioni = "• Tasto SX: Muri\n• Tasto DX: Cancella\n• Click Pianta: Scheda"
        tk.Label(self.sidebar, text=istruzioni, font=("Segoe UI", 9), bg=BG_SIDEBAR, fg="#bdc3c7", justify="left", anchor="w").pack(fill=tk.X, padx=20)
        
        tk.Frame(self.sidebar, bg="#34495e", height=2).pack(fill=tk.X, padx=20, pady=10)
        
        # Legenda a Griglia 2x2 (Il trucco salvaspazio!)
        tk.Label(self.sidebar, text="LEGENDA:", font=("Segoe UI", 10, "bold"), bg=BG_SIDEBAR, fg="white", anchor="w").pack(fill=tk.X, padx=20, pady=(0,5))
        
        frame_legenda = tk.Frame(self.sidebar, bg=BG_SIDEBAR)
        frame_legenda.pack(fill=tk.X, padx=20)
        
        # Usiamo il posizionamento a griglia per affiancarli
        self.add_legenda_grid(frame_legenda, "🥀 Malata", COLOR_MALATA, 0, 0)
        self.add_legenda_grid(frame_legenda, "🌱 Sana", COLOR_SANA, 0, 1)
        self.add_legenda_grid(frame_legenda, "🤖 Rover", COLOR_ROBOT, 1, 0)
        self.add_legenda_grid(frame_legenda, "⬛ Muro", COLOR_WALL, 1, 1)

    def crea_pulsante(self, parent, text, bg_color, command):
        # Spaziature interne (pady=4) ed esterne ridotte
        btn = tk.Button(parent, text=text, bg=bg_color, fg="white", font=("Segoe UI", 10, "bold"),
                        relief=tk.FLAT, activebackground="#34495e", activeforeground="white",
                        command=command, cursor="hand2", pady=4)
        btn.pack(fill=tk.X, padx=20, pady=5)

    def add_legenda_grid(self, parent, text, color, r, c):
        # Nuova funzione per gestire la legenda a griglia invece che in lista verticale
        frame = tk.Frame(parent, bg=BG_SIDEBAR)
        frame.grid(row=r, column=c, sticky="w", padx=(0, 10), pady=4)
        tk.Canvas(frame, width=12, height=12, bg=color, highlightthickness=0).pack(side=tk.LEFT)
        tk.Label(frame, text=text, bg=BG_SIDEBAR, fg="#ecf0f1", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)

    def costruisci_main_area(self):
        # --- COLONNA CENTRALE: Mappa della Serra ---
        frame_canvas = tk.Frame(self.main_area, bg=BG_MAIN, padx=10, pady=5)
        # Usiamo side=tk.LEFT per affiancare gli elementi in orizzontale!
        frame_canvas.pack(side=tk.LEFT, anchor="n") 
        
        self.canvas = tk.Canvas(frame_canvas, width=COLONNE*DIM_CELLA, height=RIGHE*DIM_CELLA, bg=BG_GRID, highlightthickness=1, highlightbackground=COLOR_LINE)
        self.canvas.pack()
        
        # --- COLONNA DESTRA: Terminale Verticale ---
        # Senza altezza fissa, si espanderà per riempire tutto lo spazio verticale
        frame_console = tk.Frame(self.main_area, bg="#1e1e1e")
        frame_console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=20)
        
        tk.Label(frame_console, text=">_ TERMINALE MISSIONE (A*)", font=("Consolas", 10, "bold"), bg="#1e1e1e", fg="#2ecc71", anchor="w").pack(fill=tk.X, padx=10, pady=(10,5))
        
        self.terminal = tk.Text(frame_console, bg="#1e1e1e", fg="#ecf0f1", font=("Consolas", 10), relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD)
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def log_terminal(self, message, msg_type="info"):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.terminal.config(state=tk.NORMAL)
        
        color_tag = "white"
        if msg_type == "error": color_tag = "#e74c3c"
        elif msg_type == "success": color_tag = "#2ecc71"
        elif msg_type == "warning": color_tag = "#f39c12"
        elif msg_type == "action": color_tag = "#3498db"
        
        self.terminal.tag_config(msg_type, foreground=color_tag)
        self.terminal.insert(tk.END, f"{timestamp} {message}\n", msg_type)
        self.terminal.see(tk.END) 
        self.terminal.config(state=tk.DISABLED)

    def carica_dataset(self):
        # Percorso adattabile a seconda di dove includi il file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, "data", "piante_dataset.csv")
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path).to_dict('records')
        else:
            mock_data = []
            famiglie = ['Solanaceae', 'Lamiaceae', 'Rosaceae', 'Cucurbitaceae']
            diagnosi = list(DIAGNOSI_CURE.keys())
            for _ in range(50):
                d = random.choice(diagnosi)
                mock_data.append({
                    'Famiglia': random.choice(famiglie),
                    'Sintomi_Visivi': 'Nessuno' if d == 'Sano' else 'Vari',
                    'Ore_Luce': round(random.uniform(4.0, 12.0), 1),
                    'Umidita_Ottimale': round(random.uniform(0.3, 0.9), 2),
                    'Temperatura_Ottimale': round(random.uniform(15.0, 32.0), 1),
                    'PH_Suolo': round(random.uniform(5.5, 7.5), 1),
                    'Diagnosi_Reale': d
                })
            return mock_data

    def rigenera_piante(self):
        self.piante_info.clear()
        self.piante_da_visitare.clear()
        self.piante_fallite.clear() 
        self.ostacoli.clear()
        self.robot_pos = self.start_iniziale
        
        posizioni_usate = set([self.start_iniziale])
        for _ in range(6):
            r, c = random.randint(1, RIGHE-2), random.randint(1, COLONNE-2)
            while (r, c) in posizioni_usate:
                r, c = random.randint(1, RIGHE-2), random.randint(1, COLONNE-2)
            posizioni_usate.add((r, c))
            
            pianta_data = random.choice(self.dataset).copy() 
            pianta_data['Stato_Attuale'] = 'malata' if pianta_data['Diagnosi_Reale'] != 'Sano' else 'sana'
            
            self.piante_info[(r, c)] = pianta_data
            self.piante_da_visitare[(r, c)] = pianta_data['Stato_Attuale']
            
        self.disegna_griglia()
        self.log_terminal("Serra rigenerata. Nuove piante caricate dal dataset.", "action")

    def disegna_griglia(self):
        self.canvas.delete("all")
        self.icone_piante.clear()
        self.sfondi_piante.clear()
        
        for r in range(RIGHE):
            for c in range(COLONNE):
                x1, y1 = c * DIM_CELLA, r * DIM_CELLA
                x2, y2 = x1 + DIM_CELLA, y1 + DIM_CELLA
                
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=BG_GRID, outline=COLOR_LINE)
                self.celle[(r, c)] = rect
                
                if (r, c) in self.ostacoli:
                    self.canvas.itemconfig(rect, fill=COLOR_WALL, outline=COLOR_WALL)
                
                if (r, c) in self.piante_info:
                    stato = self.piante_info[(r, c)]['Stato_Attuale']
                    if stato == 'malata': color_vaso = COLOR_MALATA
                    elif stato == 'sana': color_vaso = COLOR_SANA
                    elif stato == 'curata': color_vaso = COLOR_CURATA
                    else: color_vaso = COLOR_INNAFFIATA
                    
                    pad = 2
                    vaso = self.canvas.create_oval(x1+pad, y1+pad, x2-pad, y2-pad, fill=color_vaso, outline="")
                    self.sfondi_piante[(r, c)] = vaso
                    
                    icona = "🥀" if stato == 'malata' else "🌱"
                    if stato == 'curata': icona = "🌿"
                    if stato == 'innaffiata': icona = "💧"
                    
                    text_id = self.canvas.create_text(x1+DIM_CELLA/2, y1+DIM_CELLA/2, text=icona, font=("Segoe UI Emoji", 12))
                    self.icone_piante[(r, c)] = text_id

        rx, ry = self.robot_pos[1] * DIM_CELLA, self.robot_pos[0] * DIM_CELLA
        pad = 2
        self.canvas.create_oval(rx+pad, ry+pad, rx+DIM_CELLA-pad, ry+DIM_CELLA-pad, fill=COLOR_ROBOT, outline="")
        self.robot_icon = self.canvas.create_text(rx+DIM_CELLA/2, ry+DIM_CELLA/2, text="🤖", font=("Segoe UI Emoji", 12))

    def click_sinistro(self, event):
        c, r = event.x // DIM_CELLA, event.y // DIM_CELLA
        if (r, c) in self.piante_info:
            self.mostra_scheda_tecnica(r, c)
        else:
            self.aggiungi_ostacolo(event)

    def mostra_scheda_tecnica(self, r, c):
        dati = self.piante_info[(r, c)]
        diagnosi = dati['Diagnosi_Reale']
        cura_prevista = DIAGNOSI_CURE.get(diagnosi, 'Analisi manuale')
        
        popup = tk.Toplevel(self.parent.winfo_toplevel())
        popup.title(f"Scheda Botanica - Vaso [{r+1},{c+1}]")
        popup.configure(bg=BG_MAIN)
        popup.transient(self.parent.winfo_toplevel()) 
        
        bg_color = COLOR_MALATA if dati['Stato_Attuale'] == 'malata' else COLOR_SANA
        if dati['Stato_Attuale'] == 'curata': bg_color = COLOR_CURATA
        if dati['Stato_Attuale'] == 'innaffiata': bg_color = COLOR_INNAFFIATA
        
        tk.Label(popup, text=f"🌿 Famiglia: {dati['Famiglia']}", bg=bg_color, fg="white", font=("Segoe UI", 14, "bold"), pady=15).pack(fill=tk.X)
        
        frame_dati = tk.Frame(popup, bg=BG_MAIN, padx=20, pady=15)
        frame_dati.pack(fill=tk.BOTH, expand=True)
        
        def add_info(label, value, is_alert=False, is_action=False):
            color = "#c0392b" if is_alert else "#2c3e50"
            if is_action: color = "#d35400"
            tk.Label(frame_dati, text=f"{label}:", font=("Segoe UI", 10, "bold"), bg=BG_MAIN, fg="#7f8c8d").pack(anchor="w")
            tk.Label(frame_dati, text=str(value), font=("Segoe UI", 11), bg=BG_MAIN, fg=color, justify="left", wraplength=300).pack(anchor="w", pady=(0, 12))

        add_info("Sintomi Visivi", dati['Sintomi_Visivi'], is_alert=(dati['Sintomi_Visivi'] not in ['Nessuno', 'Risolti']))
        add_info("Diagnosi IA", diagnosi, is_alert=(dati['Stato_Attuale']=='malata'))
        add_info("Protocollo Operativo", cura_prevista, is_action=True)
        add_info("Parametri Sensori (Digital Twin)", f"☀ Luce: {dati['Ore_Luce']}h\n💧 Umidità: {dati['Umidita_Ottimale']}\n🌡 Temp: {dati['Temperatura_Ottimale']}°C\n⚗ pH: {dati['PH_Suolo']}")
        add_info("Stato Attuale", dati['Stato_Attuale'].upper(), is_alert=(dati['Stato_Attuale']=='malata'))

    def aggiungi_ostacolo(self, event):
        c, r = event.x // DIM_CELLA, event.y // DIM_CELLA
        if 0 <= r < RIGHE and 0 <= c < COLONNE and (r, c) != self.robot_pos and (r, c) not in self.piante_info:
            self.ostacoli.add((r, c))
            self.canvas.itemconfig(self.celle[(r, c)], fill=COLOR_WALL, outline=COLOR_WALL)

    def trascina_muri(self, event):
        self.aggiungi_ostacolo(event)

    def rimuovi_ostacolo(self, event):
        c, r = event.x // DIM_CELLA, event.y // DIM_CELLA
        if (r, c) in self.ostacoli:
            self.ostacoli.remove((r, c))
            self.canvas.itemconfig(self.celle[(r, c)], fill=BG_GRID, outline=COLOR_LINE)

    def euristica_manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def avvia_missione(self):
        if not self.piante_da_visitare:
            messagebox.showinfo("Missione", "Nessun task in coda.", parent=self.parent.winfo_toplevel())
            return
        self.log_terminal("Inizio missione. Calcolo sequenza ottimale dei target...", "action")
        self.pianifica_prossimo_target()

    def pianifica_prossimo_target(self):
        if not self.piante_da_visitare:
            if not self.piante_fallite:
                self.log_terminal("MISSIONE COMPLETATA CON SUCCESSO. Tutte le piante sono state processate.", "success")
                messagebox.showinfo("Vittoria", "Tutte le piante curate e manutenute!", parent=self.parent.winfo_toplevel())
            else:
                msg = f"MISSIONE TERMINATA CON CRITICITA'. {len(self.piante_fallite)} vasi irraggiungibili."
                self.log_terminal(msg, "warning")
                messagebox.showwarning("Warning", msg, parent=self.parent.winfo_toplevel())
            return

        target_vicino = min(self.piante_da_visitare.keys(), key=lambda p: self.euristica_manhattan(self.robot_pos, p))
        stato_target = self.piante_da_visitare[target_vicino]
        
        azione = "Cura" if stato_target == 'malata' else "Manutenzione"
        self.log_terminal(f"Target Acquisito: Vaso [{target_vicino[0]+1}, {target_vicino[1]+1}]. Operazione: {azione}. Avvio A*...")
        self.parent.update()

        self.pulisci_scia_percorso()
        self.esegui_astar(self.robot_pos, target_vicino, stato_target)

    def pulisci_scia_percorso(self):
        for r in range(RIGHE):
            for c in range(COLONNE):
                if (r, c) not in self.ostacoli and (r, c) not in self.piante_info:
                    self.canvas.itemconfig(self.celle[(r, c)], fill=BG_GRID)

    def esegui_astar(self, start, goal, stato_target):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = { (r, c): float('inf') for r in range(RIGHE) for c in range(COLONNE) }
        g_score[start] = 0
        f_score = { (r, c): float('inf') for r in range(RIGHE) for c in range(COLONNE) }
        f_score[start] = self.euristica_manhattan(start, goal)
        
        esplorati_per_animazione = []

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                self.ricostruisci_e_anima(came_from, current, esplorati_per_animazione, goal, stato_target)
                return

            if current != start: esplorati_per_animazione.append(current)

            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]: 
                vicino = (current[0] + dr, current[1] + dc)
                if 0 <= vicino[0] < RIGHE and 0 <= vicino[1] < COLONNE and vicino not in self.ostacoli:
                    tentativo_g_score = g_score[current] + 1
                    if tentativo_g_score < g_score[vicino]:
                        came_from[vicino] = current
                        g_score[vicino] = tentativo_g_score
                        f_score[vicino] = tentativo_g_score + self.euristica_manhattan(vicino, goal)
                        if vicino not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[vicino], vicino))
                            
        self.log_terminal(f"ERRORE DI NAVIGAZIONE: Il vaso [{goal[0]+1}, {goal[1]+1}] è bloccato da ostacoli fisici!", "error")
        self.piante_fallite.add(goal) 
        del self.piante_da_visitare[goal] 
        self.parent.after(1500, self.pianifica_prossimo_target)

    def ricostruisci_e_anima(self, came_from, current, esplorati, goal, stato_target):
        percorso = []
        while current in came_from:
            current = came_from[current]
            if current != self.robot_pos: percorso.append(current)
        percorso.reverse()
        percorso.append(goal) 
        
        delay = 10
        def disegna_esplorati(index):
            if index < len(esplorati):
                nodo = esplorati[index]
                if nodo not in self.piante_info:
                    self.canvas.itemconfig(self.celle[nodo], fill=COLOR_ESPLORATO)
                self.parent.after(delay, disegna_esplorati, index + 1)
            else:
                self.log_terminal("Rotta calcolata. Inizio spostamento...")
                muovi_robot(0)
                
        def muovi_robot(index):
            if index < len(percorso):
                nodo = percorso[index]
                if nodo != goal and nodo not in self.piante_info:
                    self.canvas.itemconfig(self.celle[nodo], fill=COLOR_PERCORSO)
                
                x, y = nodo[1] * DIM_CELLA + DIM_CELLA/2, nodo[0] * DIM_CELLA + DIM_CELLA/2
                self.canvas.coords(self.robot_icon, x, y)
                self.robot_pos = nodo
                self.parent.after(100, muovi_robot, index + 1)
            else:
                self.esegui_azione_su_pianta(goal, stato_target)

        disegna_esplorati(0)

    def esegui_azione_su_pianta(self, pianta_pos, stato):
        r, c = pianta_pos[0]+1, pianta_pos[1]+1
        
        if stato == 'malata':
            self.log_terminal(f"Protocollo Eseguito: Pianta al Vaso [{r}, {c}] CURATA.", "success")
            self.canvas.itemconfig(self.sfondi_piante[pianta_pos], fill=COLOR_CURATA) 
            self.canvas.itemconfig(self.icone_piante[pianta_pos], text="🌿")
            self.piante_info[pianta_pos]['Stato_Attuale'] = 'curata'
            self.piante_info[pianta_pos]['Sintomi_Visivi'] = 'Risolti'
        else:
            self.log_terminal(f"Protocollo Eseguito: Innaffiatura Vaso [{r}, {c}] completata.", "action")
            self.canvas.itemconfig(self.sfondi_piante[pianta_pos], fill=COLOR_INNAFFIATA)
            self.canvas.itemconfig(self.icone_piante[pianta_pos], text="💧")
            self.piante_info[pianta_pos]['Stato_Attuale'] = 'innaffiata'

        del self.piante_da_visitare[pianta_pos]
        self.parent.after(1000, self.pianifica_prossimo_target)