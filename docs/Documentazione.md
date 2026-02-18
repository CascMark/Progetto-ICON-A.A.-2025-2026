# **"Green Leaf - Giardino intelligente" documentazione**

## Gruppo di lavoro:
- ### Marco Pio Cascella, Matr: 796170, m.cascella10@studenti.uniba.it

- ### Angelo Piccolo, Matr: 802314, a.piccolo34@studenti.uniba.it

Repository Github: https://github.com/CascMark/Progetto-ICON-A.A.-2025-2026

Progetto dell'esame di "Ingegneria della conoscenza" A.A. 2025-26

## **Introduzione**
L'idea principale al centro di "Green Leaf" è progettare un sistema capace di classificare malattie che possono presentarsi all'interno di determinate specie di piante, supportando l'utente nella loro individuazione e suggerendo efficaci consigli per cure e rimedi, permettendo di poter costruire in totale salute e semplicità il proprio giardino.

### Requisiti funzionali
- Linguaggio di programmazione del progetto: Python (3.11.9)
- IDE: Visual Studio Code (VSC)

### Librerie utilizzate
- owlready2
- pgmpy
- pyswip
- pandas
- scikit-learn
- numpy
- python-constraint 
- tkinter

### Installazione e avvio
Da decidere se creare un .bat per avviare il progetto
 
## **Sommario**
Green Leaf è un sistema basato su conoscenza (Knowledge-Based System, KBS) progettato per la diagnosi di malattie fitosanitarie e il supporto alla cura di piante da giardino e da orto. L'architettura del sistema segue un approccio ibrido, integrando tecniche di ragionamento simbolico con metodi di apprendimento automatico, al fine di garantire diagnosi accurate, interpretabili e contestualizzate.

Il componente centrale del sistema è una Knowledge Base articolata su due livelli: un livello logico-dichiarativo, implementato in Prolog, che codifica regole di diagnosi e trattamento derivate dalla letteratura agronomica (es. diagnosi('Rosa', 'Muffa_Bianca', 'Oidio')), e un livello ontologico, rappresentato tramite un'ontologia OWL, che formalizza le proprietà biologiche delle specie vegetali, come per esempio il fabbisogno di luce e umidità, rendendole interrogabili in modo strutturato.

Il KBS implementa quattro moduli specializzati che coprono i principali paradigmi dell'Intelligenza Artificiale:

- Il modulo di apprendimento supervisionato addestra un Random Forest e una rete neurale sul dataset delle osservazioni sintomatiche, restituendo una diagnosi con relativa confidenza.

- Il modulo di apprendimento non supervisionato applica l'algoritmo K-Means per profilare la pianta nel suo contesto climatico, classificandola in categorie ambientali come "Ambiente Umido" o "Ambiente Temperato".

- Il modulo probabilistico implementa una Rete Bayesiana con distribuzioni di probabilità condizionate (CPD), che permette di stimare la probabilità delle cause sottostanti dato un sintomo osservato. 

- Il modulo CSP (Constraint Satisfaction Problem) sfrutta i dati ontologici per determinare il posizionamento ottimale della pianta tra i vasi disponibili, soddisfacendo i vincoli biologici di luce e umidità.

## **Elenco argomenti di interesse**

| Sezione | Pagina |
| :--- | ---: |
| [1. Creazione del dataset](#1-creazione-del-dataset).................................................................................................................................|2|   
| [2. Creazione dell'ontologia](#2-creazione-dellontologia)...........................................................................................................................|  |   
| [3. Apprendimento non supervisionato](#3-apprendimento-non-supervisionato).....................................................................................................|  |   
| [4. Apprendimento supervisionato](#4-apprendimento-supervisionato)..............................................................................................................|  |   
| [5. Classificazione](#5-classificazione)...............................................................................................................................................|  |    

## **1. Creazione del dataset**

Il dataset utilizzato per il progetto è stato scaricato da "Kaggle" e fa riferimento a dati relativi a specie di piante, malattie contratte, colore delle foglie...

Il file si presenta sottoforma di file .csv all'interno della directory di progetto /data ed è stato analizzato per permettere un corretto preprocessing dei dati prima di essere utilizzato per il training dei modelli di apprendimento implementati.

Ecco una breve descrizione delle features presenti all'interno del dataset:

- Pianta: descrive la specie di pianta analizzata.

- Sintomo_Visibile: descrive i sintomi facilmente visibili all'occhio umano che hanno colpito la pianta.

- Diagnosi_Lab: descrive (qualora ci fosse) la patologia contratta dalla pianta.

- Umidità: descrive il livello di umidità presente nella pianta.

- Temperatura: descrive la temperatura interna della pianta.

- pH_Terreno: descrive l'acidità o la basicità del terreno in cui la pianta è situata.

- Ore_Luce: descrive il numero di ore di luce che la pianta riceve nell'arco della giornata

Nella feature "Pianta" possono comparire i seguenti valori: Pomodoro, Peperone, Rosa, Lattuga, Basilico, 

Nella feature "Sintomo_Visibile" possono comparire i seguenti valori: Nessuno, Foglie_Gialle, Foglie_Secche, Macchie_Fogliari, Muffa_Bianca

Nella feature "Diagnosi_Lab" possono comparire i seguenti valori: Nessuno, Stress_Idrico, Afidi, Oidio, Ruggine, Virosi

Nella feature "Umidità" può comparire un valore numerico positivo compreso nell'intervallo [0, 1]

Nella feature "Temperatura" può comparire un valore numerico reale (16.3 , 30.2 , ...)

Nella feature "pH_Terreno" può comparirre un valore numerico positivo compreso nell'intervallo [0, 14]

Nella feature "Ore_Luce" può comparire un valore numerico positivo compreso nell'intervallo [0, 24]

## **2. Creazione dell'ontologia**


## **3. Apprendimento non supervisionato**
## **4. Apprendimento supervisionato**
## **5 Classificazione**




