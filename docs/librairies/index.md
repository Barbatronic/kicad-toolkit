---
title: Librairies
nav_order: 3
has_children: true
---

# Librairies

Les symboles et empreintes sont rangés par usage plutôt que par projet d'origine.
Sept librairies, chacune sur un thème, pour retrouver un composant sans se souvenir
de la carte sur laquelle il a servi la première fois.

| Librairie | Ce qu'on y trouve |
|---|---|
| `Barbatronic_MCU` | Cartes et modules à microcontrôleur |
| `Barbatronic_Power` | Alimentation, conversion, commutation de puissance |
| `Barbatronic_Motion` | Motorisation et commande de moteurs |
| `Barbatronic_Sensors` | Capteurs |
| `Barbatronic_Connectors` | Connectique, alimentation et stockage |
| `Barbatronic_Interface` | Boutons, interrupteurs, voyants |
| `Barbatronic_Mechanical` | Mécanique et repères de fabrication |
| `Barbatronic_Display` | Écrans |

Dans KiCad, ces librairies apparaissent préfixées : `PCM_Barbatronic_MCU`, et ainsi
de suite.

## Ce qui n'est volontairement pas dedans

Le toolkit ne reprend pas les symboles et empreintes qui existent déjà dans les
librairies officielles de KiCad. Plusieurs de mes anciens projets embarquaient des
copies locales de `R`, `C`, `LED`, `Conn_01x..` ou du convertisseur `R-78E5.0` :
ces copies n'ont pas été reprises, les originales de KiCad font le même travail et
restent à jour.

Ne sont retenus que les composants réellement absents des librairies officielles,
ou dont j'ai eu besoin dans une variante particulière, comme les modules montés
par en dessous.

## Provenance

Ces fichiers viennent de mes cartes des dernières années. Ils ont été renommés de
façon cohérente au passage : plus d'espaces ni de majuscules fantaisistes dans les
noms d'empreinte, ce qui évite bien des ennuis dans les tables de librairies.

| Nom dans le toolkit | Nom d'origine |
|---|---|
| `StepStick_Driver_BottomEntry` | `Step-Stick Driver Bottom Entry Version` |
| `VL53L0X_BottomEntry` | `VL53 Bottom Entry Version` |
| `Battery_Canon_LP-E6` | `LP-e6 Batterie` |
| `SW_Push_UB16SKW03N-C` | `UB16SKW03N-C` |
| `SW_Slide_SK-12D10_1P2T` | `SK-12D10 1P2T` |
| `USB_A_3.0_Vertical` | `USB A3.0 Vertical` |
| `USB_A_3.0_PowerBank_XHC-005` | `USB A3.0 - PowerBank XHC-005` |
| `ESP32-S3-UNO` | `ESP_S3_UNO` |
| `TracoPower_TEN_50-2411` | `CONV_TEN_50-2411` |
| `Module_LR7843` | `LR7843-Board` |
| `Module_GA5A13` | `GA5A13-Board` |
| `Pololu_D36V50F5` | `D36V50F5` |
| `LED_SK6812-E_4960` | `SK6812-E-4960_ADA` |
| `Badge_Holonome` | `BadgeHolonome` |
| `Aisler_Logo_15x12mm` | `aisler_15x12mm` |
| `SD_Hirose_DM1AA-SF-PEJ82` | `SD_Hirose_DM1AA_SF_PEJ82` |
