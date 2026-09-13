---
title: Blocs de conception
nav_order: 4
---

# Blocs de conception

Des morceaux de schéma tout faits, à déposer dans une feuille plutôt qu'à
redessiner à chaque carte.

{: .note }
> Cette page est régénérée à chaque publication avec le rendu de chaque bloc.
> Si vous lisez cette version, le catalogue n'a pas encore été produit.

| Bloc | Ce qu'il contient |
|---|---|
| `Alim_LDO_3V3` | Régulateur linéaire 5 V vers 3,3 V avec découplage en entrée et en sortie |
| `Entree_Alim_Protegee` | Bornier d'entrée, fusible, diode anti-inversion, condensateur réservoir |
| `Bus_I2C` | Tirages 4k7 vers 3,3 V et connecteur quatre points |
| `Servos_x4` | Quatre sorties servomoteur sur alimentation dédiée |
| `LED_Etat` | Voyant avec sa résistance de limitation |
| `Bouton_Poussoir` | Bouton avec tirage et filtrage anti-rebond |

Voir [Installation](installation#les-blocs-de-conception) pour déclarer la
librairie de blocs dans KiCad.

## Poser un bloc

Dans l'éditeur de schéma, le panneau **Blocs de conception** s'ouvre par
**Affichage**, **Panneaux**. Sélectionnez un bloc et déposez-le dans la feuille,
soit directement, soit comme feuille hiérarchique.
