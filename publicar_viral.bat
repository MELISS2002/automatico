@echo off
REM publicar_viral.bat - Boton de UN SOLO CLICK de la app viral.
REM Scrapea portales -> imagenes reales -> feed -> build -> commit -> push -> auto-deploy.
REM Uso: doble click, o:   publicar_viral.bat 20   (para mas items)
setlocal
set "PYTHONIOENCODING=utf-8"
set "BASE=C:\Users\dza\Desktop\automatico-main"
set "LOG=%USERPROFILE%\AppData\Local\Temp\opencode\publicar_viral.log"
if not exist "%USERPROFILE%\AppData\Local\Temp\opencode" mkdir "%USERPROFILE%\AppData\Local\Temp\opencode"
set "TOP=14"
if not "%1"=="" set "TOP=%1"
echo [%date% %time%] Inicio publicador viral (top=%TOP%) >> "%LOG%"
powershell -NoProfile -ExecutionPolicy Bypass -File "%BASE%\public\publicar_viral.ps1" -Top %TOP% >> "%LOG%" 2>&1
echo [%date% %time%] Fin (exit=%errorlevel%) >> "%LOG%"
echo.
echo =============================================
echo  Publicador viral terminado. Exit=%errorlevel%
echo  Log: %LOG%
echo =============================================
pause
exit /b %errorlevel%