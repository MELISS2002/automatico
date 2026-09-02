# publicar_diario.ps1 - Orquestador diario del blog automatico (UltimoLive, automatico.pages.dev)
# Moderno: DeepSeek LOCAL (:8765) + imagenes REALES locales (sin Selenium, sin pollinations).
#
# FLUJO:
#   1) Verifica DeepSeek local vivo.
#   2) (Opcional) Construye el lote del dia desde noticias reales (le pasas --auto).
#      Por defecto procesa el lote_diario.json ya preparado.
#   3) Genera los articulos con crear_lote_v2.py (DeepSeek local, HTML periodistico, imgs locales).
#   4) Verifica con chequear_lote.py (0 pollinations, imgs locales, JSON).
#   5) Inyecta metadata OG + barra compartir (inject-share-meta.py + fix-og-localize.py).
#   6) Commit QUIRURGICO (solo nuevos posts + JSON + sitemap/robots + lote) + push (con reintento).
#
# USO:
#   powershell -ExecutionPolicy Bypass -File public\publicar_diario.ps1            (procesa lote_diario.json)
#   powershell -ExecutionPolicy Bypass -File public\publicar_diario.ps1 --solo "slug"   (solo un articulo)
#   powershell -ExecutionPolicy Bypass -File public\publicar_diario.ps1 --auto          (intenta armar lote desde noticias)
#
# RECOMENDADO para "crear cada dia" en Programador de tareas: ver _correr_diario.bat

$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"

$base   = "C:\Users\dza\Desktop\automatico-main"
$public = Join-Path $base "public"
$tools  = "C:\Users\dza\Desktop\neo\tools"
$python = "python"

function Write-Step([string]$msg, [string]$color = "Cyan") { Write-Host "`n==> $msg" -ForegroundColor $color }

function Test-LLM {
    try {
        $h = Invoke-RestMethod "http://127.0.0.1:8765/health" -TimeoutSec 8 -UseBasicParsing
        if ($h.ready) { Write-Step "DeepSeek local OK (model=$($h.model))" -color Green; return $true }
    } catch { }
    Write-Host "!! DeepSeek local NO responde en :8765. Inicia el stack: neo\deepseek-stack.ps1" -ForegroundColor Red
    return $false
}

function Build-LoteDiario {
    # Construye un lote_diario.json base desde los titulares reales del dia (noticias-pe).
    # NOTA: deja 'nota' vacia y 'imgs' vacia -> el usuario/comando posterior las completa
    # con imagenes reales (via news-og + dl). No publica con imagenes vacias por si solo.
    Write-Step "Generando temas del dia via noticias-pe.cjs --top 20..."
    $tmp = Join-Path $env:TEMP "noticias_pe_$(Get-Date -Format yyyyMMdd).json"
    $raw = & node (Join-Path $tools "noticias-pe.cjs") --top 20 2>&1 | Out-String
    $lote = @()
    # noticias-pe imprime titulares; armamos entradas de relleno (cat por defecto home)
    foreach ($linea in ($raw -split "`r?`n")) {
        $l = $linea.Trim()
        if ($l -and $l -notmatch "^(==|#|Fuente|Medio|[0-9]+\.)" -and $l.Length -gt 30) {
            $slug = ($l.ToLower() -replace "[^a-z0-9\s-]", "" -replace "\s+", "-").Trim("-")
            if ($slug.Length -gt 80) { $slug = $slug.Substring(0, 80).TrimEnd("-") }
            $lote += [ordered]@{ tema = $l; cat = "home"; slug = $slug; nota = ""; imgs = @() }
        }
    }
    if ($lote.Count -ge 3) {
        $lote = $lote | Select-Object -First 6
        $lote_dest = Join-Path $public "lote_diario.json"
        $lote | ConvertTo-Json -Depth 4 | Set-Content $lote_dest -Encoding UTF8
        Write-Step "Lote provisional escrito en $lote_dest ($($lote.Count) items)."
        Write-Host "  IMPORTANTE: completa 'nota' (datos reales) y 'imgs' (URLs) en lote_diario.json antes de publicar." -ForegroundColor Yellow
        return $true
    }
    Write-Host "No se pudo armar lote automatico (noticias-pe no devolvio titulares)." -ForegroundColor Yellow
    return $false
}

function Generate-Lote([string]$solo) {
    $env:PYTHONIOENCODING = "utf-8"
    $args = @((Join-Path $public "crear_lote_v2.py"))
    if ($solo) { $args += @("--slug", $solo) }
    Write-Step "Generando articulos con crear_lote_v2.py (DeepSeek local)..."
    & $python $args
    if ($LASTEXITCODE -ne 0) { throw "crear_lote_v2.py fallo (exit=$LASTEXITCODE)" }
}

function Verify-Lote([string]$solo) {
    $args = @((Join-Path $public "chequear_lote.py"))
    if ($solo) { $args += @("--slug", $solo) }
    Write-Step "Verificando posts (0 pollinations, imagenes locales, JSON)..."
    $out = & $python $args 2>&1 | Out-String
    Write-Host $out
    if ($LASTEXITCODE -ne 0 -or $out -match "HAY PROBLEMAS") {
        Write-Host "!! Verificacion con problemas. Revisa arriba." -ForegroundColor Red
        return $false
    }
    return $true
}

function Inject-Metadata {
    Write-Step "Inyectando metadata OG + barra compartir (inject-share-meta)..."
    & $python (Join-Path $tools "inject-share-meta.py") 2>&1 | Out-String | Write-Host
    # NOTA: NO se corre fix-og-localize.py aqui: procesa TODOS los posts y tarda mucho
    # (descarga og externas). El post nuevo ya queda con og:image LOCAL via inject-share-meta.
    # Correr fix-og-localize manualmente solo como mantenimiento batch puntual.
}

function Commit-Quirurgico {
    Write-Step "Commit QUIRURGICO (solo posts de este lote + JSON + sitemap/robots + lote)..."
    $lote = @()
    try { $lote = Get-Content (Join-Path $public "lote_diario.json") -Raw | ConvertFrom-Json } catch { }
    $paths = @()
    foreach ($a in $lote) { $paths += "public/posts/$($a.slug)" }
    $paths += "public/posts/home.json", "public/posts/salud.json", "public/posts/gana.json"
    $paths += "public/lote_diario.json", "public/sitemap.xml", "public/robots.txt"
    # mantener solo paths existentes (git add ignora los inexistentes)
    Set-Location $base
    foreach ($p in $paths) {
        $guarded = $p -replace '"', ''
        & git add -- "$guarded" 2>&1 | Out-Null
    }
    # items limpiados del lote que ya no existen como carpeta -> pueden quedar sin seguimiento; los omitimos.
    $staged = @(git diff --cached --name-only)
    if ($staged.Count -eq 0) {
        Write-Host "Nada nuevo para commitear." -ForegroundColor Yellow
        return $false
    }
    $msg = "Articulos diarios $(Get-Date -Format yyyy-MM-dd) ($($staged.Count) archivos)"
    & git add -u -- $paths 2>&1 | Out-Null   # actualiza borrados/renombrados dentro de lo seleccionado
    & git commit -m $msg -q
    if ($LASTEXITCODE -ne 0) { Write-Host "commit fallo"; return $false }
    # push con reintento (GitHub "Empty reply" es temporal)
    for ($i = 1; $i -le 4; $i++) {
        Write-Step "Push intento $i/4..."
        & git push 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) { Write-Step "Push OK" -color Green; return $true }
        Start-Sleep -Seconds 8
    }
    Write-Host "!! Push fallo tras 4 intentos. Revisar red/GitHub." -ForegroundColor Red
    return $false
}

function Check-Tools {
    foreach ($t in @("noticias-pe.cjs", "news-og.cjs", "dl-news-new.cjs", "inject-share-meta.py", "fix-og-localize.py")) {
        if (-not (Test-Path (Join-Path $tools $t))) { Write-Host "!! Falta herramienta: $t" -ForegroundColor Yellow }
    }
}

# ── MAIN ───────────────────────────────────────────────────────────────────
$solo = $null; $auto = $false
if ($args -contains "--solo") { $solo = $args[$args.IndexOf("--solo") + 1] }
if ($args -contains "--auto") { $auto = $true }

Write-Host "=== PUBLICADOR DIARIO UltimoLive (automatico.pages.dev) ===" -ForegroundColor Green
Check-Tools
if ($auto -and -not (Collect-DataExists)) { }
if ($auto) { $null = Build-LoteDiario }

if (-not (Test-LLM)) { exit 1 }
if (-not (Test-Path (Join-Path $public "lote_diario.json"))) {
    Write-Host "No hay lote_diario.json. Corre con --auto para armar uno, o prepara el lote manualmente." -ForegroundColor Yellow
    exit 1
}
Generate-Lote $solo
$ok = Verify-Lote $solo
if (-not $ok) { Write-Host "Detenido por verificacion. No se hara commit." -ForegroundColor Red; exit 1 }
Inject-Metadata
if (-not $solo) { $null = Commit-Quirurgico }
Write-Host "`n=== LISTO ===" -ForegroundColor Green