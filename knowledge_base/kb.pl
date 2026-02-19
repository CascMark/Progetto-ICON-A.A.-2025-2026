% =======================================================
%  KNOWLEDGE BASE PROLOG - SMART GARDEN V4.0 (Ibrida)
% =======================================================

% --- 0. ALIAS (IL PONTE TRA ML E KB) ---
% Il ML usa nomi complessi (es. Infestazione_Afidi), noi li mappiamo sui tuoi nomi semplici.
% Sintassi: map_malattia('Nome_ML', 'Nome_KB').

map_malattia('Infestazione_Afidi', 'Afidi').
map_malattia('Clorosi_Ferrica', 'Carenza_Ferro').
map_malattia('Marciume_Radicale', 'Marciume_Radicale'). 
map_malattia('Ragnetto_Rosso', 'Ragnetto_Rosso').     
map_malattia('Stress_Idrico', 'Stress_Idrico').      
map_malattia('Peronospora', 'Peronospora').
map_malattia('Oidio', 'Oidio').
map_malattia('Botrite', 'Botrite').
map_malattia('Virosi', 'Virosi').
map_malattia('Sano', 'Sano').
map_malattia(X, X). % Fallback: se non c'è mapping, usa il nome così com'è

% --- 1. REGOLE DI TRATTAMENTO (CURE) ---
% Qui c'è la tua logica originale che funziona benissimo.

trattamento('Afidi', 'Olio_di_Neem_e_Sapone_Molle').
trattamento('Carenza_Ferro', 'Somministrare_Ferro_Chelato').
trattamento('Carenza_Calcio', 'Integratore_Fogliare_Calcio').
trattamento('Peronospora', 'Trattamento_Rameico_Metallo').
trattamento('Ruggine', 'Fungicida_Rameico_o_Equiseto').
trattamento('Stress_Idrico', 'Regolare_Irrigazione_immediatamente').
trattamento('Oidio', 'Zolfo_Bagnabile_o_Bicarbonato').
trattamento('Muffa_Bianca', 'Zolfo_Bagnabile').
trattamento('Botrite', 'Fungicida_Antibotritico_Specifico').
trattamento('Virosi', 'Rimozione_Pianta_Infetta_(Incurabile)').
trattamento('Ragnetto_Rosso', 'Acaricida_Specifico_e_Umidificare').
trattamento('Marciume_Radicale', 'Sospendere_Acqua_e_Travasare').

% Casi speciali (I tuoi preferiti)
trattamento('Sano', 'Nessuna_Azione_Richiesta_-_Pianta_in_Salute').
trattamento('Nessuna', 'Monitoraggio_Preventivo').

% --- REGOLA PRINCIPALE DI CONSULTAZIONE ---
% Questa è la regola che Python chiamerà. 
% 1. Converte il nome ML nel nome KB.
% 2. Cerca il trattamento.
% 3. Se fallisce, usa il fallback dell'Agronomo.

trova_cura(MalattiaML, Cura) :-
    map_malattia(MalattiaML, MalattiaKB),
    trattamento(MalattiaKB, Cura), !. % Il 'cut' (!) ferma la ricerca se trova una corrispondenza

% Fallback (La tua regola di sicurezza)
trova_cura(_, 'Patologia_Sconosciuta_-_Consultare_Agronomo').


% --- 2. REGOLE DI DIAGNOSI LOGICA (Il Tuo Manuale Completo) ---
% Sintassi: diagnosi('Pianta', 'Sintomo', 'Malattia').
% Queste servono per verificare se il ML sta "allucinando" o è coerente.

% --- BASILICO ---
diagnosi('Basilico', 'Foglie_Gialle', 'Afidi').
diagnosi('Basilico', 'Macchie_Fogliari', 'Peronospora').
diagnosi('Basilico', 'Foglie_Arricciate', 'Stress_Idrico').

% --- POMODORO ---
diagnosi('Pomodoro', 'Macchie_Fogliari', 'Peronospora').
diagnosi('Pomodoro', 'Foglie_Gialle', 'Carenza_Ferro').
diagnosi('Pomodoro', 'Marciume_Apicale', 'Carenza_Calcio').
diagnosi('Pomodoro', 'Foglie_Arricciate', 'Virosi').

% --- LATTUGA ---
diagnosi('Lattuga', 'Foglie_Secche', 'Stress_Idrico').
diagnosi('Lattuga', 'Muffa_Bianca', 'Botrite').
diagnosi('Lattuga', 'Foglie_Gialle', 'Afidi').

% --- ROSA ---
diagnosi('Rosa', 'Muffa_Bianca', 'Oidio').
diagnosi('Rosa', 'Macchie_Fogliari', 'Ruggine').
diagnosi('Rosa', 'Ragnatele', 'Ragnetto_Rosso').

% --- PEPERONE ---
diagnosi('Peperone', 'Macchie_Fogliari', 'Virosi').
diagnosi('Peperone', 'Foglie_Arricciate', 'Afidi').

% --- FRAGOLA ---
diagnosi('Fragola', 'Muffa_Bianca', 'Botrite').
diagnosi('Fragola', 'Macchie_Fogliari', 'Ruggine').

% --- ZUCCHINA ---
diagnosi('Zucchina', 'Muffa_Bianca', 'Oidio').
diagnosi('Zucchina', 'Foglie_Gialle', 'Carenza_Nutrienti').

% --- MENTA ---
diagnosi('Menta', 'Ragnatele', 'Ragnetto_Rosso').
diagnosi('Menta', 'Macchie_Fogliari', 'Ruggine').

% Regola per verificare la diagnosi da Python
verifica_consistenza(Pianta, Sintomo, MalattiaSuggerita) :-
    diagnosi(Pianta, Sintomo, MalattiaSuggerita).