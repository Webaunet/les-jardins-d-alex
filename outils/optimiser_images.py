#!/usr/bin/env python3
"""Redimensionne et compresse les photos sources vers images/ (jamais d'agrandissement)."""
import os, sys
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/Maquettes/Images/Paysagiste"
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")

# source : (nom de sortie, largeur max, qualité)
M = {
    "imgi_7_entretien-jardin.jpg": ("hero-jardin-allee.jpg", 1200, 78),
    "jardin-robot": None,
    "robot tonte de pelouse.jpg": ("jardin-robot-tonte-terrasse.jpg", 1200, 78),
    "imgi_4_creation-espace-vert.jpg": ("creation-jardin-contemporain.jpg", 640, 78),
    "chantier terrasse en bois.jpg": ("terrasse-bois-chantier.jpg", 640, 78),
    "alléé pavés carrelage extérieure.jpg": ("allee-pavee-muret-pierre.jpg", 640, 78),
    "maçonerie paysagère.jpg": ("maconnerie-paysagere-escalier.jpg", 640, 78),
    "imgi_6_plantation.jpg": ("plantation-massif.jpg", 640, 78),
    "conception chantier.jpg": ("conception-jardin-tablette.jpg", 640, 78),
    "imgi_2_tonte.jpg": ("tonte-pelouse.jpg", 640, 78),
    "imgi_1_taille-haies.jpg": ("taille-haie-laurier.jpg", 640, 78),
    "imgi_1_elagage-chene.jpg": ("elagage-chene.jpg", 640, 78),
    "imgi_3_dessouchage.jpg": ("dessouchage.jpg", 640, 78),
    "imgi_5_feuilles.jpg": ("ramassage-feuilles.jpg", 640, 78),
    "imgi_8_nivellement.jpg": ("nivellement-terrain.jpg", 640, 78),
    "imgi_7_terrassement.jpg": ("terrassement-jardin.jpg", 640, 78),
    "imgi_4_desherbage.jpg": ("desherbage-massif.jpg", 640, 78),
    "imgi_7_dechets-verts.jpg": ("evacuation-dechets-verts.jpg", 640, 78),
    "imgi_3_entretien-general.jpg": ("tonte-pelouse-casque.jpg", 640, 78),
    "imgi_10_nettoyage.jpg": ("nettoyage-jardin-brouette.jpg", 640, 78),
    "imgi_1_hero-elagage-chene.jpg": ("elagage-chene-jardin.jpg", 640, 78),
    "chantier allée dallée.jpg": ("chantier-allee-dallee-eclairee.jpg", 640, 78),
    "imgi_4_taille-haies.jpg": ("taille-haie-jardin.jpg", 640, 78),
}
os.makedirs(DST, exist_ok=True)
for s, v in M.items():
    if v is None:
        continue
    n, w, q = v
    im = Image.open(os.path.join(SRC, s)).convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    p = os.path.join(DST, n)
    im.save(p, "JPEG", quality=q, optimize=True, progressive=True)
    print(n, im.size, os.path.getsize(p) // 1024, "Ko")
