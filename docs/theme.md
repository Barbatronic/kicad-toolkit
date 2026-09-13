---
title: Thème sombre
nav_order: 7
---

# Thème sombre

Le thème de couleurs que j'utilise au quotidien, pensé pour les longues séances de
saisie de schéma et de routage.

## Choisir le thème

Après installation du paquet **Barbatronic - thème sombre** :

- Schéma : **Préférences**, **Éditeur de schémas**, **Couleurs**, puis
  **Barbatronic** dans la liste des thèmes.
- Circuit imprimé : **Préférences**, **Éditeur de circuits imprimés**,
  **Couleurs**, même liste.

## La palette

Sur le schéma, fond gris-bleu profond, contours de symbole et broches en ambre,
fils et jonctions en vert, valeurs et étiquettes de feuille en turquoise,
étiquettes globales en orange, champs en mauve.

Sur le circuit, cuivre avant en rouge et cuivre arrière en bleu, contour de carte
en jaune clair, sérigraphie en blanc cassé, cotes et repères de fabrication en gris.

## Le modifier

Le thème est un simple fichier JSON. Copiez-le dans votre configuration KiCad pour
en faire une variante :

```bash
cp "${KICAD10_3RD_PARTY}/colors/com_github_barbatronic_kicad-theme/Barbatronic.json" \
   ~/.config/kicad/9.0/colors/Barbatronic-perso.json
```

Changez le champ `meta.name` du fichier copié, sinon les deux thèmes portent le
même nom dans la liste.
