---
title: Installation
nav_order: 2
---

# Installation
{: .no_toc }

1. TOC
{:toc}

---

## Ajouter le dépôt dans KiCad

L'installation passe par le gestionnaire de plugins et de contenu de KiCad. Une
fois le dépôt ajouté, les mises à jour se font depuis la même fenêtre.

1. Ouvrez KiCad, puis **Plugin and Content Manager** depuis l'écran d'accueil.
2. Déroulez la liste des dépôts en haut à droite et choisissez **Manage...**.
3. Ajoutez une ligne avec ces deux champs :

   | Champ | Valeur |
   |---|---|
   | Nom | `Barbatronic` |
   | URL | `https://barbatronic.github.io/kicad-toolkit/repository.json` |

4. Validez, puis sélectionnez **Barbatronic** dans la liste des dépôts.

Les trois paquets apparaissent alors dans les onglets **Libraries** et **Color Themes**.

## Installer les paquets

Cochez **Install** sur les paquets voulus, puis **Apply Pending Changes**.

KiCad télécharge chaque paquet, l'installe dans son dossier de contenu tiers et
inscrit les librairies dans vos tables globales. Elles portent le préfixe `PCM_`,
par exemple `PCM_Barbatronic_MCU`.

{: .note }
> Le préfixe `PCM_` se règle dans **Préférences**, **Plugin and Content Manager**.
> Videz le champ si vous préférez des noms de librairie plus courts.

## Mettre à jour

Rouvrez le gestionnaire de contenu : les paquets qui ont une nouvelle version
s'affichent avec un bouton **Update**. Rien d'autre à faire, les tables de
librairies suivent automatiquement.

## Ce qui reste à activer à la main

Trois éléments ne sont pas inscrits automatiquement par KiCad, parce que le
gestionnaire de contenu ne gère pas encore ces catégories. Chacun se met en place
en une fois.

### Les blocs de conception

Menu **Préférences**, **Gérer les librairies de blocs de conception**, puis
ajoutez une ligne :

| Champ | Valeur |
|---|---|
| Nom | `Barbatronic` |
| Chemin | `${KICAD10_3RD_PARTY}/resources/com_github_barbatronic_kicad-toolkit/design-blocks/Barbatronic.kicad_blocks` |
| Format | KiCad |



### Le cartouche

Dans un projet, menu **Fichier**, **Configuration de la mise en page**, champ
**Fichier de mise en page** :

```
${KICAD10_3RD_PARTY}/resources/com_github_barbatronic_kicad-toolkit/worksheets/Barbatronic.kicad_wks
```

À faire une fois pour le schéma et une fois pour le circuit imprimé. Les projets
créés depuis le modèle de projet embarquent déjà leur propre copie du cartouche.

### Les règles de conception

Copiez le fichier qui correspond à votre fabricant depuis

```
${KICAD10_3RD_PARTY}/resources/com_github_barbatronic_kicad-toolkit/design-rules/
```

vers votre projet, sous le nom `<nom du projet>.kicad_dru`. Voir la page
[Règles de conception](regles-de-conception).

## Installer sans passer par le dépôt

Le gestionnaire de contenu accepte aussi une archive locale, par **Install from File**.
Les archives de chaque version sont jointes aux
[releases du dépôt](https://github.com/Barbatronic/kicad-toolkit/releases).

## Désinstaller

Dans le gestionnaire de contenu, bouton **Uninstall** sur le paquet concerné.
KiCad retire les fichiers et nettoie les entrées correspondantes dans les tables
de librairies.
