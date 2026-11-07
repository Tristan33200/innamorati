#!/usr/bin/env python3
"""Génère le site de la Chatterie des Innamorati dans docs/.

Sources : data/catalogue.json (export Facebook), data/config.json (classement),
photos/ (versions web filigranées) et src/assets/.
Usage : python3 src/build.py
"""
import html, json, os, re, shutil, datetime, posixpath
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
CAT = json.load(open(os.path.join(ROOT, "data/catalogue.json"), encoding="utf-8"))
CAT += json.load(open(os.path.join(ROOT, "data/albums_ajoutes.json"), encoding="utf-8"))  # chats sans album Facebook
_AJ = json.load(open(os.path.join(ROOT, "data/photos_ajoutees.json"), encoding="utf-8"))  # photos envoyées hors Facebook
import hashlib
_v = lambda *fs: hashlib.md5(b"".join(open(os.path.join(ROOT, "src/assets", f), "rb").read() for f in fs)).hexdigest()[:8]
VER_CSS, VER_JS = _v("style.css", "motion.css"), _v("site.js")  # le navigateur recharge le style dès qu'il change
CFG = json.load(open(os.path.join(ROOT, "data/config.json"), encoding="utf-8"))
_RETIREES = set(CFG.get("photos_retirees", []))  # photos à ne pas publier (radios, etc.)
for _a in CAT:
    _a["photos"] = [p for p in _a["photos"] + _AJ.get(_a["fb"], []) if p["id"] not in _RETIREES]
    if _a["cover"] in _RETIREES and _a["photos"]: _a["cover"] = _a["photos"][0]["id"]
COULEURS_FR = COULEURS = json.load(open(os.path.join(ROOT, "data/couleurs.json"), encoding="utf-8"))
COULEURS_EN = json.load(open(os.path.join(ROOT, "data/couleurs_en.json"), encoding="utf-8"))
SIRET = "829 118 769 00019"
EMAIL = "innamoraticats@tristanperrier.fr"
# Adresse publique du site : le domaine du fichier CNAME s'il existe, sinon GitHub Pages
_cname = os.path.join(ROOT, "docs", "CNAME")
SITE = ("https://" + open(_cname).read().strip() + "/") if os.path.exists(_cname) else "https://tristan33200.github.io/innamorati/"
PLAN = []  # pages pour sitemap.xml : (chemin, priorité)
e = html.escape
MOIS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MOIS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MOIS = MOIS_FR

# ---------- Langues ----------
# Le site est généré deux fois : en français à la racine, en anglais sous /en/ avec des adresses en anglais.
L = "fr"


def T(fr, en):
    """Texte dans la langue de la page en cours."""
    return en if L == "en" else fr


CHEMINS_EN = {"chatons": "kittens", "nos-chats": "our-cats", "portees": "litters", "ils-ont-grandi": "grown-up",
              "expositions": "cat-shows", "le-birman": "birman-cat", "couleurs": "birman-cat-colors", "adopter": "adopt",
              "contact": "contact", "mentions-legales": "legal-notice", "chat": "cat", "merci": "thank-you"}


def chemin_en(c):
    """Adresse anglaise d'une page : "chat/x/" devient "en/cat/x/"."""
    parts = [x for x in c.split("/") if x]
    parts = [CHEMINS_EN.get(p, p) if i == 0 or parts[0] == "contact" else p for i, p in enumerate(parts)]
    return "en/" + "".join(p + "/" for p in parts)


def chemin_l(c):
    """Chemin d'une page (donné en français) dans la langue en cours, avec / final."""
    c = c.strip("/") + "/" if c.strip("/") else ""
    return chemin_en(c) if L == "en" else c


def lien(c):
    """Adresse complète d'une page (chemin français) dans la langue en cours."""
    return SITE + chemin_l(c)


def date_fr(iso, jour=True):
    d = datetime.date.fromisoformat(iso)
    if L == "en":
        return f"{MOIS_EN[d.month-1]} {d.day}, {d.year}" if jour else f"{MOIS_EN[d.month-1]} {d.year}"
    return f"{d.day} {MOIS[d.month-1]} {d.year}" if jour else f"{MOIS[d.month-1]} {d.year}"


def rb(robe):
    """Nom de la robe affiché : « Chocolat » devient « Chocolate » en anglais."""
    return re.sub(r"\b([Cc])hocolat\b", r"\1hocolate", robe) if L == "en" else robe


STATUTS_EN = {"adopté": "adopted", "adoptée": "adopted", "reste à la maison": "stays with us", "reste à la mais": "stays with us",
              "réservé": "reserved", "réservée": "reserved", "option de l'élevage": "breeder's option", "option": "breeder's option",
              "adoptée retraitée": "retired and adopted", "retraitée à 2 ans et 3 mois": "retired at 2 years and 3 months",
              "pré-réservée": "pre-reserved", "pré-réservé": "pre-reserved", "à adopter": "available", "à réserver": "available",
              "Championne Internationale FIFe": "FIFe International Champion"}
NOTES_EN = {"Retraitée en famille": "Retired to a loving family", "Retraitée, stérilisée, vit à la maison": "Retired, spayed, lives with us",
            "Retraité, stérilisé, vit à la maison": "Retired, neutered, lives with us",
            "Retraitée, stérilisée, rejoint bientôt sa famille adoptive": "Retired, spayed, soon joining her adoptive family",
            "Retraité, stérilisé, placé en famille. Décédé le 11 décembre 2018": "Retired, neutered, rehomed with a loving family. Passed away on December 11, 2018"}


def titre_en(t):
    m = re.match(r"^Portées? (.+?) (\d{4})$", t)
    if m: return f'{m.group(1).replace(" et ", " and ")} litter{"s" if t.startswith("Portées") else ""}, {m.group(2)}'
    t = re.sub(r"^(\d{4}-\d\d-\d\d) à (\d+)", r"\1 & \2", t)
    for fr, en in (("Exposition de beauté du chat", "Cat show"), ("Exposition de beauté chats", "Cat show"), ("Exposition de beauté féline", "Cat show"),
                   ("Exposition International à", "International cat show in"), ("Exposition Paris Animal Show", "Paris Animal Show"),
                   ("Exposition à ", "Cat show in "), ("exposition Rome", "Cat show, Rome"), ("Salon du chat", "Cat show"),
                   ("(jour ", "(day "), ("Italie", "Italy"), ("Espagne", "Spain")):
        t = t.replace(fr, en)
    return t


def langue(l):
    """Bascule les textes des albums (sexe, statut, notes, titres de portée) dans la langue l."""
    global L, MOIS, COULEURS
    L = l
    MOIS = MOIS_EN if l == "en" else MOIS_FR
    COULEURS = COULEURS_EN if l == "en" else COULEURS_FR
    for a in albums:
        f = a.setdefault("fr", {k: a[k] for k in ("sexe", "statut", "note", "titre")})
        a["statut_fr"] = f["statut"]
        if l == "fr":
            a.update(f)
        else:
            a["sexe"] = {"Mâle": "Male", "Femelle": "Female"}.get(f["sexe"], f["sexe"])
            a["statut"] = STATUTS_EN.get(f["statut"], f["statut"])
            a["note"] = NOTES_EN.get(f["note"], f["note"])
            a["titre"] = titre_en(f["titre"]) if a["type"] in ("portee", "expo") else f["titre"]


# ---------- Lecture des albums ----------
def clean(text):
    text = re.sub(r"@\[\d+:\d+:([^\]]+)\]", r"\1", text or "")
    text = re.sub(r"[\U0001F300-\U0001FAFF☀-➿️‍]", "", text)
    return text.strip()


def nom_affiche(nom):
    n = re.sub(r"\(.*?\)", "", nom)
    n = re.sub(r"[\U0001F300-\U0001FAFF☀-➿️]", "", n).replace('"', "").strip()
    n = re.sub(r"\binnamorati\b", "Innamorati", n)
    return re.sub(r"\s+", " ", n)


def statut_fb(nom):
    m = re.findall(r"\(([^)]*)\)", nom)
    st = m[-1].strip() if m else ""
    return re.sub(r"(?i)^reste à la mais$", lambda x: x.group(0) + "on", st)  # nom d'album Facebook tronqué


ROBES = [  # motif dans la description -> nom affiché
    (r"seal smoke tortie", "Seal smoke tortie point"), (r"blue smoke tortie|bleu smoke tortie", "Blue smoke tortie point"),
    (r"chocolat silver tabby", "Chocolat silver tabby point"), (r"lilac silver tabby", "Lilac silver tabby point"),
    (r"(bleu|blue) silver tabby", "Blue silver tabby point"), (r"seal silver tabby", "Seal silver tabby point"),
    (r"chocolat tortie tabby", "Chocolat tortie tabby point"), (r"seal tortie tabby", "Seal tortie tabby point"),
    (r"chocolat tortie", "Chocolat tortie point"), (r"seal tortie", "Seal tortie point"),
    (r"seal tabby", "Seal tabby point"), (r"(bleu|blue) tabby", "Blue tabby point"), (r"chocolat tabby", "Chocolat tabby point"),
    (r"lilac tabby", "Lilac tabby point"), (r"red tabby", "Red tabby point"), (r"cream tabby", "Cream tabby point"),
    (r"seal point", "Seal point"), (r"(bleu|blue) point", "Blue point"), (r"chocolat point", "Chocolat point"),
    (r"lilac point", "Lilac point"), (r"red point", "Red point"), (r"cream point", "Cream point"),
]


def robe_de(txt):
    t = txt.lower()
    for motif, nom in ROBES:
        if re.search(motif + r"\s+point", t) or (motif.endswith("point") and re.search(motif, t)):
            return nom
    return ""


def parents_de(desc):
    for ligne in desc.splitlines():
        if "💘" in ligne:
            g, d = [clean(x) for x in ligne.split("💘", 1)]
            g = re.split(r"\)\s+|\s{2,}", g)[-1]
            d = re.split(r"\s{2,}|\s+(?=(Mâle|Male|Femelle)\b)", d)[0]
            nettoie = lambda x: re.sub(r"^(IC|GIC|SC|CH|NW)\s*-\s*", "", x).strip()
            return nettoie(g), nettoie(d)
    return "", ""


def cle_nom(n):
    n = n.lower().replace("’", "'").replace("backkara", "bacckara").replace("œ", "oe")
    n = re.sub(r"\s+aka\s+\S+", "", n)
    n = n.replace("real sugar daddy", "sugar daddy")
    n = n.replace("s*easy love's crush", "crush").replace("mia bella des innamorati", "mia bella de la tribu birmane")  # même chat, deux graphies
    return re.sub(r"\s+", " ", n).strip()


albums = []
for a in CAT:
    nom = a["nom"]
    texte = a["description"] + "\n" + "\n".join(p["legende"] for p in a["photos"][:3])
    photos = sorted([p for p in a["photos"]], key=lambda p: p["date"])
    sexe = "Mâle" if re.search(r"\bm[âa]le\b", texte, re.I) else ("Femelle" if re.search(r"\bfemelle\b", texte, re.I) else "")
    mere, pere = parents_de(a["description"])
    albums.append(dict(fb=a["fb"], slug=a["slug"], nom=nom, titre=nom_affiche(nom), statut=statut_fb(nom),
                       description=clean(a["description"]), photos=photos, cover=a["cover"], robe=robe_de(texte),
                       sexe=sexe, mere=mere, pere=pere, debut=photos[0]["date"], fin=photos[-1]["date"]))
BY = {a["fb"]: a for a in albums}

S = lambda k: set(CFG.get(k, []))
for a in albums:
    fb, n = a["fb"], a["nom"]
    if fb in S("masques"): a["type"] = "masque"
    elif fb in S("reproductrices"): a["type"] = "repro"
    elif fb in S("retraites_maison"): a["type"] = "retraite"
    elif fb in S("anciennes_reproductrices"): a["type"] = "ancienne"
    elif fb in S("anciens_males"): a["type"] = "male"
    elif fb in S("chatons_disponibles"): a["type"] = "chaton"
    elif n.startswith("Portée"): a["type"] = "portee"
    elif re.match(r"\d{4}-\d{2}-\d{2}", n): a["type"] = "expo"
    else: a["type"] = "grandi"
    if fb in CFG.get("statuts", {}): a["statut"] = CFG["statuts"][fb]
    a["note"] = CFG["notes"].get(fb, "")
    a["titres"] = CFG["titres"].get(fb, "")
    a["ne"] = CFG.get("naissances", {}).get(fb, "")
    if fb in CFG.get("parents", {}): a["mere"], a["pere"] = CFG["parents"][fb]  # parents absents des textes Facebook
    a["url"] = ("expositions/" if a["type"] == "expo" else "chat/") + a["slug"] + "/"

chats = [a for a in albums if a["type"] not in ("masque", "expo", "portee")]
age = lambda a: a["ne"] or a["debut"]

# Palmarès : résultats d'expositions relevés dans les dossiers de l'élevage
PALM = {}
for _r in json.load(open(os.path.join(ROOT, "data/palmares.json"), encoding="utf-8")):
    if _r["fb"]: PALM.setdefault(_r["fb"], []).append(_r)
MOIS_C = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
MOIS_C_EN = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def palmares(fb):
    lst = sorted(PALM.get(fb, []), key=lambda x: x["date"], reverse=True)
    if not lst: return ""
    wk = {(x["lieu"], x["date"][:7]) for x in lst}
    nbis = sum(1 for x in lst if "BIS" in x["res"] or "BEST" in x["res"])
    nbob = sum(1 for x in lst if "BOB" in x["res"])
    resume = T(f'{len(wk)} exposition{"s" if len(wk) > 1 else ""} · {len(lst)} jugement{"s" if len(lst) > 1 else ""}',
               f'{len(wk)} show{"s" if len(wk) > 1 else ""} · {len(lst)} judging{"s" if len(lst) > 1 else ""}')
    if nbis: resume += f' · {nbis} Best in Show'
    if nbob: resume += f' · {nbob} Best of Best'
    ans = OrderedDict()
    for x in lst: ans.setdefault(x["date"][:4], []).append(x)
    def res(t):
        t = e(t).replace(" + ", " · ")
        return re.sub(r"\b(BIS|BEST(?: x?\d)?|BOB(?: [0-9]\S*)?)", r"<b>\1</b>", t)
    blocs = "".join(f'<div class="pl-an"><h3>{an}</h3><ul>' + "".join(
        f'<li><time datetime="{x["date"]}">{T(str(int(x["date"][8:])) + " " + MOIS_C[int(x["date"][5:7]) - 1], MOIS_C_EN[int(x["date"][5:7]) - 1] + " " + str(int(x["date"][8:])))}</time><span>{e(x["lieu"])}</span><em>{res(x["res"])}</em></li>' for x in l)
        + '</ul></div>' for an, l in ans.items())
    return (f'<div class="pl"><div class="litter"><h2>{T("Palmarès", "Show results")}</h2><span>{resume}</span></div><div class="pl-ans">{blocs}</div>'
            + T('<p class="abbr pl-abbr">EXC Excellent (classement) · CAC, CACIB, CAGCIB, CACS certificats de champion, champion international, grand champion international et suprême · CAP, CAPIB, CAGPIB, CAPS équivalents pour les chats stérilisés · '
            'BIV meilleur de la variété · NOM nommé pour le Best in Show · BIS Best in Show · BOB Best of Best, le meilleur de toute l’exposition</p></div>',
            '<p class="abbr pl-abbr">EXC Excellent (placing) · CAC, CACIB, CAGCIB, CACS certificates for Champion, International Champion, Grand International Champion and Supreme Champion · CAP, CAPIB, CAGPIB, CAPS the same for neutered cats · '
            'BIV Best in Variety · NOM nominated for Best in Show · BIS Best in Show · BOB Best of Best, the best cat of the whole show</p></div>'))
NOMS = {}
for a in chats:
    NOMS[a["titre"].lower()] = a
    court = re.sub(r"\s+(aka|dite?)\s+.*?(?=\s+des\s+innamorati|$)", "", a["titre"], flags=re.I)
    NOMS[court.lower()] = a


def lien_chat(nom, r):
    """Renvoie le nom, avec un lien vers sa page si on a son album."""
    cle = cle_nom(nom)
    for k, a in NOMS.items():
        if cle_nom(k) == cle or (len(cle) > 6 and cle_nom(k).startswith(cle)):
            return f'<a href="{r}{a["url"]}">{e(nom)}</a>'
    return e(nom)


# ---------- Gabarit ----------
NAV_G = [("chatons/", "Chatons", "Kittens"), ("nos-chats/", "Nos chats", "Our cats"), ("portees/", "Portées", "Litters"), ("ils-ont-grandi/", "Ils ont grandi", "All grown up")]
NAV_D = [("expositions/", "Expositions", "Cat shows"), ("le-birman/", "Le Birman", "The Birman"), ("couleurs/", "Couleurs", "Colors"), ("adopter/", "Adopter", "Adopt")]
NAV_PLUS = [("contact/", "Contact", "Contact")]
NAV_PIED = [("adopter/#verifier", "Vérifier une annonce", "Check an ad"), ("mentions-legales/", "Mentions légales", "Legal notice")]


def vers_en(doc, chemin):
    """Réécrit les liens relatifs d'une page française pour sa version anglaise (adresses absolues sous /en/)."""
    base = "/" + (chemin.strip("/") + "/" if chemin.strip("/") else "")

    def un(u):
        if re.match(r"^(https?:|mailto:|tel:|data:|#|//|/)", u): return u
        m = re.match(r"^([^?#]*)(.*)$", u)
        p, reste = m.groups()
        cible = posixpath.normpath(posixpath.join(base, p)) if p else base.rstrip("/") or "/"
        if cible.startswith(("/photos/", "/assets/")) or re.search(r"\.(jpg|png|svg|css|js|txt|xml|pdf)$", cible):
            return cible + reste
        return "/" + chemin_en(cible.strip("/")) + reste

    doc = re.sub(r'(href|src)="([^"]*)"', lambda m: f'{m.group(1)}="{un(m.group(2))}"', doc)
    return re.sub(r'srcset="([^"]*)"', lambda m: 'srcset="' + ", ".join(
        " ".join([un(x.strip().split(" ")[0])] + x.strip().split(" ")[1:]) for x in m.group(1).split(",")) + '"', doc)


def taille_jpeg(chemin):
    """Largeur et hauteur d'un JPEG, sans bibliothèque externe."""
    try:
        with open(chemin, "rb") as f:
            f.read(2)
            while True:
                m = f.read(2)
                if len(m) < 2 or m[0] != 0xFF: return None
                n = int.from_bytes(f.read(2), "big")
                if 0xC0 <= m[1] <= 0xCF and m[1] not in (0xC4, 0xC8, 0xCC):
                    f.read(1); h = int.from_bytes(f.read(2), "big"); w = int.from_bytes(f.read(2), "big")
                    return w, h
                f.seek(n - 2, 1)
    except OSError:
        return None


POLICES = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap"


def page(chemin, titre, corps, desc="", sombre_entete=False, image=None, ld=None, prio=None, og_type="website", image_alt="", indexer=True):
    profondeur = len([x for x in chemin.split("/") if x])
    r = "../" * profondeur
    url_fr = SITE + (chemin.strip("/") + "/" if chemin else "")
    url_en = SITE + chemin_en(chemin)
    _m = re.search(r'<img src="([^"]+)"(?: srcset="([^"]+)" sizes="([^"]+)")?[^>]*fetchpriority="high"', corps)
    precharge = (f'<link rel="preload" as="image" href="{_m.group(1)}"' + (f' imagesrcset="{_m.group(2)}" imagesizes="{_m.group(3)}"' if _m.group(2) else "") + ' fetchpriority="high">\n') if _m else ""
    url = url_en if L == "en" else url_fr
    desc = desc or T("Chatterie des Innamorati, élevage familial de Sacrés de Birmanie à Bordeaux.", "Chatterie des Innamorati, a family-run Birman cat cattery in Bordeaux, France.")
    if indexer: PLAN.append((url, prio if prio is not None else (0.5 if profondeur > 1 else 0.7), url_fr, url_en))
    blocs_ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (ld or []))
    nav = lambda items: "".join(f'<a href="{r}{u}">{T(f, en)}</a>' for u, f, en in items)
    autre = ("/" + chemin.strip("/") + "/" if chemin.strip("/") else "/") if L == "en" else "/" + chemin_en(chemin)
    bascule = T(f'<a class="lang" href="{autre}" hreflang="en" lang="en" title="English version">EN</a>',
                f'<a class="lang" href="{autre}" hreflang="fr" lang="fr" title="Version française">FR</a>')
    locale = T('<meta property="og:locale" content="fr_FR"><meta property="og:locale:alternate" content="en_US"><meta property="og:locale:alternate" content="en_GB">',
               '<meta property="og:locale" content="en_US"><meta property="og:locale:alternate" content="en_GB"><meta property="og:locale:alternate" content="fr_FR">')
    alternates = (f'<link rel="alternate" hreflang="fr" href="{url_fr}"><link rel="alternate" hreflang="en" href="{url_en}">'
                  f'<link rel="alternate" hreflang="x-default" href="{url_fr}">') if indexer else ""
    tagline = T("Sacrés de Birmanie · Bordeaux", "Birman cats · Bordeaux, France")
    entete = "top over" if sombre_entete else "top"
    meta_img = ""
    image = image or "2084329241748221"  # par défaut : le regard saphir de l'accueil
    if image:
        dim = taille_jpeg(os.path.join(OUT, "photos", image + ".jpg"))
        alt = e(image_alt or titre)
        meta_img = (f'<meta property="og:image" content="{SITE}photos/{image}.jpg"><meta property="og:image:type" content="image/jpeg">'
                    + (f'<meta property="og:image:width" content="{dim[0]}"><meta property="og:image:height" content="{dim[1]}">' if dim else "")
                    + f'<meta property="og:image:alt" content="{alt}"><meta name="twitter:image" content="{SITE}photos/{image}.jpg"><meta name="twitter:image:alt" content="{alt}">\n')
    robots = "index, follow, max-image-preview:large, max-snippet:-1" if indexer else "noindex, follow"
    doc = f"""<!doctype html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titre)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">{alternates}
<meta name="author" content="Chatterie des Innamorati"><meta name="theme-color" content="#161514">
<meta property="og:type" content="{og_type}">{locale}<meta property="og:site_name" content="Chatterie des Innamorati">
<meta property="og:title" content="{e(titre)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
{meta_img}<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(titre)}"><meta name="twitter:description" content="{e(desc)}">
{blocs_ld}
{precharge}<noscript><link rel="stylesheet" href="{r}assets/fonts.css"></noscript>
<link rel="stylesheet" href="{r}assets/style.css?v={VER_CSS}">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="{r}assets/favicon-192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">
</head>
<body>
<header class="{entete}"><div class="wrap">
  <nav class="g" aria-label="{T("Rubriques", "Sections")}">{nav(NAV_G)}</nav>
  <a class="logo" href="{r}"><b>des Innamorati</b><small>{tagline}</small></a>
  <nav class="d" aria-label="{T("Rubriques", "Sections")}">{nav(NAV_D)}</nav>
  <button class="burger" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  {bascule}
</div>
<nav class="menu" id="menu" hidden aria-label="Menu">{nav(NAV_G + NAV_D + NAV_PLUS)}{bascule.replace('class="lang"', 'class="lang-m"').replace(">EN<", ">English<").replace(">FR<", ">Français<")}</nav>
</header>
<main>
{corps}
</main>
<footer><div class="wrap">
  <a class="logo" href="{r}"><b>des Innamorati</b><small>{tagline}</small></a>
  <nav class="foot">{nav(NAV_G + NAV_D + NAV_PLUS + NAV_PIED)}{bascule.replace('class="lang"', '').replace(">EN<", ">English<").replace(">FR<", ">Français<")}</nav>
  <p class="fine">{T("Affixe LOOF « des Innamorati »", "LOOF-registered cattery name « des Innamorati »")} · Magali Perrier, SIRET {SIRET}<br>{T("Photographies", "Photographs")} © <a href="https://tristanperrier.fr" target="_blank" rel="noopener">Tristan Perrier</a>. {T("Toute reproduction est interdite.", "All rights reserved, no reproduction.")}</p>
</div></footer>
<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="{T("Photo agrandie", "Enlarged photo")}">
  <button type="button" class="lb-x" aria-label="{T("Fermer", "Close")}">{T("Fermer", "Close")}</button>
  <button type="button" class="lb-p" aria-label="{T("Photo précédente", "Previous photo")}">‹</button>
  <figure><div class="lb-img"><img alt=""></div><figcaption></figcaption></figure>
  <button type="button" class="lb-n" aria-label="{T("Photo suivante", "Next photo")}">›</button>
</div>
<script src="{r}assets/site.js?v={VER_JS}"></script>
</body>
</html>"""
    if L == "en":
        doc = vers_en(doc, chemin)
        chemin = chemin_en(chemin).rstrip("/")
    dest = os.path.join(OUT, chemin, "index.html") if chemin else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(doc)


def faq(titre, items, label=None):
    """Bloc de questions dépliables + données structurées FAQPage pour Google."""
    label = label or T("Questions fréquentes", "Frequently asked questions")
    q = "".join(f"<details><summary>{e(a)}</summary><p>{b}</p></details>" for a, b in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", b)}} for a, b in items]}
    return f'<section class="faq"><div class="wrap narrow"><div class="head"><p class="label">{label}</p><h2>{titre}</h2></div>{q}</div></section>', ld


def ariane(*etapes):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": lien(u)} for i, (n, u) in enumerate(etapes)]}


def slug_robe(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


CADRAGE = json.load(open(os.path.join(ROOT, "data/cadrages.json"), encoding="utf-8"))  # centre du visage (yeux bleus)


def img(r, pid, alt, cls="", grand=False, attrs=""):
    """Vignette nette : la version 1400 px est proposée aux écrans qui en ont besoin, cadrée sur le visage."""
    src = f"{r}photos/{pid}.jpg" if grand else f"{r}photos/t/{pid}.jpg"
    jeu = "" if grand else f' srcset="{r}photos/t/{pid}.jpg 520w, {r}photos/{pid}.jpg 1400w" sizes="(max-width: 760px) 170px, (max-width: 1000px) 33vw, 25vw"'
    pos = f' style="object-position:{CADRAGE[pid][0]}% {CADRAGE[pid][1]}%"' if pid in CADRAGE else ""
    return f'<div class="ph {cls}"><img src="{src}"{jeu} alt="{e(alt)}" loading="lazy" decoding="async"{pos} {attrs}></div>'


def carte(r, a, extra=""):
    lignes = []
    if a["titres"]: lignes.append(f'<span class="titles">{e(a["titres"])}</span>')
    lignes.append(f'<h3>{e(a["titre"])}</h3>')
    infos = " · ".join(x for x in [a["sexe"], rb(a["robe"]).lower() if a["robe"] else ""] if x)
    if infos: lignes.append(f'<span class="robe">{e(infos[0].upper() + infos[1:])}</span>')
    if a["note"]: lignes.append(f'<span class="robe">{e(a["note"])}</span>')
    lignes.append(extra)
    return f'<a class="card" href="{r}{a["url"]}">{img(r, a["cover"], a["titre"])}<div class="t">{"".join(lignes)}</div></a>'


def tete(label, titre, texte=""):
    return f'<div class="head"><p class="label">{label}</p><h1>{titre}</h1>{f"<p>{texte}</p>" if texte else ""}</div>'


def legende(a, p):
    if L == "en": return date_fr(p["date"])  # légendes Facebook en français : seule la date en anglais
    leg = clean(p["legende"])
    if a["titre"].lower()[:12] in leg.lower() or leg == clean(a["description"]): leg = ""
    return date_fr(p["date"]) + (" · " + leg[:300].replace("\n", " ") if leg else "")


def jeu_photo(r, pid):
    """srcset 520 / 900 / 1400 px ; la version 900 px (téléphones) est créée au besoin à partir de la photo filigranée."""
    m = os.path.join(OUT, "photos", "m", pid + ".jpg")
    if not os.path.exists(m):
        try:
            from PIL import Image
            im = Image.open(os.path.join(OUT, "photos", pid + ".jpg"))
            if im.width > 1000:
                os.makedirs(os.path.dirname(m), exist_ok=True)
                im.convert("RGB").resize((900, round(im.height * 900 / im.width)), Image.LANCZOS).save(m, quality=78, optimize=True, progressive=True)
        except Exception:
            pass
    moyen = f", {r}photos/m/{pid}.jpg 900w" if os.path.exists(m) else ""
    return f"{r}photos/t/{pid}.jpg 520w{moyen}, {r}photos/{pid}.jpg 1400w"


def apercu(pid):
    """Aperçu flou minuscule (environ 1 Ko) affiché instantanément sous la grande photo du haut, le temps qu'elle arrive."""
    try:
        import base64, io
        from PIL import Image, ImageFilter
        im = Image.open(os.path.join(OUT, "photos", "t", pid + ".jpg")).convert("RGB")
        im = im.resize((24, max(1, round(im.height * 24 / im.width))), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1))
        b = io.BytesIO(); im.save(b, "JPEG", quality=45)
        return ' style="background:#2b2724 url(data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode() + ') center/cover"'
    except Exception:
        return ' style="background:#2b2724"'


def entete_album(r, a, titre, sur, sous):
    """Grande photo de couverture plein écran, titre par-dessus (parallaxe)."""
    return (f'<div class="hero album-hero"><div class="ph"{apercu(a["cover"])}><img src="{r}photos/{a["cover"]}.jpg" srcset="{jeu_photo(r, a["cover"])}" sizes="100vw" alt="{e(a["titre"])}" fetchpriority="high"></div>'
            f'<div class="wrap"><p class="crumb">{sur}</p><h1>{e(titre)}</h1><p>{sous}</p></div></div>')


FILM_MIN = 10**6  # défilé horizontal abandonné (nov. 2026) : galerie en colonnes pour tous les albums


def film(r, a, n=10):
    if len(a["photos"]) < FILM_MIN: return ""
    items = "".join(f'<a class="g-item f-item" href="{r}photos/{p["id"]}.jpg" data-cap="{e(legende(a, p))}">'
                    f'<div class="ph"><img src="{r}photos/{p["id"]}.jpg" alt="{e(a["titre"])}, {date_fr(p["date"])}" loading="lazy" decoding="async"></div>'
                    f'<span class="f-n">{i + 1:02d}</span></a>' for i, p in enumerate(a["photos"][:n]))
    return f'<div class="film"><div class="film-pin"><div class="film-track">{items}</div></div></div>'


def dims(pid):
    d = taille_jpeg(os.path.join(OUT, "photos", "t", pid + ".jpg"))
    return f' width="{d[0]}" height="{d[1]}"' if d else ""


def galerie(r, a):
    figs = []
    debut = min(10, len(a["photos"])) if len(a["photos"]) >= FILM_MIN else 0
    for p in a["photos"][debut:]:
        cap = legende(a, p)
        figs.append(f'<a class="g-item" href="{r}photos/{p["id"]}.jpg" data-cap="{e(cap)}">'
                    f'<div class="ph"><img data-src="{r}photos/t/{p["id"]}.jpg"{dims(p["id"])} data-srcset="{r}photos/t/{p["id"]}.jpg 520w, {r}photos/{p["id"]}.jpg 1400w" sizes="(max-width: 700px) 170px, 33vw" alt="{e(a["titre"])}, {date_fr(p["date"])}" loading="lazy" decoding="async"></div></a>')
    return f'<div class="gallery">{"".join(figs)}</div>' if figs else ""


# ---------- Préparation de docs/ ----------
if os.path.isdir(OUT):
    for x in os.listdir(OUT):
        if x in ("photos", "CNAME"): continue
        p = os.path.join(OUT, x)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(OUT, exist_ok=True)
shutil.copytree(os.path.join(ROOT, "src/assets"), os.path.join(OUT, "assets"), ignore=shutil.ignore_patterns("motion.css"))
# Une seule feuille de style (une requête de moins avant l'affichage)
with open(os.path.join(OUT, "assets/style.css"), "a", encoding="utf-8") as _f:
    _f.write("\n" + open(os.path.join(ROOT, "src/assets/motion.css"), encoding="utf-8").read())
open(os.path.join(OUT, ".nojekyll"), "w").close()

# ---------- Pages, en français puis en anglais ----------
for L in ("fr", "en"):
    langue(L)
    exec(open(os.path.join(ROOT, "src/pages.py"), encoding="utf-8").read())
    exec(open(os.path.join(ROOT, "src/pages_fixes.py"), encoding="utf-8").read())
# Plan du site pour Google
aujourdhui = datetime.date.today().isoformat()
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "".join(f'<url><loc>{u}</loc><xhtml:link rel="alternate" hreflang="fr" href="{fr}"/><xhtml:link rel="alternate" hreflang="en" href="{en}"/>'
              f'<xhtml:link rel="alternate" hreflang="x-default" href="{fr}"/><lastmod>{aujourdhui}</lastmod><priority>{p}</priority></url>\n' for u, p, fr, en in PLAN)
    + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
print(f"OK : {len(chats)} chats, {len(grandis)} anciens chatons, {len(litters)} portées, {len(expos)} expositions")
