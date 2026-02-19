@echo off
cd /d "%~dp0"

echo ============================================
echo          GREEN LEAF - Avvio Sistema
echo ============================================

:: Controllo presenza Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRORE] Python non trovato. Assicurati che Python sia installato e nel PATH.
    pause
    exit /b 1
)

:: Controllo presenza requirements.txt
if not exist requirements.txt (
    echo [ERRORE] File requirements.txt non trovato.
    pause
    exit /b 1
)

:: Installazione dipendenze solo se necessario
echo [1/2] Verifica dipendenze in corso...
pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo [ERRORE] Installazione dipendenze fallita.
    pause
    exit /b 1
)

echo [SUCCESSO] Dipendenze verificate.

:: Avvio programma
echo [2/2] Avvio Green Leaf...
echo ============================================
python src/main.py

if %errorlevel% neq 0 (
    echo [ERRORE] Il programma si e' chiuso con un errore.
)

pause