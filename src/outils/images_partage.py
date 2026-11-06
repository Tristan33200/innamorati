"""Icônes du site et image de partage de la page Couleurs (à relancer si les têtes changent). Nécessite Pillow."""
import json, os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

# Icônes : un « I » italique clair sur fond nuit, comme favicon.svg
for nom, n in (("favicon-192.png", 192), ("apple-touch-icon.png", 180)):
    im = Image.new("RGB", (n, n), "#161514"); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(SERIF_I, int(n * .62))
    d.text((n / 2, n * .53), "I", font=f, fill="#f1ede6", anchor="mm")
    im.save(os.path.join(ROOT, "src/assets", nom))

# Image de partage 1200 x 630 : les têtes du tableau des couleurs
T = json.load(open(os.path.join(ROOT, "data/tetes.json"), encoding="utf-8"))
W, H = 1200, 630
im = Image.new("RGB", (W, H), "#faf8f4"); d = ImageDraw.Draw(im)
d.text((W / 2, 92), "Les couleurs du Sacré de Birmanie", font=ImageFont.truetype(SERIF, 58), fill="#161514", anchor="mm")
d.text((W / 2, 150), "Chatterie des Innamorati · Bordeaux", font=ImageFont.truetype(SERIF_I, 28), fill="#3b5a9a", anchor="mm")
tetes = list(T.values())[:16]
c, gap = 118, 22
for k, t in enumerate(tetes):
    rang, col = divmod(k, 8)
    x = (W - (8 * c + 7 * gap)) // 2 + col * (c + gap); y = 222 + rang * (c + 44)
    t_im = Image.open(os.path.join(ROOT, "docs/photos", t["fichier"])).convert("RGB").resize((c, c), Image.LANCZOS)
    m = Image.new("L", (c * 4, c * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, c * 4 - 1, c * 4 - 1), fill=255)
    m = m.resize((c, c), Image.LANCZOS)
    d.ellipse((x - 4, y - 4, x + c + 3, y + c + 3), outline="#3b5a9a", width=2)
    im.paste(t_im, (x, y), m)
d.text((W / 2, 572), "desinnamorati.fr", font=ImageFont.truetype(SERIF_I, 26), fill="#6b665f", anchor="mm")
im.save(os.path.join(ROOT, "docs/photos/partage-couleurs.jpg"), quality=88)
print("ok")
