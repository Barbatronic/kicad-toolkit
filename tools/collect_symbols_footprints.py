#!/usr/bin/env python3
"""Assemble les librairies maison du toolkit depuis les projets d'origine.

Regenere symbols/Barbatronic_*.kicad_sym, footprints/Barbatronic_*.pretty et
3dmodels/Barbatronic.3dshapes a partir des fichiers sources releves dans les
anciens projets. Necessite un clone local de ces depots, indique par PROJETS
(par defaut ~/Documents/GitHub).
"""
import os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kicad_sch as K

GH = os.environ.get("PROJETS", os.path.expanduser("~/Documents/GitHub"))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "sources")  # fichiers recuperes manuellement, voir README
DST = os.path.join(ROOT, "packages/barbatronic-kicad-toolkit")

K25H = f"{GH}/Karibous-2025-Hardware/ECAD"
K25P = f"{GH}/Karibous-2025-PAMI/ECAD"
K26D = f"{GH}/Karibous-2026-Differential-Robot/ECAD/MainBoardDifferential2026/lib"
K26N = f"{GH}/Karibous-2026-PAMI-Ninja/ECAD/PumpBoard-2026"
OMNI = f"{GH}/Omni-RC-Robot/ecad/lib"

# --- Symboles : (theme, fichier source, nom d'origine, nouveau nom, empreinte, description, mots-cles)
SYMBOLS = [
 ("MCU", f"{OMNI}/omni-symbols.kicad_sym", "ESP32-C3-Zero", "ESP32-C3-Zero",
  "Barbatronic_MCU:ESP32-C3-Zero_Castellated",
  "Waveshare ESP32-C3-Zero, module WiFi/BLE RISC-V au format Zero",
  "ESP32 C3 RISC-V WiFi BLE Waveshare Zero module"),
 ("MCU", f"{OMNI}/omni-symbols.kicad_sym", "ESP32-S3-Zero", "ESP32-S3-Zero",
  "Barbatronic_MCU:ESP32-S3-Zero_Castellated",
  "Waveshare ESP32-S3-Zero, module WiFi/BLE double coeur au format Zero",
  "ESP32 S3 WiFi BLE Waveshare Zero module USB"),
 ("MCU", f"{K26D}/symbol-project/makerspace-unilasalle.kicad_sym", "ESP32-S3-UNO", "ESP32-S3-UNO",
  "Barbatronic_MCU:ESP32-S3-UNO",
  "Carte ESP32-S3 au format Arduino UNO",
  "ESP32 S3 UNO Arduino shield WiFi BLE"),
 ("Power", f"{K25H}/MainBoard-2025/Librairies/TEN 50-2411/TEN_50-2411.kicad_sym", "TEN_50-2411", "TEN_50-2411",
  "Barbatronic_Power:TracoPower_TEN_50-2411",
  "TracoPower TEN 50-2411, convertisseur DC/DC 50 W isole 24 V vers 5,1 V",
  "DC-DC convertisseur isole TracoPower TEN50 alimentation"),
 ("Power", f"{SRC}/lib2023/LR7843-Board.kicad_sym", "LR7843-Board", "Module_LR7843",
  "Barbatronic_Power:Module_LR7843",
  "Module MOSFET de puissance LR7843, commande PWM haut courant",
  "MOSFET module puissance PWM commutation LR7843"),
 ("Power", f"{SRC}/lib2023/GA5A13-BOARD.kicad_sym", "GA5A13-Board", "Module_GA5A13",
  "Barbatronic_Power:Module_GA5A13",
  "Module MOSFET de puissance GA5A13, entree PWM isolee",
  "MOSFET module puissance PWM commutation GA5A13"),
 ("Power", f"{GH}/Karibous-2026-Differential-Robot/ECAD/MainBoardDifferential2026/MainBoardDifferential2026.kicad_sch", "D36V50F5:D36V50F5", "Pololu_D36V50F5",
  "Barbatronic_Power:Pololu_D36V50F5",
  "Pololu D36V50Fx, regulateur a decoupage step-down 5 A, entree jusqu'a 36 V",
  "Pololu regulateur step-down buck D36V50F alimentation", "embedded"),
 ("Interface", f"{SRC}/keytar/SK6812-E-4960_ADA.kicad_sym", "SK6812", "LED_SK6812-E",
  "Barbatronic_Interface:LED_SK6812-E_4960",
  "LED RGB adressable SK6812-E, boitier 4960 a ailettes",
  "LED RGB adressable NeoPixel SK6812 WS2812 serie"),
 ("Interface", f"{K25P}/Mini-PAMI-2025/Mini-PAMI-2025.kicad_sch",
  "Interface_Expansion:MCP23008-xSO", "MCP23008-xSO", "",
  "Microchip MCP23008, extenseur d'E/S 8 bits sur bus I2C",
  "GPIO expander I2C IO extenseur Microchip MCP23008", "embedded"),
 ("Interface", f"{GH}/pocket-controller/ecad/pocket-controller-pcb/pocket-controller-pcb.kicad_sch",
  "Interface_Expansion:PCF8574AT", "PCF8574AT", "",
  "NXP PCF8574, extenseur d'E/S 8 bits sur bus I2C",
  "GPIO expander I2C IO extenseur NXP PCF8574", "embedded"),
]

# --- Empreintes : (theme, chemin source, nouveau nom)
FOOTPRINTS = [
 ("MCU", f"{OMNI}/omni-footprints.pretty/ESP32-C3-Zero_Castellated.kicad_mod", "ESP32-C3-Zero_Castellated"),
 ("MCU", f"{OMNI}/omni-footprints.pretty/ESP32-C3-Zero_THT.kicad_mod", "ESP32-C3-Zero_THT"),
 ("MCU", f"{OMNI}/omni-footprints.pretty/ESP32-S3-Zero_Castellated.kicad_mod", "ESP32-S3-Zero_Castellated"),
 ("MCU", f"{OMNI}/omni-footprints.pretty/ESP32-S3-Zero_THT.kicad_mod", "ESP32-S3-Zero_THT"),
 ("MCU", f"{K26D}/footprint-project.pretty/ESP_S3_UNO.kicad_mod", "ESP32-S3-UNO"),
 ("Power", f"{K25H}/MainBoard-2025/Librairies/TEN 50-2411/CONV_TEN_50-2411.kicad_mod", "TracoPower_TEN_50-2411"),
 ("Power", f"{SRC}/lib2023/LR7843-Board.kicad_mod", "Module_LR7843"),
 ("Power", f"{SRC}/lib2023/GA5A13-Board.kicad_mod", "Module_GA5A13"),
 ("Power", f"{K26D}/footprint-project.pretty/D36V50F5.kicad_mod", "Pololu_D36V50F5"),
 ("Motion", f"{K25P}/MainBoard-PAMI-2025/Libraries/PAMI-2025.pretty/Step-Stick Driver Bottom Entry Version.kicad_mod", "StepStick_Driver_BottomEntry"),
 ("Sensors", f"{K25P}/MainBoard-PAMI-2025/Libraries/PAMI-2025.pretty/VL53 Bottom Entry Version.kicad_mod", "VL53L0X_BottomEntry"),
 ("Connectors", f"{SRC}/pami2024/USB_A3.0_Vertical.kicad_mod", "USB_A_3.0_Vertical"),
 ("Connectors", f"{SRC}/pami2024/USB_A3.0_PowerBank_XHC-005.kicad_mod", "USB_A_3.0_PowerBank_XHC-005"),
 ("Connectors", f"{K25P}/MainBoard-PAMI-2025/Libraries/PAMI-2025.pretty/LP-e6 Batterie.kicad_mod", "Battery_Canon_LP-E6"),
 ("Connectors", f"{K26D}/footprint-project.pretty/SD_Hirose_DM1AA_SF_PEJ82.kicad_mod", "SD_Hirose_DM1AA-SF-PEJ82"),
 ("Interface", f"{K25P}/MainBoard-PAMI-2025/Libraries/PAMI-2025.pretty/UB16SKW03N-C.kicad_mod", "SW_Push_UB16SKW03N-C"),
 ("Interface", f"{K25H}/Ihm-2025/footprints/SK-12D10 1P2T.kicad_mod", "SW_Slide_SK-12D10_1P2T"),
 ("Interface", f"{K26D}/footprint-project.pretty/SW_Push_KMR2.kicad_mod", "SW_Push_KMR2"),
 ("Interface", f"{SRC}/keytar/SK6812-E-4960_ADA.kicad_mod", "LED_SK6812-E_4960"),
 ("Mechanical", f"{SRC}/lib2023/BadgeHolonome.kicad_mod", "Badge_Holonome"),
 ("Mechanical", f"{K25H}/MainBoard-2025/Librairies/aisler.pretty/aisler_15x12mm.kicad_mod", "Aisler_Logo_15x12mm"),
]

# --- Modeles 3D directs (deja au format .step, simple copie) : (source, nom)
MODELS3D = [
 (f"{K25H}/Ihm-2025/packages3D/SK-12D10 1P2T.step", "SW_Slide_SK-12D10_1P2T.step"),
 (f"{K25H}/DriverBoard-2025/Libraries/TMC2208_3d.step", "StepStick_Driver_BottomEntry.step"),
]

# --- Empreintes extraites d'un placement sur PCB (jamais exportees en .pretty
# a la source) : (theme, fichier .kicad_pcb, "Lib:Nom" place, nouveau nom,
# fichier modele 3D source, extension du modele copie)
EMBEDDED_FOOTPRINTS = [
 ("Connectors", f"{K25H}/PumpBoard-2025/PumpBoard-2025.kicad_pcb", "BarbaLib:MiniEV", "Connector_MiniEV",
  f"{K25H}/PumpBoard-2025/models/miniEV.step", "Connector_MiniEV.step"),
 ("Motion", f"{K26N}/PumpBoard-2026.kicad_pcb", "BarbaLib:motor-pump-370", "Motor_Pump_370",
  f"{K26N}/packages3D/MICRO-POMPE 370 v2.step", "Motor_Pump_370.step"),
]


def fp_rename(text, new):
    """Renomme une empreinte et met a jour son champ Reference/valeur affichee."""
    text = re.sub(r'(\(\s*footprint\s+")(?:[^"\\]|\\.)*(")', r'\g<1>' + new + r'\g<2>', text, count=1)
    text = re.sub(r'(\(\s*property\s+"Value"\s+)"(?:[^"\\]|\\.)*"', r'\g<1>"' + new + '"', text, count=1)
    text = re.sub(r'(\(\s*fp_text\s+value\s+)"(?:[^"\\]|\\.)*"', r'\g<1>"' + new + '"', text, count=1)
    return text


def extract_embedded_footprint(pcb_path, full_name, new_name, model_target):
    """Convertit un footprint place sur un PCB en definition de librairie autonome."""
    text = open(pcb_path, encoding="utf-8").read()
    block = None
    for d, s, e in K._scan(text):
        if d == 1 and text[s:e].startswith(f'(footprint "{full_name}"'):
            block = text[s:e]
            break
    if block is None:
        raise SystemExit(f"empreinte introuvable sur le PCB : {full_name} ({pcb_path})")

    out = [f'(footprint "{new_name}"', '\t(version 20241229)', '\t(generator "pcbnew")',
           '\t(generator_version "9.0")', '\t(layer "B.Cu")']
    for it in [block[s:e] for d, s, e in K._scan(block) if d == 1]:
        head = re.match(r'\(\s*([a-z_]+)', it)
        kind = head.group(1) if head else ""
        if kind in ("locked", "layer", "uuid", "at", "path", "sheetname", "sheetfile"):
            continue
        if kind == "property":
            m = re.match(r'\(\s*property\s+"(Reference|ki_fp_filters)"', it)
            if m and m.group(1) == "Reference":
                it = re.sub(r'(\(\s*property\s+"Reference"\s+)"[^"]*"', r'\g<1>"REF**"', it, count=1)
            if m and m.group(1) == "ki_fp_filters":
                continue  # filtre herite d'un gabarit, non pertinent ici
        if kind == "pad":
            it = re.sub(r'\n\s*\(\s*net\s+\d+\s+"[^"]*"\)', '', it)
        if kind == "model":
            it = re.sub(r'(\(\s*model\s+)"[^"]*"', r'\g<1>"' + model_target + '"', it, count=1)
        it = re.sub(r'\n\s*\(uuid "[0-9a-f-]{36}"\)', '', it)
        base = re.match(r'^(\t*)', it).group(1)
        lines = it.split("\n")
        it = "\t" + "\n".join(ln[len(base):] if ln.startswith(base) else ln for ln in lines)
        out.append(it)
    out.append(")")
    return "\n".join(out) + "\n"


def main():
    by_theme = {}
    for entry in SYMBOLS:
        theme, src, old, new, footprint, desc, kw = entry[:7]
        embedded = len(entry) > 7 and entry[7] == "embedded"
        if embedded:
            text = open(src, encoding="utf-8").read()
            lib_symbols = next((text[s:e] for d, s, e in K._scan(text)
                               if text[s:e].startswith('(lib_symbols')), None)
            blocks = dict(K.split_symbols(lib_symbols)) if lib_symbols else {}
        else:
            blocks = dict(K.split_symbols(open(src, encoding="utf-8").read()))
        if old not in blocks:
            print(f"  MANQUE symbole {old} dans {src}")
            continue
        b = K.to_kicad9(blocks[old])
        b = K.rename(b, old, new)
        b = K.set_property(b, "Value", new)
        b = K.set_property(b, "Description", desc)
        b = K.set_property(b, "ki_keywords", kw)
        b = K.set_property(b, "Footprint", ("PCM_" + footprint) if footprint else "")
        by_theme.setdefault(theme, []).append((new, b))
    for theme, items in sorted(by_theme.items()):
        items.sort()
        path = f"{DST}/symbols/Barbatronic_{theme}.kicad_sym"
        open(path, "w", encoding="utf-8").write(K.build_symbol_lib([b for _, b in items]))
        print(f"symbols/Barbatronic_{theme}.kicad_sym : {', '.join(n for n, _ in items)}")

    counts = {}
    for theme, src, new in FOOTPRINTS:
        if not os.path.exists(src):
            print(f"  MANQUE empreinte {src}")
            continue
        out = f"{DST}/footprints/Barbatronic_{theme}.pretty/{new}.kicad_mod"
        open(out, "w", encoding="utf-8").write(fp_rename(open(src, encoding="utf-8").read(), new))
        counts[theme] = counts.get(theme, 0) + 1

    for theme, pcb, full_name, new_name, model_src, model_name in EMBEDDED_FOOTPRINTS:
        d3 = f"{DST}/3dmodels/Barbatronic.3dshapes"
        os.makedirs(d3, exist_ok=True)
        if os.path.exists(model_src):
            shutil.copy2(model_src, f"{d3}/{model_name}")
        model_ref = ("${KICAD10_3RD_PARTY}/3dmodels/com_github_barbatronic_kicad-toolkit"
                    f"/Barbatronic.3dshapes/{model_name}")
        content = extract_embedded_footprint(pcb, full_name, new_name, model_ref)
        out = f"{DST}/footprints/Barbatronic_{theme}.pretty/{new_name}.kicad_mod"
        open(out, "w", encoding="utf-8").write(content)
        counts[theme] = counts.get(theme, 0) + 1

    for theme, n in sorted(counts.items()):
        print(f"footprints/Barbatronic_{theme}.pretty : {n} empreintes")

    d3 = f"{DST}/3dmodels/Barbatronic.3dshapes"
    os.makedirs(d3, exist_ok=True)
    for src, new in MODELS3D:
        if os.path.exists(src):
            shutil.copy2(src, f"{d3}/{new}")
            print(f"3dmodels/Barbatronic.3dshapes/{new}")
        else:
            print(f"  MANQUE modele {src}")


if __name__ == "__main__":
    main()
