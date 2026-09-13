"""Construction de schemas KiCad 9 pour les blocs de conception."""
import os, re, hashlib, urllib.request

# Emplacements possibles des librairies de symboles officielles, du plus local
# au plus distant. Le cache permet de regenerer les blocs sans KiCad installe,
# en local comme dans l'integration continue.
SYMBOL_DIRS = [
    "/usr/share/kicad/symbols",
    "/usr/local/share/kicad/symbols",
    "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols",
    os.path.expanduser("~/.cache/barbatronic-kicad-toolkit/symbols"),
]

# Version des librairies officielles utilisee quand il faut les telecharger.
SYMBOL_LIB_TAG = "10.0.6"
SYMBOL_LIB_URL = ("https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/"
                  + SYMBOL_LIB_TAG + "/{lib}.kicad_sym")
DOWNLOAD_DIR = os.path.expanduser("~/.cache/barbatronic-kicad-toolkit/symbols")


def _download_lib(lib):
    """Recupere une librairie officielle dans le cache local."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    dest = os.path.join(DOWNLOAD_DIR, lib + ".kicad_sym")
    url = SYMBOL_LIB_URL.format(lib=lib)
    with urllib.request.urlopen(url, timeout=60) as r:
        data = r.read()
    if not data.lstrip().startswith(b"(kicad_symbol_lib"):
        raise RuntimeError(f"reponse inattendue pour {lib} depuis {url}")
    with open(dest, "wb") as f:
        f.write(data)
    return dest


def _scan(text):
    depth, in_str, esc, stack = 0, False, False, []
    for j, c in enumerate(text):
        if esc:
            esc = False
            continue
        if c == '\\':
            esc = True
        elif c == '"':
            in_str = not in_str
        elif not in_str:
            if c == '(':
                stack.append((depth, j))
                depth += 1
            elif c == ')':
                depth -= 1
                d, s = stack.pop()
                yield d, s, j + 1


def _blocks(text, depth, head):
    """Retourne les listes de profondeur donnee dont le premier jeton est head."""
    out = []
    pat = re.compile(r'\(\s*' + head + r'(?=[\s(])')
    for d, s, e in _scan(text):
        if d == depth and pat.match(text[s:e]):
            out.append(text[s:e])
    return out


class SymbolCache:
    """Charge les definitions de symboles des librairies KiCad."""

    def __init__(self, extra_dirs=()):
        self.dirs = list(SYMBOL_DIRS) + list(extra_dirs)
        self._libs = {}

    def _load_lib(self, lib):
        if lib in self._libs:
            return self._libs[lib]
        for d in self.dirs:
            p = os.path.join(d, lib + ".kicad_sym")
            if os.path.exists(p):
                text = open(p, encoding="utf-8").read()
                syms = {}
                for b in _blocks(text, 1, "symbol"):
                    name = re.match(r'\(\s*symbol\s+"((?:[^"\\]|\\.)*)"', b).group(1)
                    syms[name] = b
                self._libs[lib] = syms
                return syms
        # absente du disque : la recuperer depuis les librairies officielles
        path = _download_lib(lib)
        text = open(path, encoding="utf-8").read()
        syms = {}
        for b in _blocks(text, 1, "symbol"):
            name = re.match(r'\(\s*symbol\s+"((?:[^"\\]|\\.)*)"', b).group(1)
            syms[name] = b
        self._libs[lib] = syms
        return syms

    def definition(self, lib_id):
        """Retourne le bloc (symbol ...) renomme en lib_id complet, prêt pour lib_symbols."""
        lib, name = lib_id.split(":", 1)
        syms = self._load_lib(lib)
        if name not in syms:
            raise KeyError(f"symbole {name} absent de {lib}")
        block = syms[name]
        # (extends "Base") : fusionner avec le parent
        m = re.search(r'\(\s*extends\s+"((?:[^"\\]|\\.)*)"\s*\)', block)
        if m:
            parent = syms[m.group(1)]
            block = self._merge_extends(block, parent, name, m.group(1))
        # seul le symbole racine porte le nom complet "Lib:Nom" ; les sous-unites
        # gardent leur nom court, comme le fait KiCad dans lib_symbols.
        esc = lib_id.replace('\\', '\\\\').replace('"', '\\"')
        block = re.sub(r'(\(\s*symbol\s+")(?:[^"\\]|\\.)*(")', r'\g<1>' + esc + r'\g<2>',
                       block, count=1)
        return block

    def _merge_extends(self, child, parent, child_name, parent_name):
        """Remplace (extends "P") par les unites graphiques du parent."""
        units = [b for b in _blocks(parent, 1, "symbol")]
        child = re.sub(r'\n?\s*\(\s*extends\s+"(?:[^"\\]|\\.)*"\s*\)', '', child)
        renamed = []
        for u in units:
            renamed.append(re.sub(r'(\(\s*symbol\s+")' + re.escape(parent_name) + r'(_\d+_\d+")',
                                  r'\g<1>' + child_name + r'\g<2>', u))
        return child[:-1].rstrip() + "\n" + "\n".join(renamed) + "\n)"

    def pins(self, lib_id):
        """Retourne {numero: (x, y, angle, type)} dans le repere du symbole."""
        block = self.definition(lib_id)
        out = {}
        for p in _blocks(block, 2, "pin"):
            at = re.search(r'\(\s*at\s+(-?[\d.]+)\s+(-?[\d.]+)\s*(-?[\d.]+)?\s*\)', p)
            num = re.search(r'\(\s*number\s+"((?:[^"\\]|\\.)*)"', p)
            typ = re.match(r'\(\s*pin\s+(\w+)', p)
            if at and num:
                out[num.group(1)] = (float(at.group(1)), float(at.group(2)),
                                     float(at.group(3) or 0), typ.group(1) if typ else "passive")
        return out

    def bbox(self, lib_id):
        """Boite englobante du dessin du symbole, dans son propre repere."""
        block = self.definition(lib_id)
        xs, ys = [], []
        for tok in ("start", "end", "center", "mid", "at", "xy"):
            for m in re.finditer(r'\(\s*' + tok + r'\s+(-?[\d.]+)\s+(-?[\d.]+)', block):
                xs.append(float(m.group(1)))
                ys.append(float(m.group(2)))
        for px, py, _, _ in self.pins(lib_id).values():
            xs.append(px)
            ys.append(py)
        if not xs:
            return (-1.27, -1.27, 1.27, 1.27)
        return (min(xs), min(ys), max(xs), max(ys))

    def properties(self, lib_id):
        """Retourne les proprietes de premier niveau du symbole."""
        block = self.definition(lib_id)
        out = {}
        for p in _blocks(block, 1, "property"):
            m = re.match(r'\(\s*property\s+"((?:[^"\\]|\\.)*)"\s+"((?:[^"\\]|\\.)*)"', p)
            if m:
                out[m.group(1)] = m.group(2).replace('\\"', '"').replace('\\\\', '\\')
        return out


def stable_uuid(*parts):
    """UUID reproductible : un même bloc regenere donne le même fichier."""
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def rotate(x, y, angle):
    """Applique la rotation KiCad (degres, sens antihoraire) a un point du symbole."""
    a = int(angle) % 360
    if a == 0:
        return x, y
    if a == 90:
        return -y, x
    if a == 180:
        return -x, -y
    return y, -x


def pin_position(sym_at, angle, mirror, pin_xy):
    """Coordonnee absolue d'une pin dans le schema.

    Le repere du symbole a un axe Y ascendant, celui du schema un axe Y descendant.
    """
    px, py = pin_xy
    if mirror == "x":
        py = -py
    elif mirror == "y":
        px = -px
    px, py = rotate(px, py, angle)
    return round(sym_at[0] + px, 4), round(sym_at[1] - py, 4)


class Schematic:
    """Assemble un schema KiCad 9 : symboles, fils, jonctions, labels."""

    def __init__(self, name, cache, paper="A4"):
        self.name = name
        self.cache = cache
        self.paper = paper
        self.used = []          # lib_id dans l'ordre d'apparition
        self.items = []         # fragments s-expr de premier niveau
        self.refs = {}          # prefixe -> compteur

    # -- placement ---------------------------------------------------------
    def place(self, lib_id, at, ref=None, value=None, footprint="", angle=0,
              mirror=None, hide_value=False):
        """Place un symbole et retourne un accesseur de position de pin."""
        if lib_id not in self.used:
            self.used.append(lib_id)
        props = self.cache.properties(lib_id)
        prefix = props.get("Reference", "U")
        if ref is None:
            if prefix.startswith("#"):
                ref = prefix + self.name.upper()[:3] + str(len(self.items))
            else:
                self.refs[prefix] = self.refs.get(prefix, 0) + 1
                ref = f"{prefix}{self.refs[prefix]}"
        if value is None:
            value = props.get("Value", "")
        uid = stable_uuid(self.name, lib_id, at, ref)

        def esc(s):
            return s.replace('\\', '\\\\').replace('"', '\\"')

        hide = "\t\t\t\t(hide yes)\n" if prefix.startswith("#") else ""
        hide_v = "\t\t\t\t(hide yes)\n" if hide_value else ""
        mir = f"\n\t\t(mirror {mirror})" if mirror else ""
        # Reference au-dessus du dessin, Value en dessous, hors de la boite englobante.
        x0, y0, x1, y1 = self.cache.bbox(lib_id)
        (rx, ry) = pin_position(at, angle, mirror, ((x0 + x1) / 2, y1 + 2.54))
        (vx, vy) = pin_position(at, angle, mirror, ((x0 + x1) / 2, y0 - 2.54))
        self.items.append(f'''	(symbol
		(lib_id "{esc(lib_id)}")
		(at {at[0]} {at[1]} {int(angle)}){mir}
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(fields_autoplaced yes)
		(uuid "{uid}")
		(property "Reference" "{esc(ref)}"
			(at {rx} {ry} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
{hide}			)
		)
		(property "Value" "{esc(value)}"
			(at {vx} {vy} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
{hide_v}			)
		)
		(property "Footprint" "{esc(footprint)}"
			(at {at[0]} {at[1]} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Datasheet" "{esc(props.get("Datasheet", ""))}"
			(at {at[0]} {at[1]} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
	)''')
        pins = self.cache.pins(lib_id)

        def pin(number):
            if str(number) not in pins:
                raise KeyError(f"{lib_id} n'a pas de pin {number} (pins: {sorted(pins)})")
            px, py, _, _ = pins[str(number)]
            return pin_position(at, angle, mirror, (px, py))

        return pin

    # -- liaisons ----------------------------------------------------------
    def wire(self, a, b):
        self.items.append(f'''	(wire
		(pts
			(xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})
		)
		(stroke
			(width 0)
			(type default)
		)
		(uuid "{stable_uuid(self.name, "w", a, b)}")
	)''')

    def route(self, *points):
        """Relie une suite de points par des segments successifs."""
        for a, b in zip(points, points[1:]):
            self.wire(a, b)

    def junction(self, at):
        self.items.append(f'''	(junction
		(at {at[0]} {at[1]})
		(diameter 0)
		(color 0 0 0 0)
		(uuid "{stable_uuid(self.name, "j", at)}")
	)''')

    def label(self, at, text, angle=0, glob=False):
        kind = "global_label" if glob else "label"
        shape = '\n\t\t(shape input)' if glob else ''
        self.items.append(f'''	({kind}
		"{text}"
		(at {at[0]} {at[1]} {int(angle)}){shape}
		(fields_autoplaced yes)
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify left)
		)
		(uuid "{stable_uuid(self.name, kind, at, text)}")
	)''')

    def no_connect(self, at):
        self.items.append(f'''	(no_connect
		(at {at[0]} {at[1]})
		(uuid "{stable_uuid(self.name, "nc", at)}")
	)''')

    def text(self, at, content, size=1.27):
        self.items.append(f'''	(text
		"{content}"
		(exclude_from_sim no)
		(at {at[0]} {at[1]} 0)
		(effects
			(font
				(size {size} {size})
			)
			(justify left)
		)
		(uuid "{stable_uuid(self.name, "t", at, content)}")
	)''')

    # -- sortie ------------------------------------------------------------
    def render(self, title_block=None):
        defs = "\n".join(
            "\n".join("\t\t" + ln.strip() if i else "\t\t" + ln
                      for i, ln in enumerate(self.cache.definition(l).split("\n")))
            for l in self.used)
        tb = ""
        if title_block:
            rows = "\n".join(f'\t\t({k} "{v}")' for k, v in title_block.items())
            tb = f"\n\t(title_block\n{rows}\n\t)"
        body = "\n".join(self.items)
        return f'''(kicad_sch
	(version 20250114)
	(generator "eeschema")
	(generator_version "9.0")
	(uuid "{stable_uuid(self.name, "root")}")
	(paper "{self.paper}"){tb}
	(lib_symbols
{defs}
	)
{body}
	(sheet_instances
		(path "/"
			(page "1")
		)
	)
	(embedded_fonts no)
)
'''


# Jetons introduits par le format KiCad 10 et ignores par KiCad 9.
KICAD10_ONLY = ("in_pos_files", "duplicate_pin_numbers_are_jumpers",
                "show_name", "do_not_autoplace", "exclude_from_bom",
                "jumper_pin_group")

def to_kicad9(text):
    """Retire les listes propres au format KiCad 10 pour rester lisible par KiCad 9."""
    cuts = []
    for d, s, e in _scan(text):
        m = re.match(r'\(\s*([a-z_0-9]+)', text[s:e])
        if m and m.group(1) in KICAD10_ONLY:
            cuts.append((s, e))
    cuts.sort(reverse=True)
    for s, e in cuts:
        # avale l'indentation et le saut de ligne qui precedent
        p = s
        while p > 0 and text[p - 1] in " \t":
            p -= 1
        if p > 0 and text[p - 1] == "\n":
            p -= 1
        text = text[:p] + text[e:]
    return text


# -- Edition de librairies de symboles deja existantes (fichiers .kicad_sym) --
# A la difference de SymbolCache, qui resout des lib_id depuis les librairies
# officielles pour construire un schema, ces fonctions decoupent et modifient
# un fichier de librairie donne sans en reformater le contenu.

def split_symbols(text):
    """Retourne [(nom, bloc)] pour les symboles de premier niveau d'un .kicad_sym."""
    out = []
    for d, s, e in _scan(text):
        if d != 1:
            continue
        m = re.match(r'\(\s*symbol\s+"((?:[^"\\]|\\.)*)"', text[s:e])
        if m:
            out.append((m.group(1), text[s:e]))
    out.sort(key=lambda x: text.find(x[1]))
    return out


def rename(block, old, new):
    """Renomme un symbole et ses sous-unites <old>_<u>_<v>."""
    o = re.escape(old)
    block = re.sub(r'(\(\s*symbol\s+")' + o + r'(")', r'\g<1>' + new + r'\g<2>', block, count=1)
    block = re.sub(r'(\(\s*symbol\s+")' + o + r'(_\d+_\d+")', r'\g<1>' + new + r'\g<2>', block)
    block = re.sub(r'(\(\s*extends\s+")' + o + r'(")', r'\g<1>' + new + r'\g<2>', block)
    return block


def set_property(block, name, value):
    """Remplace la valeur d'une propriete de premier niveau du symbole."""
    pat = re.compile(r'(\(\s*property\s+"' + re.escape(name) + r'"\s+)"(?:[^"\\]|\\.)*"')
    if pat.search(block):
        return pat.sub(lambda m: m.group(1) + '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"',
                       block, count=1)
    return block


def build_symbol_lib(blocks, version="20241209"):
    """Assemble une liste de blocs (symbol ...) en un fichier .kicad_sym complet."""
    body = "\n".join(b.rstrip() for b in blocks)
    return ('(kicad_symbol_lib\n\t(version %s)\n\t(generator "kicad_symbol_editor")\n'
            '\t(generator_version "9.0")\n%s\n)\n' % (version, body))
