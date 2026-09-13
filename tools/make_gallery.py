#!/usr/bin/env python3
"""Rend chaque symbole, empreinte et bloc en SVG et ecrit les pages de catalogue.

Necessite kicad-cli. Les SVG vont dans docs/assets/catalogue/, les pages
Markdown correspondantes dans docs/librairies/ et docs/blocs.md.
"""
import glob, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "packages")
DOCS = os.path.join(ROOT, "docs")
ASSETS = os.path.join(DOCS, "assets", "catalogue")

KICAD_CLI = shutil.which("kicad-cli")


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode == 0 and "Fini" in (r.stdout + r.stderr) or r.returncode == 0, r


def symbol_names(path):
    """Noms des symboles de premier niveau d'une librairie."""
    names = []
    text = open(path, encoding="utf-8").read()
    depth, in_str, esc, stack = 0, False, False, []
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
                    m = re.match(r'\(\s*symbol\s+"((?:[^"\\]|\\.)*)"', text[s:j + 1])
                    if m:
                        names.append(m.group(1))
    return names


def symbol_info(path, name):
    """Description et mots-cles d'un symbole."""
    text = open(path, encoding="utf-8").read()
    i = text.find(f'(symbol "{name}"')
    if i < 0:
        return "", ""
    chunk = text[i:i + 4000]
    d = re.search(r'\(property "Description" "((?:[^"\\]|\\.)*)"', chunk)
    k = re.search(r'\(property "ki_keywords" "((?:[^"\\]|\\.)*)"', chunk)
    return (d.group(1) if d else "", k.group(1) if k else "")


def render_symbols(out):
    """Rend chaque librairie de symboles, retourne {lib: [(nom, svg, descr, mots)]}."""
    result = {}
    for path in sorted(glob.glob(f"{PKG}/*/symbols/*.kicad_sym")):
        lib = os.path.basename(path)[:-len(".kicad_sym")]
        d = os.path.join(out, "symboles", lib)
        os.makedirs(d, exist_ok=True)
        ok, r = run([KICAD_CLI, "sym", "export", "svg", "--no-background-color", "-o", d, path])
        entries = []
        for name in symbol_names(path):
            svg = os.path.join(d, name + ".svg")
            descr, kw = symbol_info(path, name)
            entries.append((name, svg if os.path.exists(svg) else None, descr, kw))
        result[lib] = entries
        print(f"  symboles {lib} : {len(entries)}")
    return result


def render_footprints(out):
    result = {}
    for path in sorted(glob.glob(f"{PKG}/*/footprints/*.pretty")):
        lib = os.path.basename(path)[:-len(".pretty")]
        d = os.path.join(out, "empreintes", lib)
        os.makedirs(d, exist_ok=True)
        run([KICAD_CLI, "fp", "export", "svg", "--layers",
             "F.Cu,F.Paste,F.SilkS,F.Mask,Edge.Cuts,F.Fab,F.CrtYd,B.Cu,B.SilkS",
             "-o", d, path])
        entries = []
        for mod in sorted(glob.glob(os.path.join(path, "*.kicad_mod"))):
            name = os.path.basename(mod)[:-len(".kicad_mod")]
            svg = os.path.join(d, name + ".svg")
            entries.append((name, svg if os.path.exists(svg) else None))
        result[lib] = entries
        print(f"  empreintes {lib} : {len(entries)}")
    return result


def render_blocks(out):
    entries = []
    d = os.path.join(out, "blocs")
    os.makedirs(d, exist_ok=True)
    for blk in sorted(glob.glob(f"{PKG}/*/resources/design-blocks/*.kicad_blocks/*.kicad_block")):
        name = os.path.basename(blk)[:-len(".kicad_block")]
        sch = os.path.join(blk, name + ".kicad_sch")
        meta_path = os.path.join(blk, name + ".json")
        meta = json.load(open(meta_path, encoding="utf-8")) if os.path.exists(meta_path) else {}
        run([KICAD_CLI, "sch", "export", "svg", "--no-background-color",
             "--exclude-drawing-sheet", "-o", d, sch])
        svg = os.path.join(d, name + ".svg")
        entries.append((name, svg if os.path.exists(svg) else None,
                        meta.get("description", ""), meta.get("keywords", "")))
    print(f"  blocs : {len(entries)}")
    return entries


def rel(svg):
    return "/kicad-toolkit/assets/catalogue/" + os.path.relpath(svg, ASSETS).replace(os.sep, "/")


THEMES = {
    "MCU": "Cartes et modules à microcontrôleur",
    "Power": "Alimentation, conversion et commutation de puissance",
    "Motion": "Motorisation et commande de moteurs",
    "Sensors": "Capteurs",
    "Connectors": "Connectique, alimentation et stockage",
    "Interface": "Interface : boutons, interrupteurs, voyants",
    "Mechanical": "Mécanique et repères de fabrication",
}


def write_pages(symbols, footprints, blocks):
    os.makedirs(os.path.join(DOCS, "librairies"), exist_ok=True)

    # --- symboles
    lines = ["---", "title: Symboles", "parent: Librairies", "nav_order: 1", "---", "",
             "# Symboles", "",
             "Tous les symboles du toolkit, rendus automatiquement depuis les fichiers "
             "de librairie à chaque publication.", ""]
    for lib, entries in sorted(symbols.items()):
        theme = lib.replace("Barbatronic_", "")
        lines += [f"## {lib}", "", f"*{THEMES.get(theme, '')}*", "",
                  "Dans KiCad, cette librairie apparaît sous le nom "
                  f"`PCM_{lib}`.", ""]
        for name, svg, descr, kw in entries:
            lines.append(f"### {name}")
            lines.append("")
            if descr:
                lines += [descr, ""]
            if svg:
                lines += [f'<img src="{rel(svg)}" alt="Symbole {name}" '
                          f'style="max-height:220px;max-width:100%">', ""]
            if kw:
                lines += [f"Mots-clés : {kw}", ""]
    open(os.path.join(DOCS, "librairies", "symboles.md"), "w", encoding="utf-8").write(
        "\n".join(lines) + "\n")

    # --- empreintes
    lines = ["---", "title: Empreintes", "parent: Librairies", "nav_order: 2", "---", "",
             "# Empreintes", ""]
    mine = {k: v for k, v in footprints.items() if k.startswith("Barbatronic_")}
    third = {k: v for k, v in footprints.items() if not k.startswith("Barbatronic_")}
    for title, group in (("Empreintes du toolkit", mine),
                         ("Empreintes tierces redistribuées", third)):
        if not group:
            continue
        lines += [f"## {title}", ""]
        for lib, entries in sorted(group.items()):
            theme = lib.replace("Barbatronic_", "")
            lines += [f"### {lib}", ""]
            if theme in THEMES:
                lines += [f"*{THEMES[theme]}*", ""]
            lines += ['<div class="catalogue">', ""]
            for name, svg in entries:
                lines.append('<figure class="carte">')
                if svg:
                    lines.append(f'<img src="{rel(svg)}" alt="Empreinte {name}" loading="lazy">')
                lines.append(f"<figcaption>{name}</figcaption>")
                lines.append("</figure>")
            lines += ["", "</div>", ""]
    open(os.path.join(DOCS, "librairies", "empreintes.md"), "w", encoding="utf-8").write(
        "\n".join(lines) + "\n")

    # --- blocs
    lines = ["---", "title: Blocs de conception", "nav_order: 4", "---", "",
             "# Blocs de conception", "",
             "Des morceaux de schéma tout faits, à déposer dans une feuille plutôt "
             "qu'à redessiner à chaque carte.", "",
             "{: .note }", "> Les blocs de conception demandent KiCad 9 ou plus récent.", ""]
    for name, svg, descr, kw in blocks:
        lines += [f"## {name.replace('_', ' ')}", ""]
        if descr:
            lines += [descr, ""]
        if svg:
            lines += [f'<img src="{rel(svg)}" alt="Bloc {name}" '
                      f'style="max-width:100%;background:#fff">', ""]
        if kw:
            lines += [f"Mots-clés : {kw}", ""]
    open(os.path.join(DOCS, "blocs.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


def main():
    if not KICAD_CLI:
        sys.exit("kicad-cli est introuvable : installez KiCad 9 ou plus récent "
                 "pour produire le catalogue.")
    if os.path.isdir(ASSETS):
        shutil.rmtree(ASSETS)
    os.makedirs(ASSETS)
    print("rendu du catalogue :")
    symbols = render_symbols(ASSETS)
    footprints = render_footprints(ASSETS)
    blocks = render_blocks(ASSETS)
    write_pages(symbols, footprints, blocks)
    n = sum(len(v) for v in symbols.values()) + sum(len(v) for v in footprints.values()) + len(blocks)
    print(f"\ncatalogue ecrit : {n} elements, pages mises a jour dans docs/")


if __name__ == "__main__":
    main()
