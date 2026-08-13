@echo off
timeout /t 3 /nobreak >nul
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --no-first-run --no-default-browser-check --user-data-dir="C:\Users\dza\.neo\chrome-debug" --new-window https://github.com/login
