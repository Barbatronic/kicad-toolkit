# Librairies tierces redistribuées

Ce paquet regroupe les librairies KiCad que je n'ai pas créées mais qui reviennent
dans mes cartes. Elles sont redistribuées sous leur licence d'origine, avec pour
certaines les retouches que j'y ai apportées au fil des projets.

Seul le nom de la librairie a reçu un préfixe `ThirdParty_`, pour éviter les
collisions dans la table des librairies de KiCad.

| Librairie | Auteur d'origine | Licence | Source |
|---|---|---|---|
| `ThirdParty_SparkFun_RF` | SparkFun Electronics | CC BY 4.0 | [SparkFun-KiCad-Libraries](https://github.com/sparkfun/SparkFun-KiCad-Libraries) |
| `ThirdParty_SparkFun` | SparkFun Electronics, via SnapEDA | voir ci-dessous | [snapeda.com](https://www.snapeda.com/) |
| `ThirdParty_Teensy` | Ricardo Band | MIT | [XenGi/teensy.pretty](https://github.com/XenGi/teensy.pretty) |
| `ThirdParty_Digikey` | Digi-Key Electronics | CC BY-SA 4.0 | [Digi-Key/digikey-kicad-library](https://github.com/Digi-Key/digikey-kicad-library) |
| `ThirdParty_Seeed_XIAO` | Seeed Studio | non précisée | [Seeed-Studio/OPL_Kicad_Library](https://github.com/Seeed-Studio/OPL_Kicad_Library) |
| `ThirdParty_TMC_StepStick` | via SnapEDA | voir ci-dessous | [snapeda.com](https://www.snapeda.com/) |
| `ThirdParty_DFRobot` | DFRobot, via SnapEDA | voir ci-dessous | [snapeda.com](https://www.snapeda.com/) |
| `ThirdParty_Arduino` | Projet KiCad | CC BY-SA 4.0 avec exception | modèle de projet Arduino livré avec KiCad |
| `ThirdParty_RS` | RS Components | non précisée | export CAO du site RS Components (référence RS PRO 185-4727) |

## Modifications apportées

Les empreintes des modules montés par en dessous, les variantes d'implantation et
les ajustements de pastilles sont de moi. Les fichiers ne sont donc pas toujours
identiques à ceux publiés par leur auteur d'origine.

Les références de modèles 3D pointant vers des chemins qui n'existaient que sur
ma machine ont été réécrites ou retirées. Les champs de description contenant le
chemin de téléchargement local d'un tiers ont été supprimés.

## Licences

### CC BY 4.0, SparkFun

Usage commercial explicitement autorisé, attribution demandée. Texte complet dans
`SparkFun-CC-BY-4.0.txt`.

### MIT, Teensy

Texte complet dans `Teensy-MIT.txt`.

### CC BY-SA 4.0, Digi-Key

Digi-Key autorise l'usage libre de sa librairie dans des projets commerciaux ou
fermés, sans obligation de partager les fichiers de conception. En revanche, la
redistribution de la librairie elle-même, y compris modifiée, doit se faire sous
la même licence et conserver l'attribution. C'est le cas ici. Texte complet dans
`Digikey-CC-BY-SA-4.0.md`.

### Modèles issus de SnapEDA

Les symboles et empreintes `TMC2208_SILENTSTEPSTICK`, `TMC2209_SILENTSTEPSTICK`,
`DEV-15583`, `BOB-12009` et `DFR0299` ont été obtenus via SnapEDA. Les conditions
d'utilisation de SnapEDA encadrent la redistribution de ces modèles. Ils sont
inclus ici parce que je les ai retouchés pour mes cartes et que je souhaite que
mes projets restent reproductibles.

Si vous êtes ayant droit et que cette redistribution pose problème, ouvrez une
issue sur [le dépôt](https://github.com/Barbatronic/kicad-toolkit/issues) et je
retirerai les fichiers concernés.

### Seeed Studio

Le dépôt OPL de Seeed Studio ne porte pas de fichier de licence. Les fichiers sont
diffusés publiquement par Seeed pour encourager l'usage de leurs cartes. Même
remarque que ci-dessus en cas de désaccord de leur part.
