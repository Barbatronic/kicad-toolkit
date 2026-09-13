#!/usr/bin/env python3
"""Rassemble les librairies tierces utilisees dans mes projets.

Les fichiers sont repris tels quels, y compris les retouches que j'ai faites au
fil des cartes. Seuls les noms de librairie recoivent un prefixe ThirdParty_,
pour eviter les collisions dans la table des librairies de KiCad.
"""
import os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kicad_sch as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "packages/barbatronic-kicad-thirdparty")
GH = os.environ.get("PROJETS", os.path.expanduser("~/Documents/GitHub"))
SCRATCH = os.environ.get("TP_SOURCES", "")

K25H = f"{GH}/Karibous-2025-Hardware/ECAD"
K25P = f"{GH}/Karibous-2025-PAMI/ECAD"
K26N = f"{GH}/Karibous-2026-PAMI-Ninja/ECAD/NinjaPAMI-2026/Libraries"
K26D = f"{GH}/Karibous-2026-Differential-Robot/ECAD/MainBoardDifferential2026/lib"

# --- Librairies de symboles : nom cible -> [fichiers sources]
SYMBOL_LIBS = {
    "ThirdParty_Seeed_XIAO": [
        f"{GH}/RC-Robot/ECAD/iBus-interpreter/lib/XIAO_Series_SCH_Symbols/Seeed_Studio_XIAO_Series.kicad_sym",
        f"{K26N}/Seeed Studio XIAO ESP32S3 Plus KiCAD Library 2/MOUDLE-SEEEDUINO-XIAO-ESP32S3-Plus.kicad_sym",
        f"{K25P}/MiniAmpli-2025/Seeeduino xiao ESP32C3 KiCAD Library/MOUDLE-SEEEDUINO-XIAO-ESP32C3.kicad_sym",
    ],
    "ThirdParty_TMC_StepStick": [
        f"{K25H}/DriverBoard-2025/Libraries/TMC2209_SILENTSTEPSTICK/TMC2209_SILENTSTEPSTICK.kicad_sym",
        f"{SCRATCH}/tmc/TMC2208_SILENTSTEPSTICK.kicad_sym",
    ],
    "ThirdParty_SparkFun": [
        f"{K25H}/MainBoard-2025/Librairies/teensy_4_0/DEV-15583.kicad_sym",
        f"{K26D}/symbol-project/BOB-12009.kicad_sym",
    ],
    "ThirdParty_DFRobot": [
        f"{K25P}/MiniAmpli-2025/DFR0299/DFR0299.kicad_sym",
    ],
}

# --- Librairies d'empreintes : nom cible -> [dossier .pretty ou fichier]
FOOTPRINT_LIBS = {
    "ThirdParty_SparkFun_RF": [f"{K25H}/MainBoard-2025/Librairies/RF.pretty"],
    "ThirdParty_Teensy": [f"{K25H}/MainBoard-2025/Librairies/teensy.pretty"],
    "ThirdParty_Digikey": [f"{K25H}/MainBoard-2025/Librairies/digikey/digikey-footprints.pretty"],
    "ThirdParty_Seeed_XIAO": [
        f"{K25P}/MiniAmpli-2025/Seeeduino xiao ESP32C3 KiCAD Library/xiao ESP32C3_PCB.pretty",
        f"{K26N}/Seeed Studio XIAO ESP32S3 Plus KiCAD Library 2/xiao ESP32S3 Plus_PCB.pretty",
        f"{SCRATCH}/xiaos3",
    ],
    "ThirdParty_TMC_StepStick": [
        f"{K25H}/DriverBoard-2025/Libraries/TMC2209_SILENTSTEPSTICK/MODULE_TMC2209_SILENTSTEPSTICK.kicad_mod",
        f"{SCRATCH}/tmc/MODULE_TMC2208_SILENTSTEPSTICK.kicad_mod",
    ],
    "ThirdParty_SparkFun": [
        f"{K25H}/MainBoard-2025/Librairies/teensy_4_0/MODULE_DEV-15583.kicad_mod",
        f"{K26D}/footprint-project.pretty/CONV_BOB-12009.kicad_mod",
    ],
    "ThirdParty_DFRobot": [f"{K25P}/MiniAmpli-2025/DFR0299/MODULE_DFR0299.kicad_mod"],
    "ThirdParty_Arduino": [f"{GH}/puzzle-bot/Project/Electronics/CNC-Shield-MKS/Arduino_MountingHole.pretty"],
}

# --- Modeles 3D fournis avec ces librairies : (source, librairie 3dshapes)
MODELS3D = [
    (f"{K25H}/MainBoard-2025/Librairies/teensy.pretty", "ThirdParty_Teensy"),
    (f"{K25P}/MiniAmpli-2025/DFR0299/DFR0299.step", "ThirdParty_DFRobot"),
    (f"{K25H}/MainBoard-2025/Librairies/teensy_4_0/DEV-15583.step", "ThirdParty_SparkFun"),
    (f"{K25H}/DriverBoard-2025/Libraries/TMC2209_SILENTSTEPSTICK/TMC2209_SILENTSTEPSTICK.step",
     "ThirdParty_TMC_StepStick"),
    (f"{K25H}/DriverBoard-2025/Libraries/TMC2208_3d.step", "ThirdParty_TMC_StepStick"),
]

IGNORE = {".DS_Store", "desktop.ini", "Thumbs.db", ".gitignore", "how-to-import.htm"}
MODEL_EXT = (".step", ".stp", ".wrl", ".STEP", ".STP", ".WRL")


def gather_symbols():
    for lib, sources in SYMBOL_LIBS.items():
        blocks, seen = [], set()
        for src in sources:
            if not os.path.exists(src):
                print(f"  ABSENT {src}")
                continue
            text = open(src, encoding="utf-8", errors="replace").read()
            for name, block in split(text):
                if name in seen:
                    continue
                seen.add(name)
                blocks.append(K.to_kicad9(block) if hasattr(K, "to_kicad9") else block)
        if not blocks:
            continue
        out = os.path.join(DST, "symbols", lib + ".kicad_sym")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(build(blocks))
        print(f"  symbols/{lib}.kicad_sym : {len(blocks)} symboles")


def split(text):
    out = []
    for d, s, e in K._scan(text):
        if d != 1:
            continue
        m = re.match(r'\(\s*symbol\s+"((?:[^"\\]|\\.)*)"', text[s:e])
        if m:
            out.append((m.group(1), text[s:e]))
    return out


def build(blocks):
    body = "\n".join(b.rstrip() for b in blocks)
    return ('(kicad_symbol_lib\n\t(version 20241209)\n\t(generator "kicad_symbol_editor")\n'
            '\t(generator_version "9.0")\n%s\n)\n' % body)


def gather_footprints():
    for lib, sources in FOOTPRINT_LIBS.items():
        dest = os.path.join(DST, "footprints", lib + ".pretty")
        os.makedirs(dest, exist_ok=True)
        n = 0
        for src in sources:
            if not os.path.exists(src):
                print(f"  ABSENT {src}")
                continue
            if os.path.isdir(src):
                for fn in sorted(os.listdir(src)):
                    if fn in IGNORE or not fn.endswith(".kicad_mod"):
                        continue
                    shutil.copy2(os.path.join(src, fn), os.path.join(dest, fn))
                    n += 1
            elif src.endswith(".kicad_mod"):
                shutil.copy2(src, os.path.join(dest, os.path.basename(src)))
                n += 1
        print(f"  footprints/{lib}.pretty : {n} empreintes")


def gather_models():
    for src, lib in MODELS3D:
        dest = os.path.join(DST, "3dmodels", lib + ".3dshapes")
        os.makedirs(dest, exist_ok=True)
        if os.path.isdir(src):
            for fn in sorted(os.listdir(src)):
                if fn.endswith(MODEL_EXT):
                    shutil.copy2(os.path.join(src, fn), os.path.join(dest, fn))
                    print(f"  3dmodels/{lib}.3dshapes/{fn}")
        elif os.path.exists(src):
            shutil.copy2(src, os.path.join(dest, os.path.basename(src)))
            print(f"  3dmodels/{lib}.3dshapes/{os.path.basename(src)}")
        else:
            print(f"  ABSENT {src}")


def gather_legacy_symbols():
    """Symboles Digi-Key au format KiCad 5, conserves pour import manuel."""
    src = f"{K25H}/MainBoard-2025/Librairies/digikey/digikey-symbols"
    if not os.path.isdir(src):
        return
    dest = os.path.join(DST, "resources", "symboles-format-ancien", "digikey")
    os.makedirs(dest, exist_ok=True)
    n = 0
    for fn in sorted(os.listdir(src)):
        if fn in IGNORE or not fn.endswith((".lib", ".dcm")):
            continue
        shutil.copy2(os.path.join(src, fn), os.path.join(dest, fn))
        n += 1
    print(f"  resources/symboles-format-ancien/digikey : {n} fichiers")


def main():
    print("librairies tierces :")
    gather_symbols()
    gather_footprints()
    gather_models()
    gather_legacy_symbols()


if __name__ == "__main__":
    main()
