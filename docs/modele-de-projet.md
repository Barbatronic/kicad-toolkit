---
title: Modèle de projet
nav_order: 5
---

# Modèle de projet

Le paquet installe un modèle de projet nommé **Barbatronic_Carte**, pour démarrer
une carte deux couches sans repasser par les mêmes réglages à chaque fois.

## Créer un projet à partir du modèle

Menu **Fichier**, **Nouveau projet à partir d'un modèle**, onglet **Modèles système**
ou **Modèles utilisateur** selon l'emplacement d'installation, puis **Barbatronic_Carte**.

## Ce qui est déjà réglé

### Classes de nets

Quatre classes, chacune avec sa couleur pour les distinguer d'un coup d'oeil sur
le schéma comme sur le circuit.

| Classe | Piste | Via | Isolation | Usage |
|---|---|---|---|---|
| `Default` | 0,25 mm | 0,6 / 0,3 mm | 0,2 mm | Tout le reste |
| `Signal` | 0,2 mm | 0,6 / 0,3 mm | 0,15 mm | Signaux logiques |
| `Power` | 0,5 mm | 0,8 / 0,4 mm | 0,25 mm | Rails d'alimentation |
| `HighCurrent` | 1,5 mm | 1,2 / 0,6 mm | 0,3 mm | Moteurs, puissance |

### Contraintes de fabrication

Des valeurs prudentes, acceptées par tous les fabricants courants en deux couches :
isolation minimale 0,15 mm, largeur de piste minimale 0,15 mm, perçage minimal
0,3 mm, couronne de via 0,13 mm, cuivre à 0,3 mm du bord de carte.

Pour serrer davantage selon le fabricant, ajoutez le jeu de
[règles de conception](regles-de-conception) correspondant.

### Le reste

- Cartouche Barbatronic sur le schéma et sur le circuit, copie locale au projet
  pour que celui-ci reste autonome.
- Largeurs de piste et tailles de via prêtes dans les listes déroulantes.
- Contour de carte de 100 × 80 mm sur `Edge.Cuts`, à redimensionner.
- Sortie de fabrication dirigée vers le sous-dossier `fab/`.
- Variables de texte `LICENCE`, `PROJET` et `VARIANTE`, utilisables dans le
  schéma sous la forme `${LICENCE}`.

## Après la création

Renseignez le cartouche par **Fichier**, **Configuration de la page** : titre,
révision, et le champ Commentaire 1 pour le sous-ensemble.
