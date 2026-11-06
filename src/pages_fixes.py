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
kits = "".join(carte(r, BY[f], f'<span class="status{" libre" if "réserver" in BY[f]["statut"] else ""}">{e(BY[f]["statut"].capitalize())}</span>') for f in sorted(CFG["chatons_disponibles"], key=lambda f: BY[f]["debut"], reverse=True)[:4])
corps = f"""
<div class="hero">
  {grand(r, P["hero"], "Les yeux saphir de Sanae des Innamorati")}
  <div class="wrap"><p class="big">Le regard saphir</p><h1 class="kicker">Élevage de Sacrés de Birmanie à Bordeaux</h1><a class="btn light" href="chatons/">Nos chatons</a></div>
</div>
<section class="center"><div class="wrap">
  <div class="narrow intro">
    <p class="label">Élevage familial depuis 2016</p>
    <h2>Des Birmans de champions, élevés en famille à Bordeaux</h2>
    <div class="rule"></div>
    <p>La Chatterie des Innamorati est un élevage familial de Sacrés de Birmanie installé à Bordeaux, en Gironde, et déclaré au LOOF sous l'affixe « des Innamorati ». Chez nous, les chats ne vivent pas en chatterie. Ils partagent la maison, les canapés et les jeux de nos enfants. Les chatons naissent et grandissent au milieu de la vie de famille, ce qui en fait des compagnons confiants et doux.</p>
    <p>Depuis 2016, {st["grandis"]} chatons des Innamorati ont rejoint leur famille, et nos chats ont été titrés de Paris à Milan.</p>
  </div>
  <div class="doors">
    <a class="door" href="chatons/">{grand(r, P["bianca"], "Bianca des Innamorati")}<h3>Nos chatons</h3><span class="label">Portées 2026</span></a>
    <a class="door" href="nos-chats/">{grand(r, P["sanae"], "Sanae des Innamorati")}<h3>Nos chats</h3><span class="label">Reproductrices et retraités</span></a>
    <a class="door" href="couleurs/">{grand(r, P["regard"], "Birman aux yeux bleus")}<h3>Les couleurs</h3><span class="label">Toutes les robes du Birman</span></a>
  </div>
</div></section>
<div class="band">{grand(r, P["oedipe"], "Œdipe des Innamorati et ses trophées")}
  <blockquote><p>« Ici, rien ne passe avant le bonheur de nos chats. »</p><cite>Magali &amp; Tristan</cite></blockquote></div>
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
    <p>Tristan, <a href="https://tristanperrier.fr" target="_blank" rel="noopener">photographe</a>, est présent à la maison en journée. Il veille sur les chats au quotidien, les accompagne en exposition et signe la plupart des photos de ce site. Les autres nous sont envoyées par les familles de nos chatons.</p>
    <p>Malgré le prix de nos chatons, l'élevage reste déficitaire. C'est un choix : santé, tests, expositions et temps passé avec chaque chaton passent avant tout.</p>
    <p class="sign">Magali &amp; Tristan</p>
  </div>
</div></section>
"""
faq_html, faq_ld = faq("Adopter un Sacré de Birmanie à Bordeaux", [
    ("Où trouver un chaton Sacré de Birmanie à Bordeaux ?", 'Notre élevage familial se trouve à Bordeaux, en Gironde. Nos chatons disponibles sont présentés sur la page <a href="chatons/">Nos chatons</a>, avec leurs parents et leur album photo. Nous recevons les familles à la maison pour rencontrer les chats.'),
    ("Quel est le prix d'un chaton Sacré de Birmanie ?", "Nos chatons sont proposés à 1 800 €. Ce prix comprend le pedigree LOOF, la puce électronique, les vaccins, les vermifuges, le certificat vétérinaire et la stérilisation."),
    ("À quel âge partent les chatons ?", "Nos chatons rejoignent leur famille entre 15 semaines et 4 mois et demi. Ils partent déjà stérilisés, sociabilisés et habitués à la vie de famille."),
    ("Vos chatons sont-ils inscrits au LOOF ?", "Oui. Tous nos chatons sont inscrits au LOOF, le livre officiel des origines félines, sous l'affixe « des Innamorati ». En France, seul un chat inscrit au LOOF peut être vendu comme Sacré de Birmanie."),
    ("Comment éviter les fausses annonces ?", 'Nos photos sont parfois volées pour de fausses annonces. Vérifiez toujours le SIRET de l\'éleveur et la présence du chaton sur son site. Notre page <a href="adopter/#verifier">Vérifier une annonce</a> explique comment faire.'),
])
corps += faq_html
page("", "Sacré de Birmanie à Bordeaux · Chatterie des Innamorati, éleveur LOOF", corps, sombre_entete=True, image=P["hero"], prio=1.0,
     desc="Chatterie des Innamorati, élevage familial de Sacrés de Birmanie à Bordeaux (Gironde) depuis 2016. Chatons LOOF stérilisés, parents champions, portées et expositions.",
     ld=[{"@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "#elevage", "name": "Chatterie des Innamorati",
          "alternateName": "des Innamorati", "description": "Élevage familial de Sacrés de Birmanie (chats Birman) inscrit au LOOF.",
          "url": SITE, "image": SITE + "photos/" + P["hero"] + ".jpg", "priceRange": "1800 €", "founder": "Magali Perrier",
          "address": {"@type": "PostalAddress", "addressLocality": "Bordeaux", "addressRegion": "Gironde", "addressCountry": "FR"},
          "areaServed": ["Bordeaux", "Gironde", "Nouvelle-Aquitaine", "France"],
          "email": EMAIL, "sameAs": ["https://www.facebook.com/desinnamorati"], "identifier": "SIRET " + SIRET},
         {"@context": "https://schema.org", "@type": "WebSite", "name": "Chatterie des Innamorati", "url": SITE, "inLanguage": "fr"},
         faq_ld])

# ---------- Le Birman ----------
r = "../"
SECTIONS = [
 ("histoire", "Une histoire française", [
  "Les origines du Sacré de Birmanie restent assez obscures. Selon le récit transmis par la Fédération Féline Française, un couple de chats dérobé au temple de Lao-Tsun aurait gagné la France en 1920, à bord du yacht d'un millionnaire américain. Le mâle mourut pendant la traversée, mais la femelle, Sita, était déjà pleine.",
  "En 1926, une femelle seal point, Poupée de Maldapour, est présentée à l'exposition de Paris organisée par le Cat Club de France et de Belgique. Elle est la première Birmane inscrite. D'autres hypothèses existent : l'éleveuse Simone Poirier, de la chatterie de Crespières, pensait que la race était née du croisement d'un Siamois ganté de blanc et d'un chat à poil long.",
  "Après la Seconde Guerre mondiale, il ne restait qu'un seul couple, Orloff et Xéna de Kaaba. D'après les livres d'origines, tous les Birmans d'aujourd'hui descendent d'eux. Depuis plus de soixante-dix ans, la race a gardé les mêmes traits distinctifs."]),
 ("physique", "Le physique du Birman", [
  "Le Birman est un chat massif, au corps allongé, porté par des pattes courtes et fortes. Sa tête est puissante, avec des joues pleines et rondes et un front légèrement bombé. Son nez court a un léger profil romain : ni droit comme celui du Siamois, ni « stoppé » comme celui du Persan. Ses grands yeux ronds ou légèrement ovales sont du bleu le plus intense possible.",
  "Sa robe soyeuse est très longue sur le dos et les flancs. Courte sur la face, elle s'allonge sur les joues en une collerette abondante. Le corps est très clair, couleur coquille d'œuf, le dos beige doré, le ventre blanc cassé, et les extrémités sont plus foncées. Sa queue, en panache, est souvent portée haute."]),
 ("caractere", "Son caractère", [
  "Calme et posé sans être inactif, le Birman est très joueur : il n'est pas rare qu'il apporte sa plume pour réclamer une partie. C'est un vrai « chat-chien », qui suit ses humains partout et n'aime pas les portes fermées. Il parle peu, d'une voix douce, et il est sensible à l'humeur de sa famille.",
  "Il adore les enfants, s'entend bien avec les chiens et voyage facilement tant qu'il est avec les siens. Il vit très bien en appartement, et profite volontiers d'un jardin pour chasser ou se dorer au soleil."]),
 ("entretien", "Entretien et santé", [
  "Sa fourrure soyeuse s'emmêle peu. Un brossage par semaine suffit à retirer les poils morts, et c'est aussi un joli moment de complicité.",
  "Le Birman est une race robuste. Chez un éleveur sérieux, les reproducteurs sont suivis avec le vétérinaire, et la sélection veille à préserver la santé autant que la beauté."]),
 ("differences", "Birman, Ragdoll ou Siamois ?", [
  "On confond souvent ces trois races aux yeux bleus. Le Siamois a le poil court et un corps fin et élancé. Le Ragdoll est plus grand et plus lourd, et ses pattes ne sont pas toujours blanches.",
  "Le Birman se reconnaît à coup sûr à ses quatre gants blancs, nets et symétriques, et à ses éperons blancs qui remontent à l'arrière des pattes postérieures."]),
 ("eleveur", "Bien choisir son éleveur", [
  "En France, un chat ne peut être vendu comme Sacré de Birmanie que s'il est inscrit au LOOF, le livre officiel des origines félines. L'éleveur doit afficher son numéro SIRET dans toutes ses annonces, et le chaton doit être identifié par puce, vacciné, et accompagné d'un certificat vétérinaire.",
  'Méfiez-vous des prix trop bas et des vendeurs qui refusent une visite : de nombreuses fausses annonces utilisent des photos volées, y compris les nôtres. Nos conseils sont sur la page <a href="../adopter/#verifier">Vérifier une annonce</a>.']),
]
sommaire = "".join(f'<a href="#{i}">{t}</a>' for i, t, _ in SECTIONS)
articles = "".join(f'<section class="art" id="{i}"><h2>{t}</h2>' + "".join(f"<p>{x}</p>" for x in ps) + "</section>" for i, t, ps in SECTIONS)
faq_html, faq_ld = faq("Le Sacré de Birmanie en questions", [
    ("Quelle est la différence entre Sacré de Birmanie et Birman ?", "Aucune : c'est la même race. Sacré de Birmanie est son nom français, Birman son nom international. On dit aussi simplement « Birman » en France."),
    ("D'où vient le Sacré de Birmanie ?", "Malgré son nom et sa légende birmane, c'est une race française. Les premiers Birmans sont présentés à Paris dans les années 1920, et tous les Birmans actuels descendent d'Orloff et Xéna de Kaaba, le seul couple qui restait après la Seconde Guerre mondiale."),
    ("Combien de temps vit un Sacré de Birmanie ?", "Le Birman est une race robuste. Bien suivi par son vétérinaire et vivant à l'intérieur, il partage souvent la vie de sa famille pendant de longues années, couramment plus de quinze ans."),
    ("Le Sacré de Birmanie perd-il beaucoup ses poils ?", "Moins que son poil mi-long le laisse penser. Sa fourrure soyeuse s'emmêle peu et un brossage par semaine suffit à retirer les poils morts."),
    ("Un Birman peut-il vivre en appartement ?", "Oui, il s'adapte très bien à la vie en appartement. Très attaché à sa famille et joueur, il a surtout besoin de compagnie et de jeux. S'il a un jardin, il en profite pour chasser et se dorer au soleil."),
    ("Mâle ou femelle : lequel choisir ?", "Une fois stérilisés, les deux font d'excellents compagnons. Le mâle est souvent plus grand et très câlin, la femelle un peu plus indépendante. Le caractère individuel compte davantage que le sexe."),
    ("Combien coûte un chaton Sacré de Birmanie ?", 'Chez nous, un chaton coûte 1 800 €, stérilisé, pucé, vacciné et inscrit au LOOF. Le détail est sur la page <a href="../adopter/">Adopter</a>.'),
])
corps = f"""<section><div class="wrap">
{tete("Le Sacré de Birmanie", "Le Sacré de Birmanie, le chat aux gants blancs", "Histoire, légende, standard, caractère et entretien : tout savoir sur le Birman, par une famille d'éleveurs qui vit avec lui depuis 2016.")}
<div class="birman-grid">{grand(r, P["oedipe9"], "Œdipe des Innamorati, Sacré de Birmanie seal point aux yeux saphir")}
<div class="text">
<p class="label">La légende</p>
<h2 class="h-art">Le temple de Lao-Tsun</h2>
<p>On raconte que le temple de Lao-Tsun, « le temple des temples », se dressait dans les hautes montagnes. Le vieux prêtre Mun-Ha y vivait avec Sinh, un chat blanc. Une nuit, des pillards attaquèrent le temple et Mun-Ha mourut devant la statue de Tsun-Kyan-Kse, la déesse aux yeux de saphir.</p>
<p>Sinh posa alors ses pattes sur son maître. Sa robe prit les reflets dorés de la déesse, ses yeux devinrent bleus comme les siens, et ses pattes, posées sur le prêtre, restèrent d'un blanc pur. Les gants du Birman seraient le souvenir de ce geste.</p>
<div class="std">
<div><b>Les gants</b><span>D'un blanc absolument pur. Ils s'arrêtent entre la base des doigts et l'articulation, sans jamais la dépasser.</span></div>
<div><b>Les éperons</b><span>Aux pattes arrière, le blanc forme une pointe sous le pied. Leur absence est éliminatoire en exposition.</span></div>
<div><b>Les yeux</b><span>Grands, ronds ou légèrement ovales, du bleu le plus intense possible.</span></div>
<div><b>Les couleurs</b><span>Quarante couleurs reconnues, toujours en colourpoint. <a href="../couleurs/">Voir toutes les couleurs</a>.</span></div>
</div></div></div>
<nav class="sommaire" aria-label="Sommaire">{sommaire}</nav>
<div class="articles">{articles}</div>
<p class="note">Sources : <a href="https://www.fff-asso.fr/race/sacre-de-birmanie/" rel="noopener" target="_blank">Fédération Féline Française</a> et <a href="https://cfsbi.fr/portfolio-item/d-une-legende-a-la-realite/" rel="noopener" target="_blank">Club Français du Sacré de Birmanie (CFSBI)</a>.</p>
</div></section>{faq_html}"""
page("le-birman", "Sacré de Birmanie : histoire, caractère, standard et entretien du Birman", corps, image=P["oedipe9"], prio=0.9,
     desc="Tout savoir sur le Sacré de Birmanie (Birman) : légende de Lao-Tsun, histoire de la race, standard, gants blancs, caractère, entretien, santé et différences avec le Ragdoll.",
     ld=[{"@context": "https://schema.org", "@type": "Article", "headline": "Le Sacré de Birmanie, le chat aux gants blancs",
          "image": SITE + "photos/" + P["oedipe9"] + ".jpg", "inLanguage": "fr", "author": {"@type": "Person", "name": "Magali Perrier"},
          "publisher": {"@id": SITE + "#elevage"}, "mainEntityOfPage": SITE + "le-birman/"},
         ariane(("Accueil", ""), ("Le Sacré de Birmanie", "le-birman/")), faq_ld])

# ---------- Adopter ----------
corps = f"""<section><div class="wrap">
{tete("Adopter un chaton", "Ce que vous adoptez vraiment", "Nos chatons partent entre 15 semaines et 4 mois et demi, stérilisés, après des mois de soins, de socialisation et de suivi vétérinaire.")}
<div class="adopt"><div>
<p class="price">1 800 €</p><p class="price-note">Chaton de compagnie, tout compris</p>
<ul class="incl"><li>Pedigree LOOF</li><li>Stérilisation déjà faite</li><li>Identification par puce électronique</li><li>Vaccins, vermifuges et certificat vétérinaire</li><li>Parents testés et suivis</li><li>Contrat de cession et document d'information</li><li>Album photo et suivi pour toute sa vie</li></ul>
</div>
<ol class="steps">
<li><span class="n">i.</span><div><b>Nous faire connaissance</b><p>Vous nous écrivez. Nous parlons de votre foyer, de votre rythme et du chaton qui vous ressemble.</p></div></li>
<li><span class="n">ii.</span><div><b>Rencontrer nos chats</b><p>Vous venez à la maison découvrir les parents et la vie de nos chats en famille.</p></div></li>
<li><span class="n">iii.</span><div><b>Réserver</b><p>Un acompte réserve votre chaton. Vous recevez ses photos semaine après semaine.</p></div></li>
<li><span class="n">iv.</span><div><b>L'accueillir</b><p>Entre 15 semaines et 4 mois et demi, stérilisé, il rejoint votre foyer. Nous restons là pour vous, et ses photos continuent d'enrichir son album.</p></div></li>
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
page("adopter", "Adopter un chaton Sacré de Birmanie à Bordeaux · des Innamorati", corps, desc="Adopter un chaton Sacré de Birmanie LOOF près de Bordeaux : 1 800 €, stérilisé, pucé, vacciné, départ entre 15 semaines et 4 mois et demi. Déroulement et vérification des annonces.", ld=[ariane(("Accueil", ""), ("Adopter", "adopter/"))], prio=0.8)

# ---------- Contact ----------
r = "../"
chatons_opts = "".join(f'<option>{e(BY[f]["titre"])}</option>' for f in CFG["chatons_disponibles"] if "à réserver" in (BY[f]["statut"] or ""))
corps = f"""<section><div class="wrap contact">
<div class="text"><p class="label">Contact</p><h1>Parlons de votre futur Birman</h1>
<p>Magali vous répond personnellement, le soir et le week-end, et Tristan la seconde pour vous répondre aussi en journée.</p>
<p>Chatterie des Innamorati<br>Bordeaux, Gironde</p>
<p>E-mail : <a class="mel" href="#" data-u="innamoraticats" data-d="tristanperrier.fr">innamoraticats [at] tristanperrier.fr</a><br>
Facebook : <a href="https://www.facebook.com/desinnamorati" target="_blank" rel="noopener">facebook.com/desinnamorati</a><br>Messenger : <a href="https://m.me/desinnamorati" target="_blank" rel="noopener">m.me/desinnamorati</a></p>
</div>
<form class="form" id="formulaire" action="https://formsubmit.co/{EMAIL}" method="POST">
<p class="label">Nous écrire</p>
<input type="hidden" name="_subject" value="Nouveau message depuis le site des Innamorati">
<input type="hidden" name="_next" value="{SITE}contact/merci/">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false">
<input type="text" name="_honey" class="pot" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="f2"><label>Prénom et nom<input name="Nom" required autocomplete="name"></label>
<label>E-mail<input type="email" name="email" required autocomplete="email"></label></div>
<div class="f2"><label><span>Téléphone <small>· facultatif</small></span><input type="tel" name="Téléphone" autocomplete="tel"></label>
<label>Ville<input name="Ville" required autocomplete="address-level2"></label></div>
<label>Votre projet<select name="Projet" required>
<option value="">Choisir</option><option>Entrer dans notre liste de pré-réservation</option><option>Adopter un chaton</option><option>Adopter un retraité</option><option>Autre question</option></select></label>
<label><span>Chaton qui vous intéresse <small>· facultatif</small></span><select name="Chaton" id="f-chaton"><option value="">Aucun en particulier</option>{chatons_opts}</select></label>
<label>Votre message<textarea name="Message" rows="6" required placeholder="Votre foyer, vos autres animaux, vos questions…"></textarea></label>
<button class="btn" type="submit">Envoyer</button>
<p class="fine-form">Vos coordonnées servent uniquement à vous répondre.</p>
</form></div></section>
<script>
(function () {{
  var m = document.querySelector(".mel"); if (m) {{ var a = m.dataset.u + "@" + m.dataset.d; m.href = "mailto:" + a; m.textContent = a; }}
  var c = new URLSearchParams(location.search).get("chaton"), s = document.getElementById("f-chaton");
  if (c && s) {{ var o = Array.prototype.find.call(s.options, function (x) {{ return x.text === c; }});
    if (!o) {{ o = new Option(c, c); s.add(o); }} s.value = o.value;
    var p = document.querySelector('select[name="Projet"]'); if (p) p.value = "Adopter un chaton"; }}
}})();
</script>"""
page("contact", "Contact · Chatterie des Innamorati, Sacrés de Birmanie à Bordeaux", corps, prio=0.6,
     desc="Contacter la Chatterie des Innamorati, élevage de Sacrés de Birmanie à Bordeaux : formulaire, e-mail, Facebook et Messenger.")

corps = f"""<section><div class="wrap narrow center">{tete("Message envoyé", "Merci, votre message est bien parti", "Magali vous répond personnellement le soir et le week-end, et Tristan en journée. Pensez à vérifier vos courriers indésirables.")}
<p><a class="btn" href="../../chatons/">Voir nos chatons</a> <a class="btn" href="../../">Retour à l'accueil</a></p></div></section>"""
page("contact/merci", "Message envoyé · Chatterie des Innamorati", corps, prio=0.1)

# ---------- Mentions légales ----------
corps = f"""<section><div class="wrap narrow">{tete("Mentions légales", "Mentions légales")}
<div class="text legal">
<p><b>Éditeur</b><br>Magali Perrier, entreprise individuelle, élevage de Sacrés de Birmanie sous l'affixe LOOF « des Innamorati ».<br>SIRET {SIRET} · Bordeaux (33).</p>
<p><b>Photographies</b><br>La plupart des photographies sont l'œuvre de <a href="https://tristanperrier.fr" target="_blank" rel="noopener">Tristan Perrier, photographe</a>. Les autres ont été prises par les adoptants de nos chatons, qui nous les ont confiées. Toutes sont publiées par la Chatterie des Innamorati. Toute reproduction, en particulier dans des annonces de vente, est interdite et fera l'objet d'un signalement.</p>
<p><b>Hébergement</b><br>GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<p><b>Données personnelles</b><br>Ce site ne dépose aucun cookie de suivi. Les messages envoyés par le formulaire de contact transitent par le service FormSubmit jusqu'à notre boîte e-mail. Ils servent uniquement à vous répondre et ne sont jamais transmis à des tiers.</p>
</div></div></section>"""
page("mentions-legales", "Mentions légales · Chatterie des Innamorati", corps)
