---
title: Maintenir le toolkit
nav_order: 8
---

# Maintenir le toolkit
{: .no_toc }

Comment ajouter un composant et publier une nouvelle version. Cette page s'adresse
à moi dans six mois, quand j'aurai oublié comment tout cela s'articule.

1. TOC
{:toc}

---

## Réglages GitHub à faire une fois

Ces deux réglages conditionnent la publication automatique. Ils ne sont à faire
qu'au premier démarrage du dépôt.

1. **Activer GitHub Pages** : onglet **Settings**, section **Pages**, champ
   **Source**, choisir **GitHub Actions**. Sans cela, le workflow de publication
   échoue à la dernière étape.
2. **Autoriser les workflows à écrire** : **Settings**, **Actions**, **General**,
   section **Workflow permissions**, choisir **Read and write permissions**. C'est
   ce qui permet au workflow de créer la release et d'y joindre les archives.

L'adresse du dépôt PCM devient alors
`https://barbatronic.github.io/kicad-toolkit/repository.json`, et elle ne change plus.

## Organisation du dépôt

```
packages/                          un dossier par paquet PCM
  barbatronic-kicad-toolkit/       le paquet principal
    metadata.json                  fiche du paquet
    symbols/                       librairies de symboles
    footprints/                    librairies d'empreintes
    3dmodels/                      modèles 3D
    templates/                     modèles de projet
    resources/                     icône, blocs, cartouche, règles
  barbatronic-kicad-thirdparty/    librairies tierces redistribuées
  barbatronic-kicad-theme/         thème de couleurs
tools/                             scripts de construction
docs/                              ce site
dist/                              sortie de construction, non versionnée
```

Ce qui est dans `packages/` est exactement ce qui sera installé sur le disque.
KiCad n'extrait que les dossiers `symbols`, `footprints`, `3dmodels`, `resources`,
`colors`, `templates`, `scripts` et `plugins` : un fichier posé ailleurs est ignoré
sans avertissement.

## Ajouter un symbole ou une empreinte

1. Placez le fichier dans la librairie du thème qui convient, par exemple
   `packages/barbatronic-kicad-toolkit/footprints/Barbatronic_Power.pretty/`.
2. Nommez-le sans espace ni caractère accentué.
3. Vérifiez qu'il se charge :

   ```bash
   kicad-cli fp export svg -o /tmp/verif packages/barbatronic-kicad-toolkit/footprints/Barbatronic_Power.pretty
   ```

4. Publiez une nouvelle version, voir plus bas.

Un symbole ou une empreinte qui existe déjà dans les librairies officielles de
KiCad n'a pas sa place ici.

Pour une librairie tierce, la place est dans `packages/barbatronic-kicad-thirdparty/`,
avec une ligne dans `resources/licenses/NOTICE.md` indiquant l'auteur d'origine, la
licence et ce que j'ai modifié.

## Ajouter un bloc de conception

Les blocs sont produits par un script, pour rester cohérents et reproductibles.
Ajoutez une fonction dans `tools/make_design_blocks.py`, inscrivez-la dans la liste
`BLOCS`, puis :

```bash
python3 tools/make_design_blocks.py
```

Le script récupère au besoin les librairies de symboles officielles de KiCad dans
`~/.cache/barbatronic-kicad-toolkit/`, il fonctionne donc même sans KiCad installé.

Les blocs peuvent aussi être créés à la main depuis l'éditeur de schéma, par
**Créer un bloc de conception à partir de la sélection**. Dans ce cas, le script
n'est plus la source de vérité pour ce bloc.

## Publier une version

La publication est automatique : elle part d'un tag Git.

```bash
git tag v1.1.0
git push origin v1.1.0
```

Le workflow `release.yml` construit les archives, valide le dépôt contre le schéma
officiel de KiCad, crée la release GitHub avec les archives jointes, puis publie
`repository.json`, `packages.json` et `resources.zip` sur GitHub Pages avec le
catalogue à jour.

Les versions précédentes sont conservées dans `packages.json` : le gestionnaire de
contenu peut proposer une version antérieure si besoin.

## Construire en local

```bash
python3 tools/build_pcm.py --version 1.1.0   # archives et dépôt dans dist/
python3 tools/valider_pcm.py                 # validation contre le schéma officiel
python3 tools/make_gallery.py                # catalogue illustré, nécessite kicad-cli
python3 tools/make_design_blocks.py          # régénère les blocs de conception
python3 tools/check_privacy.py               # recherche de données personnelles
```

Deux scripts ne servent qu'à la reprise de fichiers venus d'ailleurs :

```bash
PROJETS=~/Documents/GitHub python3 tools/collect_thirdparty.py  # réimporte les librairies tierces
python3 tools/fix_3d_paths.py                                   # normalise les références de modèles 3D
```

`fix_3d_paths.py` est à relancer après toute reprise d'empreinte venant d'un
projet : il redirige les modèles 3D fournis par le paquet, laisse ceux des
librairies officielles de KiCad et retire les chemins morts. Sans lui, une
empreinte peut publier l'arborescence de la machine sur laquelle elle a été faite,
ce qui est déjà arrivé.

## Prévisualiser la documentation en local

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Le site est alors sur `http://localhost:4000/kicad-toolkit/`. Le catalogue illustré
n'apparaît qu'après un passage de `tools/make_gallery.py`.

## Numérotation

Le format est `majeur.mineur.correctif`.

- **correctif** : une empreinte corrigée, une faute dans la documentation.
- **mineur** : de nouveaux composants, un nouveau bloc.
- **majeur** : un renommage ou une suppression, autrement dit quelque chose qui
  casse les projets existants.

Un renommage d'empreinte oblige à corriger les projets qui l'utilisent. À éviter
sauf bonne raison, et à signaler dans les notes de version.
