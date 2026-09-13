---
title: Librairies tierces
parent: Librairies
nav_order: 3
---

# Librairies tierces

Certaines librairies que j'utilise ne sont pas de moi. Elles sont réunies dans un
paquet séparé, sous leur licence d'origine, avec le texte de chaque licence.

Plusieurs de ces fichiers portent les retouches que j'y ai faites au fil des
projets, notamment les variantes d'implantation des modules montés par en dessous.
Ils ne sont donc pas toujours identiques à ceux publiés par leur auteur.

## Ce que contient le paquet

| Librairie | Contenu | Auteur d'origine | Licence |
|---|---|---|---|
| `ThirdParty_Seeed_XIAO` | 27 symboles et 4 empreintes de la gamme XIAO | Seeed Studio | non précisée |
| `ThirdParty_Digikey` | 318 empreintes | Digi-Key Electronics | CC BY-SA 4.0 |
| `ThirdParty_SparkFun_RF` | 34 empreintes RF, XBee, RFM, ID-12 | SparkFun Electronics | CC BY 4.0 |
| `ThirdParty_Teensy` | 12 empreintes et 3 modèles 3D | Ricardo Band | MIT |
| `ThirdParty_TMC_StepStick` | TMC2208 et TMC2209 SilentStepStick | via SnapEDA | voir ci-dessous |
| `ThirdParty_SparkFun` | Teensy 4.0 DEV-15583, convertisseur BOB-12009 | SparkFun, via SnapEDA | voir ci-dessous |
| `ThirdParty_DFRobot` | Lecteur MP3 DFR0299 | DFRobot, via SnapEDA | voir ci-dessous |
| `ThirdParty_Arduino` | Trous de fixation Arduino | Projet KiCad | CC BY-SA 4.0 |

Le paquet pèse environ 45 Mo, dont 40 Mo de modèles 3D. Les modules Teensy à eux
seuls représentent 26 Mo : le modèle du Teensy 4.1 fait 18 Mo. Si le
téléchargement vous gêne, n'installez que le paquet principal.

## Origine et licences

### Les modèles issus de SnapEDA

Les symboles et empreintes `TMC2208_SILENTSTEPSTICK`, `TMC2209_SILENTSTEPSTICK`,
`DEV-15583`, `BOB-12009` et `DFR0299` viennent de SnapEDA. Leurs conditions
d'utilisation encadrent la redistribution. Ils figurent ici parce que je les ai
retouchés pour mes cartes et que je tiens à ce que mes projets restent
reproductibles à partir de ce seul dépôt.

Si vous êtes ayant droit et que cela pose problème, ouvrez une
[issue](https://github.com/Barbatronic/kicad-toolkit/issues) et je retirerai les
fichiers concernés.

### Digi-Key

Digi-Key autorise l'usage libre de sa librairie dans des projets commerciaux ou
fermés, sans obligation de partager ses fichiers de conception. La redistribution
de la librairie elle-même doit en revanche rester sous CC BY-SA 4.0 avec
attribution, ce qui est le cas ici.

Le dépôt officiel Digi-Key est aussi disponible directement dans le gestionnaire
de contenu de KiCad, et s'y met à jour tout seul.

### Seeed Studio

Le dépôt [OPL de Seeed Studio](https://github.com/Seeed-Studio/OPL_Kicad_Library)
ne porte pas de fichier de licence. Les fichiers sont diffusés publiquement par
Seeed pour encourager l'usage de leurs cartes.

## Les symboles Digi-Key

Digi-Key diffuse ses symboles au format `.lib` hérité de KiCad 5, que KiCad 10 ne
charge plus directement. Ils sont conservés dans le paquet, sous
`resources/symboles-format-ancien/digikey/`, avec la marche à suivre pour les
convertir. Les **empreintes** Digi-Key, elles, sont au format courant et
s'utilisent immédiatement.

## Nettoyage effectué

Les références de modèles 3D qui pointaient vers des chemins n'existant que sur ma
machine ont été réécrites vers les modèles fournis par le paquet, ou retirées
quand le modèle n'était pas disponible.

Sept empreintes Digi-Key portaient dans leur champ de description le chemin de
téléchargement local d'un employé de Digi-Key, du genre
`file:///C:/Users/<prénom_nom>/Downloads/...`. Ces champs ont été supprimés :
le lien était mort, et il n'y a pas de raison de republier ce nom.
