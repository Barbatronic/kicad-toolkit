---
title: Accueil
nav_order: 1
---

# Barbatronic KiCad Toolkit

Mes librairies, blocs de conception et réglages KiCad, rassemblés au même endroit
et installables en deux clics depuis le gestionnaire de contenu de KiCad.

Je conçois des cartes de robotique et d'électronique depuis plusieurs années, et
les mêmes empreintes revenaient d'un projet à l'autre, recopiées à la main. Ce
dépôt met fin à cette recopie : une seule source, mise à jour depuis KiCad.

[Installer le toolkit](installation){: .btn .btn-primary }
[Voir ce qu'il contient](librairies){: .btn }

---

## Les trois paquets

| Paquet | Contenu |
|---|---|
| **Barbatronic Toolkit** | Symboles, empreintes et modèles 3D rangés par thème, blocs de conception, cartouche, règles de conception par fabricant, modèle de projet |
| **Librairies tierces** | SparkFun, Teensy, Digi-Key, Seeed XIAO, TMC SilentStepStick et DFRobot, sous leur licence d'origine |
| **Thème sombre** | Le thème de couleurs que j'utilise pour le schéma et le routage |

Les trois s'installent séparément : rien n'oblige à tout prendre.

## En un coup d'oeil

- Sept librairies de symboles et d'empreintes classées par usage : microcontrôleurs,
  alimentation, motorisation, capteurs, connectique, interface, mécanique.
- Six blocs de conception à déposer dans un schéma plutôt qu'à redessiner.
- Un cartouche qui affiche titre, sous-ensemble, révision, licence et index de feuille.
- Trois jeux de règles de conception prêts pour JLCPCB et AISLER.
- Un modèle de projet avec ses classes de nets et ses contraintes déjà réglées.

## Compatibilité

Le toolkit demande **KiCad 10.0 ou plus récent**. Les chemins des modèles 3D et des
ressources reposent sur la variable `KICAD10_3RD_PARTY`, qui n'existe pas sur les
versions antérieures.
