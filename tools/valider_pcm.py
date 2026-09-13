#!/usr/bin/env python3
"""Valide le depot construit dans dist/ contre le schema officiel de KiCad.

Verifie aussi que chaque archive ne contient que des dossiers reconnus par le
gestionnaire de contenu : un fichier place ailleurs serait ignore a l'installation,
sans le moindre message.
"""
import json, os, sys, urllib.request, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
SCHEMA_URL = "https://go.kicad.org/pcm/schemas/v1"
PCM_DIRS = {"plugins", "footprints", "3dmodels", "symbols", "resources",
            "colors", "templates", "scripts"}


CACHE = os.path.expanduser("~/.cache/barbatronic-kicad-toolkit/pcm.v1.schema.json")


def charger_schema():
    """Recupere le schema officiel, avec un cache local pour les rejeux hors ligne."""
    try:
        req = urllib.request.Request(SCHEMA_URL, headers={"User-Agent": "barbatronic-kicad-toolkit"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        json.loads(data)
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        with open(CACHE, "wb") as f:
            f.write(data)
        return json.loads(data)
    except Exception as e:
        if os.path.exists(CACHE):
            print(f"  schema distant indisponible ({e}), utilisation du cache local")
            return json.load(open(CACHE, encoding="utf-8"))
        raise


def main():
    try:
        import jsonschema
    except ImportError:
        sys.exit("le module jsonschema est requis : pip install jsonschema")

    if not os.path.isdir(DIST):
        sys.exit("dist/ est absent : lancez d'abord tools/build_pcm.py")

    schema = charger_schema()

    def sous_schema(nom):
        s = dict(schema)
        s.pop("$ref", None)
        s["$ref"] = f"#/definitions/{nom}"
        return s

    erreurs = []

    def valider(objet, nom_schema, etiquette):
        try:
            jsonschema.validate(objet, sous_schema(nom_schema))
            print(f"  {etiquette} : conforme")
        except jsonschema.ValidationError as e:
            erreurs.append(f"{etiquette} : {e.message} (à {list(e.path)})")
            print(f"  {etiquette} : NON CONFORME")

    valider(json.load(open(os.path.join(DIST, "repository.json"), encoding="utf-8")),
            "Repository", "repository.json")
    paquets = json.load(open(os.path.join(DIST, "packages.json"), encoding="utf-8"))
    valider(paquets, "PackageArray", "packages.json")

    for p in paquets["packages"]:
        valider(p, "Package", f"  {p['identifier']}")

    print("\ncontenu des archives :")
    for p in paquets["packages"]:
        for v in p["versions"]:
            nom = f"{p['identifier']}-{v['version']}.zip"
            chemin = os.path.join(DIST, nom)
            if not os.path.exists(chemin):
                continue
            with zipfile.ZipFile(chemin) as z:
                noms = z.namelist()
            racines = {n.split("/")[0] for n in noms if "/" in n}
            hors = racines - PCM_DIRS
            fichiers_racine = [n for n in noms if "/" not in n and n != "metadata.json"]
            if hors:
                erreurs.append(f"{nom} : dossiers ignores par KiCad {sorted(hors)}")
                print(f"  {nom} : dossiers non reconnus {sorted(hors)}")
            elif fichiers_racine:
                erreurs.append(f"{nom} : fichiers ignores a la racine {fichiers_racine}")
                print(f"  {nom} : fichiers inutiles a la racine {fichiers_racine}")
            else:
                print(f"  {nom} : {len(noms)} fichiers, arborescence conforme")

            attendu = v["download_sha256"]
            import hashlib
            h = hashlib.sha256()
            with open(chemin, "rb") as f:
                for bloc in iter(lambda: f.read(1 << 20), b""):
                    h.update(bloc)
            if h.hexdigest() != attendu:
                erreurs.append(f"{nom} : empreinte SHA-256 differente de celle annoncee")

    if erreurs:
        print(f"\n{len(erreurs)} probleme(s) :")
        for e in erreurs:
            print("  -", e)
        return 1
    print("\ndepot PCM valide")
    return 0


if __name__ == "__main__":
    sys.exit(main())
