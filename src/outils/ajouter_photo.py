"""Ajoute une photo à l'album d'un chat : python3 src/outils/ajouter_photo.py <fb> <image> <AAAA-MM-JJ> "<légende>" [--adoptant]
Version web 1400 px filigranée sans métadonnées, vignette 520 px, inscription dans data/photos_ajoutees.json. Nécessite Pillow."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ADOPTANT = "--adoptant" in sys.argv  # photo d'adoptant : pas de « © Tristan Perrier », seulement le site
fb, src, date, leg = [x for x in sys.argv[1:] if x != "--adoptant"][:4]
f_json = os.path.join(ROOT, "data/photos_ajoutees.json")
data = json.load(open(f_json, encoding="utf-8")) if os.path.exists(f_json) else {}
liste = data.setdefault(fb, [])
pid = f"ajout-{fb}-{len(liste) + 1}"
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB"); im.thumbnail((1400, 1400))
ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", 26)
t = "desinnamorati.fr" if ADOPTANT else "© Tristan Perrier · desinnamorati.fr"
d.text(((im.width - d.textlength(t, font=font)) / 2, im.height - 96), t, font=font, fill=(255, 255, 255, 140))
im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
im.save(os.path.join(ROOT, "docs/photos", pid + ".jpg"), quality=80, optimize=True, progressive=True)
th = im.copy(); th.thumbnail((520, 520)); th.save(os.path.join(ROOT, "docs/photos/t", pid + ".jpg"), quality=72, optimize=True)
liste.append({"id": pid, "src": "", "date": date, "legende": leg})
json.dump(data, open(f_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(pid)
