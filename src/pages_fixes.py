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
<div class="ribbon" aria-hidden="true"><div class="track"><span>Le regard saphir</span><i>✦</i><span>Les gants blancs</span><i>✦</i><span>La légende de Lao-Tsun</span><i>✦</i><span>des Innamorati</span><i>✦</i><span>Le regard saphir</span></div></div>
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
          "sameAs": ["https://www.facebook.com/desinnamorati"], "identifier": "SIRET " + SIRET},
         {"@context": "https://schema.org", "@type": "WebSite", "name": "Chatterie des Innamorati", "url": SITE, "inLanguage": "fr"},
         faq_ld])

# ---------- Le Birman ----------
r = "../"
SECTIONS = [
 ("histoire", "Une histoire française", [
  "Le Sacré de Birmanie est une race née en France. Selon le récit le plus souvent repris, un couple de chats sacrés aurait été envoyé de Birmanie vers la France à la fin des années 1910. Le mâle n'aurait pas survécu au voyage, mais la femelle, Sita, aurait donné naissance à une chatte, Poupée de Madalpour, souvent présentée comme l'ancêtre de la race.",
  "Les premiers Birmans sont présentés en exposition dans les années 1920 et la race est reconnue en France en 1925. La Seconde Guerre mondiale la mène au bord de l'extinction : on raconte qu'il ne restait qu'un seul couple. Des éleveurs français la reconstruisent patiemment après la guerre. Le Birman est ensuite reconnu en Grande-Bretagne en 1966, puis aux États-Unis en 1967, avant de conquérir le monde entier."]),
 ("physique", "Le physique du Birman", [
  "Le Birman est un chat de taille moyenne à grande, solide et bien charpenté. Une femelle pèse en général de 3 à 5 kg, un mâle de 5 à 7 kg. Sa tête est large et arrondie, son nez légèrement busqué, ses oreilles moyennes.",
  "Son poil mi-long est soyeux et forme une collerette autour du cou. Sa queue est en panache. Comme tous les colourpoint, il a le corps clair et les extrémités colorées : masque, oreilles, pattes et queue. Il lui faut deux à trois ans pour atteindre sa pleine maturité."]),
 ("caractere", "Son caractère", [
  "Le Birman est doux, calme et très sociable. Il suit ses humains de pièce en pièce, aime les câlins sans être envahissant, et parle d'une voix discrète. Il s'entend bien avec les enfants et cohabite volontiers avec d'autres chats ou un chien bien élevé.",
  "C'est un chat d'intérieur idéal, qui se plaît très bien en appartement. Il supporte mal la solitude prolongée : si la maison est vide toute la journée, deux chats sont souvent plus heureux qu'un seul."]),
 ("entretien", "Entretien et santé", [
  "Son poil n'a pas de sous-poil laineux et s'emmêle peu. Un brossage par semaine suffit, un peu plus pendant la mue du printemps.",
  "Le Birman est une race robuste, qui vit en moyenne de 12 à 16 ans. Un éleveur sérieux suit la santé de ses reproducteurs avec son vétérinaire et connaît leur groupe sanguin, car le groupe B est plus fréquent chez le Birman que chez la plupart des autres races."]),
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
    ("Combien de temps vit un Sacré de Birmanie ?", "Un Birman vit en moyenne de 12 à 16 ans, parfois davantage, s'il est bien suivi par son vétérinaire et vit à l'intérieur."),
    ("Le Sacré de Birmanie perd-il beaucoup ses poils ?", "Moins que son poil mi-long le laisse penser. Sans sous-poil laineux, il s'emmêle peu et un brossage hebdomadaire suffit. La mue est plus marquée au printemps."),
    ("Un Birman peut-il vivre en appartement ?", "Oui, très bien. Calme et attaché à sa famille, il n'a pas besoin d'extérieur. Il faut surtout lui offrir de la compagnie, des jeux et un arbre à chat."),
    ("Mâle ou femelle : lequel choisir ?", "Une fois stérilisés, les deux font d'excellents compagnons. Le mâle est souvent plus grand et très câlin, la femelle un peu plus indépendante. Le caractère individuel compte davantage que le sexe."),
    ("Combien coûte un chaton Sacré de Birmanie ?", 'Chez nous, un chaton coûte 1 800 €, stérilisé, pucé, vacciné et inscrit au LOOF. Le détail est sur la page <a href="../adopter/">Adopter</a>.'),
])
corps = f"""<section><div class="wrap">
{tete("Le Sacré de Birmanie", "Le Sacré de Birmanie, le chat aux gants blancs", "Histoire, légende, standard, caractère et entretien : tout savoir sur le Birman, par une famille d'éleveurs qui vit avec lui depuis 2016.")}
<div class="birman-grid">{grand(r, P["oedipe9"], "Œdipe des Innamorati, Sacré de Birmanie seal point aux yeux saphir")}
<div class="text">
<p class="label">La légende</p>
<h2 class="h-art">Le temple de Lao-Tsun</h2>
<p>On raconte qu'au temple de Lao-Tsun, en Birmanie, vivait le vieux prêtre Mun-Ha et son chat Sinh. Une nuit, des pillards attaquèrent le temple et Mun-Ha mourut devant la statue de Tsun-Kyan-Kse, la déesse aux yeux de saphir.</p>
<p>Sinh posa alors ses pattes sur son maître. Sa robe prit les reflets dorés de la déesse, ses yeux devinrent bleus comme les siens, et ses pattes, posées sur le prêtre, restèrent d'un blanc pur. Les gants du Birman seraient le souvenir de ce geste.</p>
<div class="std">
<div><b>Les gants</b><span>Blancs, nets et symétriques aux pattes avant, arrêtés à l'articulation.</span></div>
<div><b>Les éperons</b><span>Aux pattes arrière, le blanc remonte en pointe vers le jarret.</span></div>
<div><b>Les yeux</b><span>Ronds, d'un bleu saphir le plus profond possible.</span></div>
<div><b>Les couleurs</b><span>Plus d'une vingtaine, toujours en colourpoint. <a href="../couleurs/">Voir toutes les couleurs</a>.</span></div>
</div></div></div>
<nav class="sommaire" aria-label="Sommaire">{sommaire}</nav>
<div class="articles">{articles}</div>
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
