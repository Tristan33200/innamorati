# Pages rédigées à la main. Exécuté par build.py après pages.py, une fois par langue (T(français, anglais)).
P = {  # photos choisies (numéros de l'export Facebook)
    "hero": "2084329241748221", "sanae": "2084329255081553", "oedipe": "1335020643345755", "regard": "902865393227951",
    "magali": "551069241740903", "enfant": "753369611510864", "expo_yeux": "2077785872402558", "milan": "1190960814418406",
    "presentation": "1456228661224952", "table": "1391940180987134", "carre": "2077785365735942", "nw2019": "1418632404984578",
    "oedipe9": "1300215273492959", "rosettes": "1216272991887188", "bianca": "1707822147123326",
}
st = json.load(open(os.path.join(ROOT, "data/stats.json")))


def grand(r, pid, alt, style="", prio=False, sizes="(max-width: 700px) 100vw, 50vw"):
    """Grande photo : version 520 px pour les petits écrans, chargement différé sauf pour la photo du haut de page."""
    st = ' style="' + style + '"' if style else ""
    jeu = f' srcset="{jeu_photo(r, pid)}" sizes="{sizes}"' if os.path.exists(os.path.join(OUT, "photos", "t", pid + ".jpg")) else ""
    if prio:
        return f'<div class="ph"><img src="{r}photos/{pid}.jpg"{jeu} alt="{e(alt)}"{st} fetchpriority="high" decoding="async"></div>'
    # Photos plus bas dans la page : chargées seulement après la photo du haut (site.js), copie sans script pour les moteurs
    return (f'<div class="ph"><img data-src="{r}photos/{pid}.jpg"{jeu.replace(" srcset=", " data-srcset=")} alt="{e(alt)}"{st} loading="lazy" decoding="async">'
            f'<noscript><img src="{r}photos/{pid}.jpg" alt="{e(alt)}"{st}></noscript></div>')


# ---------- Accueil ----------
r = ""
kits = "".join(carte(r, BY[f], f'<span class="status{" libre" if "réserver" in BY[f]["statut_fr"] else ""}">{e(BY[f]["statut"].capitalize())}</span>') for f in sorted(CFG["chatons_disponibles"], key=lambda f: BY[f]["debut"], reverse=True)[:4])
ch = lambda fb: f'{BY[fb]["sexe"]} {rb(BY[fb]["robe"]).lower()}'
corps = f"""
<div class="hero">
  {grand(r, P["hero"], T("Les yeux saphir de Sanae des Innamorati", "The sapphire eyes of Sanae des Innamorati"), prio=True, sizes="100vw")}
  <div class="wrap"><p class="big">{T("Le regard saphir", "The sapphire gaze")}</p><h1 class="kicker">{T("Élevage de Sacrés de Birmanie à Bordeaux", "Birman cat breeder in Bordeaux, France")}</h1><a class="btn light" href="chatons/">{T("Nos chatons", "Our kittens")}</a></div>
</div>
<section class="center"><div class="wrap">
  <div class="narrow intro">
    <p class="label">{T("Élevage familial depuis 2016", "A family cattery since 2016")}</p>
    <h2>{T("Des Birmans de champions, élevés en famille à Bordeaux", "Champion Birman cats, raised in our family home in Bordeaux")}</h2>
    <div class="rule"></div>
    {T(f'''<p>La Chatterie des Innamorati est un élevage familial de Sacrés de Birmanie installé à Bordeaux, en Gironde, et déclaré au LOOF sous l'affixe « des Innamorati ». Chez nous, les chats ne vivent pas en chatterie. Ils partagent la maison, les canapés et les jeux de nos enfants. Les chatons naissent et grandissent au milieu de la vie de famille, ce qui en fait des compagnons confiants et doux.</p>
    <p>Depuis 2016, {st["grandis"]} chatons des Innamorati ont rejoint leur famille, et nos chats ont été titrés de Paris à Milan. Nos chatons Sacré de Birmanie partent stérilisés, entre 15 semaines et 4 mois et demi, vers Bordeaux, la Gironde et toute la Nouvelle-Aquitaine.</p>''',
    f'''<p>The Chatterie des Innamorati is a family-run Birman cat cattery in Bordeaux, in south-west France, registered with the LOOF (the official French cat pedigree registry) under the cattery name « des Innamorati ». Our cats do not live in a cattery building. They share our home, our sofas and our children’s games. The kittens are born and grow up in the middle of family life, which makes them trusting, gentle companions.</p>
    <p>Since 2016, {st["grandis"]} Innamorati kittens have joined their new families, and our cats have won titles from Paris to Milan. Our Birman kittens leave already spayed or neutered, between 15 weeks and 4½ months of age.</p>''')}
  </div>
  <div class="doors">
    <a class="door" href="chatons/">{grand(r, P["bianca"], "Bianca des Innamorati")}<h3>{T("Nos chatons", "Our kittens")}</h3><span class="label">{T("Portées 2026", "2026 litters")}</span></a>
    <a class="door" href="nos-chats/">{grand(r, P["sanae"], "Sanae des Innamorati")}<h3>{T("Nos chats", "Our cats")}</h3><span class="label">{T("Reproductrices et retraités", "Queens and retired cats")}</span></a>
    <a class="door" href="couleurs/">{grand(r, P["regard"], T("Birman aux yeux bleus", "Blue-eyed Birman cat"))}<h3>{T("Les couleurs", "Colors")}</h3><span class="label">{T("Toutes les robes du Birman", "Every Birman coat color")}</span></a>
  </div>
</div></section>
<div class="band">{grand(r, P["oedipe"], T("Œdipe des Innamorati et ses trophées", "Œdipe des Innamorati and his trophies"), sizes="100vw")}
  <blockquote><p>{T("« Ici, rien ne passe avant le bonheur de nos chats. »", "“Here, nothing comes before the happiness of our cats.”")}</p><cite>Magali &amp; Tristan</cite></blockquote></div>
<section><div class="wrap">
  <div class="head"><p class="label">{T("Nos chatons", "Our kittens")}</p><h2>{T("Les portées de 2026", "The 2026 litters")}</h2><p>{T("Chaque chaton a son album, enrichi au fil de sa vie par nos photos puis par celles de ses adoptants.", "Every kitten has its own album, filled over the years with our photos and then with those of its new family.")}</p></div>
  <div class="grid g4">{kits}</div>
  <p class="center" style="margin-top:56px"><a class="btn" href="chatons/">{T("Voir tous les chatons", "See all kittens")}</a> <a class="btn" href="portees/">{T("Toutes nos portées", "All our litters")}</a></p>
</div></section>
<section class="palm"><div class="wrap">
  <div class="head"><p class="label">{T("Palmarès", "Show titles")}</p><h2>{T("Douze saisons d'expositions", "Twelve show seasons")}</h2><p>{T("Chaque hiver et chaque printemps, nous présentons nos chats en exposition : Paris, Bordeaux, Biarritz, Nantes, Rome, Milan, Valladolid.", "Every winter and spring we show our cats: Paris, Bordeaux, Biarritz, Nantes, Rome, Milan, Valladolid.")}</p></div>
  <div class="palm-grid">{grand(r, P["nw2019"], "Œdipe des Innamorati, National Winner 2019")}
    <div><ul class="titles-list">
      <li><div><b><a href="{BY['204']['url']}">Œdipe des Innamorati</a></b><span>{T("Mâle seal point · Best of Best à Sartrouville (2019), Pontchâteau (2021) et Pontorson (2022)", "Seal point male · Best of Best in Sartrouville (2019), Pontchâteau (2021) and Pontorson (2022)")}</span></div><em>SC · NW · JW · DSM · DVM</em></li>
      <li><div><b><a href="{BY['2']['url']}">{BY['2']['titre']}</a></b><span>{ch('2')}</span></div><em>GIC</em></li>
      <li><div><b><a href="{BY['98']['url']}">{BY['98']['titre']}</a></b><span>{ch('98')} · {T("Best in Show à Paris, 2023", "Best in Show in Paris, 2023")}</span></div><em>GIP</em></li>
      <li><div><b><a href="{BY['148']['url']}">Simone de Beauvoir des Innamorati</a></b><span>{T("Femelle seal tabby point", "Seal tabby point female")}</span></div><em>IC</em></li>
      <li><div><b><a href="{BY['143']['url']}">Sanae des Innamorati</a></b><span>{T("Femelle blue point", "Blue point female")}</span></div><em>IC · DVM</em></li>
    </ul>
    <p class="abbr">{T("SC Champion Suprême · GIC Grand Champion International · IC Champion International · GIP Grand Premior International (chat stérilisé) · NW National Winner · JW Junior Winner · DSM Distinguished Show Merit · DVM Distinguished Variety Merit",
                        "SC Supreme Champion · GIC Grand International Champion · IC International Champion · GIP Grand International Premior (neutered cat) · NW National Winner · JW Junior Winner · DSM Distinguished Show Merit · DVM Distinguished Variety Merit")}</p>
    <p style="margin-top:28px"><a class="btn light" href="expositions/">{T("Toutes nos expositions", "All our cat shows")}</a></p></div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="mosaic">
    {grand(r, P["expo_yeux"], T("Birman en exposition", "Birman cat at a show"))}{grand(r, P["milan"], T("Milan, exposition internationale", "Milan international cat show"))}{grand(r, P["presentation"], T("Présentation au juge", "Presenting a cat to the judge"))}{grand(r, P["rosettes"], T("Œdipe et ses rosettes", "Œdipe and his rosettes"))}{grand(r, P["table"], T("Sur la table de jugement", "On the judging table"))}{grand(r, P["carre"], T("Dans notre carré d'exposition", "In our show pen"))}
  </div>
</div></section>
<section style="padding-top:20px"><div class="wrap family">
  <div class="stack">{grand(r, P["magali"], T("Magali et un chaton", "Magali with a kitten"), "object-position:40% 50%")}{grand(r, P["enfant"], T("Notre fille et un Birman", "Our daughter with a Birman"))}</div>
  <div class="text">
    <p class="label">{T("Notre famille", "Our family")}</p>
    <h2>{T("Magali, Tristan, nos enfants et nos chats", "Magali, Tristan, our children and our cats")}</h2>
    {T('''<p>Magali est l'éleveuse de la chatterie. Infirmière diplômée et directrice de crèche, elle consacre ses soirées et ses week-ends aux chats, avec un œil exercé sur leur santé.</p>
    <p>Tristan, <a href="https://tristanperrier.fr" target="_blank" rel="noopener">photographe</a>, est présent à la maison en journée. Il veille sur les chats au quotidien, les accompagne en exposition et signe la plupart des photos de ce site. Les autres nous sont envoyées par les familles de nos chatons.</p>
    <p>Malgré le prix de nos chatons, l'élevage reste déficitaire. C'est un choix : santé, tests, expositions et temps passé avec chaque chaton passent avant tout.</p>''',
    '''<p>Magali is the breeder. A registered nurse and nursery director, she devotes her evenings and weekends to the cats, with a trained eye on their health.</p>
    <p>Tristan, a <a href="https://tristanperrier.fr" target="_blank" rel="noopener">photographer</a>, is at home during the day. He looks after the cats every day, takes them to shows and took most of the photos on this site. The others were sent to us by our kittens’ families.</p>
    <p>Despite the price of our kittens, the cattery runs at a loss. That is our choice: health, testing, shows and time spent with each kitten come first.</p>''')}
    <p class="sign">Magali &amp; Tristan</p>
  </div>
</div></section>
"""
faq_html, faq_ld = faq(T("Adopter un Sacré de Birmanie à Bordeaux", "Adopting a Birman kitten from France"), T([
    ("Où trouver un chaton Sacré de Birmanie à Bordeaux ?", 'Notre élevage familial se trouve à Bordeaux, en Gironde. Nos chatons disponibles sont présentés sur la page <a href="chatons/">Nos chatons</a>, avec leurs parents et leur album photo. Nous recevons les familles à la maison pour rencontrer les chats.'),
    ("Quel est le prix d'un chaton Sacré de Birmanie ?", "Nos chatons sont proposés à 1 800 €. Ce prix comprend le pedigree LOOF, la puce électronique, les vaccins, les vermifuges, le certificat vétérinaire et la stérilisation."),
    ("À quel âge partent les chatons ?", "Nos chatons rejoignent leur famille entre 15 semaines et 4 mois et demi. Ils partent déjà stérilisés, sociabilisés et habitués à la vie de famille."),
    ("Vos chatons sont-ils inscrits au LOOF ?", "Oui. Tous nos chatons sont inscrits au LOOF, le livre officiel des origines félines, sous l'affixe « des Innamorati ». En France, seul un chat inscrit au LOOF peut être vendu comme Sacré de Birmanie."),
    ("Comment éviter les fausses annonces ?", 'Nos photos sont parfois volées pour de fausses annonces. Vérifiez toujours le SIRET de l\'éleveur et la présence du chaton sur son site. Notre page <a href="adopter/#verifier">Vérifier une annonce</a> explique comment faire.'),
], [
    ("Where is your Birman cattery?", 'Our family cattery is in Bordeaux, in the Gironde region of south-west France. Our available kittens are shown on the <a href="chatons/">Our kittens</a> page, with their parents and photo albums. We welcome families at home to meet the cats.'),
    ("How much does a Birman kitten cost?", "Our kittens are €1,800. The price includes the LOOF pedigree, microchip, vaccinations, deworming, veterinary certificate and spaying or neutering."),
    ("At what age do the kittens leave?", "Our kittens join their families between 15 weeks and 4½ months of age. They leave already spayed or neutered, well socialized and used to family life."),
    ("Are your kittens pedigree cats?", "Yes. All our kittens are registered with the LOOF, the official French pedigree registry, under the cattery name « des Innamorati ». In France, only a LOOF-registered cat may be sold as a Birman."),
    ("Can families from outside France adopt?", 'Yes, but we never ship kittens. Every family comes to collect their kitten in person in Bordeaux, after getting to know us. Families have traveled from all over France and from abroad, some from as far as the Sultanate of Oman. <a href="contact/">Write to us</a> to talk about your plans.'),
    ("How can I avoid fake listings?", 'Our photos are sometimes stolen for fake kitten ads. Always check the breeder’s SIRET business number and that the kitten appears on the breeder’s own website. Our <a href="adopter/#verifier">Check an ad</a> section explains how.'),
]))
corps += faq_html
page("", T("Sacré de Birmanie à Bordeaux · Chatterie des Innamorati, éleveur LOOF", "Birman Cat Breeder in France · Chatterie des Innamorati, Bordeaux"), corps, sombre_entete=True, image=P["hero"], prio=1.0,
     desc=T("Chatterie des Innamorati, élevage familial de Sacrés de Birmanie à Bordeaux (Gironde) depuis 2016. Chatons LOOF stérilisés, parents champions, portées et expositions.",
            "Chatterie des Innamorati, a family Birman cat breeder in Bordeaux, France, since 2016. LOOF pedigree Birman kittens, spayed or neutered, champion parents, litters and cat shows."),
     ld=[{"@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "#elevage", "name": "Chatterie des Innamorati", "logo": SITE + "assets/favicon-192.png",
          "knowsAbout": T(["Sacré de Birmanie", "Birman", "élevage félin LOOF"], ["Birman cat", "Sacred Cat of Burma", "LOOF pedigree cat breeding"]),
          "geo": {"@type": "GeoCoordinates", "latitude": 44.84, "longitude": -0.58}, "foundingDate": "2016",
          "alternateName": "des Innamorati", "description": T("Élevage familial de Sacrés de Birmanie (chats Birman) inscrit au LOOF.", "Family-run Birman cat cattery registered with the LOOF, in Bordeaux, France."),
          "url": lien(""), "image": SITE + "photos/" + P["hero"] + ".jpg", "priceRange": "1800 €", "founder": "Magali Perrier",
          "address": {"@type": "PostalAddress", "addressLocality": "Bordeaux", "addressRegion": "Gironde", "addressCountry": "FR"},
          "areaServed": ["Bordeaux", "Gironde", "Nouvelle-Aquitaine", "France"],
          "email": EMAIL, "sameAs": ["https://www.facebook.com/desinnamorati"], "identifier": "SIRET " + SIRET},
         {"@context": "https://schema.org", "@type": "WebSite", "name": "Chatterie des Innamorati", "url": lien(""), "inLanguage": L},
         faq_ld])

# ---------- Le Birman ----------
r = "../"
SECTIONS = T([
 ("histoire", "Une histoire française", [
  "Les origines du Sacré de Birmanie restent assez obscures. Selon le récit transmis par la Fédération Féline Française, un couple de chats dérobé au temple de Lao-Tsun aurait gagné la France en 1920, à bord du yacht d'un millionnaire américain. Le mâle mourut pendant la traversée, mais la femelle, Sita, était déjà pleine.",
  "En 1926, une femelle seal point, Poupée de Maldapour, est présentée à l'exposition de Paris organisée par le Cat Club de France et de Belgique. Elle est la première Birmane inscrite. D'autres hypothèses existent : l'éleveuse Simone Poirier, de la chatterie de Crespières, pensait que la race était née du croisement d'un Siamois ganté de blanc et d'un chat à poil long.",
  "Après la Seconde Guerre mondiale, il ne restait qu'un seul couple, Orloff et Xéna de Kaaba. D'après les livres d'origines, tous les Birmans d'aujourd'hui descendent d'eux. Depuis plus de soixante-dix ans, la race a gardé les mêmes traits distinctifs."]),
 ("physique", "Le physique du Birman", [
  "Le Birman est un chat massif, au corps allongé, porté par des pattes courtes et fortes. Sa tête est puissante, avec des joues pleines et rondes et un front légèrement bombé. Son nez court a un léger profil romain : ni droit comme celui du Siamois, ni « stoppé » comme celui du Persan. Ses grands yeux ronds ou légèrement ovales sont du bleu le plus intense possible.",
  "Sa robe soyeuse est très longue sur le dos et les flancs. Courte sur la face, elle s'allonge sur les joues en une collerette abondante. Le corps est très clair, couleur coquille d'œuf, le dos beige doré, le ventre blanc cassé, et les extrémités sont plus foncées. Sa queue, en panache, est souvent portée haute."]),
 ("caractere", "Son caractère", [
  "Calme et posé sans être inactif, le Birman est très joueur : il n'est pas rare qu'il apporte sa plume pour réclamer une partie. C'est un vrai « chat-chien », qui suit ses humains partout et n'aime pas les portes fermées. Il parle peu, d'une voix douce, et il est sensible à l'humeur de sa famille.",
  "Il adore les enfants, s'entend bien avec les chiens et voyage facilement tant qu'il est avec les siens. Il vit très bien en intérieur. Nos lignées sont domestiquées depuis des décennies : le Birman ne connaît pas les dangers du dehors, se perd facilement et ne sait pas revenir. Il ne sort donc jamais sans surveillance, seulement en harnais et à la longe, ou dans un enclos sécurisé."]),
 ("entretien", "Entretien et santé", [
  "Sa fourrure soyeuse s'emmêle peu. Un brossage par semaine suffit à retirer les poils morts, et c'est aussi un joli moment de complicité.",
  "Le Birman est une race robuste. Chez un éleveur sérieux, les reproducteurs sont suivis avec le vétérinaire, et la sélection veille à préserver la santé autant que la beauté."]),
 ("differences", "Birman, Ragdoll ou Siamois ?", [
  "On confond souvent ces trois races aux yeux bleus. Le Siamois a le poil court et un corps fin et élancé. Le Ragdoll est plus grand et plus lourd, et ses pattes ne sont pas toujours blanches.",
  "Le Birman se reconnaît à coup sûr à ses quatre gants blancs, nets et symétriques, et à ses éperons blancs qui remontent à l'arrière des pattes postérieures."]),
 ("eleveur", "Bien choisir son éleveur", [
  "En France, un chat ne peut être vendu comme Sacré de Birmanie que s'il est inscrit au LOOF, le livre officiel des origines félines. L'éleveur doit afficher son numéro SIRET dans toutes ses annonces, et le chaton doit être identifié par puce, vacciné, et accompagné d'un certificat vétérinaire.",
  'Méfiez-vous des prix trop bas et des vendeurs qui refusent une visite : de nombreuses fausses annonces utilisent des photos volées, y compris les nôtres. Nos conseils sont sur la page <a href="../adopter/#verifier">Vérifier une annonce</a>.']),
], [
 ("histoire", "A French story", [
  "The origins of the Birman, also called the Sacred Cat of Burma, remain rather obscure. According to the account handed down by the Fédération Féline Française, a pair of cats stolen from the temple of Lao-Tsun reached France in 1920 aboard the yacht of an American millionaire. The male died during the voyage, but the female, Sita, was already pregnant.",
  "In 1926, a seal point female, Poupée de Maldapour, was shown at the Paris cat show organized by the Cat Club de France et de Belgique. She was the first Birman ever registered. Other theories exist: the breeder Simone Poirier, of the Crespières cattery, believed the breed came from crossing a white-gloved Siamese with a longhaired cat.",
  "After the Second World War, only one pair remained, Orloff and Xéna de Kaaba. According to the stud books, every Birman alive today descends from them. For more than seventy years, the breed has kept the same distinctive features."]),
 ("physique", "What a Birman looks like", [
  "The Birman is a sturdy cat with a long body carried on short, strong legs. Its head is powerful, with full round cheeks and a slightly rounded forehead. Its short nose has a slight Roman profile: neither straight like the Siamese nor with the marked stop of the Persian. Its large round or slightly oval eyes are the deepest blue possible.",
  "Its silky coat is very long on the back and flanks. Short on the face, it lengthens on the cheeks into a full ruff. The body is very pale, eggshell in color, the back golden beige, the belly off-white, and the points are darker. Its plumed tail is often carried high."]),
 ("caractere", "Personality", [
  "Calm and composed without being lazy, the Birman is very playful: it often brings its feather toy to ask for a game. It is a true “dog-like cat” that follows its people everywhere and dislikes closed doors. It is quiet, with a soft voice, and very sensitive to its family’s mood.",
  "It loves children, gets along well with dogs and travels easily as long as it is with its people. It is perfectly happy as an indoor cat. Our lines have been domesticated for decades: a Birman does not understand outdoor dangers, gets lost easily and cannot find its way home. So it never goes outside unsupervised, only on a harness and leash, or in a secure enclosure."]),
 ("entretien", "Grooming and health", [
  "Its silky fur rarely mats. Brushing once a week is enough to remove loose hair, and it is a lovely bonding moment too.",
  "The Birman is a hardy breed. With a responsible breeder, breeding cats are followed closely by the vet, and selection aims to preserve health as much as beauty."]),
 ("differences", "Birman, Ragdoll or Siamese?", [
  "These three blue-eyed breeds are often confused. The Siamese has short hair and a fine, slender body. The Ragdoll is larger and heavier, and its paws are not always white.",
  "A Birman is unmistakable thanks to its four white gloves, clean and symmetrical, and the white laces that run up the back of its hind legs."]),
 ("eleveur", "Choosing a good breeder", [
  "In France, a cat may only be sold as a Birman if it is registered with the LOOF, the official French pedigree registry. The breeder must show their SIRET business number in every ad, and the kitten must be microchipped, vaccinated and come with a veterinary certificate.",
  'Beware of prices that are too low and of sellers who refuse a visit: many fake ads use stolen photos, including ours. Our advice is in the <a href="../adopter/#verifier">Check an ad</a> section.']),
])
sommaire = "".join(f'<a href="#{i}">{t}</a>' for i, t, _ in SECTIONS)
ILLUS = {"physique": ("1125078997673255", T("Crowned Dream Kacey, Sacré de Birmanie seal tabby point adulte : corps massif, collerette et yeux bleus", "Crowned Dream Kacey, adult seal tabby point Birman: sturdy body, full ruff and blue eyes")),
         "caractere": (P["enfant"], T("Un Sacré de Birmanie dans les bras d'un enfant : un chat doux et très attaché à sa famille", "A Birman in a child’s arms: a gentle cat, very attached to its family")),
         "differences": ("crush-boom-bang-1", T("Les quatre gants blancs du Sacré de Birmanie : Crush Boom Bang, seal tabby point", "The Birman’s four white gloves: Crush Boom Bang, seal tabby point"))}
def illus(i):
    if i not in ILLUS: return ""
    pid, alt = ILLUS[i]
    return f'<figure class="art-fig"><div class="ph"><img src="{r}photos/{pid}.jpg" alt="{e(alt)}" loading="lazy"></div><figcaption>{e(alt)}</figcaption></figure>'
articles = "".join(f'<section class="art" id="{i}"><h2>{t}</h2>' + "".join(f"<p>{x}</p>" for x in ps) + illus(i) + "</section>" for i, t, ps in SECTIONS)
faq_html, faq_ld = faq(T("Le Sacré de Birmanie en questions", "The Birman cat: your questions"), T([
    ("Quelle est la différence entre Sacré de Birmanie et Birman ?", "Aucune : c'est la même race. Sacré de Birmanie est son nom français, Birman son nom international. On dit aussi simplement « Birman » en France."),
    ("D'où vient le Sacré de Birmanie ?", "Malgré son nom et sa légende birmane, c'est une race française. Les premiers Birmans sont présentés à Paris dans les années 1920, et tous les Birmans actuels descendent d'Orloff et Xéna de Kaaba, le seul couple qui restait après la Seconde Guerre mondiale."),
    ("Combien de temps vit un Sacré de Birmanie ?", "Le Birman est une race robuste. Bien suivi par son vétérinaire et vivant à l'intérieur, il partage souvent la vie de sa famille pendant de longues années, couramment plus de quinze ans."),
    ("Le Sacré de Birmanie perd-il beaucoup ses poils ?", "Moins que son poil mi-long le laisse penser. Sa fourrure soyeuse s'emmêle peu et un brossage par semaine suffit à retirer les poils morts."),
    ("Un Birman peut-il vivre en appartement ?", "Oui, et c'est même là qu'il est le plus heureux. Très attaché à sa famille et joueur, il a surtout besoin de compagnie, de jeux et d'un arbre à chat. Il ne doit jamais sortir sans surveillance : domestiqué depuis des décennies, il ne comprend pas les dangers, se perd et ne sait pas revenir. Dehors, c'est uniquement en harnais et à la longe, ou dans un enclos sécurisé."),
    ("Mâle ou femelle : lequel choisir ?", "Une fois stérilisés, les deux font d'excellents compagnons. Le mâle est souvent plus grand et très câlin, la femelle un peu plus indépendante. Le caractère individuel compte davantage que le sexe."),
    ("Combien coûte un chaton Sacré de Birmanie ?", 'Chez nous, un chaton coûte 1 800 €, stérilisé, pucé, vacciné et inscrit au LOOF. Le détail est sur la page <a href="../adopter/">Adopter</a>.'),
], [
    ("Is the Birman the same as the Sacred Cat of Burma?", "Yes, it is the same breed. Birman is its international name, Sacré de Birmanie its French name, and Sacred Cat of Burma the literal translation."),
    ("Where does the Birman come from?", "Despite its name and its Burmese legend, the Birman is a French breed. The first Birmans were shown in Paris in the 1920s, and all Birmans today descend from Orloff and Xéna de Kaaba, the only pair left after the Second World War."),
    ("How long do Birman cats live?", "The Birman is a hardy breed. Well looked after by its vet and living indoors, it often shares its family’s life for many years, commonly more than fifteen."),
    ("Do Birman cats shed a lot?", "Less than their semi-long coat suggests. Their silky fur rarely mats, and brushing once a week is enough to remove loose hair."),
    ("Can a Birman live in an apartment?", "Yes, that is where it is happiest. Playful and very attached to its family, it mostly needs company, toys and a cat tree. It must never go outside unsupervised: domesticated for decades, it does not understand dangers, gets lost and cannot find its way home. Outdoors means only on a harness and leash, or in a secure enclosure."),
    ("Male or female: which should I choose?", "Once spayed or neutered, both make wonderful companions. Males are often bigger and very cuddly, females a little more independent. Individual personality matters more than sex."),
    ("How much does a Birman kitten cost?", 'With us, a kitten costs €1,800, spayed or neutered, microchipped, vaccinated and LOOF-registered. Details are on the <a href="../adopter/">Adopt</a> page.'),
]))
corps = f"""<section><div class="wrap">
{tete(T("Le Sacré de Birmanie", "The Birman cat"), T("Le Sacré de Birmanie, le chat aux gants blancs", "The Birman, the cat with white gloves"), T("Histoire, légende, standard, caractère et entretien : tout savoir sur le Birman, par une famille d'éleveurs qui vit avec lui depuis 2016.", "History, legend, breed standard, personality and care: all about the Birman, also known as the Sacred Cat of Burma, from a breeding family who has lived with Birmans since 2016."))}
<div class="birman-grid">{grand(r, P["oedipe9"], T("Œdipe des Innamorati, Sacré de Birmanie seal point aux yeux saphir", "Œdipe des Innamorati, seal point Birman with sapphire eyes"), prio=True)}
<div class="text">
{T('''<p class="label">La légende</p>
<h2 class="h-art">Le temple de Lao-Tsun</h2>
<p>On raconte que le temple de Lao-Tsun, « le temple des temples », se dressait dans les hautes montagnes. Le vieux prêtre Mun-Ha y vivait avec Sinh, un chat blanc. Une nuit, des pillards attaquèrent le temple et Mun-Ha mourut devant la statue de Tsun-Kyan-Kse, la déesse aux yeux de saphir.</p>
<p>Sinh posa alors ses pattes sur son maître. Sa robe prit les reflets dorés de la déesse, ses yeux devinrent bleus comme les siens, et ses pattes, posées sur le prêtre, restèrent d'un blanc pur. Les gants du Birman seraient le souvenir de ce geste.</p>
<div class="std">
<div><b>Les gants</b><span>D'un blanc absolument pur. Ils s'arrêtent entre la base des doigts et l'articulation, sans jamais la dépasser.</span></div>
<div><b>Les éperons</b><span>Aux pattes arrière, le blanc forme une pointe sous le pied. Leur absence est éliminatoire en exposition.</span></div>
<div><b>Les yeux</b><span>Grands, ronds ou légèrement ovales, du bleu le plus intense possible.</span></div>
<div><b>Les couleurs</b><span>Quarante couleurs reconnues, toujours en colourpoint. <a href="../couleurs/">Voir toutes les couleurs</a>.</span></div>
</div>''', '''<p class="label">The legend</p>
<h2 class="h-art">The temple of Lao-Tsun</h2>
<p>Legend has it that the temple of Lao-Tsun, “the temple of temples”, stood high in the mountains. The old priest Mun-Ha lived there with Sinh, a white cat. One night, raiders attacked the temple and Mun-Ha died before the statue of Tsun-Kyan-Kse, the goddess with sapphire eyes.</p>
<p>Sinh then laid his paws on his master. His coat took on the golden glow of the goddess, his eyes turned blue like hers, and his paws, resting on the priest, stayed pure white. The Birman’s gloves are said to be the memory of that gesture.</p>
<div class="std">
<div><b>The gloves</b><span>Pure, brilliant white. They stop between the base of the toes and the joint, never going beyond it.</span></div>
<div><b>The laces</b><span>On the hind legs, the white forms a point running up under the foot. Without them, a cat is disqualified at shows.</span></div>
<div><b>The eyes</b><span>Large, round or slightly oval, the deepest blue possible.</span></div>
<div><b>The colors</b><span>Forty recognized colors, always colorpoint. <a href="../couleurs/">See all colors</a>.</span></div>
</div>''')}</div></div>
<nav class="sommaire" aria-label="{T("Sommaire", "Contents")}">{sommaire}</nav>
<div class="articles">{articles}</div>
<p class="note">Sources{T(" : ", ": ")}<a href="https://www.fff-asso.fr/race/sacre-de-birmanie/" rel="noopener" target="_blank">Fédération Féline Française</a> {T("et", "and")} <a href="https://cfsbi.fr/portfolio-item/d-une-legende-a-la-realite/" rel="noopener" target="_blank">Club Français du Sacré de Birmanie (CFSBI)</a>{T("", ", in French")}.</p>
</div></section>{faq_html}"""
page("le-birman", T("Sacré de Birmanie : histoire, caractère, standard et entretien du Birman", "Birman Cat: History, Personality, Standard and Care · des Innamorati"), corps, image=P["oedipe9"], prio=0.9, og_type="article",
     image_alt=T("Œdipe des Innamorati, Sacré de Birmanie seal point aux yeux saphir", "Œdipe des Innamorati, seal point Birman cat with sapphire eyes"),
     desc=T("Tout savoir sur le Sacré de Birmanie (Birman) : légende de Lao-Tsun, histoire de la race, standard, gants blancs, caractère, entretien, santé et différences avec le Ragdoll.",
            "All about the Birman cat (Sacred Cat of Burma): the Lao-Tsun legend, breed history, standard, white gloves, personality, grooming, health and how it differs from the Ragdoll."),
     ld=[{"@context": "https://schema.org", "@type": "Article", "headline": T("Le Sacré de Birmanie, le chat aux gants blancs", "The Birman, the cat with white gloves"),
          "image": SITE + "photos/" + P["oedipe9"] + ".jpg", "inLanguage": L, "author": {"@type": "Person", "name": "Magali Perrier"},
          "publisher": {"@id": SITE + "#elevage"}, "mainEntityOfPage": lien("le-birman/"),
          "about": {"@type": "Thing", "name": T("Sacré de Birmanie", "Birman cat"), "alternateName": T("Birman", "Sacred Cat of Burma"), "sameAs": T("https://fr.wikipedia.org/wiki/Sacr%C3%A9_de_Birmanie", "https://en.wikipedia.org/wiki/Birman")}},
         ariane((T("Accueil", "Home"), ""), (T("Le Sacré de Birmanie", "The Birman cat"), "le-birman/")), faq_ld])

# ---------- Adopter ----------
corps = T(f"""<section><div class="wrap">
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
<section class="center"><div class="wrap"><a class="btn" href="../contact/">Nous écrire</a></div></section>""", f"""<section><div class="wrap">
{tete("Adopt a kitten", "What you are really adopting", "Our kittens leave between 15 weeks and 4½ months of age, already spayed or neutered, after months of care, socialization and veterinary follow-up.")}
<div class="adopt"><div>
<p class="price">€1,800</p><p class="price-note">Pet kitten, everything included</p>
<ul class="incl"><li>LOOF pedigree</li><li>Already spayed or neutered</li><li>Microchip identification</li><li>Vaccinations, deworming and veterinary certificate</li><li>Tested, closely followed parents</li><li>Sales contract and information document</li><li>Photo album and lifelong support</li></ul>
</div>
<ol class="steps">
<li><span class="n">i.</span><div><b>Getting to know each other</b><p>You write to us. We talk about your home, your lifestyle and the kitten that suits you.</p></div></li>
<li><span class="n">ii.</span><div><b>Meeting our cats</b><p>You visit us at home in Bordeaux to meet the parents and see how our cats live with the family.</p></div></li>
<li><span class="n">iii.</span><div><b>Reserving</b><p>A deposit reserves your kitten. You receive its photos week after week.</p></div></li>
<li><span class="n">iv.</span><div><b>Welcoming your kitten</b><p>Between 15 weeks and 4½ months, spayed or neutered, your kitten joins your home. We are always here for you, and its photos keep growing its album.</p></div></li>
</ol></div>
</div></section>
<section class="verify" id="verifier"><div class="wrap">
<div class="head" style="margin-bottom:0"><p class="label">Check an ad</p><h2>Our photos sometimes appear in fake ads</h2></div>
<div class="verify-grid">
<div><b>Our kittens are here</b><p>Only the kittens shown on our <a href="../chatons/">Our kittens</a> page are available. Any ad elsewhere using our photos under another name is a scam.</p></div>
<div><b>A real French breeder has a SIRET</b><p>Every kitten ad in France must show this business number. Ours: <span class="siret">{SIRET}</span>.</p></div>
<div><b>In doubt? Write to us</b><p>Send us the link to the ad. We will answer you and report it.</p></div>
</div></div></section>
<section class="center"><div class="wrap"><a class="btn" href="../contact/">Write to us</a></div></section>""")
page("adopter", T("Adopter un chaton Sacré de Birmanie à Bordeaux · des Innamorati", "Adopt a Birman Kitten from a French Breeder · des Innamorati"), corps,
     desc=T("Adopter un chaton Sacré de Birmanie LOOF près de Bordeaux : 1 800 €, stérilisé, pucé, vacciné, départ entre 15 semaines et 4 mois et demi. Déroulement et vérification des annonces.",
            "Adopt a LOOF pedigree Birman kitten from our family cattery in Bordeaux, France: €1,800, spayed or neutered, microchipped, vaccinated, leaving between 15 weeks and 4½ months. How it works and how to spot fake ads."),
     ld=[ariane((T("Accueil", "Home"), ""), (T("Adopter", "Adopt"), "adopter/"))], prio=0.8)

# ---------- Contact ----------
r = "../"
chatons_opts = "".join(f'<option>{e(BY[f]["titre"])}</option>' for f in CFG["chatons_disponibles"] if "à réserver" in (BY[f]["statut_fr"] or ""))
projets = T(["Entrer dans notre liste de pré-réservation", "Adopter un chaton", "Adopter un retraité", "Autre question"],
            ["Join our pre-reservation list", "Adopt a kitten", "Adopt a retired cat", "Other question"])
corps = f"""<section><div class="wrap contact">
<div class="text"><p class="label">Contact</p><h1>{T("Parlons de votre futur Birman", "Let’s talk about your future Birman")}</h1>
<p>{T("Magali vous répond personnellement, le soir et le week-end, et Tristan la seconde pour vous répondre aussi en journée.", "Magali answers personally in the evenings and at weekends, and Tristan helps her reply during the day. We are happy to write in English.")}</p>
<p>Chatterie des Innamorati<br>Bordeaux, Gironde{T("", ", France")}</p>
<p>E-mail{T(" : ", ": ")}<a class="mel" href="#" data-u="innamoraticats" data-d="tristanperrier.fr">innamoraticats [at] tristanperrier.fr</a><br>
Facebook{T(" : ", ": ")}<a href="https://www.facebook.com/desinnamorati" target="_blank" rel="noopener">facebook.com/desinnamorati</a><br>Messenger{T(" : ", ": ")}<a href="https://m.me/desinnamorati" target="_blank" rel="noopener">m.me/desinnamorati</a></p>
</div>
<form class="form" id="formulaire" action="https://formsubmit.co/{EMAIL}" method="POST">
<p class="label">{T("Nous écrire", "Write to us")}</p>
<input type="hidden" name="_subject" value="{T("Nouveau message depuis le site des Innamorati", "Nouveau message en anglais depuis le site des Innamorati")}">
<input type="hidden" name="_next" value="{lien("contact/merci/")}">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false">
{T("", '<input type="hidden" name="Langue" value="Anglais (version anglaise du site)">')}
<input type="text" name="_honey" class="pot" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="f2"><label>{T("Prénom et nom", "Full name")}<input name="Nom" required autocomplete="name"></label>
<label>E-mail<input type="email" name="email" required autocomplete="email"></label></div>
<div class="f2"><label><span>{T("Téléphone", "Phone")} <small>· {T("facultatif", "optional")}</small></span><input type="tel" name="Téléphone" autocomplete="tel"></label>
<label>{T("Ville", "City and country")}<input name="Ville" required autocomplete="address-level2"></label></div>
<label>{T("Votre projet", "Your plans")}<select name="Projet" required>
<option value="">{T("Choisir", "Choose")}</option>{"".join(f"<option>{x}</option>" for x in projets)}</select></label>
<label><span>{T("Chaton qui vous intéresse", "Kitten you are interested in")} <small>· {T("facultatif", "optional")}</small></span><select name="Chaton" id="f-chaton"><option value="">{T("Aucun en particulier", "None in particular")}</option>{chatons_opts}</select></label>
<label>{T("Votre message", "Your message")}<textarea name="Message" rows="6" required placeholder="{T("Votre foyer, vos autres animaux, vos questions…", "Your home, your other pets, your questions…")}"></textarea></label>
<button class="btn" type="submit">{T("Envoyer", "Send")}</button>
<p class="fine-form">{T("Vos coordonnées servent uniquement à vous répondre.", "Your details are only used to reply to you.")}</p>
</form></div></section>
<script>
(function () {{
  var m = document.querySelector(".mel"); if (m) {{ var a = m.dataset.u + "@" + m.dataset.d; m.href = "mailto:" + a; m.textContent = a; }}
  var c = new URLSearchParams(location.search).get("chaton"), s = document.getElementById("f-chaton");
  if (c && s) {{ var o = Array.prototype.find.call(s.options, function (x) {{ return x.text === c; }});
    if (!o) {{ o = new Option(c, c); s.add(o); }} s.value = o.value;
    var p = document.querySelector('select[name="Projet"]'); if (p) p.value = "{projets[1]}"; }}
}})();
</script>"""
page("contact", T("Contact · Chatterie des Innamorati, Sacrés de Birmanie à Bordeaux", "Contact · Chatterie des Innamorati, Birman cats in Bordeaux, France"), corps, prio=0.6,
     desc=T("Contacter la Chatterie des Innamorati, élevage de Sacrés de Birmanie à Bordeaux : formulaire, e-mail, Facebook et Messenger.",
            "Contact the Chatterie des Innamorati, Birman cat breeder in Bordeaux, France: contact form, e-mail, Facebook and Messenger. We reply in English."))

corps = f"""<section><div class="wrap narrow center">{tete(T("Message envoyé", "Message sent"), T("Merci, votre message est bien parti", "Thank you, your message is on its way"), T("Magali vous répond personnellement le soir et le week-end, et Tristan en journée. Pensez à vérifier vos courriers indésirables.", "Magali replies personally in the evenings and at weekends, and Tristan during the day. Please check your spam folder too."))}
<p><a class="btn" href="../../chatons/">{T("Voir nos chatons", "See our kittens")}</a> <a class="btn" href="../../">{T("Retour à l'accueil", "Back to home")}</a></p></div></section>"""
page("contact/merci", T("Message envoyé · Chatterie des Innamorati", "Message sent · Chatterie des Innamorati"), corps, indexer=False)

# ---------- Mentions légales ----------
corps = T(f"""<section><div class="wrap narrow">{tete("Mentions légales", "Mentions légales")}
<div class="text legal">
<p><b>Éditeur</b><br>Magali Perrier, entreprise individuelle, élevage de Sacrés de Birmanie sous l'affixe LOOF « des Innamorati ».<br>SIRET {SIRET} · Bordeaux (33).</p>
<p><b>Photographies</b><br>La plupart des photographies sont l'œuvre de <a href="https://tristanperrier.fr" target="_blank" rel="noopener">Tristan Perrier, photographe</a>. Les autres ont été prises par les adoptants de nos chatons, qui nous les ont confiées. Toutes sont publiées par la Chatterie des Innamorati. Toute reproduction, en particulier dans des annonces de vente, est interdite et fera l'objet d'un signalement.</p>
<p><b>Hébergement</b><br>GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<p><b>Données personnelles</b><br>Ce site ne dépose aucun cookie de suivi. Les messages envoyés par le formulaire de contact transitent par le service FormSubmit jusqu'à notre boîte e-mail. Ils servent uniquement à vous répondre et ne sont jamais transmis à des tiers.</p>
</div></div></section>""", f"""<section><div class="wrap narrow">{tete("Legal notice", "Legal notice")}
<div class="text legal">
<p><b>Publisher</b><br>Magali Perrier, sole proprietorship, Birman cat breeding under the LOOF cattery name « des Innamorati ».<br>SIRET {SIRET} · Bordeaux (Gironde, France).</p>
<p><b>Photographs</b><br>Most photographs are by <a href="https://tristanperrier.fr" target="_blank" rel="noopener">Tristan Perrier, photographer</a>. The others were taken by the families of our kittens, who shared them with us. All are published by the Chatterie des Innamorati. Any reproduction, especially in sales ads, is prohibited and will be reported.</p>
<p><b>Hosting</b><br>GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA.</p>
<p><b>Personal data</b><br>This site sets no tracking cookies. Messages sent through the contact form pass through the FormSubmit service to our mailbox. They are only used to reply to you and are never shared with third parties.</p>
</div></div></section>""")
page("mentions-legales", T("Mentions légales · Chatterie des Innamorati", "Legal notice · Chatterie des Innamorati"), corps)

# ---------- llms.txt : résumé du site pour les assistants IA ----------
if L == "fr":
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(f"""# Chatterie des Innamorati

> Élevage familial de Sacrés de Birmanie (chats Birman) à Bordeaux, en Gironde, déclaré au LOOF sous l'affixe « des Innamorati » depuis 2016. Éleveuse : Magali Perrier (SIRET {SIRET}). Les chats vivent en famille, à la maison.

Informations clés :
- Race : Sacré de Birmanie (Birman), uniquement, chats inscrits au LOOF.
- Lieu : Bordeaux (Gironde, Nouvelle-Aquitaine, France). Aucun envoi de chaton : les adoptants viennent le chercher à Bordeaux, y compris depuis l'étranger.
- Prix d'un chaton de compagnie : 1 800 €, stérilisé, pucé, vacciné, avec pedigree LOOF.
- Départ des chatons : entre 15 semaines minimum et 4 mois et demi, tous stérilisés.
- Réservation : liste de pré-réservation, contact par le formulaire du site.
- Reproducteurs titrés en expositions FIFe et LOOF (Œdipe des Innamorati : SC, National Winner, Junior Winner, DSM, DVM).
- Les photos du site sont protégées : toute annonce qui les reprend ailleurs est frauduleuse.
- Le site existe aussi en anglais : {SITE}en/

## Pages principales
- [Accueil]({SITE}): présentation de l'élevage à Bordeaux
- [Le Sacré de Birmanie]({SITE}le-birman/): histoire, légende, standard, caractère, entretien, différences avec le Ragdoll et le Siamois
- [Couleurs du Sacré de Birmanie]({SITE}couleurs/): les 40 couleurs reconnues, en photos
- [Nos chatons]({SITE}chatons/): chatons disponibles et réservés
- [Adopter]({SITE}adopter/): prix, conditions, déroulement, vérifier une annonce
- [Nos chats]({SITE}nos-chats/): reproducteurs et retraités, avec dates de naissance, titres et palmarès
- [Expositions]({SITE}expositions/): résultats depuis 2014
- [Contact]({SITE}contact/): formulaire
""")
else:
    open(os.path.join(OUT, "llms.txt"), "a", encoding="utf-8").write(f"""
## English summary

Chatterie des Innamorati is a family-run Birman cat (Sacré de Birmanie, Sacred Cat of Burma) cattery in Bordeaux, France, registered with the LOOF under the cattery name « des Innamorati » since 2016. Breeder: Magali Perrier. Pet kittens cost €1,800 and leave between 15 weeks and 4½ months, already spayed or neutered, microchipped, vaccinated and with a LOOF pedigree. Kittens are never shipped: every family collects their kitten in person in Bordeaux, including families from abroad. The site's photos are protected: any ad elsewhere using them is fraudulent.

- [Home]({SITE}en/): the cattery in Bordeaux, France
- [The Birman cat]({SITE}en/birman-cat/): history, legend, standard, personality, care, Birman vs Ragdoll and Siamese
- [Birman cat colors]({SITE}en/birman-cat-colors/): all 40 recognized colors, in photos
- [Kittens]({SITE}en/kittens/): available and reserved kittens
- [Adopt]({SITE}en/adopt/): price, conditions, process, checking an ad
- [Our cats]({SITE}en/our-cats/): breeding and retired cats, with birth dates, titles and show results
- [Cat shows]({SITE}en/cat-shows/): results since 2014
- [Contact]({SITE}en/contact/): contact form, replies in English
""")
