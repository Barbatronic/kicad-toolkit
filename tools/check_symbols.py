#!/usr/bin/env python3
"""Verifie la validite structurelle des librairies de symboles sans KiCad.

Un fichier .kicad_sym qui echoue a un seul de ces controles est rejete en
bloc par KiCad au chargement, ce qui invalide toute la librairie meme si le
reste des symboles est correct. Complementaire au chargement reel par
kicad-cli (tools/verification.yml), utile quand KiCad n'est pas disponible.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import kicad_sch as K


def check_file(path):
    problems = []
    text = open(path, encoding="utf-8", errors="replace").read()

    depth = 0
    in_str = esc = False
    for c in text:
        if esc:
            esc = False
            continue
        if c == "\\":
            esc = True
        elif c == '"':
            in_str = not in_str
        elif not in_str:
            depth += (c == "(") - (c == ")")
    if depth != 0:
        problems.append(f"parenthesage desequilibre ({depth:+d})")
        return problems  # le reste des controles n'a plus de sens

    try:
        syms = K.split_symbols(text)
    except Exception as e:
        problems.append(f"echec du decoupage en symboles : {e}")
        return problems

    if not syms:
        problems.append("aucun symbole trouve")
        return problems

    names = [n for n, _ in syms]
    for n in sorted(set(names)):
        if names.count(n) > 1:
            problems.append(f"nom en double : {n}")

    by_name = dict(syms)
    for name, block in syms:
        subunits = re.findall(r'\(\s*symbol\s+"([^"]+)"', block)[1:]
        for su in subunits:
            if not su.startswith(name):
                problems.append(f"{name} : sous-unite '{su}' ne commence pas "
                               f"par le nom du symbole (devrait etre "
                               f"'{name}_..._...')")
            elif not re.fullmatch(re.escape(name) + r"_\d+_\d+", su):
                problems.append(f"{name} : sous-unite '{su}' de forme inattendue")

        ext = re.search(r'\(\s*extends\s+"([^"]+)"', block)
        if ext and ext.group(1) not in by_name:
            problems.append(f"{name} : extends '{ext.group(1)}' introuvable "
                           f"dans le meme fichier")

    return problems


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "packages/*/symbols/*.kicad_sym")))
    total_problems = 0
    for path in files:
        rel = os.path.relpath(path, ROOT)
        problems = check_file(path)
        if problems:
            total_problems += len(problems)
            print(f"  ÉCHEC {rel}")
            for p in problems:
                print(f"     - {p}")
        else:
            print(f"  OK    {rel} ({len(K.split_symbols(open(path, encoding='utf-8').read()))} symboles)")

    if total_problems:
        print(f"\n{total_problems} problème(s) trouvé(s)")
        return 1
    print(f"\n{len(files)} fichier(s) de symboles, tous cohérents")
    return 0


if __name__ == "__main__":
    sys.exit(main())
