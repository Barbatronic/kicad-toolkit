---
title: Règles de conception
nav_order: 6
---

# Règles de conception

Trois jeux de règles au format `.kicad_dru`, un par procédé de fabrication. Ils
complètent les contraintes du projet en ajoutant les vérifications que KiCad ne
fait pas par défaut, notamment sur la sérigraphie.

## Les fichiers

| Fichier | Procédé | Piste | Isolation | Perçage |
|---|---|---|---|---|
| `JLCPCB-2couches.kicad_dru` | JLCPCB 1 à 2 couches, cuivre 1 oz | 0,127 mm | 0,127 mm | 0,3 mm |
| `AISLER-2couches-HASL.kicad_dru` | AISLER 2 couches, 35 µm, HASL | 0,2 mm | 0,15 mm | 0,3 mm |
| `AISLER-2couches-ENIG.kicad_dru` | AISLER 2 couches, 35 µm, ENIG | 0,125 mm | 0,125 mm | 0,25 mm |

Chaque jeu vérifie aussi le diamètre et la couronne des vias, l'écart entre
perçages, la distance du cuivre au bord de carte, la sérigraphie sur pastille et
la taille minimale des textes de sérigraphie.

{: .note }
> Les valeurs sont volontairement un cran au-dessus des minimums absolus annoncés
> par les fabricants, pour garder de la marge. Les capacités exactes sont sur
> [jlcpcb.com](https://jlcpcb.com/capabilities/pcb-capabilities) et
> [community.aisler.net](https://community.aisler.net/t/pcb-design-rules/41).

## Utiliser un jeu de règles

KiCad lit les règles personnalisées dans un fichier portant le nom du projet.
Copiez le jeu voulu à côté du circuit imprimé et renommez-le :

```bash
cp "${KICAD9_3RD_PARTY}/resources/com_github_barbatronic_kicad-toolkit/design-rules/JLCPCB-2couches.kicad_dru" \
   ma-carte.kicad_dru
```

Le fichier se modifie aussi directement depuis pcbnew, menu **Fichier**,
**Règles de conception personnalisées**.

Lancez ensuite le contrôle des règles de conception : les violations remontent
avec le nom de la règle en clair, par exemple *Largeur de piste minimale*.

## Pourquoi des règles en plus des contraintes du projet

Les contraintes de l'onglet **Contraintes** s'appliquent partout de la même façon.
Le fichier `.kicad_dru` permet de viser précisément : une règle sur les vias
seulement, une autre sur la sérigraphie, une troisième sur une classe de nets.
Changer de fabricant revient alors à remplacer un seul fichier.
