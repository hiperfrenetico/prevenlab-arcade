"""Convierte el original de Segu Kids (OneDrive) en segu-kids/index.html publicable.

El ORIGINAL es el archivo de OneDrive: se sigue editando ahi. Este script NO lo modifica.
Uso:  python tools/build_kids.py            -> usa el Segu Kids*.html mas reciente de la carpeta Publicaciones
      python tools/build_kids.py "ruta.html" -> usa ese archivo

Ajustes que aplica: fuente Nunito propia (sin pedidos a Google), Segu en el encabezado,
titulo y datos para compartir, aviso "jugar con un adulto" y noscript.
Si el original cambia de estructura y algun ajuste no encaja, el script falla en voz alta."""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = r"D:\OneDrive\HyS\PrevenLab\Publicaciones"
BASE = "https://hiperfrenetico.github.io/prevenlab-arcade/segu-kids/"

if len(sys.argv) > 1:
    src = sys.argv[1]
else:
    cands = glob.glob(os.path.join(PUB, "Segu Kids*.html"))
    if not cands: sys.exit("No encontre ningun 'Segu Kids*.html' en " + PUB)
    src = max(cands, key=os.path.getmtime)
print("Original:", src)
html = open(src, encoding="utf-8").read()

def sub(old, new, label, count=1):
    global html
    if old not in html: sys.exit("NO ENCAJA el ajuste '%s': el original cambio de estructura." % label)
    html = html.replace(old, new, count)

# 1) head: titulo, datos para compartir y fuente propia (sin Google Fonts)
head_old = re.search(r"<title>.*?</title>\s*<link href=\"https://fonts\.googleapis\.com[^>]*>", html, re.S)
if not head_old: sys.exit("NO ENCAJA el ajuste 'head'")
head_new = f"""<title>Segu Kids · Detective de Peligros · PrevenLab Academy</title>
<meta name="description" content="Juego gratis para chicos: encontrá los peligros escondidos en la cocina, el living, la escuela, el baño y el patio. De PrevenLab Academy.">
<meta property="og:type" content="website"><meta property="og:locale" content="es_AR">
<meta property="og:title" content="Segu Kids · Detective de Peligros">
<meta property="og:description" content="¡Encontrá los peligros escondidos! Un juego gratis de PrevenLab Academy para jugar con un adulto.">
<meta property="og:url" content="{BASE}"><meta property="og:image" content="{BASE}og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/segu.svg" type="image/svg+xml">
<link rel="canonical" href="{BASE}">"""
html = html.replace(head_old.group(0), head_new, 1)
sub("<style>", "<style>\n@font-face{font-family:'Nunito';src:url(../fonts/nunito-latin.woff2) format('woff2');font-weight:600 900;font-style:normal;font-display:swap}", "font-face")

# 2) Segu en el encabezado
sub('<div class="brand">Segu<span class="kids">KIDS</span> · Detective de Peligros</div>',
    '<div class="brand"><img class="mascota" src="../assets/segu.svg" alt="Segu, el detective de peligros">'
    '<span>Segu<span class="kids">KIDS</span> · Detective de Peligros</span></div>', "brand")
sub(".brand{font-weight:900;font-size:26px}",
    ".brand{font-weight:900;font-size:26px;display:flex;align-items:center;gap:8px}"
    ".mascota{height:64px;width:auto;flex:none}"
    ".adulto{font-size:14px;font-weight:700;color:#51606f;margin:0 0 8px}", "brand css")

# 3) aviso para jugar con un adulto + noscript
sub("</header>", '</header>\n<p class="adulto">Jugá con un adulto cerca. No pide registro ni datos.</p>\n'
    '<noscript><p class="adulto">Este juego necesita JavaScript activado.</p></noscript>', "aviso")

out = os.path.join(ROOT, "segu-kids", "index.html")
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w", encoding="utf-8", newline="").write(html)
ext = sorted(set(re.findall(r"https?://(?!www\.w3\.org)[^\"' )<>]+", html)))
print("OK ->", out, "|", os.path.getsize(out) // 1024, "KB")
print("URLs externas restantes (solo deben ser metadatos de compartir):", ext)
