@echo off
REM _correr_diario.bat - UN SOLO lanzador "todo-en-uno" del blog automatico (UltimoLive).
REM Ejecuta en secuencia:
REM   1) FEED VIRAL  : viralapp\publicar_viral.ps1  (scraper RSS -> app /viral, siempre corre)
REM   2) BLOG DIARIO : public\publicar_diario.ps1    (articulos con DeepSeek local, solo si :8765 vivo)
REM Un solo bat = un solo click/programador. Log en %USERPROFILE%\AppData\Local\Temp\opencode\publicar_diario.log
setlocal
set "PYTHONIOENCODING=utf-8"
set "BASE=C:\Users\dza\Desktop\automatico-main"
set "LOG=%USERPROFILE%\AppData\Local\Temp\opencode\publicar_diario.log"
if not exist "%USERPROFILE%\AppData\Local\Temp\opencode" mkdir "%USERPROFILE%\AppData\Local\Temp\opencode"

echo [%date% %time%] INICIO publicador UNIFICADO (viral + diario) >> "%LOG%"

echo.
echo ============================================
echo  PASO 1/2 - FEED VIRAL (app /viral)
echo ============================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%BASE%\viralapp\publicar_viral.ps1" >> "%LOG%" 2>&1
set "VIRAL_EXIT=%errorlevel%"
echo   Viral exit=%VIRAL_EXIT% >> "%LOG%"

echo.
echo ============================================
echo  PASO 2/2 - BLOG DIARIO (DeepSeek local)
echo ============================================
REM El motor diario comprueba por si solo si DeepSeek :8765 esta vivo y aborta si no.
powershell -NoProfile -ExecutionPolicy Bypass -File "%BASE%\public\publicar_diario.ps1" >> "%LOG%" 2>&1
set "DIARIO_EXIT=%errorlevel%"
echo   Diario exit=%DIARIO_EXIT% >> "%LOG%"

echo.
echo =============================================
echo  TODO EN UNO terminado. Viral=%VIRAL_EXIT% Diario=%DIARIO_EXIT%
echo  Log: %LOG%
echo =============================================
echo [%date% %time%] FIN publicador unificado (viral=%VIRAL_EXIT% diario=%DIARIO_EXIT%) >> "%LOG%"
if not defined SILENT pause
exit /b %VIRAL_EXIT%