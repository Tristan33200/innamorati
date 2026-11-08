# Pages générées depuis les albums. Exécuté par build.py une fois par langue (L = "fr" puis "en").
# ---------- Portées : regroupement des chatons par parents et par année (sert aussi aux frères et sœurs) ----------
litters = OrderedDict()
for a in sorted([x for x in chats if x["type"] in ("grandi", "chaton") or (x["mere"] and x["fb"] not in S("anciens_males") | S("males_exterieurs"))], key=lambda x: x["debut"]):
    if not a["mere"] and a["type"] not in ("grandi", "chaton"): continue
    if a["type"] not in ("grandi", "chaton") and not re.search(r"Innamorati|Tribu Birmane", a["titre"]): continue  # né ailleurs : sa portée n'est pas une portée de l'élevage
    an = a["debut"][:4]
    cle = (cle_nom(a["mere"]), cle_nom(a["pere"]), an) if a["mere"] else ("", "", an)
    litters.setdefault(cle, []).append(a)
FRATRIE = {k["fb"]: [x for x in kits if x is not k] for (m, p, an), kits in litters.items() if m for k in kits}
for _g in CFG.get("fratries", []):  # fratries connues sans les parents
    for _f in _g:
        FRATRIE[_f] = FRATRIE.get(_f, []) + [BY[x] for x in _g if x != _f and BY[x] not in FRATRIE.get(_f, [])]
de_mois = lambda d: ("d’" if d[:1].lower() in "aeiouéè" else "de ") + d
ancre_portee = lambda cle: "p-" + slug_robe("-".join(cle))
court_nom = lambda n: re.sub(r"\s+(des Innamorati|aka)\b.*$", "", n, flags=re.I)


TEMOINS = json.load(open(os.path.join(ROOT, "data/temoignages.json"), encoding="utf-8"))


def mots_famille(a):
    """Les mots de la famille adoptive, publiés avec son accord (prénom seulement)."""
    l = TEMOINS.get(a["fb"], [])
    if not l: return ""
    n = e(court_nom(a["titre"]))
    blocs = "".join(f'''<figure class="mot"><blockquote><p>{e(t["caractere"]).replace(chr(10), "<br>")}</p>{f'<p class="avis"><span class="label">{T("Sur notre élevage", "About our cattery")}</span>{e(t["avis"]).replace(chr(10), "<br>")}</p>' if t.get("avis") else ""}</blockquote><figcaption>{e(t["prenom"])}{T(", sa famille", ", their family")}</figcaption></figure>''' for t in l)
    return f'<section class="mots"><p class="label">{T("Le mot de sa famille", "In their family’s words (in French)")}</p><h2>{T(f"{n}, raconté{"e" if a["sexe"] == "Femelle" else ""} par les siens", f"{n}, as told by their family")}</h2>{blocs}</section>'


def temoignage(r, a):
    """Formulaire pour la famille adoptive : quelques mots sur le chat et sur l'élevage, publiés avec son accord."""
    n = e(court_nom(a["titre"]))
    return f'''<section class="temoin"><div class="temoin-t"><p class="label">{T("Vous êtes sa famille ?", "Are you their family?")}</p>
<h2>{T(f"Racontez-nous {n}", f"Tell us about {n}")}</h2>
<p>{T(f"Son caractère, ses petites manies, ce que vous aimez chez {n}, et quelques mots sur votre expérience avec notre élevage : nous les ajouterons à cette page, avec votre prénom seulement.", f"Their personality, little habits, what you love about {n}, and a few words about your experience with our cattery: we will add them to this page, with your first name only.")}</p>
<p>{T("Pour les photos, envoyez-nous vos plus belles par e-mail ou par l’application Messages de l’iPhone : WhatsApp les compresse et elles perdent en qualité.", "For photos, please send your best ones by e-mail or iMessage: WhatsApp compresses them and they lose quality.")}</p></div>
<form class="form" action="https://formsubmit.co/{EMAIL}" method="POST">
<input type="hidden" name="_subject" value="Témoignage pour {e(a["titre"])}">
<input type="hidden" name="_next" value="{lien("contact/merci/")}">
<input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
<input type="hidden" name="Chat" value="{e(a["titre"])}">{T("", '<input type="hidden" name="Langue" value="Anglais">')}
<input type="text" name="_honey" class="pot" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="f2"><label>{T("Votre prénom", "Your first name")}<input name="Prénom affiché" required autocomplete="given-name"></label>
<label>E-mail<input type="email" name="email" required autocomplete="email"></label></div>
<label>{T(f"Le caractère de {n}", f"{n}’s personality")}<textarea name="Caractère du chat" rows="5" required></textarea></label>
<label><span>{T("Votre avis sur notre élevage", "Your thoughts on our cattery")} <small>· {T("facultatif", "optional")}</small></span><textarea name="Avis sur l’élevage" rows="4"></textarea></label>
<label class="ok"><input type="checkbox" name="Accord de publication" value="oui" required> <span>{T("J’accepte que ces mots soient publiés sur cette page avec mon prénom.", "I agree that these words may be published on this page with my first name.")}</span></label>
<button class="btn" type="submit">{T("Envoyer", "Send")}</button>
<p class="fine-form">{T("Votre e-mail sert uniquement à vous répondre et n’est jamais publié.", "Your e-mail is only used to reply to you and is never published.")}</p>
</form></section>'''


def demi_fratrie(a, r):
    """Autres portées de la même mère et du même père, avec un lien vers chacune sur la page Portées."""
    if not a["mere"]: return ""
    m, p = cle_nom(a["mere"]), cle_nom(a["pere"])
    ici = (m, p, a["debut"][:4])
    def liste(par_mere):
        out = []
        for cle, kits in sorted(litters.items(), key=lambda kv: kv[1][0]["debut"]):
            if cle == ici or not cle[0] or (cle[0] != m if par_mere else (not p or cle[1] != p)): continue
            autre = kits[0]["pere"] if par_mere else kits[0]["mere"]
            out.append(f'<a href="{r}portees/#{ancre_portee(cle)}">{cle[2]}{T(" avec ", " with ")}{e(court_nom(autre))}</a>')
        return ", ".join(out)
    lm, lp = liste(True), liste(False)
    parts = ([T("par sa mère : ", "through the mother: ") + lm] if lm else []) + ([T("par son père : ", "through the father: ") + lp] if lp else [])
    return "<br>".join(parts)


# ---------- Pages chat (une par album) ----------
for a in chats + [x for x in albums if x["type"] == "portee"]:
    r = "../../"
    faits = []
    if a["sexe"] or a["robe"]: faits.append((T("Robe", "Color"), " · ".join(x for x in [a["sexe"], rb(a["robe"])] if x)))
    if a["ne"]: faits.append((T("Naissance", "Born"), date_fr(a["ne"])))
    if a["mere"]: faits.append(("Parents", f'{lien_chat(a["mere"], r)} × {lien_chat(a["pere"], r)}'))
    if a["titres"]: faits.append((T("Titres", "Titles"), e(a["titres"])))
    statut = a["note"] or (a["statut"][:1].upper() + a["statut"][1:] if a["statut"] else "")
    if statut: faits.append((T("Statut", "Status"), e(statut)))
    faits.append(("Album", T(f'{len(a["photos"])} photos, {de_mois(date_fr(a["debut"], False))} à {date_fr(a["fin"], False)}',
                             f'{len(a["photos"])} photos, from {date_fr(a["debut"], False)} to {date_fr(a["fin"], False)}')))
    if FRATRIE.get(a["fb"]):
        faits.append((T("Frères et sœurs", "Littermates"), ", ".join(f'<a href="{r}{x["url"]}">{e(x["titre"])}</a>' for x in FRATRIE[a["fb"]])))
    if a["type"] != "portee" and demi_fratrie(a, r):
        faits.append((T("Demi-frères et sœurs", "Half-siblings"), demi_fratrie(a, r)))
    fhtml = "".join(f'<div><span class="label">{k}</span><span>{v}</span></div>' for k, v in faits)
    rubrique = {"repro": (T("Nos reproductrices", "Our breeding queens"), "nos-chats/"), "retraite": (T("Nos retraités", "Our retired cats"), "nos-chats/"),
                "ancienne": (T("Nos anciennes reproductrices", "Our former queens"), "nos-chats/"),
                "male": (T("Nos anciens reproducteurs", "Our former studs"), "nos-chats/"), "exterieur": (T("Pères venus d’ailleurs", "Visiting studs"), "nos-chats/"), "chaton": (T("Nos chatons", "Our kittens"), "chatons/"),
                "portee": (T("Nos portées", "Our litters"), "portees/"), "grandi": (T("Ils ont grandi", "All grown up"), "ils-ont-grandi/")}[a["type"]]
    sous = " · ".join(x for x in [a["sexe"], rb(a["robe"])] if x) or f'{len(a["photos"])} photos'
    corps = f"""{entete_album(r, a, a["titre"], f'<a href="{r}{rubrique[1]}">{rubrique[0]}</a>', e(sous))}
<section class="album-page"><div class="wrap">
<div class="head"><div class="facts">{fhtml}</div></div>
{f'<p class="center" style="margin:-24px 0 56px"><a class="btn" href="{r}contact/?chaton={a["titre"].replace(" ", "+")}#formulaire">{T("Ce chaton m’intéresse", "I’m interested in this kitten")}</a></p>' if a["type"] == "chaton" and "à réserver" in (a["statut_fr"] or "") else ""}
</div>{film(r, a)}<div class="wrap">
{galerie(r, a)}
{palmares(a["fb"])}
{mots_famille(a)}{temoignage(r, a) if a["type"] == "grandi" else ""}
<p class="prot">{T("Photos réduites et marquées. Elles appartiennent à la Chatterie des Innamorati et ne peuvent pas être reprises dans une annonce.", "Photos are downsized and watermarked. They belong to the Chatterie des Innamorati and may not be used in any listing.")}</p>
</div></section>"""
    page(a["url"].rstrip("/"), f'{a["titre"]} · Chatterie des Innamorati', corps, sombre_entete=True,
         desc=T(f'{a["titre"]}, Sacré de Birmanie de la Chatterie des Innamorati. {a["robe"]}.',
                f'{a["titre"]}, Birman cat from the Chatterie des Innamorati in Bordeaux, France. {rb(a["robe"])}.'.replace(". .", ".")), image=a["cover"])

# ---------- Portées (regroupement des chatons par parents et par année) ----------
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
    titre = f'{lien_chat(k0["mere"], "../")} × {lien_chat(k0["pere"], "../")}' if k0["mere"] else T(f"Autres chatons de {an}", f"Other kittens of {an}")
    pa = album_portee(k0["mere"], an[:4])
    lien_p = f' · <a href="../{pa["url"]}">{T("album de la portée", "litter album")}</a>' if pa else ""
    cartes = "".join(carte("../", k) for k in kits)
    litter_html.append(f'<div class="litter" id="{ancre_portee((mere, pere, an))}"><h2>{titre}</h2><span>{((T("Nés le ", "Born ") + date_fr(k0["ne"])) if k0["ne"] else date_fr(k0["debut"], False).capitalize())} · {len(kits)} {T("chaton", "kitten")}{"s" if len(kits) > 1 else ""}{lien_p}</span></div><div class="grid g4">{cartes}</div>')
page("portees", T("Nos portées · Chatterie des Innamorati", "Our Birman litters · Chatterie des Innamorati"),
     f'<section><div class="wrap">{tete(T("Nos portées", "Our litters"), T("Toutes nos portées depuis 2016", "Every litter since 2016"), T("Chaque portée avec ses parents et ses chatons. Touchez un chaton pour ouvrir son album, du premier jour à l’âge adulte.", "Each litter with its parents and kittens. Tap a kitten to open its album, from day one to adulthood."))}{"".join(litter_html)}</div></section>',
     desc=T("Toutes les portées de Sacrés de Birmanie nées à la Chatterie des Innamorati depuis 2016.", "Every Birman litter born at the Chatterie des Innamorati in Bordeaux, France, since 2016, with parents and kitten albums."))

# ---------- Chatons disponibles ----------
dispo = [BY[f] for f in CFG["chatons_disponibles"]]
groupes = OrderedDict()
for k in dispo: groupes.setdefault((cle_nom(k["mere"]), cle_nom(k["pere"])), []).append(k)
blocs = []
for _, kits in sorted(groupes.items(), key=lambda kv: age(kv[1][0]), reverse=True):
    m, p = kits[0]["mere"], kits[0]["pere"]
    cartes = "".join(carte("../", k, f'<span class="status{" libre" if "réserver" in k["statut_fr"] else ""}">{e(k["statut"].capitalize())}</span>') for k in kits)
    blocs.append(f'<div class="litter"><h2>{lien_chat(m, "../")} × {lien_chat(p, "../")}</h2><span>{(T("Nés le ", "Born ") + date_fr(kits[0]["ne"])) if kits[0]["ne"] else T("Nés en ", "Born in ") + date_fr(kits[0]["debut"], False)}</span></div><div class="grid g4">{cartes}</div>')
page("chatons", T("Nos chatons · Chatterie des Innamorati", "Birman kittens for adoption · Chatterie des Innamorati, France"),
     f'<section><div class="wrap">{tete(T("Nos chatons", "Our kittens"), T("Les chatons de 2026", "Our 2026 kittens"), T("Chaque chaton a son album, mis à jour chaque semaine jusqu’à son départ, puis enrichi par les photos de sa famille. Pour réserver, écrivez-nous.", "Every kitten has its own album, updated each week until it leaves, then enriched by photos from its new family. To reserve a kitten, write to us."))}{"".join(blocs)}<p class="center" style="margin-top:64px"><a class="btn" href="../adopter/">{T("Adopter un chaton", "Adopt a kitten")}</a></p></div></section>',
     desc=T("Chatons Sacrés de Birmanie disponibles à la Chatterie des Innamorati, Bordeaux.", "Birman kittens available at the Chatterie des Innamorati, a LOOF-registered cattery in Bordeaux, France: parents, photos and status of each kitten."))

# ---------- Nos chats ----------
def bloc(titre, texte, liste):
    liste = sorted(liste, key=age, reverse=True)  # du plus jeune au plus ancien
    return f'<div class="litter"><h2>{titre}</h2><span>{texte}</span></div><div class="grid g3">{"".join(carte("../", a) for a in liste)}</div>'
cathy = CFG["males_amie"]
males_txt = T(f'<p class="note">Nos chatons ont aussi pour pères les mâles de notre amie {e(cathy["nom"])} : {", ".join(lien_chat(c, "../") for c in cathy["chats"])}.</p>',
               f'<p class="note">Some of our kittens are also sired by the studs of our friend {e(cathy["nom"])}: {", ".join(lien_chat(c, "../") for c in cathy["chats"])}.</p>')
eros_txt = T('<div class="litter"><h2>Eros, notre premier Birman</h2><span>Celui par qui tout a commencé</span></div><p class="note" style="margin-top:0">Eros n’était pas au standard de la race et n’a jamais reproduit. Il a été notre adoré chat de compagnie, et c’est grâce à lui que nous sommes tombés amoureux du Sacré de Birmanie.</p>',
             '<div class="litter"><h2>Eros, our first Birman</h2><span>The one who started it all</span></div><p class="note" style="margin-top:0">Eros was not up to the breed standard and never bred. He was our beloved pet, and thanks to him we fell in love with the Birman.</p>')
corps = (f'<section><div class="wrap">{tete(T("Nos chats", "Our cats"), T("Ceux qui font la maison", "The heart of our home"), T("Nos reproductrices actuelles, nos retraités qui vivent toujours avec nous, et tous ceux qui ont construit l’élevage.", "Our current breeding queens, our retired cats who still live with us, and all those who built the cattery."))}'
         + bloc(T("Nos reproductrices", "Our breeding queens"), T("Elles vivent avec nous et donnent naissance à nos chatons", "They live with us and give birth to our kittens"), [BY[f] for f in CFG["reproductrices"]])
         + bloc(T("Nos retraités", "Our retired cats"), T("Stérilisés, ils profitent de la maison", "Neutered and spayed, they enjoy family life"), [BY[f] for f in CFG["retraites_maison"]])
         + bloc(T("Nos anciennes reproductrices", "Our former queens"), T("Retraitées dans des familles aimantes", "Retired to loving families"), [BY[f] for f in CFG["anciennes_reproductrices"]])
         + bloc(T("Nos anciens reproducteurs", "Our former studs"), T("Les mâles qui ont vécu chez nous", "The males who lived with us"), [BY[f] for f in CFG["anciens_males"]])
         + bloc(T("Pères venus d’ailleurs", "Visiting studs"), T("Ils n’ont pas vécu chez nous mais sont les pères de nos chatons", "They did not live with us but sired some of our kittens"), [BY[f] for f in CFG["males_exterieurs"]])
         + males_txt + eros_txt + "</div></section>")
page("nos-chats", T("Nos chats · Chatterie des Innamorati", "Our Birman cats · Chatterie des Innamorati"), corps,
     desc=T("Les reproducteurs et retraités de la Chatterie des Innamorati.", "The breeding cats and retired cats of the Chatterie des Innamorati, Birman cattery in Bordeaux, France: titles, show results and pedigrees."))

# ---------- Ils ont grandi ----------
grandis = sorted([a for a in chats if a["type"] == "grandi"], key=lambda a: a["debut"], reverse=True)
par_an = OrderedDict()
for a in grandis: par_an.setdefault(a["debut"][:4], []).append(a)
nav_an = "".join(f'<a href="#a{an}">{an}</a>' for an in par_an)
blocs = "".join(f'<div class="litter" id="a{an}"><h2>{an}</h2><span>{len(l)} {T("chatons", "kittens")}</span></div><div class="grid g4">{"".join(carte("../", a) for a in l)}</div>' for an, l in par_an.items())
page("ils-ont-grandi", T("Ils ont grandi · Chatterie des Innamorati", "All grown up · Chatterie des Innamorati"),
     f'<section><div class="wrap">{tete(T("Ils ont grandi", "All grown up"), T(f"{len(grandis)} chatons nés chez nous", f"{len(grandis)} kittens born with us"), T("Nos anciens chatons, du premier jour à l’âge adulte. Les albums continuent de s’enrichir grâce aux photos de leurs familles.", "Our former kittens, from day one to adulthood. Their albums keep growing thanks to photos from their families."))}<nav class="years">{nav_an}</nav>{blocs}</div></section>',
     desc=T("Les anciens chatons de la Chatterie des Innamorati, de chatons à adultes.", "The former kittens of the Chatterie des Innamorati, Birman cats photographed from kittenhood to adulthood."))

# ---------- Expositions ----------
PALM_TOUT = sorted(json.load(open(os.path.join(ROOT, "data/palmares.json"), encoding="utf-8")), key=lambda x: x["date"])
expos = sorted([a for a in albums if a["type"] == "expo"], key=lambda a: a["nom"], reverse=True)
for a in expos:
    r = "../../"
    resultats = e(a["description"]).replace("\n", "<br>")
    if L == "en":  # les textes Facebook sont en français : en anglais, les résultats relevés dans le palmarès
        d0 = datetime.date.fromisoformat(a["nom"][:10])
        res_en = OrderedDict()
        for x in PALM_TOUT:
            if -1 <= (datetime.date.fromisoformat(x["date"]) - d0).days <= 4:
                res_en.setdefault((x["nom"], x["fb"]), []).append(x["res"].replace(" + ", " · "))
        resultats = "<br>".join(f'{lien_chat(BY[fb]["titre"], r) if fb in BY else e(nom)}: {e(" / ".join(dict.fromkeys(v)))}' for (nom, fb), v in res_en.items())
    lieu = re.sub(r"^[0-9-]+( à [0-9]+| & [0-9]+)? ", "", a["titre"])
    corps = f"""{entete_album(r, a, lieu, f'<a href="{r}expositions/">{T("Expositions", "Cat shows")}</a>', f'{date_fr(a["nom"][:10])} · {len(a["photos"])} photos')}
<section class="album-page"><div class="wrap">
{f'<div class="results">{resultats}</div>' if resultats else ''}
</div>{film(r, a)}<div class="wrap">
{galerie(r, a)}
</div></section>"""
    page(a["url"].rstrip("/"), f'{a["titre"]} · {T("Expositions", "Cat shows")}', corps, image=a["cover"], sombre_entete=True,
         desc=T(f'{lieu}, {date_fr(a["nom"][:10])} : résultats et photos des Sacrés de Birmanie de la Chatterie des Innamorati.', f'{lieu}, {date_fr(a["nom"][:10])}: results and photos of the Chatterie des Innamorati Birman cats.'))
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
    quand = T(f'{j} {MOIS[sh["fin"].month - 1]} {sh["fin"].year}', f'{MOIS[sh["fin"].month - 1]} {j}, {sh["fin"].year}')
    chats_h = "".join(f'<span>{lien_chat(BY[fb]["titre"], "../") if fb in BY else e(nom)}{T(" : ", ": ")}'
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
    blocs.append(f'<div class="litter"><h2>{T("Saison", "Season")} {s}</h2><span>{n} {T("exposition", "show")}{"s" if n > 1 else ""}{T(f" · {len(l)} en photos", f" · {len(l)} with photos") if l and autres else ""}</span></div>{grille}{sans}')
page("expositions", T("Expositions · Chatterie des Innamorati", "Cat shows · Chatterie des Innamorati, Birman cats"),
     f'<section><div class="wrap">{tete(T("Expositions", "Cat shows"), T("Douze saisons d’expositions", "Twelve show seasons"), T("Chaque hiver et chaque printemps, nous présentons nos chats en exposition FIFe et LOOF. Les résultats et les photos de chaque week-end.", "Every winter and spring we show our cats at FIFe and LOOF cat shows. Here are the results and photos of each weekend."))}{"".join(blocs)}</div></section>',
     desc=T("Résultats et photos des expositions félines de la Chatterie des Innamorati.", "Cat show results and photos of the Chatterie des Innamorati Birman cats, FIFe and LOOF shows in France, Italy and Spain since 2014."))

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
            leg = f'Photo{T(" : ", ": ")}<a href="../{chat["url"]}">{e(chat["titre"])}</a>' if isinstance(chat, dict) else e(chat)
            visuel = img("../", pid, T(f'Sacré de Birmanie {c["robe"].lower()} : ', f'{rb(c["robe"])} Birman cat: ') + (chat["titre"] if isinstance(chat, dict) else chat))
        else:
            leg = T("Photo à venir", "Photo coming soon")
            visuel = f'<div class="ph vide"><span>{leg}</span></div>'
        cartes.append(f'<div class="card coul" id="{slug_robe(c["robe"])}">{visuel}<div class="t"><h3>{e(rb(c["robe"]))}</h3><span class="robe">{e(c["texte"])}</span><span class="ex">{leg}</span></div></div>')
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
            cellules.append(f'<td class="na" title="{T("N’existe pas : le red et le cream sont déjà des couleurs rousses", "Does not exist: red and cream are already red-based colors")}">–</td>')
            continue
        robe = f"{base} {suff}"
        t = TETES.get(robe.lower())
        chat = t and PHOTO_CHAT.get(t["photo"])
        if chat:
            cible = f'#{ANCRES[robe.lower()]}' if robe.lower() in ANCRES else f'../{chat["url"]}'
            vis = f'<a class="rc-ph" href="{cible}" title="{e(rb(robe))}{T(" : ", ": ")}{e(chat["titre"])}"><img src="../photos/{t["fichier"]}" alt="{e(rb(robe))}" loading="lazy"></a>'
        else:
            vis = f'<span class="rc-dot" style="background:{pastille(fonce, roux, motif)}" title="{e(rb(robe))}"></span>'
        cellules.append(f'<td>{vis}</td>')
    lignes.append(f'<tr><th scope="row">{lib}</th>{"".join(cellules)}</tr>')
recap_txt = T('''<div class="recap"><div class="litter"><h2>Les 40 couleurs en un coup d’œil</h2><span>En photo : nos chats, adultes de préférence. En pastille : les couleurs qui ne sont pas encore nées chez nous.</span></div>@TABLE@
<div class="recap-regles"><div><b>Ce qui ne change jamais</b><span>Des yeux bleus, toujours. Quatre gants blancs. Un corps clair aux extrémités colorées.</span></div>
<div><b>Ce qui n’existe pas chez le Birman</b><span>Les yeux verts ou dorés, les robes bicolores ou à masque blanc, les robes unies sans « point ». Un chat ainsi n’est pas un Sacré de Birmanie.</span></div>
<div><b>Le tortie</b><span>Il mêle une couleur et du roux. Il n’existe donc pas en red ni en cream, et concerne presque uniquement les femelles.</span></div></div></div>''',
'''<div class="recap"><div class="litter"><h2>All 40 colors at a glance</h2><span>Photos: our own cats, adults whenever possible. Swatches: colors not yet born in our cattery.</span></div>@TABLE@
<div class="recap-regles"><div><b>What never changes</b><span>Blue eyes, always. Four white gloves. A pale body with colored points.</span></div>
<div><b>What does not exist in the Birman</b><span>Green or golden eyes, bicolor or white-faced coats, solid coats without points. A cat like this is not a Birman.</span></div>
<div><b>Tortie</b><span>It mixes a color with red. So it does not exist in red or cream, and occurs almost only in females.</span></div></div></div>''')
recap = recap_txt.replace("@TABLE@", f'''
<div class="recap-scroll"><table class="recap-t"><thead><tr><th></th>{"".join(f'<th scope="col">{rb(b)}</th>' for b, _, _ in BASES)}</tr></thead><tbody>{"".join(lignes)}</tbody></table></div>''')
faq_html, faq_ld = faq(T("Les couleurs du Birman en questions", "Birman cat colors: your questions"), COULEURS["faq"])
page("couleurs", T("Couleurs du Sacré de Birmanie : les 40 robes en photos · des Innamorati", "Birman cat colors: all 40 colors in photos · des Innamorati"),
     f'''<section><div class="wrap">{tete(T("Les couleurs", "Colors"), T("Toutes les couleurs du Sacré de Birmanie", "All the colors of the Birman cat"), COULEURS["intro"])}
{recap}
<div class="std std4">{comprendre}</div>
<nav class="sommaire" aria-label="{T("Familles de couleurs", "Color groups")}">{"".join(f'<a href="#{slug_robe(f["nom"])}">{e(f["nom"])}</a>' for f in COULEURS["familles"])}</nav>
{"".join(b.replace('<div class="litter">', f'<div class="litter" id="{slug_robe(f["nom"])}">', 1) for b, f in zip(blocs, COULEURS["familles"]))}
<p class="note">{COULEURS["note"]}</p></div></section>{faq_html}''',
     desc=T("Les 40 couleurs du Sacré de Birmanie en photos : seal, blue, chocolat, lilac, red et cream, point, tabby, tortie, silver et smoke. Reconnaître la couleur d'un chaton.",
            "All 40 Birman cat colors (colours) in photos: seal, blue, chocolate, lilac, red and cream, point, tabby, tortie, silver and smoke. How to tell a Birman kitten's color."),
     image="partage-couleurs", image_alt=T("Les couleurs du Sacré de Birmanie : têtes de Birmans seal, blue, chocolat, lilac, red, tabby, tortie et silver", "Birman cat colors: seal, blue, chocolate, lilac, red, tabby, tortie and silver Birman heads"), og_type="article",
     ld=[{"@context": "https://schema.org", "@type": "Article", "headline": T("Toutes les couleurs du Sacré de Birmanie", "All the colors of the Birman cat"), "inLanguage": L,
          "description": T("Les 40 couleurs reconnues du Sacré de Birmanie, en photos de chats de la Chatterie des Innamorati.", "The 40 recognized Birman cat colors, shown with photos of cats from the Chatterie des Innamorati."),
          "image": [SITE + "photos/partage-couleurs.jpg"] + [SITE + "photos/" + x["fichier"] for x in TETES.values()],
          "author": {"@type": "Person", "name": "Magali Perrier"}, "publisher": {"@id": SITE + "#elevage"},
          "mainEntityOfPage": lien("couleurs/"), "about": {"@type": "Thing", "name": T("Sacré de Birmanie", "Birman cat"), "sameAs": T("https://fr.wikipedia.org/wiki/Sacr%C3%A9_de_Birmanie", "https://en.wikipedia.org/wiki/Birman")}},
         faq_ld, ariane((T("Accueil", "Home"), ""), (T("Couleurs", "Colors"), "couleurs/"))], prio=0.9)

json.dump({"albums": len(albums), "chats": len(chats), "grandis": len(grandis), "portees": len(litters), "expos": len(expos)},
          open(os.path.join(ROOT, "data/stats.json"), "w"))
