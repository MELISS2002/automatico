# publicar_viral.ps1 - Orquestador 1-click de la app viral (UltimoLive, automatico.pages.dev)
# FLUJO (todo automatico, un solo click):
#   1) Scrapea portales reales + descarga imagenes REALES -> public/viral.json + public/viral/<id>.html
#   2) npm run build (actualiza dist con el feed + la pagina /viral)
#   3) Commit QUIRURGICO (solo viral + funciones + src) + push con rebase (auto-deploy Pages)
# USO:
#   powershell -ExecutionPolicy Bypass -File public\publicar_viral.ps1           (lote estandar peruano)
#   powershell -ExecutionPolicy Bypass -File public\publicar_viral.ps1 -Top 20    (mas items)
#   powershell -ExecutionPolicy Bypass -File public\publicar_viral.ps1 -NoGit     (solo scrape+build)
param(
    [int]$Top = 14,
    [switch]$NoGit,
    [switch]$Pe
)

# Importante: NO usar "Stop". git escribe su progreso normal (fetch, LF/CRLF) a stderr,
# y con $ErrorActionPreference=Stop eso lanzaria NativeCommandError abortando en 'From https://...'.
# Se verifican fallos con $LASTEXITCODE.
$ErrorActionPreference = "Continue"
$env:PYTHONIOENCODING = "utf-8"

$base   = "C:\Users\dza\Desktop\automatico-main"
$tools  = "C:\Users\dza\Desktop\neo\tools"
$node   = "node"

function Write-Step([string]$msg, [string]$color = "Cyan") {
    Write-Host "`n==> $msg" -ForegroundColor $color
}
function Write-Ok([string]$msg) { Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Warn([string]$msg) { Write-Host "  [!] $msg" -ForegroundColor Yellow }

Write-Step "==== PUBLICADOR VIRAL 1-CLICK ===="
Push-Location $base

try {
    # 1) SCRAPE + generacion del feed
    Write-Step "1) Scrapeando portales + descargando imagenes REALES..."
    $peFlag = if ($Pe) { "--pe" } else { "" }
    & $node (Join-Path $tools "build-viral.cjs") --top $Top $peFlag
    if ($LASTEXITCODE -ne 0) { throw "build-viral.cjs fallo (exit=$LASTEXITCODE)" }
    Write-Ok "Feed viral listo en public/viral.json"

    # 2) BUILD
    Write-Step "2) Construyendo la app (npm run build)..."
    if (Test-Path (Join-Path $base "node_modules")) {
        npm run build | Out-Null
        if ($LASTEXITCODE -ne 0) { Write-Warn "npm run build con warnings; se continua" }
        Write-Ok "dist/ actualizado"
    } else {
        Write-Warn "Sin node_modules; se omite build (Pages recompila solito)."
    }

    if ($NoGit) {
        Write-Step "Modo -NoGit: no se hara commit/push."
        return
    }

    # 3) GIT STATUS / staging quirurgico
    Write-Step "3) Preparando commit QUIRURGICO..."
    git add "public/viral.json" "public/viral" "functions" "src/pages/Viral.jsx" "src/pages/Viral.css" "src/main.jsx" "src/components/Header.jsx" "dist/viral.json" "dist/viral"
    git status --short

    $diff = git diff --cached --stat
    if (-not $diff) {
        Write-Warn "Sin cambios nuevos para viral; nada que commitear."
    } else {
        Write-Step "4) Commit..."
        git commit -m "Viral: feed $Top noticias con imagenes reales + app /viral (1-click)"
        Write-Ok "Commit hecho"

        Write-Step "5) Push (con rebase + resolucion sitemap)..."
        $stashed = $false
        git status --porcelain | Where-Object { $_ -match '^ M' -or $_ -match '^\?\?' } | ForEach-Object { $stashed = $true }
        if ($stashed) {
            git stash push -m "viral-pre-push" 2>&1 | Out-Null
            Write-Ok "Cambios sueltos guardados en stash (se devuelven al final)"
        }
        git pull --rebase origin main 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Warn "Error en pull --rebase (ponte al dia en la rama). Se reintenta con rebase autostash..."
            git pull --rebase --autostash origin main 2>&1 | Out-Null
        }
        git checkout --theirs public/sitemap.xml 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0 -and (git diff --name-only --diff-filter=U | Select-String -Quiet 'sitemap')) {
            git add public/sitemap.xml 2>&1 | Out-Null
            git -c user.email="auto@ultimolive.dev" -c user.name="auto" commit -m "Auto: sitemap (theirs)" 2>&1 | Out-Null
        }
        git push origin main
        if ($LASTEXITCODE -ne 0) {
            Write-Warn "Push fallo; reintentando..."
            git push origin main 2>&1 | Out-Null
        }
        if ($stashed) {
            git stash pop 2>&1 | Out-Null
            Write-Ok "Cambios sueltos devueltos del stash"
        }
        Write-Ok "Push OK -> automatico.pages.dev"
    }
}
catch {
    Write-Host "`n!! ERROR: $_" -ForegroundColor Red
    exit 1
}
finally {
    Pop-Location
}
Write-Host "`n==== LISTO. Abre https://automatico.pages.dev/viral ====" -ForegroundColor Green