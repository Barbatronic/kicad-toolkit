#!/usr/bin/env python3
"""Normalise les references de modeles 3D de toutes les empreintes des paquets.

Les empreintes viennent de projets ou les modeles etaient ranges n'importe ou :
chemins absolus d'une machine, ${KIPRJMOD} pointant vers le projet d'origine,
variables d'environnement qui n'existent que chez moi. Rien de cela ne fonctionne
chez celui qui installe le paquet, et un chemin absolu publierait au passage
l'arborescence de ma machine.

Regle appliquee, pour chaque reference :
  - le modele est fourni par le paquet          -> chemin ${KICAD10_3RD_PARTY}
  - le modele vient des librairies de KiCad     -> reference laissee telle quelle
  - sinon                                       -> reference retiree

Le chemin peut etre entre guillemets (format recent) ou non (format KiCad 5 et 6),
les deux formes sont traitees.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG_DIR = os.path.join(ROOT, "packages")
KEEP = re.compile(r'^\$\{KICAD\d*_3DMODEL_DIR\}')
MODEL_HEAD = re.compile(r'\(\s*model\s+(?:"((?:[^"\\]|\\.)*)"|([^\s)]+))')


def lists(text):
    """Positions des listes de premier niveau dans une empreinte."""
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
                if d == 1:
                    out.append((s, j + 1))
    return out


def models_of(pkg_path):
    """{nom de fichier en minuscules: chemin relatif} des modeles du paquet."""
    found = {}
    base = os.path.join(pkg_path, "3dmodels")
    for dirpath, _, filenames in os.walk(base):
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), base)
            found[fn.lower()] = rel.replace(os.sep, "/")
    return found


def main():
    total = {"redirige": 0, "conserve": 0, "retire": 0}
    for name in sorted(os.listdir(PKG_DIR)):
        pkg_path = os.path.join(PKG_DIR, name)
        meta_path = os.path.join(pkg_path, "metadata.json")
        if not os.path.isfile(meta_path):
            continue
        ident = json.load(open(meta_path, encoding="utf-8"))["identifier"].replace(".", "_")
        prefix = "${KICAD10_3RD_PARTY}/3dmodels/" + ident
        available = models_of(pkg_path)

        for dirpath, _, filenames in os.walk(os.path.join(pkg_path, "footprints")):
            for fn in sorted(filenames):
                if not fn.endswith(".kicad_mod"):
                    continue
                path = os.path.join(dirpath, fn)
                text = open(path, encoding="utf-8", errors="replace").read()
                original = text
                for s, e in reversed(lists(text)):
                    block = text[s:e]
                    m = MODEL_HEAD.match(block)
                    if not m:
                        continue
                    ref = m.group(1) if m.group(1) is not None else m.group(2)
                    if ref.startswith(prefix) or KEEP.match(ref):
                        total["conserve"] += 1
                        continue
                    base = ref.replace("\\", "/").rsplit("/", 1)[-1]
                    target = available.get(base.lower())
                    if target:
                        nouveau = f'(model "{prefix}/{target}"'
                        text = text[:s] + MODEL_HEAD.sub(nouveau, block, count=1) + text[e:]
                        total["redirige"] += 1
                    else:
                        p = s
                        while p > 0 and text[p - 1] in " \t":
                            p -= 1
                        if p > 0 and text[p - 1] == "\n":
                            p -= 1
                        text = text[:p] + text[e:]
                        total["retire"] += 1
                if text != original:
                    open(path, "w", encoding="utf-8").write(text)
        print(f"  {name} traite")

    print(f"\n{total['redirige']} reference(s) redirigee(s) vers le paquet, "
          f"{total['conserve']} conservee(s), {total['retire']} morte(s) retiree(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
