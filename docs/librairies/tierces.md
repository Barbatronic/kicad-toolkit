---
title: Librairies tierces
parent: Librairies
nav_order: 3
---

# Librairies tierces

Certaines librairies que j'utilise ne sont pas de moi. Celles dont la licence
autorise la redistribution sont réunies dans un paquet séparé, sous leur licence
d'origine et avec leur texte de licence.

## Ce que contient le paquet

| Librairie | Auteur | Licence | Source |
|---|---|---|---|
| `ThirdParty_SparkFun_RF` | SparkFun Electronics | CC BY 4.0 | [SparkFun-KiCad-Libraries](https://github.com/sparkfun/SparkFun-KiCad-Libraries) |
| `ThirdParty_Teensy` | Ricardo Band | MIT | [XenGi/teensy.pretty](https://github.com/XenGi/teensy.pretty) |

Les empreintes sont reprises telles quelles, sans modification de leur géométrie.
Seul le nom de la librairie a reçu un préfixe, pour éviter les collisions dans la
table des librairies.

## Ce qui n'y est pas, et où le trouver

Plusieurs librairies courantes ne sont pas redistribuées ici. Voici où les prendre
directement à la source.

### Modèles issus de SnapEDA

Les symboles `TMC2208_SILENTSTEPSTICK`, `TMC2209_SILENTSTEPSTICK`, `DEV-15583`,
`BOB-12009` et `DFR0299` que j'ai utilisés proviennent de SnapEDA. Leurs conditions
d'utilisation n'autorisent pas la redistribution en tant que librairie. Il faut les
télécharger depuis [snapeda.com](https://www.snapeda.com/) avec un compte.

### Digi-Key

La librairie Digi-Key est sous CC BY-SA 4.0 et pourrait être redistribuée, mais
elle est déjà disponible en un clic : ajoutez le dépôt officiel Digi-Key dans le
gestionnaire de contenu de KiCad. Rien à gagner à en refaire une copie.

### Seeed Studio XIAO

Les cartes XIAO, que j'utilise beaucoup, sont publiées par Seeed Studio sur
[Seeed-Studio/OPL_Kicad_Library](https://github.com/Seeed-Studio/OPL_Kicad_Library).
Le dépôt ne porte pas de licence explicite, je préfère ne pas le redistribuer.

### Librairies officielles de KiCad

Résistances, condensateurs, connecteurs, régulateurs courants : tout est déjà
installé avec KiCad. Inutile d'en garder des copies dans un projet.
