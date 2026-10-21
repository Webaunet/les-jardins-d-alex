#!/usr/bin/env python3
"""Génère les 5 pages HTML de la maquette. Usage : python3 outils/build.py (depuis la racine du dépôt)."""
import os, re
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = "https://webaunet.github.io/les-jardins-d-alex/"
TEL = "06 64 10 34 57"
TELURI = "tel:+33664103457"
MAIL = "alex.noc78@gmail.com"

PAGES = [("index.html", "Accueil"), ("prestations.html", "Prestations"),
         ("realisations.html", "Réalisations"), ("contact.html", "Contact")]


def dims(name):
    with Image.open(os.path.join(ROOT, "images", name)) as im:
        return im.size


def img(name, alt, lazy=True, style="", cls=""):
    w, h = dims(name)
    return ('<img src="images/%s" width="%d" height="%d"%s%s%s alt="%s">' % (
        name, w, h, ' loading="lazy"' if lazy else "",
        ' class="%s"' % cls if cls else "", ' style="%s"' % style if style else "", alt))


FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E"
           "%3Ccircle cx='20' cy='20' r='20' fill='%232c6a3c'/%3E"
           "%3Cpath d='M12 29c0-9 5-15 16-17-1 10-6 16-14 16' fill='%23fff'/%3E%3C/svg%3E")

PHONE_SVG = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
             '<path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>')
TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m7.5 12.5 3 3 6-7"/></svg>')


def header(cur):
    items = ""
    for href, label in PAGES:
        c = ' aria-current="page"' if href == cur else ""
        items += '<li><a href="%s"%s>%s</a></li>' % (href, c, label)
    return """<a class="skip" href="#contenu">Aller au contenu</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="%s" aria-label="Les Jardins d'Alex, accueil">
      <svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="20" fill="var(--accent)"/><path d="M12 29c0-9 5-15 16-17-1 10-6 16-14 16" fill="var(--accent-fg)"/><path d="M12 30c3-6 7-10 12-13" stroke="var(--accent)" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>
      <span>Les Jardins d'Alex</span>
    </a>
    <nav class="nav" id="menu" aria-label="Navigation principale"><ul>%s</ul></nav>
    <a class="btn btn-primary head-cta" href="%s" aria-label="Appeler le %s">%s<span class="label">%s</span></a>
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span></button>
  </div>
</header>""" % (BASE, items, TELURI, TEL, PHONE_SVG, TEL)


FOOTER = """<footer class="footer">
  <div class="wrap">
    <div><span class="name">Les Jardins d'Alex</span> <small>· Bazemont (78) · SIREN 894 931 880</small></div>
    <nav aria-label="Pied de page">
      <a href="%s">%s</a>
      <a href="mailto:%s">%s</a>
      <a href="mentions-legales.html">Mentions légales</a>
    </nav>
  </div>
</footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>""" % (TELURI, TEL, MAIL, MAIL)


def page(fname, title, desc, main, cur):
    html = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="icon" href="%s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Source+Sans+3:wght@400;600&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
%s
<main id="contenu">
%s
</main>
%s
<script src="site.js" defer></script>
</body>
</html>
""" % (title, desc, FAVICON, header(cur), main, FOOTER)
    with open(os.path.join(ROOT, fname), "w", encoding="utf8") as f:
        f.write(html)


# ---------------------------------------------------------------- ACCUEIL (repris de l'artefact validé)
src = open(os.path.join(ROOT, "outils", "accueil-artefact.html"), encoding="utf8").read()
index_main = src.split('<main id="accueil">')[1].split("</main>")[0]
index_main = re.sub(r'src="images/([^"]+)" width="\d+" height="\d+"',
                    lambda m: 'src="images/%s" width="%d" height="%d"' % ((m.group(1),) + dims(m.group(1))), index_main)
index_main = index_main.replace('<img src="images/hero-jardin-allee.jpg"', '<img fetchpriority="high" src="images/hero-jardin-allee.jpg"')
page("index.html", "Les Jardins d'Alex | Aménagement paysager à Bazemont (78)",
     "Les Jardins d'Alex, entreprise d'aménagement paysager à Bazemont (78) : création de jardins, terrasses, allées, murets et entretien des espaces verts.",
     index_main, "index.html")

# ---------------------------------------------------------------- PRESTATIONS
SP = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 42V24"/><path d="M24 26c0-8-6-12-14-12 0 8 6 12 14 12z"/><path d="M24 22c0-6 5-10 12-10 0 6-5 10-12 10z"/></svg>'
SU = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><circle cx="24" cy="24" r="8"/><path d="M24 6v6M24 36v6M6 24h6M36 24h6M11 11l4 4M33 33l4 4M37 11l-4 4M15 33l-4 4"/></svg>'
AU = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 38C8 22 18 10 40 8c0 22-10 32-26 30"/><path d="M10 38C16 28 22 22 30 17"/></svg>'
WI = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M24 5v38M7.5 14.5l33 19M7.5 33.5l33-19"/><path d="m19 8 5 4 5-4M19 40l5-4 5 4"/></svg>'


def season(cls, icon, pill, title, items):
    return ('<li><article class="season season--%s">%s<span class="pill">%s</span><h3>%s</h3><ul>%s</ul></article></li>'
            % (cls, icon, pill, title, "".join("<li>%s</li>" % i for i in items)))


def hrow(name, alt, title, text, style=""):
    return ('<li><article class="hrow">%s<div><h3>%s</h3><p>%s</p></div></article></li>'
            % (img(name, alt, style=style), title, text))


def panel(name, alt, title, text, style=""):
    return '<li><article class="panel">%s<div><h3>%s</h3><p>%s</p></div></article></li>' % (img(name, alt, style=style), title, text)


presta = """
<section class="phead" aria-labelledby="h1">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Prestations</p>
      <h1 id="h1">Aménager, puis entretenir.</h1>
      <p class="lead">De la préparation du terrain à la taille des haies : les travaux d'aménagement paysager de Les Jardins d'Alex, de la création du jardin à son entretien.</p>
      <div class="actions"><a class="btn btn-primary" href="#amenager">Aménager</a><a class="btn btn-ghost" href="#entretenir">Entretenir</a></div>
    </div>
    <div class="mosaic">
      %s
      %s
      %s
    </div>
  </div>
</section>

<section class="terrain" id="amenager" aria-labelledby="h-terrain">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Aménager · le terrain</p><h2 id="h-terrain">Préparer le sol, puis planter</h2></div>
      <p>Un beau jardin commence sous la surface : un terrain travaillé, nivelé, prêt à recevoir ce qu'on y met.</p>
    </div>
    <ul class="hrows">
      %s
      %s
      %s
    </ul>
  </div>
</section>

<section class="stonewood" aria-labelledby="h-pierre">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Aménager · pierre et bois</p><h2 id="h-pierre">Terrasses, allées et murets</h2></div>
      <p>Les ouvrages qui structurent un extérieur et relient la maison au jardin.</p>
    </div>
    <ul class="panels">
      %s
      %s
      %s
    </ul>
  </div>
</section>

<section class="seasons-sec" id="saisons" aria-labelledby="h-saisons">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Calendrier du jardin</p><h2 id="h-saisons">Un jardin, quatre saisons</h2></div>
      <p>Repères généraux sur les travaux habituels de chaque saison. Le calendrier réel dépend du jardin et de la météo.</p>
    </div>
    <ul class="seasons">
      %s
      %s
      %s
      %s
    </ul>
  </div>
</section>

<section class="careplan" id="entretenir" aria-labelledby="h-entretien">
  <div class="wrap grid">
    %s
    <div>
      <p class="eyebrow">Entretenir</p>
      <h2 id="h-entretien">L'entretien, toute l'année</h2>
      <ul class="ticks">
        <li>%s<span>Tonte et entretien de la pelouse</span></li>
        <li>%s<span>Taille de haies</span></li>
        <li>%s<span>Élagage des arbres</span></li>
        <li>%s<span>Dessouchage</span></li>
        <li>%s<span>Désherbage des massifs</span></li>
        <li>%s<span>Évacuation des déchets verts</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="h-band">
  <div class="wrap grid">
    <div>
      <h2 id="h-band">Un terrain, une envie : expliquez-nous.</h2>
      <p>Décrivez ce que vous voulez aménager ou entretenir. Un message suffit pour démarrer la discussion.</p>
      <div class="actions"><a class="btn btn-light" href="contact.html">Préparer ma demande</a><a class="btn btn-ghost" href="%s">Appeler le %s</a></div>
    </div>
    %s
  </div>
</section>
""" % (
    img("hero-jardin-allee.jpg", "Jardin de campagne avec pelouse, massifs fleuris et allée de gravier menant à une maison en pierre", lazy=False),
    img("tonte-pelouse-casque.jpg", "Jardinier casqué poussant une tondeuse rouge sur une pelouse devant une maison en pierre", lazy=False, style="object-position:45% 50%"),
    img("elagage-chene-jardin.jpg", "Élagueur casqué dans un chêne avec une tronçonneuse, maison en brique et jardin en arrière-plan", lazy=False, style="object-position:60% 40%"),
    hrow("terrassement-jardin.jpg", "Ouvrier creusant la terre à la pelle près d'une brouette, au pied d'une maison en brique", "Terrassement", "Mise en forme du terrain avant l'aménagement : creusement, déblais et remblais."),
    hrow("nivellement-terrain.jpg", "Jardinier en pull vert nivelant la terre au râteau devant un massif et un arbre", "Nivellement", "Un sol régulier, prêt pour une pelouse, une allée ou des massifs."),
    hrow("plantation-massif.jpg", "Jardinier agenouillé mettant en terre un arbuste dans un massif, avec hostas et lavande autour", "Plantation", "Arbustes, vivaces et massifs mis en terre dans un sol préparé."),
    panel("terrasse-bois-chantier.jpg", "Ouvrier posant les lames d'une terrasse en bois devant une maison en pierre aux volets bleus", "Terrasse en bois", "Ossature, lames et finitions, de la préparation à la pose.", "object-position:65% 50%"),
    panel("chantier-allee-dallee-eclairee.jpg", "Allée en dalles de pierre en cours de pose devant une maison en pierre éclairée en soirée", "Allées et dallages", "Cheminements en dalles ou en pavés entre la maison, la terrasse et le jardin.", "object-position:55% 50%"),
    panel("maconnerie-paysagere-escalier.jpg", "Maçon montant un escalier et un muret en pierre dans un jardin en pente", "Maçonnerie paysagère", "Murets, marches et soutènements en pierre.", "object-position:40% 55%"),
    season("sp", SP, "Mars à mai", "Printemps", ["Reprise de la tonte", "Désherbage des massifs", "Plantations"]),
    season("su", SU, "Juin à août", "Été", ["Tonte régulière", "Taille des haies", "Massifs dégagés"]),
    season("au", AU, "Sept. à nov.", "Automne", ["Ramassage des feuilles", "Plantation d'arbustes", "Nettoyage des allées"]),
    season("wi", WI, "Déc. à fév.", "Hiver", ["Élagage", "Dessouchage", "Préparation des chantiers du printemps"]),
    img("taille-haie-jardin.jpg", "Jardinier en gilet gris taillant une haie dense avec un taille-haie, bâche et râteau au sol", style="object-position:35% 50%"),
    TICK, TICK, TICK, TICK, TICK, TICK,
    TELURI, TEL,
    img("nettoyage-jardin-brouette.jpg", "Homme ratissant un tas de branchages et de feuilles à côté d'une brouette, devant une maison en pierre"),
)
page("prestations.html", "Prestations | Les Jardins d'Alex, aménagement paysager à Bazemont (78)",
     "Prestations de Les Jardins d'Alex à Bazemont (78) : terrassement, plantation, terrasse en bois, allées, maçonnerie paysagère, tonte, taille de haies et élagage.",
     presta, "prestations.html")

# ---------------------------------------------------------------- RÉALISATIONS
def fanli(name, alt, r, y, pos):
    return '<li style="--r:%sdeg;--y:%spx">%s</li>' % (r, y, img(name, alt, lazy=False, style="object-position:%s" % pos))


def fig(name, alt, cap):
    return '<li><figure>%s<figcaption>%s</figcaption></figure></li>' % (img(name, alt), cap)


def tall(name, alt, cap, pos):
    return '<li><figure class="tall">%s<figcaption>%s</figcaption></figure></li>' % (img(name, alt, style="object-position:%s" % pos), cap)


real = """
<section class="fanhead" aria-labelledby="h1">
  <div class="wrap">
    <p class="eyebrow">Réalisations</p>
    <h1 id="h1">Terrasses, allées, murets et jardins entretenus</h1>
    <p class="lead">Un aperçu des ouvrages et des travaux d'entretien qui relèvent de l'aménagement paysager.</p>
    <div class="actions"><a class="btn btn-primary" href="#amenagements">Aménagements</a><a class="btn btn-line" href="#entretien-photos">Entretien</a></div>
    <ul class="fan" aria-label="Aperçu en éventail">
      %s
      %s
      %s
      %s
      %s
    </ul>
    <p class="fan-note">Photos d'illustration.</p>
  </div>
</section>

<section class="gallery" id="amenagements" aria-labelledby="h-amen">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Aménagements</p><h2 id="h-amen">Ce que l'on construit</h2></div>
      <p>Création de jardin, préparation de terrain, plantations et ouvrages en pierre ou en bois.</p>
    </div>
    <ul class="masonry">
      %s
      %s
      %s
      %s
      %s
      %s
    </ul>
  </div>
</section>

<section class="tallsec" id="entretien-photos" aria-labelledby="h-ent">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Entretien</p><h2 id="h-ent">Ce que l'on entretient</h2></div>
      <p>Pelouse, haies, arbres et massifs : les gestes qui gardent un jardin net et en bonne santé.</p>
    </div>
    <ul class="talls">
      %s
      %s
      %s
      %s
    </ul>
  </div>
</section>

<section class="bandstone" aria-labelledby="h-bs">
  <div class="wrap">
    <h2 id="h-bs">Un projet du même genre ?</h2>
    <p>Écrivez-nous quelques lignes, avec des photos de votre terrain si vous en avez : c'est un bon point de départ.</p>
    <div class="actions"><a class="btn btn-dark" href="mailto:%s?subject=Mon%%20projet%%20de%%20jardin">Écrire un e-mail</a><a class="btn btn-line" style="border-color:#143122;color:#143122" href="contact.html">Formulaire de contact</a></div>
  </div>
</section>
""" % (
    fanli("allee-pavee-muret-pierre.jpg", "Allée dallée de pierre claire longeant un muret fleuri, menant à une maison de campagne", -12, 34, "25% 50%"),
    fanli("terrasse-bois-chantier.jpg", "Ouvrier posant les lames d'une terrasse en bois devant une maison en pierre aux volets bleus", -6, 12, "70% 50%"),
    fanli("jardin-robot-tonte-terrasse.jpg", "Jardin avec pelouse tondue par un robot, allée en pavés, muret de pierre et terrasse en bois", 0, 0, "60% 50%"),
    fanli("maconnerie-paysagere-escalier.jpg", "Maçon montant un escalier et un muret en pierre dans un jardin en pente", 6, 12, "45% 50%"),
    fanli("conception-jardin-tablette.jpg", "Deux personnes examinent sur une tablette le plan 3D d'un jardin, devant une pelouse et un muret de pierre", 12, 34, "75% 50%"),
    fig("creation-jardin-contemporain.jpg", "Jeune paysagiste plantant un massif dans un jardin contemporain, devant une maison à façade grise", "Massif et pelouse devant une maison contemporaine"),
    fig("chantier-allee-dallee-eclairee.jpg", "Allée en dalles de pierre en cours de pose devant une maison en pierre éclairée en soirée", "Pose d'une allée en dalles"),
    fig("terrassement-jardin.jpg", "Ouvrier creusant la terre à la pelle près d'une brouette, au pied d'une maison en brique", "Terrassement avant aménagement"),
    fig("hero-jardin-allee.jpg", "Jardin de campagne avec pelouse, massifs fleuris et allée de gravier menant à une maison en pierre", "Jardin de campagne, massifs et allée de gravier"),
    fig("nivellement-terrain.jpg", "Jardinier en pull vert nivelant la terre au râteau devant un massif et un arbre", "Nivellement du terrain au râteau"),
    fig("plantation-massif.jpg", "Jardinier agenouillé mettant en terre un arbuste dans un massif, avec hostas et lavande autour", "Plantation d'un arbuste en massif"),
    tall("tonte-pelouse.jpg", "Jardinier tondant une pelouse devant une maison aux volets bleus et aux rosiers", "Tonte de pelouse", "30% 50%"),
    tall("taille-haie-laurier.jpg", "Jardinier équipé d'un casque anti-bruit taillant une haie avec un taille-haie thermique", "Taille de haie", "35% 50%"),
    tall("elagage-chene.jpg", "Élagueur casqué suspendu à une corde dans un chêne, tronçonneuse en main", "Élagage d'un chêne", "35% 50%"),
    tall("dessouchage.jpg", "Dessoucheuse jaune broyant une souche d'arbre au milieu d'une pelouse", "Dessouchage", "65% 50%"),
    MAIL,
)
page("realisations.html", "Réalisations | Les Jardins d'Alex, aménagement paysager à Bazemont (78)",
     "Exemples d'aménagements paysagers et de travaux d'entretien : terrasses, allées, murets, massifs, élagage. Les Jardins d'Alex, Bazemont (78).",
     real, "realisations.html")

# ---------------------------------------------------------------- CONTACT
def tip(icon, title, text):
    return '<li><article class="tip">%s<h3>%s</h3><p>%s</p></article></li>' % (icon, title, text)


def ico(path):
    return '<svg viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % path

PIN = ico('<path d="M18 33s10-8.5 10-17a10 10 0 0 0-20 0c0 8.500 10 17 10 17z"/><circle cx="18" cy="16" r="3.5"/>')
LEAF = ico('<path d="M7 29C6 17 13 7 30 6c0 16-8 23-19 22"/><path d="M7 29c5-8 10-13 16-17"/>')
CAL = ico('<rect x="5" y="7" width="26" height="24" rx="3"/><path d="M5 14h26M12 4v6M24 4v6"/>')
CAM = ico('<path d="M5 12h5l2-3h12l2 3h5v17H5z"/><circle cx="18" cy="20" r="5"/>')

contact = """
<section class="phead phead--short" aria-labelledby="h1">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1 id="h1">Parlons de votre jardin.</h1>
    <p class="lead">Appelez, écrivez ou préparez votre demande en ligne : Les Jardins d'Alex sont installés à Bazemont, dans les Yvelines.</p>
    <ul class="chips">
      <li><a href="%s">%s</a></li>
      <li><a href="mailto:%s">%s</a></li>
      <li>Bazemont (78)</li>
    </ul>
  </div>
</section>

<section class="formsec" id="formulaire" aria-labelledby="h-form">
  <div class="wrap">
    <div class="formgrid">
      <aside class="infocard" aria-label="Coordonnées">
        %s
        <div>
          <h2>Coordonnées</h2>
          <p>Alexandre Noc, Les Jardins d'Alex, Bazemont (78).</p>
          <div class="coord"><span>%s</span><button class="copy" type="button" data-copy="%s">Copier</button></div>
          <div class="coord"><span>%s</span><button class="copy" type="button" data-copy="%s">Copier</button></div>
          <p>Le formulaire prépare votre message. Vous choisissez ensuite de l'envoyer par SMS ou par e-mail, de le copier ou d'appeler directement.</p>
        </div>
      </aside>
      <div class="formcard">
        <h2 id="h-form">Préparer ma demande</h2>
        <form id="contact-form" class="form" novalidate>
          <div class="field"><label for="f-nom">Nom *</label><input id="f-nom" name="nom" type="text" autocomplete="name" required aria-required="true" aria-describedby="e-nom"><span class="err" id="e-nom" role="alert"></span></div>
          <div class="field"><label for="f-tel">Téléphone *</label><input id="f-tel" name="tel" type="tel" inputmode="tel" autocomplete="tel" required aria-required="true" aria-describedby="e-tel" placeholder="06 12 34 56 78"><span class="err" id="e-tel" role="alert"></span></div>
          <div class="field"><label for="f-mail">E-mail (facultatif)</label><input id="f-mail" name="mail" type="email" autocomplete="email" aria-describedby="e-mail" placeholder="nom@exemple.fr"><span class="err" id="e-mail" role="alert"></span></div>
          <div class="field"><label for="f-commune">Commune du projet *</label><input id="f-commune" name="commune" type="text" autocomplete="address-level2" required aria-required="true" aria-describedby="e-commune"><span class="err" id="e-commune" role="alert"></span></div>
          <div class="field full"><label for="f-type">Type de demande *</label>
            <select id="f-type" name="type" required aria-required="true" aria-describedby="e-type">
              <option value="">Choisir…</option>
              <option>Aménagement (jardin, terrasse, allée, muret)</option>
              <option>Entretien (tonte, haies, élagage)</option>
              <option>Autre demande</option>
            </select><span class="err" id="e-type" role="alert"></span></div>
          <div class="field full"><label for="f-msg">Votre message *</label><textarea id="f-msg" name="msg" required aria-required="true" aria-describedby="e-msg"></textarea><span class="err" id="e-msg" role="alert"></span></div>
          <div class="actions"><button class="btn btn-primary" type="submit">Préparer le message</button><span class="hint">* champs obligatoires</span></div>
        </form>
        <div class="recap" id="recap" hidden>
          <h3 id="recap-title" tabindex="-1">Votre demande est prête</h3>
          <pre id="recap-text"></pre>
          <div class="actions">
            <a class="btn btn-primary" id="r-sms" href="sms:+33664103457">Envoyer par SMS</a>
            <button class="btn btn-line" type="button" id="r-copy">Copier</button>
            <a class="btn btn-line" href="%s">Appeler</a>
            <a class="btn btn-line" id="r-mail" href="mailto:%s">Envoyer par e-mail</a>
          </div>
          <p class="note">Rien n'est envoyé automatiquement : le SMS et l'e-mail s'ouvrent dans votre application, prêts à partir.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tips" aria-labelledby="h-tips">
  <div class="wrap">
    <p class="eyebrow">Avant d'écrire</p>
    <h2 id="h-tips">Ce qui aide pour un premier échange</h2>
    <ul class="tipgrid">
      %s
      %s
      %s
      %s
    </ul>
  </div>
</section>
""" % (
    TELURI, TEL, MAIL, MAIL,
    img("evacuation-dechets-verts.jpg", "Homme chargeant des branchages dans une camionnette blanche, avec un jardin et une maison en arrière-plan", style="object-position:55% 50%"),
    TEL, TEL, MAIL, MAIL,
    TELURI, MAIL,
    tip(PIN, "La commune", "Indiquez où se trouve le terrain pour situer le projet."),
    tip(LEAF, "Le besoin", "Aménagement, entretien régulier ou travail ponctuel : dites ce que vous attendez."),
    tip(CAL, "La période", "Une date ou une saison souhaitée aide à organiser les travaux."),
    tip(CAM, "Des photos", "Si vous écrivez par e-mail, quelques photos du terrain donnent une première idée."),
)
page("contact.html", "Contact | Les Jardins d'Alex, aménagement paysager à Bazemont (78)",
     "Contactez Les Jardins d'Alex à Bazemont (78) : appelez le 06 64 10 34 57, écrivez par e-mail ou préparez votre demande avec le formulaire.",
     contact, "contact.html")

# ---------------------------------------------------------------- MENTIONS LÉGALES
legal = """
<section class="lhead" aria-labelledby="h1">
  <div class="wrap">
    <p class="eyebrow">Informations légales</p>
    <h1 id="h1">Mentions légales</h1>
  </div>
</section>
<section class="legal">
  <div class="wrap">
    <div class="narrow">
      <h2>Éditeur du site</h2>
      <dl>
        <dt>Nom commercial</dt><dd>Les Jardins d'Alex</dd>
        <dt>Dénomination (registre)</dt><dd>ALEXANDRE NOC (LES JARDINS D'ALEX)</dd>
        <dt>Dirigeant (registre)</dt><dd>Alexandre NOC</dd>
        <dt>SIREN</dt><dd>894 931 880</dd>
        <dt>Activité</dt><dd>Services d'aménagement paysager</dd>
        <dt>Commune</dt><dd>Bazemont (78)</dd>
        <dt>Téléphone</dt><dd><a href="%s">%s</a></dd>
        <dt>E-mail</dt><dd><a href="mailto:%s">%s</a></dd>
      </dl>
      <h2>Informations à compléter</h2>
      <p>Les éléments suivants ne figurent pas dans les informations disponibles et doivent être renseignés avant une mise en ligne définitive :</p>
      <ul>
        <li>forme juridique et adresse complète de l'entreprise ;</li>
        <li>numéro SIRET et, le cas échéant, numéro de TVA ;</li>
        <li>directeur de la publication ;</li>
        <li>nom et coordonnées de l'hébergeur du site.</li>
      </ul>
      <h2>Données personnelles</h2>
      <p>Le formulaire de contact ne transmet aucune donnée par lui-même : ce que vous saisissez reste dans votre navigateur tant que vous ne choisissez pas de l'envoyer par SMS ou par e-mail. Ce site ne dépose pas de cookie de mesure d'audience. Les polices de caractères sont chargées depuis Google Fonts.</p>
      <h2>Maquette</h2>
      <p>Ce site est une maquette de présentation. Les photographies sont des illustrations de métier.</p>
    </div>
  </div>
</section>
""" % (TELURI, TEL, MAIL, MAIL)
page("mentions-legales.html", "Mentions légales | Les Jardins d'Alex, Bazemont (78)",
     "Mentions légales du site de Les Jardins d'Alex, entreprise d'aménagement paysager à Bazemont (78) : éditeur, SIREN, données personnelles.",
     legal, "")
print("pages générées :", [p for p in os.listdir(ROOT) if p.endswith(".html")])
