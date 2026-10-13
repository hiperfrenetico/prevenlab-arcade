"""Genera las imagenes para compartir (og:image, 1200x630) de los juegos SEGU.
Uso: python tools/make_og.py   (desde la raiz del repo)
Requiere: Pillow y resvg_py. Usa assets/segu.svg y fuentes de Windows (Impact / Arial Bold)."""
import io, os
from PIL import Image, ImageDraw, ImageFont
import resvg_py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = r"C:\Windows\Fonts"
IMPACT = os.path.join(FONTS, "impact.ttf")
BOLD = os.path.join(FONTS, "arialbd.ttf")

def segu_img(h):
    svg = open(os.path.join(ROOT, "assets", "segu.svg"), encoding="utf-8").read()
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg, height=h))
    return Image.open(io.BytesIO(png)).convert("RGBA")

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def card(path, bg, fg, accent, tag, title, sub, badge):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    # franja de peligro arriba
    for x in range(-40, W + 40, 60):
        d.polygon([(x, 0), (x + 30, 0), (x + 10, 26), (x - 20, 26)], fill=accent)
    s = segu_img(470)
    im.paste(s, (W - s.width - 30, H - s.height - 10), s)
    f_tag = ImageFont.truetype(BOLD, 30)
    f_title = ImageFont.truetype(IMPACT, 80)
    f_sub = ImageFont.truetype(BOLD, 36)
    f_badge = ImageFont.truetype(BOLD, 32)
    x = 64
    d.text((x, 62), tag.upper(), font=f_tag, fill=accent)
    y = 118
    for line in wrap(d, title.upper(), f_title, 640):
        d.text((x, y), line, font=f_title, fill=fg); y += 90
    y += 14
    for line in wrap(d, sub, f_sub, 680):
        d.text((x, y), line, font=f_sub, fill=fg); y += 46
    bw = d.textlength(badge, font=f_badge) + 56
    d.rounded_rectangle((x, H - 100, x + bw, H - 40), radius=30, fill=accent)
    d.text((x + 28, H - 92), badge, font=f_badge, fill=bg)
    im.save(path, "JPEG", quality=86, optimize=True)
    print(path, os.path.getsize(path) // 1024, "KB")

card(os.path.join(ROOT, "segu-tension", "og.jpg"), "#101215", "#f3f1ec", "#F5A623",
     "SEGU Adultos · PrevenLab Academy", "¿Sabés qué EPP usar con tensión?",
     "De 220 V a 132 kV: elegí guantes, pértiga y taburete correctos.", "Jugá gratis")
card(os.path.join(ROOT, "segu-kids", "og.jpg"), "#FFC400", "#1f2a37", "#1f2a37",
     "SEGU Kids · PrevenLab Academy", "Detective de peligros",
     "¡Encontrá los peligros escondidos en la cocina, el patio y la escuela!", "Jugá gratis")
card(os.path.join(ROOT, "og.jpg"), "#101215", "#f3f1ec", "#F5A623",
     "PrevenLab Academy", "SEGU: juegos de seguridad",
     "Adultos y Kids. Aprendé jugando a prevenir.", "Jugá gratis")
