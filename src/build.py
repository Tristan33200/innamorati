#!/usr/bin/env python3
"""Génère le site de la Chatterie des Innamorati dans docs/.

Sources : data/catalogue.json (export Facebook), data/config.json (classement),
photos/ (versions web filigranées) et src/assets/.
Usage : python3 src/build.py
"""
import html, json, os, re, shutil, datetime
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
CAT = json.load(open(os.path.join(ROOT, "data/catalogue.json"), encoding="utf-8"))
CFG = json.load(open(os.path.join(ROOT, "data/config.json"), encoding="utf-8"))
COULEURS = json.load(open(os.path.join(ROOT, "data/couleurs.json"), encoding="utf-8"))
SIRET = "829 118 769 00019"
e = html.escape
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def date_fr(iso, jour=True):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {MOIS[d.month-1]} {d.year}" if jour else f"{MOIS[d.month-1]} {d.year}"


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
    return m[-1].strip() if m else ""


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
    a["note"] = CFG["notes"].get(fb, "")
    a["titres"] = CFG["titres"].get(fb, "")
    a["url"] = ("expositions/" if a["type"] == "expo" else "chat/") + a["slug"] + "/"

chats = [a for a in albums if a["type"] not in ("masque", "expo", "portee")]
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
NAV_G = [("chatons/", "Chatons"), ("nos-chats/", "Nos chats"), ("portees/", "Portées"), ("ils-ont-grandi/", "Ils ont grandi")]
NAV_D = [("expositions/", "Expositions"), ("le-birman/", "Le Birman"), ("couleurs/", "Couleurs"), ("adopter/", "Adopter")]


def page(chemin, titre, corps, desc="", sombre_entete=False, image=None):
    profondeur = len([x for x in chemin.split("/") if x])
    r = "../" * profondeur
    nav = lambda items: "".join(f'<a href="{r}{u}">{t}</a>' for u, t in items)
    entete = "top over" if sombre_entete else "top"
    meta_img = f'<meta property="og:image" content="{r}photos/{image}.jpg">' if image else ""
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titre)}</title>
<meta name="description" content="{e(desc or 'Chatterie des Innamorati, élevage familial de Sacrés de Birmanie à Bordeaux.')}">
{meta_img}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap">
<link rel="stylesheet" href="{r}assets/style.css">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
</head>
<body>
<header class="{entete}"><div class="wrap">
  <nav class="g" aria-label="Rubriques">{nav(NAV_G)}</nav>
  <a class="logo" href="{r}"><b>des Innamorati</b><small>Sacrés de Birmanie · Bordeaux</small></a>
  <nav class="d" aria-label="Rubriques">{nav(NAV_D)}</nav>
  <button class="burger" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
</div>
<nav class="menu" id="menu" hidden aria-label="Menu">{nav(NAV_G + NAV_D + [("contact/", "Contact")])}</nav>
</header>
<main>
{corps}
</main>
<footer><div class="wrap">
  <a class="logo" href="{r}"><b>des Innamorati</b><small>Sacrés de Birmanie · Bordeaux</small></a>
  <nav class="foot">{nav(NAV_G + NAV_D + [("contact/", "Contact"), ("adopter/#verifier", "Vérifier une annonce"), ("mentions-legales/", "Mentions légales")])}</nav>
  <p class="fine">Affixe LOOF « des Innamorati » · Magali Perrier, SIRET {SIRET}<br>Photographies © Tristan Perrier. Toute reproduction est interdite.</p>
</div></footer>
<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Photo agrandie">
  <button type="button" class="lb-x" aria-label="Fermer">Fermer</button>
  <button type="button" class="lb-p" aria-label="Photo précédente">‹</button>
  <figure><div class="lb-img"><img alt=""></div><figcaption></figcaption></figure>
  <button type="button" class="lb-n" aria-label="Photo suivante">›</button>
</div>
<script src="{r}assets/site.js"></script>
</body>
</html>"""
    dest = os.path.join(OUT, chemin, "index.html") if chemin else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(doc)


def img(r, pid, alt, cls="", grand=False, attrs=""):
    src = f"{r}photos/{pid}.jpg" if grand else f"{r}photos/t/{pid}.jpg"
    return f'<div class="ph {cls}"><img src="{src}" alt="{e(alt)}" loading="lazy" {attrs}></div>'


def carte(r, a, extra=""):
    lignes = []
    if a["titres"]: lignes.append(f'<span class="titles">{e(a["titres"])}</span>')
    lignes.append(f'<h3>{e(a["titre"])}</h3>')
    infos = " · ".join(x for x in [a["sexe"], a["robe"].lower() if a["robe"] else ""] if x)
    if infos: lignes.append(f'<span class="robe">{e(infos[0].upper() + infos[1:])}</span>')
    if a["note"]: lignes.append(f'<span class="robe">{e(a["note"])}</span>')
    lignes.append(extra)
    return f'<a class="card" href="{r}{a["url"]}">{img(r, a["cover"], a["titre"])}<div class="t">{"".join(lignes)}</div></a>'


def tete(label, titre, texte=""):
    return f'<div class="head"><p class="label">{label}</p><h1>{titre}</h1>{f"<p>{texte}</p>" if texte else ""}</div>'


def galerie(r, a):
    figs = []
    for p in a["photos"]:
        leg = clean(p["legende"])
        if a["titre"].lower()[:12] in leg.lower() or leg == clean(a["description"]): leg = ""
        cap = date_fr(p["date"]) + (" · " + leg[:300].replace("\n", " ") if leg else "")
        figs.append(f'<a class="g-item" href="{r}photos/{p["id"]}.jpg" data-cap="{e(cap)}">'
                    f'<div class="ph"><img src="{r}photos/t/{p["id"]}.jpg" alt="{e(a["titre"])}, {date_fr(p["date"])}" loading="lazy"></div></a>')
    return f'<div class="gallery">{"".join(figs)}</div>'


# ---------- Préparation de docs/ ----------
if os.path.isdir(OUT):
    for x in os.listdir(OUT):
        if x in ("photos", "CNAME"): continue
        p = os.path.join(OUT, x)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(OUT, exist_ok=True)
shutil.copytree(os.path.join(ROOT, "src/assets"), os.path.join(OUT, "assets"))
open(os.path.join(OUT, ".nojekyll"), "w").close()

# ---------- Pages chat (une par album) ----------
for a in chats + [x for x in albums if x["type"] == "portee"]:
    r = "../../"
    faits = []
    if a["sexe"] or a["robe"]: faits.append(("Robe", " · ".join(x for x in [a["sexe"], a["robe"]] if x)))
    if a["mere"]: faits.append(("Parents", f'{lien_chat(a["mere"], r)} × {lien_chat(a["pere"], r)}'))
    if a["titres"]: faits.append(("Titres", e(a["titres"])))
    statut = a["note"] or (a["statut"][:1].upper() + a["statut"][1:] if a["statut"] else "")
    if statut: faits.append(("Statut", e(statut)))
    faits.append(("Album", f'{len(a["photos"])} photos, de {date_fr(a["debut"], False)} à {date_fr(a["fin"], False)}'))
    fhtml = "".join(f'<div><span class="label">{k}</span><span>{v}</span></div>' for k, v in faits)
    rubrique = {"repro": ("Nos reproductrices", "nos-chats/"), "retraite": ("Nos retraités", "nos-chats/"), "ancienne": ("Nos anciennes reproductrices", "nos-chats/"),
                "male": ("Nos anciens reproducteurs", "nos-chats/"), "chaton": ("Nos chatons", "chatons/"), "portee": ("Nos portées", "portees/"),
                "grandi": ("Ils ont grandi", "ils-ont-grandi/")}[a["type"]]
    corps = f"""<section class="album-page"><div class="wrap">
<p class="crumb"><a href="{r}{rubrique[1]}">{rubrique[0]}</a></p>
<div class="head"><h1>{e(a["titre"])}</h1><div class="facts">{fhtml}</div></div>
{galerie(r, a)}
<p class="prot">Photos réduites et marquées. Elles appartiennent à la Chatterie des Innamorati et ne peuvent pas être reprises dans une annonce.</p>
</div></section>"""
    page(a["url"].rstrip("/"), f'{a["titre"]} · Chatterie des Innamorati', corps,
         desc=f'{a["titre"]}, Sacré de Birmanie de la Chatterie des Innamorati. {a["robe"]}.', image=a["cover"])

# ---------- Portées (regroupement des chatons par parents et par année) ----------
litters = OrderedDict()
for a in sorted([x for x in chats if x["type"] in ("grandi", "chaton") or (x["mere"] and x["fb"] not in S("anciens_males"))], key=lambda x: x["debut"]):
    if not a["mere"] and a["type"] not in ("grandi", "chaton"): continue
    an = a["debut"][:4]
    cle = (cle_nom(a["mere"]), cle_nom(a["pere"]), an) if a["mere"] else ("", "", an)
    litters.setdefault(cle, []).append(a)
portee_albums = [x for x in albums if x["type"] == "portee"]


def album_portee(mere, an):
    m = mere.split()[0].lower() if mere else ""
    for p in portee_albums:
        t = p["titre"].lower()
        if an in t and m and m[:4] in t.replace("é", "e").replace("odysée", "odyssee"):
            return p
    return None


litter_html = []
for (mere, pere, an), kits in sorted(litters.items(), key=lambda kv: kv[1][0]["debut"], reverse=True):
    k0 = kits[0]
    titre = f'{lien_chat(k0["mere"], "../")} × {lien_chat(k0["pere"], "../")}' if k0["mere"] else f"Autres chatons de {an}"
    pa = album_portee(k0["mere"], an[:4])
    lien = f' · <a href="../{pa["url"]}">album de la portée</a>' if pa else ""
    cartes = "".join(carte("../", k) for k in kits)
    litter_html.append(f'<div class="litter"><h2>{titre}</h2><span>{date_fr(k0["debut"], False).capitalize()} · {len(kits)} chaton{"s" if len(kits) > 1 else ""}{lien}</span></div><div class="grid g4">{cartes}</div>')
page("portees", "Nos portées · Chatterie des Innamorati",
     f'<section><div class="wrap">{tete("Nos portées", "Toutes nos portées depuis 2016", "Chaque portée avec ses parents et ses chatons. Touchez un chaton pour ouvrir son album, du premier jour à l’âge adulte.")}{"".join(litter_html)}</div></section>',
     desc="Toutes les portées de Sacrés de Birmanie nées à la Chatterie des Innamorati depuis 2016.")

# ---------- Chatons disponibles ----------
dispo = [BY[f] for f in CFG["chatons_disponibles"]]
groupes = OrderedDict()
for k in dispo: groupes.setdefault((cle_nom(k["mere"]), cle_nom(k["pere"])), []).append(k)
blocs = []
for _, kits in groupes.items():
    m, p = kits[0]["mere"], kits[0]["pere"]
    cartes = "".join(carte("../", k, f'<span class="status{" libre" if "réserver" in k["statut"] else ""}">{e(k["statut"].capitalize())}</span>') for k in kits)
    blocs.append(f'<div class="litter"><h2>{lien_chat(m, "../")} × {lien_chat(p, "../")}</h2><span>Nés en {date_fr(kits[0]["debut"], False)}</span></div><div class="grid g4">{cartes}</div>')
page("chatons", "Nos chatons · Chatterie des Innamorati",
     f'<section><div class="wrap">{tete("Nos chatons", "Les chatons de 2026", "Chaque chaton a son album, mis à jour chaque semaine jusqu’à son départ, puis enrichi par les photos de sa famille. Pour réserver, écrivez-nous.")}{"".join(blocs)}<p class="center" style="margin-top:64px"><a class="btn" href="../adopter/">Adopter un chaton</a></p></div></section>',
     desc="Chatons Sacrés de Birmanie disponibles à la Chatterie des Innamorati, Bordeaux.")

# ---------- Nos chats ----------
def bloc(titre, texte, liste):
    return f'<div class="litter"><h2>{titre}</h2><span>{texte}</span></div><div class="grid g3">{"".join(carte("../", a) for a in liste)}</div>'
cathy = CFG["males_amie"]
males_txt = f'<p class="note">Nos chatons ont aussi pour pères les mâles de notre amie {e(cathy["nom"])} : {", ".join(lien_chat(c, "../") for c in cathy["chats"])}. Crush Boom Bang a aussi été l’un de nos reproducteurs.</p>'
eros_txt = '<div class="litter"><h2>Eros, notre premier Birman</h2><span>Celui par qui tout a commencé</span></div><p class="note" style="margin-top:0">Eros n’était pas au standard de la race et n’a jamais reproduit. Il a été notre adoré chat de compagnie, et c’est grâce à lui que nous sommes tombés amoureux du Sacré de Birmanie.</p>'
corps = (f'<section><div class="wrap">{tete("Nos chats", "Ceux qui font la maison", "Nos reproductrices actuelles, nos retraités qui vivent toujours avec nous, et tous ceux qui ont construit l’élevage.")}'
         + bloc("Nos reproductrices", "Elles vivent avec nous et donnent naissance à nos chatons", [BY[f] for f in CFG["reproductrices"]])
         + bloc("Nos retraités", "Stérilisés, ils profitent de la maison", [BY[f] for f in CFG["retraites_maison"]])
         + bloc("Nos anciennes reproductrices", "Retraitées dans des familles aimantes", [BY[f] for f in CFG["anciennes_reproductrices"]])
         + bloc("Nos anciens reproducteurs", "Les mâles qui ont vécu chez nous", [BY[f] for f in CFG["anciens_males"]])
         + males_txt + eros_txt + "</div></section>")
page("nos-chats", "Nos chats · Chatterie des Innamorati", corps, desc="Les reproducteurs et retraités de la Chatterie des Innamorati.")

# ---------- Ils ont grandi ----------
grandis = sorted([a for a in chats if a["type"] == "grandi"], key=lambda a: a["debut"], reverse=True)
par_an = OrderedDict()
for a in grandis: par_an.setdefault(a["debut"][:4], []).append(a)
nav_an = "".join(f'<a href="#a{an}">{an}</a>' for an in par_an)
blocs = "".join(f'<div class="litter" id="a{an}"><h2>{an}</h2><span>{len(l)} chatons</span></div><div class="grid g4">{"".join(carte("../", a) for a in l)}</div>' for an, l in par_an.items())
page("ils-ont-grandi", "Ils ont grandi · Chatterie des Innamorati",
     f'<section><div class="wrap">{tete("Ils ont grandi", f"{len(grandis)} chatons nés chez nous", "Nos anciens chatons, du premier jour à l’âge adulte. Les albums continuent de s’enrichir grâce aux photos de leurs familles.")}<nav class="years">{nav_an}</nav>{blocs}</div></section>',
     desc="Les anciens chatons de la Chatterie des Innamorati, de chatons à adultes.")

# ---------- Expositions ----------
expos = sorted([a for a in albums if a["type"] == "expo"], key=lambda a: a["nom"], reverse=True)
for a in expos:
    r = "../../"
    resultats = e(a["description"]).replace("\n", "<br>")
    corps = f"""<section class="album-page"><div class="wrap">
<p class="crumb"><a href="{r}expositions/">Expositions</a></p>
<div class="head"><h1>{e(re.sub(r"^[0-9-]+( à [0-9]+| & [0-9]+)? ", "", a["titre"]))}</h1><p class="label">{date_fr(a["nom"][:10])} · {len(a["photos"])} photos</p></div>
{f'<div class="results">{resultats}</div>' if resultats else ''}
{galerie(r, a)}
</div></section>"""
    page(a["url"].rstrip("/"), f'{a["titre"]} · Expositions', corps, image=a["cover"])
saisons = OrderedDict()
for a in expos:
    d = datetime.date.fromisoformat(a["nom"][:10])
    s = f"{d.year}–{d.year+1}" if d.month >= 9 else f"{d.year-1}–{d.year}"
    saisons.setdefault(s, []).append(a)
blocs = []
for s, l in saisons.items():
    items = "".join(f'<a class="card" href="../{a["url"]}">{img("../", a["cover"], a["titre"])}<div class="t"><span class="titles">{date_fr(a["nom"][:10])}</span><h3>{e(re.sub(r"^[0-9-]+( à [0-9]+| & [0-9]+)? ", "", a["titre"]))}</h3><span class="robe">{len(a["photos"])} photos</span></div></a>' for a in l)
    blocs.append(f'<div class="litter"><h2>Saison {s}</h2><span>{len(l)} albums</span></div><div class="grid g3">{items}</div>')
page("expositions", "Expositions · Chatterie des Innamorati",
     f'<section><div class="wrap">{tete("Expositions", "Dix saisons d’expositions", "Chaque hiver et chaque printemps, nous présentons nos chats en exposition FIFe et LOOF. Les résultats et les photos de chaque week-end.")}{"".join(blocs)}</div></section>',
     desc="Résultats et photos des expositions félines de la Chatterie des Innamorati.")

# ---------- Couleurs ----------
def exemple_couleur(c):
    if c.get("photo"): return c["photo"], c.get("chat", "")
    ordre = {"repro": 0, "retraite": 1, "ancienne": 2, "male": 3, "chaton": 4, "grandi": 5}
    cands = sorted([a for a in chats if a["robe"] == c["robe"]], key=lambda a: a["debut"], reverse=True)
    return (cands[0]["cover"], cands[0]) if cands else (None, None)
blocs = []
for fam in COULEURS["familles"]:
    cartes = []
    for c in fam["couleurs"]:
        pid, chat = exemple_couleur(c)
        if pid:
            leg = f'<a href="../{chat["url"]}">{e(chat["titre"])}</a>' if isinstance(chat, dict) else e(chat)
            visuel = img("../", pid, f'{c["robe"]} : {chat["titre"] if isinstance(chat, dict) else chat}')
        else:
            leg = "Photo à venir"
            visuel = '<div class="ph vide"><span>Photo à venir</span></div>'
        cartes.append(f'<div class="card coul">{visuel}<div class="t"><h3>{e(c["robe"])}</h3><span class="robe">{e(c["texte"])}</span><span class="ex">{leg}</span></div></div>')
    blocs.append(f'<div class="litter"><h2>{e(fam["nom"])}</h2><span>{e(fam["texte"])}</span></div><div class="grid g4">{"".join(cartes)}</div>')
page("couleurs", "Les couleurs du Sacré de Birmanie · Chatterie des Innamorati",
     f'<section><div class="wrap">{tete("Les couleurs", "Toutes les robes du Sacré de Birmanie", COULEURS["intro"])}{"".join(blocs)}<p class="note">{COULEURS["note"]}</p></div></section>',
     desc="Toutes les couleurs du Sacré de Birmanie, illustrées par les chats de la Chatterie des Innamorati.")

json.dump({"albums": len(albums), "chats": len(chats), "grandis": len(grandis), "portees": len(litters), "expos": len(expos)},
          open(os.path.join(ROOT, "data/stats.json"), "w"))
exec(open(os.path.join(ROOT, "src/pages_fixes.py"), encoding="utf-8").read())
print(f"OK : {len(chats)} chats, {len(grandis)} anciens chatons, {len(litters)} portées, {len(expos)} expositions")
