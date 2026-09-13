# Symboles au format KiCad 5

Les symboles Digi-Key sont diffusés au format `.lib` et `.dcm`, hérité de KiCad 5.
KiCad 10 ne les charge plus directement et le gestionnaire de contenu ne les
inscrit pas dans la table des librairies, qui n'accepte que le format `.kicad_sym`.

Ils sont conservés ici pour rester disponibles. Les **empreintes** Digi-Key, elles,
sont au format courant et fonctionnent immédiatement : voir la librairie
`ThirdParty_Digikey`.

## Convertir une librairie

Dans l'éditeur de symboles, menu **Fichier**, **Importer**, **Librairie de symboles**,
puis choisir le fichier `.lib` voulu. KiCad convertit et propose d'enregistrer au
format actuel.

En ligne de commande, pour convertir une librairie :

```bash
kicad-cli sym upgrade dk_Sensors-Transducers.lib
```

## Pourquoi ne pas tout convertir d'avance

La librairie Digi-Key compte une centaine de catégories, soit plusieurs milliers de
symboles dont je n'utilise qu'une poignée. Les convertir toutes alourdirait le
paquet pour un intérêt limité, alors que le dépôt officiel Digi-Key est disponible
dans le gestionnaire de contenu de KiCad et se met à jour tout seul.
