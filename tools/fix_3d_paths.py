#!/usr/bin/env python3
"""Normalise les references de modeles 3D des empreintes du toolkit.

Les empreintes viennent de projets ou les modeles etaient ranges n'importe ou :
chemins absolus d'une machine, ${KIPRJMOD} pointant vers le projet d'origine,
variables d'environnement qui n'existent que chez moi. Rien de tout cela ne
fonctionne chez celui qui installe le paquet.

Regle appliquee : on garde les modeles officiels de KiCad et ceux fournis par le
paquet, on retire les autres references plutot que de laisser un chemin mort.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "packages/barbatronic-kicad-toolkit")
FP_DIR = os.path.join(PKG, "footprints")
SHAPES = "${KICAD9_3RD_PARTY}/3dmodels/com_github_barbatronic_kicad-toolkit/Barbatronic.3dshapes"

# Modeles fournis par le paquet : ancien fragment de chemin -> nouveau fichier.
PROVIDED = {
    "SK-12D10": "SW_Slide_SK-12D10_1P2T.step",
    "TMC2208_SILENTSTEPSTICK": "StepStick_Driver_BottomEntry.step",
}

KEEP_PREFIXES = ("${KICAD6_3DMODEL_DIR}", "${KICAD7_3DMODEL_DIR}",
                 "${KICAD8_3DMODEL_DIR}", "${KICAD9_3DMODEL_DIR}",
                 "${KICAD10_3DMODEL_DIR}", SHAPES)


def model_blocks(text):
    """Positions des listes (model ...) de premier niveau de l'empreinte."""
    out, depth, in_str, esc, stack = [], 0, False, False, []
    for j, c in enumerate(text):
        if esc:
            esc = False
            continue
        if c == "\\":
            esc = True
        elif c == '"':
            in_str = not in_str
        elif not in_str:
            if c == "(":
                stack.append((depth, j))
                depth += 1
            elif c == ")":
                depth -= 1
                d, s = stack.pop()
                if d == 1 and re.match(r'\(\s*model(?=[\s"])', text[s:j + 1]):
                    out.append((s, j + 1))
    return out


def main():
    changed, removed, retargeted = 0, 0, 0
    for dirpath, _, filenames in os.walk(FP_DIR):
        for fn in sorted(filenames):
            if not fn.endswith(".kicad_mod"):
                continue
            path = os.path.join(dirpath, fn)
            text = open(path, encoding="utf-8").read()
            original = text
            for s, e in reversed(model_blocks(text)):
                block = text[s:e]
                m = re.match(r'\(\s*model\s+"((?:[^"\\]|\\.)*)"', block)
                if not m:
                    continue
                ref = m.group(1)
                if ref.startswith(KEEP_PREFIXES):
                    continue
                target = next((f for frag, f in PROVIDED.items() if frag in ref), None)
                if target:
                    text = text[:s] + block.replace(f'"{ref}"', f'"{SHAPES}/{target}"', 1) + text[e:]
                    retargeted += 1
                else:
                    # retire la reference et l'indentation qui la precede
                    p = s
                    while p > 0 and text[p - 1] in " \t":
                        p -= 1
                    if p > 0 and text[p - 1] == "\n":
                        p -= 1
                    text = text[:p] + text[e:]
                    removed += 1
            if text != original:
                open(path, "w", encoding="utf-8").write(text)
                changed += 1
                print(f"  {os.path.relpath(path, ROOT)}")
    print(f"\n{changed} empreintes modifiees : {retargeted} modele(s) redirige(s) "
          f"vers le paquet, {removed} reference(s) morte(s) retiree(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
