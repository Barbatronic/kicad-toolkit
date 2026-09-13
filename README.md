# Barbatronic KiCad Toolkit

Mes librairies, blocs de conception et réglages KiCad, rassemblés au même endroit
et installables depuis le gestionnaire de contenu de KiCad.

**[Documentation et catalogue](https://barbatronic.github.io/kicad-toolkit/)**

## Installation

Dans KiCad, ouvrez le **Plugin and Content Manager**, déroulez la liste des dépôts,
choisissez **Manage...** et ajoutez :

```
https://barbatronic.github.io/kicad-toolkit/repository.json
```

Les trois paquets apparaissent ensuite dans les onglets **Libraries** et
**Color Themes**. Les mises à jour se font depuis la même fenêtre.

Le détail, y compris les quelques éléments à activer à la main, est sur la
[page d'installation](https://barbatronic.github.io/kicad-toolkit/installation).

## Contenu

| Paquet | Contenu |
|---|---|
| **Barbatronic Toolkit** | Symboles, empreintes et modèles 3D par thème, blocs de conception, cartouche, règles de conception, modèle de projet |
| **Librairies tierces** | SparkFun, Teensy, Digi-Key, Seeed XIAO, TMC SilentStepStick, DFRobot, sous leur licence d'origine |
| **Thème sombre** | Thème de couleurs pour le schéma et le routage |

Les librairies sont rangées par usage : `Barbatronic_MCU`, `Barbatronic_Power`,
`Barbatronic_Motion`, `Barbatronic_Sensors`, `Barbatronic_Connectors`,
`Barbatronic_Interface`, `Barbatronic_Mechanical`, `Barbatronic_Display`.

Compatible **KiCad 10.0 et plus récent**.

## Organisation du dépôt

```
packages/     un dossier par paquet, le contenu est celui qui sera installé
tools/        scripts de construction et de vérification
docs/         le site de documentation
```

## Construire en local

```bash
python3 tools/build_pcm.py --version 1.0.0   # archives et dépôt PCM dans dist/
python3 tools/make_gallery.py                # catalogue illustré, nécessite kicad-cli
python3 tools/check_privacy.py               # vérifie l'absence de données personnelles
```

## Publier une version

```bash
git tag v1.1.0 && git push origin v1.1.0
```

Le reste est automatique : construction des archives, validation contre le schéma
officiel de KiCad, release GitHub, publication du dépôt et du catalogue sur GitHub
Pages. Voir la page
[Maintenir le toolkit](https://barbatronic.github.io/kicad-toolkit/maintenance).

## Licence

Mes symboles, empreintes, blocs et réglages sont sous licence MIT, voir
[LICENSE](LICENSE).

Les librairies tierces du paquet `barbatronic-kicad-thirdparty` gardent leur
licence d'origine, reproduite dans le paquet, et portent pour certaines mes
retouches. Le détail de chaque provenance est sur la page
[Librairies tierces](https://barbatronic.github.io/kicad-toolkit/librairies/tierces).
