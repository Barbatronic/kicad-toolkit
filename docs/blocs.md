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
| `Alim_LDO_3V3` | Régulateur linéaire 5 V vers 3,3 V (AMS1117) avec découplage en entrée et en sortie |
| `Regul_5V` | Régulateur 78E05 vers 5 V, avec ses deux LED de signalisation |
| `Bus_I2C` | Tirages 4k7 vers 3,3 V et connecteur quatre points |
| `Servos` | Une sortie servomoteur avec résistance de série sur le signal, à dupliquer autant que nécessaire |
| `LED_Etat` | Voyant avec sa résistance de limitation |
| `Bouton_Poussoir` | Bouton avec tirage et filtrage anti-rebond |

Voir [Installation](installation#les-blocs-de-conception) pour déclarer la
librairie de blocs dans KiCad.

{: .note }
> Le bloc `Regul_5V` utilise un symbole de la librairie **SparkFun KiCad
> Libraries** (`PCM_SparkFun-PowerSymbol:VCC`). Installez ce paquet depuis le
> gestionnaire de contenu si le symbole apparaît en rouge après avoir posé
> le bloc.

## Poser un bloc

Dans l'éditeur de schéma, le panneau **Blocs de conception** s'ouvre par
**Affichage**, **Panneaux**. Sélectionnez un bloc et déposez-le dans la feuille,
soit directement, soit comme feuille hiérarchique.

## Maintenance

Ces six blocs sont désormais tenus à jour directement dans KiCad, pas par un
script : les modifier revient à ouvrir le `.kicad_sch` du bloc dans l'éditeur
de schéma, l'ajuster, puis l'enregistrer. Voir
[Maintenir le toolkit](maintenance#ajouter-un-bloc-de-conception).
