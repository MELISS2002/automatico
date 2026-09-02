@echo off
REM _correr_diario.bat - Launcher del publicador diario (para Programador de tareas de Windows).
REM Ejecuta el orquestador publicar_diario.ps1 sobre el lote_diario.json preparado.
REM Log completo en %USERPROFILE%\AppData\Local\Temp\opencode\publicar_diario.log
setlocal
set "PYTHONIOENCODING=utf-8"
set "BASE=C:\Users\dza\Desktop\automatico-main"
set "LOG=%USERPROFILE%\AppData\Local\Temp\opencode\publicar_diario.log"
if not exist "%USERPROFILE%\AppData\Local\Temp\opencode" mkdir "%USERPROFILE%\AppData\Local\Temp\opencode"
echo [%date% %time%] Inicio publicador diario >> "%LOG%"
powershell -NoProfile -ExecutionPolicy Bypass -File "%BASE%\public\publicar_diario.ps1" >> "%LOG%" 2>&1
echo [%date% %time%] Fin (exit=%errorlevel%) >> "%LOG%"
exit /b %errorlevel%