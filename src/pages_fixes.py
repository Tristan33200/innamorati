# Pages rédigées à la main. Exécuté à la fin de build.py (mêmes fonctions et données).
P = {  # photos choisies (numéros de l'export Facebook)
    "hero": "2084329241748221", "sanae": "2084329255081553", "oedipe": "1335020643345755", "regard": "902865393227951",
    "magali": "551069241740903", "enfant": "753369611510864", "expo_yeux": "2077785872402558", "milan": "1190960814418406",
    "presentation": "1456228661224952", "table": "1391940180987134", "carre": "2077785365735942", "nw2019": "1418632404984578",
    "oedipe9": "1300215273492959", "rosettes": "1216272991887188", "bianca": "1707822147123326",
}
st = json.load(open(os.path.join(ROOT, "data/stats.json")))


def grand(r, pid, alt, style=""):
    st = ' style="' + style + '"' if style else ""
    return f'<div class="ph"><img src="{r}photos/{pid}.jpg" alt="{e(alt)}"{st}></div>'


# ---------- Accueil ----------
r = ""
kits = "".join(carte(r, BY[f], f'<span class="status{" libre" if "réserver" in BY[f]["statut"] else ""}">{e(BY[f]["statut"].capitalize())}</span>') for f in CFG["chatons_disponibles"][:4])
corps = f"""
<div class="hero">
  {grand(r, P["hero"], "Les yeux saphir de Sanae des Innamorati")}
  <div class="wrap"><h1>Le regard saphir</h1><p>Chatterie des Innamorati · Sacrés de Birmanie</p><a class="btn light" href="chatons/">Nos chatons</a></div>
</div>
<section class="center"><div class="wrap">
  <div class="narrow intro">
    <p class="label">Élevage familial depuis 2016</p>
    <h2>Des Birmans de champions, élevés au cœur d'une famille</h2>
    <div class="rule"></div>
    <p>Chez nous, les chats ne vivent pas en chatterie. Ils partagent la maison, les canapés et les jeux de nos enfants. Les chatons naissent et grandissent au milieu de la vie de famille, ce qui en fait des compagnons confiants et doux.</p>
    <p>Depuis 2016, {st["grandis"]} chatons des Innamorati ont rejoint leur famille, et nos chats ont été titrés de Paris à Milan.</p>
  </div>
  <div class="doors">
    <a class="door" href="chatons/">{grand(r, P["bianca"], "Bianca des Innamorati")}<h3>Nos chatons</h3><span class="label">Portées 2026</span></a>
    <a class="door" href="nos-chats/">{grand(r, P["sanae"], "Sanae des Innamorati")}<h3>Nos chats</h3><span class="label">Reproductrices et retraités</span></a>
    <a class="door" href="couleurs/">{grand(r, P["regard"], "Birman aux yeux bleus")}<h3>Les couleurs</h3><span class="label">Toutes les robes du Birman</span></a>
  </div>
</div></section>
<div class="band">{grand(r, P["oedipe"], "Œdipe des Innamorati et ses trophées")}
  <blockquote><p>« Nous ne cherchons pas à gagner de l'argent. Nous voulons donner une belle vie à nos chats. »</p><cite>Magali &amp; Tristan</cite></blockquote></div>
<section><div class="wrap">
  <div class="head"><p class="label">Nos chatons</p><h2>Les portées de 2026</h2><p>Chaque chaton a son album, enrichi au fil de sa vie par nos photos puis par celles de ses adoptants.</p></div>
  <div class="grid g4">{kits}</div>
  <p class="center" style="margin-top:56px"><a class="btn" href="chatons/">Voir tous les chatons</a> <a class="btn" href="portees/">Toutes nos portées</a></p>
</div></section>
<section class="palm"><div class="wrap">
  <div class="head"><p class="label">Palmarès</p><h2>Dix saisons d'expositions</h2><p>Chaque hiver et chaque printemps, nous présentons nos chats en exposition : Paris, Bordeaux, Biarritz, Nantes, Rome, Milan, Valladolid.</p></div>
  <div class="palm-grid">{grand(r, P["nw2019"], "Œdipe des Innamorati, National Winner 2019")}
    <div><ul class="titles-list">
      <li><div><b><a href="{BY['204']['url']}">Œdipe des Innamorati</a></b><span>Mâle seal point · Best in Show à Nantes, 2021</span></div><em>GIC · NW · JW · DVM</em></li>
      <li><div><b><a href="{BY['148']['url']}">Simone de Beauvoir des Innamorati</a></b><span>Femelle seal tabby point</span></div><em>IC</em></li>
      <li><div><b><a href="{BY['143']['url']}">Sanae des Innamorati</a></b><span>Femelle blue point</span></div><em>IC</em></li>
    </ul>
    <p class="abbr">GIC Grand Champion International · IC Champion International · NW National Winner · JW Junior Winner · DVM Distinguished Variety Merit</p>
    <p style="margin-top:28px"><a class="btn light" href="expositions/">Toutes nos expositions</a></p></div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="mosaic">
    {grand(r, P["expo_yeux"], "Birman en exposition")}{grand(r, P["milan"], "Milan, exposition internationale")}{grand(r, P["presentation"], "Présentation au juge")}{grand(r, P["rosettes"], "Œdipe et ses rosettes")}{grand(r, P["table"], "Sur la table de jugement")}{grand(r, P["carre"], "Dans notre carré d'exposition")}
  </div>
</div></section>
<section style="padding-top:20px"><div class="wrap family">
  <div class="stack">{grand(r, P["magali"], "Magali et un chaton", "object-position:40% 50%")}{grand(r, P["enfant"], "Notre fille et un Birman")}</div>
  <div class="text">
    <p class="label">Notre famille</p>
    <h2>Magali, Tristan, nos enfants et nos chats</h2>
    <p>Magali est l'éleveuse de la chatterie. Infirmière diplômée et directrice de crèche, elle consacre ses soirées et ses week-ends aux chats, avec un œil exercé sur leur santé.</p>
    <p>Tristan, photographe, est présent à la maison en journée. Il veille sur les chats au quotidien, les accompagne en exposition et signe les photos de ce site.</p>
    <p>Malgré le prix de nos chatons, l'élevage reste déficitaire. C'est un choix : santé, tests, expositions et temps passé avec chaque chaton passent avant tout.</p>
    <p class="sign">Magali &amp; Tristan</p>
  </div>
</div></section>
"""
page("", "Chatterie des Innamorati · Sacrés de Birmanie à Bordeaux", corps, sombre_entete=True, image=P["hero"],
     desc="Chatterie des Innamorati : élevage familial de Sacrés de Birmanie à Bordeaux depuis 2016. Chatons, reproducteurs champions, portées et expositions.")

# ---------- Le Birman ----------
r = "../"
corps = f"""<section><div class="wrap">
{tete("Le Sacré de Birmanie", "La légende du temple de Lao-Tsun")}
<div class="birman-grid">{grand(r, P["oedipe9"], "Œdipe des Innamorati, seal point aux yeux saphir")}
<div class="text">
<p>On raconte qu'au temple de Lao-Tsun vivait le prêtre Mun-Ha et son chat Sinh. Lorsque le prêtre mourut devant la déesse aux yeux de saphir, Sinh posa ses pattes sur son maître. Sa robe prit les reflets dorés de la déesse, ses yeux devinrent bleus, et ses pattes restèrent d'un blanc pur.</p>
<p>L'histoire réelle s'écrit en France dans les années 1920, où les premiers Birmans sont présentés et enregistrés. La race frôle l'extinction pendant la Seconde Guerre mondiale, puis est reconstruite par des éleveurs français avant d'être reconnue dans le monde entier.</p>
<p>Le Birman est un chat de taille moyenne à grande, au poil mi-long soyeux, sans sous-poil laineux, donc facile à entretenir. Son caractère est doux, sociable et très attaché à sa famille, à l'aise avec les enfants.</p>
<div class="std">
<div><b>Les gants</b><span>Blancs, nets et symétriques aux pattes avant, arrêtés à l'articulation.</span></div>
<div><b>Les éperons</b><span>Aux pattes arrière, le blanc remonte en pointe sous le talon.</span></div>
<div><b>Les yeux</b><span>Ronds, d'un bleu saphir le plus profond possible.</span></div>
<div><b>Les couleurs</b><span>Seal, blue, chocolat, lilac, red, cream, en tabby, tortie, silver ou smoke. <a href="../couleurs/">Voir toutes les couleurs</a>.</span></div>
</div></div></div>
<p class="note">Ce texte est un point de départ : Magali l'enrichira de ses sources et de son expérience d'éleveuse.</p>
</div></section>"""
page("le-birman", "Le Sacré de Birmanie · Chatterie des Innamorati", corps, desc="Histoire, légende et standard du Sacré de Birmanie.")

# ---------- Adopter ----------
corps = f"""<section><div class="wrap">
{tete("Adopter un chaton", "Ce que vous adoptez vraiment", "Nos chatons partent à 13 semaines minimum, après des mois de soins, de socialisation et de suivi vétérinaire.")}
<div class="adopt"><div>
<p class="price">1 800 €</p><p class="price-note">Chaton de compagnie, tout compris</p>
<ul class="incl"><li>Pedigree LOOF</li><li>Identification par puce électronique</li><li>Vaccins, vermifuges et certificat vétérinaire</li><li>Parents testés et suivis</li><li>Contrat de cession et document d'information</li><li>Album photo et suivi pour toute sa vie</li></ul>
</div>
<ol class="steps">
<li><span class="n">i.</span><div><b>Nous faire connaissance</b><p>Vous nous écrivez. Nous parlons de votre foyer, de votre rythme et du chaton qui vous ressemble.</p></div></li>
<li><span class="n">ii.</span><div><b>Rencontrer nos chats</b><p>Vous venez à la maison découvrir les parents et la vie de nos chats en famille.</p></div></li>
<li><span class="n">iii.</span><div><b>Réserver</b><p>Un acompte réserve votre chaton. Vous recevez ses photos semaine après semaine.</p></div></li>
<li><span class="n">iv.</span><div><b>L'accueillir</b><p>À 13 semaines, il rejoint votre foyer. Nous restons là pour vous, et ses photos continuent d'enrichir son album.</p></div></li>
</ol></div>
</div></section>
<section class="verify" id="verifier"><div class="wrap">
<div class="head" style="margin-bottom:0"><p class="label">Vérifier une annonce</p><h2>Nos photos circulent parfois dans de fausses annonces</h2></div>
<div class="verify-grid">
<div><b>Nos chatons sont ici</b><p>Seuls les chatons présentés sur la page <a href="../chatons/">Nos chatons</a> sont à l'adoption. Une annonce Leboncoin avec nos photos sous un autre nom est une arnaque.</p></div>
<div><b>Un vrai éleveur a un SIRET</b><p>Toute annonce de chaton en France doit l'afficher. Le nôtre : <span class="siret">{SIRET}</span>.</p></div>
<div><b>Un doute ? Écrivez-nous</b><p>Envoyez-nous le lien de l'annonce. Nous vous répondons et la signalons.</p></div>
</div></div></section>
<section class="center"><div class="wrap"><a class="btn" href="../contact/">Nous écrire</a></div></section>"""
page("adopter", "Adopter un chaton · Chatterie des Innamorati", corps, desc="Adopter un chaton Sacré de Birmanie : prix, ce qui est inclus, déroulement.")

# ---------- Contact ----------
corps = f"""<section><div class="wrap contact">
<div class="text"><p class="label">Contact</p><h1>Parlons de votre futur Birman</h1>
<p>Magali vous répond personnellement, le soir et le week-end.</p>
<p>Chatterie des Innamorati<br>Bordeaux, Gironde</p>
<p>Facebook : <a href="https://www.facebook.com/desinnamorati" target="_blank" rel="noopener">facebook.com/desinnamorati</a><br>Messenger : <a href="https://m.me/desinnamorati" target="_blank" rel="noopener">m.me/desinnamorati</a></p>
</div>
<div class="text"><p class="label">Le plus simple</p>
<p>Écrivez-nous sur Messenger en précisant votre projet : le chaton qui vous intéresse, votre région et la composition de votre foyer.</p>
<p><a class="btn" href="https://m.me/desinnamorati" target="_blank" rel="noopener">Écrire sur Messenger</a></p>
</div></div></section>"""
page("contact", "Contact · Chatterie des Innamorati", corps)

# ---------- Mentions légales ----------
corps = f"""<section><div class="wrap narrow">{tete("Mentions légales", "Mentions légales")}
<div class="text legal">
<p><b>Éditeur</b><br>Magali Perrier, entreprise individuelle, élevage de Sacrés de Birmanie sous l'affixe LOOF « des Innamorati ».<br>SIRET {SIRET} · Bordeaux (33).</p>
<p><b>Photographies</b><br>Toutes les photographies sont la propriété de Tristan Perrier et de la Chatterie des Innamorati. Toute reproduction, en particulier dans des annonces de vente, est interdite et fera l'objet d'un signalement.</p>
<p><b>Hébergement</b><br>GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<p><b>Données personnelles</b><br>Ce site ne dépose aucun cookie et ne collecte aucune donnée.</p>
</div></div></section>"""
page("mentions-legales", "Mentions légales · Chatterie des Innamorati", corps)
