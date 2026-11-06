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
CAT += json.load(open(os.path.join(ROOT, "data/albums_ajoutes.json"), encoding="utf-8"))  # chats sans album Facebook
CFG = json.load(open(os.path.join(ROOT, "data/config.json"), encoding="utf-8"))
COULEURS = json.load(open(os.path.join(ROOT, "data/couleurs.json"), encoding="utf-8"))
SIRET = "829 118 769 00019"
EMAIL = "innamoraticats@tristanperrier.fr"
# Adresse publique du site : le domaine du fichier CNAME s'il existe, sinon GitHub Pages
_cname = os.path.join(ROOT, "docs", "CNAME")
SITE = ("https://" + open(_cname).read().strip() + "/") if os.path.exists(_cname) else "https://tristan33200.github.io/innamorati/"
PLAN = []  # pages pour sitemap.xml : (chemin, priorité)
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
    if fb in CFG.get("statuts", {}): a["statut"] = CFG["statuts"][fb]
    a["note"] = CFG["notes"].get(fb, "")
    a["titres"] = CFG["titres"].get(fb, "")
    a["ne"] = CFG.get("naissances", {}).get(fb, "")
    a["url"] = ("expositions/" if a["type"] == "expo" else "chat/") + a["slug"] + "/"

chats = [a for a in albums if a["type"] not in ("masque", "expo", "portee")]
age = lambda a: a["ne"] or a["debut"]

# Palmarès : résultats d'expositions relevés dans les dossiers de l'élevage
PALM = {}
for _r in json.load(open(os.path.join(ROOT, "data/palmares.json"), encoding="utf-8")):
    if _r["fb"]: PALM.setdefault(_r["fb"], []).append(_r)
MOIS_C = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]


def palmares(fb):
    lst = sorted(PALM.get(fb, []), key=lambda x: x["date"], reverse=True)
    if not lst: return ""
    wk = {(x["lieu"], x["date"][:7]) for x in lst}
    nbis = sum(1 for x in lst if "BIS" in x["res"] or "BEST" in x["res"])
    nbob = sum(1 for x in lst if "BOB" in x["res"])
    resume = f'{len(wk)} exposition{"s" if len(wk) > 1 else ""} · {len(lst)} jugement{"s" if len(lst) > 1 else ""}'
    if nbis: resume += f' · {nbis} Best in Show'
    if nbob: resume += f' · {nbob} Best of Best'
    ans = OrderedDict()
    for x in lst: ans.setdefault(x["date"][:4], []).append(x)
    def res(t):
        t = e(t).replace(" + ", " · ")
        return re.sub(r"\b(BIS|BEST(?: x?\d)?|BOB(?: [0-9]\S*)?)", r"<b>\1</b>", t)
    blocs = "".join(f'<div class="pl-an"><h3>{an}</h3><ul>' + "".join(
        f'<li><time datetime="{x["date"]}">{int(x["date"][8:])} {MOIS_C[int(x["date"][5:7]) - 1]}</time><span>{e(x["lieu"])}</span><em>{res(x["res"])}</em></li>' for x in l)
        + '</ul></div>' for an, l in ans.items())
    return (f'<div class="pl"><div class="litter"><h2>Palmarès</h2><span>{resume}</span></div><div class="pl-ans">{blocs}</div>'
            '<p class="abbr pl-abbr">EXC Excellent (classement) · CAC, CACIB, CAGCIB, CACS certificats de champion, champion international, grand champion international et suprême · CAP, CAPIB, CAGPIB, CAPS équivalents pour les chats stérilisés · '
            'BIV meilleur de la variété · NOM nommé pour le Best in Show · BIS Best in Show · BOB Best of Best, le meilleur de toute l’exposition</p></div>')
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


def page(chemin, titre, corps, desc="", sombre_entete=False, image=None, ld=None, prio=None):
    profondeur = len([x for x in chemin.split("/") if x])
    r = "../" * profondeur
    url = SITE + (chemin.strip("/") + "/" if chemin else "")
    desc = desc or "Chatterie des Innamorati, élevage familial de Sacrés de Birmanie à Bordeaux."
    PLAN.append((url, prio if prio is not None else (0.5 if profondeur > 1 else 0.7)))
    blocs_ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (ld or []))
    nav = lambda items: "".join(f'<a href="{r}{u}">{t}</a>' for u, t in items)
    entete = "top over" if sombre_entete else "top"
    meta_img = f'<meta property="og:image" content="{SITE}photos/{image}.jpg">' if image else ""
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titre)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="Chatterie des Innamorati">
<meta property="og:title" content="{e(titre)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
{meta_img}<meta name="twitter:card" content="summary_large_image">
{blocs_ld}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap">
<link rel="stylesheet" href="{r}assets/style.css">
<link rel="stylesheet" href="{r}assets/motion.css">
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
  <p class="fine">Affixe LOOF « des Innamorati » · Magali Perrier, SIRET {SIRET}<br>Photographies © <a href="https://tristanperrier.fr" target="_blank" rel="noopener">Tristan Perrier</a>. Toute reproduction est interdite.</p>
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


def faq(titre, items, label="Questions fréquentes"):
    """Bloc de questions dépliables + données structurées FAQPage pour Google."""
    q = "".join(f"<details><summary>{e(a)}</summary><p>{b}</p></details>" for a, b in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", b)}} for a, b in items]}
    return f'<section class="faq"><div class="wrap narrow"><div class="head"><p class="label">{label}</p><h2>{titre}</h2></div>{q}</div></section>', ld


def ariane(*etapes):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(etapes)]}


def slug_robe(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


CADRAGE = json.load(open(os.path.join(ROOT, "data/cadrages.json"), encoding="utf-8"))  # centre du visage (yeux bleus)


def img(r, pid, alt, cls="", grand=False, attrs=""):
    """Vignette nette : la version 1400 px est proposée aux écrans qui en ont besoin, cadrée sur le visage."""
    src = f"{r}photos/{pid}.jpg" if grand else f"{r}photos/t/{pid}.jpg"
    jeu = "" if grand else f' srcset="{r}photos/t/{pid}.jpg 520w, {r}photos/{pid}.jpg 1400w" sizes="(max-width: 700px) 100vw, 45vw"'
    pos = f' style="object-position:{CADRAGE[pid][0]}% {CADRAGE[pid][1]}%"' if pid in CADRAGE else ""
    return f'<div class="ph {cls}"><img src="{src}"{jeu} alt="{e(alt)}" loading="lazy"{pos} {attrs}></div>'


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


def legende(a, p):
    leg = clean(p["legende"])
    if a["titre"].lower()[:12] in leg.lower() or leg == clean(a["description"]): leg = ""
    return date_fr(p["date"]) + (" · " + leg[:300].replace("\n", " ") if leg else "")


def entete_album(r, a, titre, sur, sous):
    """Grande photo de couverture plein écran, titre par-dessus (parallaxe)."""
    return (f'<div class="hero album-hero"><div class="ph"><img src="{r}photos/{a["cover"]}.jpg" alt="{e(a["titre"])}"></div>'
            f'<div class="wrap"><p class="crumb">{sur}</p><h1>{e(titre)}</h1><p>{sous}</p></div></div>')


FILM_MIN = 8  # nombre de photos à partir duquel l'album s'ouvre sur un défilé horizontal


def film(r, a, n=10):
    if len(a["photos"]) < FILM_MIN: return ""
    items = "".join(f'<a class="g-item f-item" href="{r}photos/{p["id"]}.jpg" data-cap="{e(legende(a, p))}">'
                    f'<div class="ph"><img src="{r}photos/{p["id"]}.jpg" alt="{e(a["titre"])}, {date_fr(p["date"])}" loading="lazy"></div>'
                    f'<span class="f-n">{i + 1:02d}</span></a>' for i, p in enumerate(a["photos"][:n]))
    return f'<div class="film"><div class="film-pin"><div class="film-track">{items}</div></div></div>'


def galerie(r, a):
    figs = []
    debut = min(10, len(a["photos"])) if len(a["photos"]) >= FILM_MIN else 0
    for p in a["photos"][debut:]:
        cap = legende(a, p)
        figs.append(f'<a class="g-item" href="{r}photos/{p["id"]}.jpg" data-cap="{e(cap)}">'
                    f'<div class="ph"><img src="{r}photos/t/{p["id"]}.jpg" srcset="{r}photos/t/{p["id"]}.jpg 520w, {r}photos/{p["id"]}.jpg 1400w" sizes="(max-width: 700px) 50vw, 30vw" alt="{e(a["titre"])}, {date_fr(p["date"])}" loading="lazy"></div></a>')
    return f'<div class="gallery">{"".join(figs)}</div>' if figs else ""


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
    if a["ne"]: faits.append(("Naissance", date_fr(a["ne"])))
    if a["mere"]: faits.append(("Parents", f'{lien_chat(a["mere"], r)} × {lien_chat(a["pere"], r)}'))
    if a["titres"]: faits.append(("Titres", e(a["titres"])))
    statut = a["note"] or (a["statut"][:1].upper() + a["statut"][1:] if a["statut"] else "")
    if statut: faits.append(("Statut", e(statut)))
    faits.append(("Album", f'{len(a["photos"])} photos, de {date_fr(a["debut"], False)} à {date_fr(a["fin"], False)}'))
    fhtml = "".join(f'<div><span class="label">{k}</span><span>{v}</span></div>' for k, v in faits)
    rubrique = {"repro": ("Nos reproductrices", "nos-chats/"), "retraite": ("Nos retraités", "nos-chats/"), "ancienne": ("Nos anciennes reproductrices", "nos-chats/"),
                "male": ("Nos anciens reproducteurs", "nos-chats/"), "chaton": ("Nos chatons", "chatons/"), "portee": ("Nos portées", "portees/"),
                "grandi": ("Ils ont grandi", "ils-ont-grandi/")}[a["type"]]
    sous = " · ".join(x for x in [a["sexe"], a["robe"]] if x) or f'{len(a["photos"])} photos'
    corps = f"""{entete_album(r, a, a["titre"], f'<a href="{r}{rubrique[1]}">{rubrique[0]}</a>', e(sous))}
<section class="album-page"><div class="wrap">
<div class="head"><div class="facts">{fhtml}</div></div>
{f'<p class="center" style="margin:-24px 0 56px"><a class="btn" href="{r}contact/?chaton={a["titre"].replace(" ", "+")}#formulaire">Ce chaton m\'intéresse</a></p>' if a["type"] == "chaton" and "à réserver" in (a["statut"] or "") else ""}
</div>{film(r, a)}<div class="wrap">
{galerie(r, a)}
{palmares(a["fb"])}
<p class="prot">Photos réduites et marquées. Elles appartiennent à la Chatterie des Innamorati et ne peuvent pas être reprises dans une annonce.</p>
</div></section>"""
    page(a["url"].rstrip("/"), f'{a["titre"]} · Chatterie des Innamorati', corps, sombre_entete=True,
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
    litter_html.append(f'<div class="litter"><h2>{titre}</h2><span>{(("Nés le " + date_fr(k0["ne"])) if k0["ne"] else date_fr(k0["debut"], False).capitalize())} · {len(kits)} chaton{"s" if len(kits) > 1 else ""}{lien}</span></div><div class="grid g4">{cartes}</div>')
page("portees", "Nos portées · Chatterie des Innamorati",
     f'<section><div class="wrap">{tete("Nos portées", "Toutes nos portées depuis 2016", "Chaque portée avec ses parents et ses chatons. Touchez un chaton pour ouvrir son album, du premier jour à l’âge adulte.")}{"".join(litter_html)}</div></section>',
     desc="Toutes les portées de Sacrés de Birmanie nées à la Chatterie des Innamorati depuis 2016.")

# ---------- Chatons disponibles ----------
dispo = [BY[f] for f in CFG["chatons_disponibles"]]
groupes = OrderedDict()
for k in dispo: groupes.setdefault((cle_nom(k["mere"]), cle_nom(k["pere"])), []).append(k)
blocs = []
for _, kits in sorted(groupes.items(), key=lambda kv: age(kv[1][0]), reverse=True):
    m, p = kits[0]["mere"], kits[0]["pere"]
    cartes = "".join(carte("../", k, f'<span class="status{" libre" if "réserver" in k["statut"] else ""}">{e(k["statut"].capitalize())}</span>') for k in kits)
    blocs.append(f'<div class="litter"><h2>{lien_chat(m, "../")} × {lien_chat(p, "../")}</h2><span>{("Nés le " + date_fr(kits[0]["ne"])) if kits[0]["ne"] else "Nés en " + date_fr(kits[0]["debut"], False)}</span></div><div class="grid g4">{cartes}</div>')
page("chatons", "Nos chatons · Chatterie des Innamorati",
     f'<section><div class="wrap">{tete("Nos chatons", "Les chatons de 2026", "Chaque chaton a son album, mis à jour chaque semaine jusqu’à son départ, puis enrichi par les photos de sa famille. Pour réserver, écrivez-nous.")}{"".join(blocs)}<p class="center" style="margin-top:64px"><a class="btn" href="../adopter/">Adopter un chaton</a></p></div></section>',
     desc="Chatons Sacrés de Birmanie disponibles à la Chatterie des Innamorati, Bordeaux.")

# ---------- Nos chats ----------
def bloc(titre, texte, liste):
    liste = sorted(liste, key=age, reverse=True)  # du plus jeune au plus ancien
    return f'<div class="litter"><h2>{titre}</h2><span>{texte}</span></div><div class="grid g3">{"".join(carte("../", a) for a in liste)}</div>'
cathy = CFG["males_amie"]
males_txt = f'<p class="note">Nos chatons ont aussi pour pères les mâles de notre amie {e(cathy["nom"])} : {", ".join(lien_chat(c, "../") for c in cathy["chats"])}.</p>'
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
    lieu = re.sub(r"^[0-9-]+( à [0-9]+| & [0-9]+)? ", "", a["titre"])
    corps = f"""{entete_album(r, a, lieu, f'<a href="{r}expositions/">Expositions</a>', f'{date_fr(a["nom"][:10])} · {len(a["photos"])} photos')}
<section class="album-page"><div class="wrap">
{f'<div class="results">{resultats}</div>' if resultats else ''}
</div>{film(r, a)}<div class="wrap">
{galerie(r, a)}
</div></section>"""
    page(a["url"].rstrip("/"), f'{a["titre"]} · Expositions', corps, image=a["cover"], sombre_entete=True)
saisons = OrderedDict()
for a in expos:
    d = datetime.date.fromisoformat(a["nom"][:10])
    s = f"{d.year}–{d.year+1}" if d.month >= 9 else f"{d.year-1}–{d.year}"
    saisons.setdefault(s, []).append(a)
# Expositions relevées dans les dossiers de l'élevage, y compris celles sans album photo
def saison_de(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.year}–{d.year+1}" if d.month >= 9 else f"{d.year-1}–{d.year}"
shows = []
for x in sorted(json.load(open(os.path.join(ROOT, "data/palmares.json"), encoding="utf-8")), key=lambda x: x["date"]):
    d = datetime.date.fromisoformat(x["date"])
    sh = next((s for s in shows if s["lieu"] == x["lieu"] and (d - s["fin"]).days <= 3), None)
    if not sh:
        sh = {"lieu": x["lieu"], "debut": d, "fin": d, "chats": OrderedDict()}; shows.append(sh)
    sh["fin"] = max(sh["fin"], d)
    sh["chats"].setdefault((x["nom"], x["fb"]), []).append(x["res"])
dates_albums = [datetime.date.fromisoformat(a["nom"][:10]) for a in expos]
sans_album = OrderedDict()
for sh in sorted(shows, key=lambda s: s["debut"], reverse=True):
    if any(-3 <= (da - sh["debut"]).days <= 4 for da in dates_albums): continue
    sans_album.setdefault(saison_de(sh["debut"].isoformat()), []).append(sh)
    saisons.setdefault(saison_de(sh["debut"].isoformat()), [])
saisons = OrderedDict(sorted(saisons.items(), reverse=True))


def ligne_show(sh):
    j = f'{sh["debut"].day}' + (f'–{sh["fin"].day}' if sh["fin"] != sh["debut"] else "")
    quand = f'{j} {MOIS[sh["fin"].month - 1]} {sh["fin"].year}'
    chats_h = "".join(f'<span>{lien_chat(BY[fb]["titre"], "../") if fb in BY else e(nom)} : '
                      + re.sub(r"\b(BIS|BEST|BOB(?: [0-9]\S*)?)", r"<b>\1</b>", e(" / ".join(dict.fromkeys(r.replace(" + ", " · ") for r in res))))
                      + '</span>' for (nom, fb), res in sh["chats"].items())
    return f'<li><time>{quand}</time><div><b class="ex-lieu">{e(sh["lieu"])}</b>{chats_h}</div></li>'


blocs = []
for s, l in saisons.items():
    autres = sans_album.get(s, [])
    sans = f'<ul class="ex-sans">{"".join(ligne_show(sh) for sh in autres)}</ul>' if autres else ""
    n = len(l) + len(autres)
    items = "".join(f'<a class="card" href="../{a["url"]}">{img("../", a["cover"], a["titre"])}<div class="t"><span class="titles">{date_fr(a["nom"][:10])}</span><h3>{e(re.sub(r"^[0-9-]+( à [0-9]+| & [0-9]+)? ", "", a["titre"]))}</h3><span class="robe">{len(a["photos"])} photos</span></div></a>' for a in l)
    grille = f'<div class="grid g3">{items}</div>' if items else ""
    blocs.append(f'<div class="litter"><h2>Saison {s}</h2><span>{n} exposition{"s" if n > 1 else ""}{f" · {len(l)} en photos" if l and autres else ""}</span></div>{grille}{sans}')
page("expositions", "Expositions · Chatterie des Innamorati",
     f'<section><div class="wrap">{tete("Expositions", "Douze saisons d’expositions", "Chaque hiver et chaque printemps, nous présentons nos chats en exposition FIFe et LOOF. Les résultats et les photos de chaque week-end.")}{"".join(blocs)}</div></section>',
     desc="Résultats et photos des expositions félines de la Chatterie des Innamorati.")

# ---------- Couleurs ----------
def exemple_couleur(c):
    if c.get("photo"): return c["photo"], c.get("chat", "")
    ordre = {"repro": 0, "retraite": 1, "ancienne": 2, "male": 3, "chaton": 4, "grandi": 5}
    cands = sorted([a for a in chats if a["robe"] == c["robe"]], key=lambda a: a["debut"], reverse=True)
    return (cands[0]["cover"], cands[0]) if cands else (None, None)
blocs, nb_robes = [], 0
for fam in COULEURS["familles"]:
    cartes = []
    for c in fam["couleurs"]:
        nb_robes += 1
        pid, chat = exemple_couleur(c)
        if pid:
            leg = f'Photo : <a href="../{chat["url"]}">{e(chat["titre"])}</a>' if isinstance(chat, dict) else e(chat)
            visuel = img("../", pid, f'Sacré de Birmanie {c["robe"].lower()} : {chat["titre"] if isinstance(chat, dict) else chat}')
        else:
            leg = "Photo à venir"
            visuel = '<div class="ph vide"><span>Photo à venir</span></div>'
        cartes.append(f'<div class="card coul" id="{slug_robe(c["robe"])}">{visuel}<div class="t"><h3>{e(c["robe"])}</h3><span class="robe">{e(c["texte"])}</span><span class="ex">{leg}</span></div></div>')
    blocs.append(f'<div class="litter"><h2>{e(fam["nom"])}</h2><span>{e(fam["texte"])}</span></div><div class="grid g4">{"".join(cartes)}</div>')
comprendre = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in COULEURS["comprendre"])
# Tableau récapitulatif des 40 couleurs reconnues : 6 bases x 8 motifs (tortie impossible sur red et cream)
BASES = [("Seal", "#3b2a22", "#c9733a"), ("Blue", "#6f7b8c", "#e3c39b"), ("Chocolat", "#7a5236", "#d48a4e"),
         ("Lilac", "#b3a6a8", "#ecd2b4"), ("Red", "#d48a4e", None), ("Cream", "#e8c9a0", None)]
MOTIFS = [("Point", "point", ""), ("Tabby point", "tabby point", "tabby"), ("Tortie point", "tortie point", "tortie"),
          ("Tortie tabby point", "tortie tabby point", "tortie tabby"), ("Silver tabby point", "silver tabby point", "silver tabby"),
          ("Silver tortie tabby point", "silver tortie tabby point", "silver tortie tabby"), ("Smoke point", "smoke point", "smoke"),
          ("Smoke tortie point", "smoke tortie point", "smoke tortie")]
# Têtes de chats adultes recadrées (data/tetes.json, images dans docs/photos/rc/)
TETES = json.load(open(os.path.join(ROOT, "data/tetes.json"), encoding="utf-8"))
PHOTO_CHAT = {p["id"]: a for a in chats for p in a["photos"]}
ROBES_CHATS = {}
for _a in sorted(chats, key=lambda x: x["debut"], reverse=True):
    if _a["robe"]: ROBES_CHATS.setdefault(_a["robe"].lower(), _a)
ANCRES = {c["robe"].lower(): slug_robe(c["robe"]) for f in COULEURS["familles"] for c in f["couleurs"]}


def pastille(fonce, roux, motif):
    """Petit disque qui évoque la couleur : corps clair, extrémité colorée, rayures, écaille, argent."""
    couches = []
    if "tabby" in motif: couches.append(f"repeating-linear-gradient(115deg, {fonce} 0 5px, transparent 5px 10px)")
    if "tortie" in motif and roux: couches.append(f"conic-gradient(from 30deg, {roux} 0 22%, transparent 22% 48%, {roux} 48% 66%, transparent 66%)")
    fond = "#e9ecef" if ("silver" in motif or "smoke" in motif) else "#f4ede2"
    centre = f"radial-gradient(circle at 50% 70%, {fonce} 0 38%, {fond} 39%)"
    if "smoke" in motif: centre = f"radial-gradient(circle at 50% 70%, #f6f6f6 0 14%, {fonce} 15% 38%, {fond} 39%)"
    return ", ".join(couches + [centre])


lignes = []
for lib, suff, motif in MOTIFS:
    cellules = []
    for base, fonce, roux in BASES:
        if "tortie" in motif and not roux:
            cellules.append('<td class="na" title="N’existe pas : le red et le cream sont déjà des couleurs rousses">–</td>')
            continue
        robe = f"{base} {suff}"
        t = TETES.get(robe.lower())
        chat = t and PHOTO_CHAT.get(t["photo"])
        if chat:
            cible = f'#{ANCRES[robe.lower()]}' if robe.lower() in ANCRES else f'../{chat["url"]}'
            vis = f'<a class="rc-ph" href="{cible}" title="{e(robe)} : {e(chat["titre"])}"><img src="../photos/{t["fichier"]}" alt="{e(robe)}" loading="lazy"></a>'
        else:
            vis = f'<span class="rc-dot" style="background:{pastille(fonce, roux, motif)}" title="{e(robe)}"></span>'
        cellules.append(f'<td>{vis}</td>')
    lignes.append(f'<tr><th scope="row">{lib}</th>{"".join(cellules)}</tr>')
recap = (f'''<div class="recap"><div class="litter"><h2>Les 40 couleurs en un coup d’œil</h2><span>En photo : nos chats, adultes de préférence. En pastille : les couleurs qui ne sont pas encore nées chez nous.</span></div>
<div class="recap-scroll"><table class="recap-t"><thead><tr><th></th>{"".join(f'<th scope="col">{b}</th>' for b, _, _ in BASES)}</tr></thead><tbody>{"".join(lignes)}</tbody></table></div>
<div class="recap-regles"><div><b>Ce qui ne change jamais</b><span>Des yeux bleus, toujours. Quatre gants blancs. Un corps clair aux extrémités colorées.</span></div>
<div><b>Ce qui n’existe pas chez le Birman</b><span>Les yeux verts ou dorés, les robes bicolores ou à masque blanc, les robes unies sans « point ». Un chat ainsi n’est pas un Sacré de Birmanie.</span></div>
<div><b>Le tortie</b><span>Il mêle une couleur et du roux. Il n’existe donc pas en red ni en cream, et concerne presque uniquement les femelles.</span></div></div></div>''')
faq_html, faq_ld = faq("Les couleurs du Birman en questions", COULEURS["faq"])
page("couleurs", "Couleurs du Sacré de Birmanie : toutes les robes en photos · des Innamorati",
     f'''<section><div class="wrap">{tete("Les couleurs", "Toutes les couleurs du Sacré de Birmanie", COULEURS["intro"])}
{recap}
<div class="std std4">{comprendre}</div>
<nav class="sommaire" aria-label="Familles de couleurs">{"".join(f'<a href="#{slug_robe(f["nom"])}">{e(f["nom"])}</a>' for f in COULEURS["familles"])}</nav>
{"".join(b.replace('<div class="litter">', f'<div class="litter" id="{slug_robe(f["nom"])}">', 1) for b, f in zip(blocs, COULEURS["familles"]))}
<p class="note">{COULEURS["note"]}</p></div></section>{faq_html}''',
     desc=f"Les couleurs du Sacré de Birmanie en photos (40 reconnues) : seal, blue, chocolat, lilac, red, cream point, tabby, tortie, silver et smoke. Génétique et reconnaissance de la couleur d'un chaton.",
     ld=[faq_ld, ariane(("Accueil", ""), ("Couleurs", "couleurs/"))], prio=0.9)

json.dump({"albums": len(albums), "chats": len(chats), "grandis": len(grandis), "portees": len(litters), "expos": len(expos)},
          open(os.path.join(ROOT, "data/stats.json"), "w"))
exec(open(os.path.join(ROOT, "src/pages_fixes.py"), encoding="utf-8").read())
# Plan du site pour Google
aujourdhui = datetime.date.today().isoformat()
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"<url><loc>{u}</loc><lastmod>{aujourdhui}</lastmod><priority>{p}</priority></url>\n" for u, p in PLAN)
    + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
print(f"OK : {len(chats)} chats, {len(grandis)} anciens chatons, {len(litters)} portées, {len(expos)} expositions")
