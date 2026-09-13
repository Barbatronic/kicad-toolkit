#!/usr/bin/env python3
"""Construit les archives des paquets et le depot PCM servi par GitHub Pages.

Produit dans dist/ :
  <identifiant>-<version>.zip   une archive par paquet, a joindre a la release
  packages.json                 la liste des paquets et de leurs versions
  repository.json               le point d'entree ajoute dans KiCad
  resources.json / resources.zip les icones affichees par le gestionnaire
"""
import argparse, hashlib, json, os, sys, time, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG_DIR = os.path.join(ROOT, "packages")
DIST = os.path.join(ROOT, "dist")

# Seuls ces dossiers sont extraits par KiCad, le reste de l'archive est ignore.
PCM_DIRS = ("plugins", "footprints", "3dmodels", "symbols", "resources",
            "colors", "templates", "scripts")

REPO_NAME = "Barbatronic - librairies et outils KiCad"
DEFAULT_BASE = "https://barbatronic.github.io/kicad-toolkit"
DEFAULT_DOWNLOAD = "https://github.com/Barbatronic/kicad-toolkit/releases/download"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def collect(pkg_path):
    """Fichiers a archiver, en chemins relatifs, tries pour un zip reproductible."""
    out = []
    meta = os.path.join(pkg_path, "metadata.json")
    if os.path.exists(meta):
        out.append("metadata.json")
    for d in PCM_DIRS:
        base = os.path.join(pkg_path, d)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames.sort()
            for fn in sorted(filenames):
                if fn in (".DS_Store", "desktop.ini", "Thumbs.db"):
                    continue
                full = os.path.join(dirpath, fn)
                out.append(os.path.relpath(full, pkg_path))
    return out


def make_zip(pkg_path, dest, files):
    """Archive deterministe : ordre et horodatage fixes."""
    total = 0
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in files:
            full = os.path.join(pkg_path, rel)
            total += os.path.getsize(full)
            info = zipfile.ZipInfo(rel.replace(os.sep, "/"), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(full, "rb") as f:
                z.writestr(info, f.read())
    return total


def build_resources(packages, dest):
    """Archive des icones, une par identifiant de paquet."""
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for ident, pkg_path in packages:
            icon = os.path.join(pkg_path, "resources", "icon.png")
            if not os.path.exists(icon):
                continue
            info = zipfile.ZipInfo(f"{ident}/icon.png", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(icon, "rb") as f:
                z.writestr(info, f.read())


def resource_entry(path, url):
    st = os.stat(path)
    return {
        "url": url,
        "sha256": sha256(path),
        "update_timestamp": int(st.st_mtime),
        "update_time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(st.st_mtime)),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", required=True, help="version des paquets, par exemple 1.0.0")
    ap.add_argument("--status", default="stable",
                    choices=["stable", "testing", "development", "deprecated"])
    ap.add_argument("--kicad-version", default="10.0", help="version minimale de KiCad")
    ap.add_argument("--base-url", default=DEFAULT_BASE, help="URL publique du depot")
    ap.add_argument("--download-base", default=DEFAULT_DOWNLOAD,
                    help="URL de base des archives, le tag est ajoute ensuite")
    ap.add_argument("--previous", help="packages.json deja publie, pour garder l'historique")
    args = ap.parse_args()

    if not args.version.replace(".", "").isdigit() or args.version.count(".") > 2:
        sys.exit(f"version invalide : {args.version} (attendu majeur[.mineur[.correctif]])")

    os.makedirs(DIST, exist_ok=True)
    history = {}
    if args.previous and os.path.exists(args.previous):
        for p in json.load(open(args.previous, encoding="utf-8")).get("packages", []):
            history[p["identifier"]] = p.get("versions", [])

    packages, ids = [], []
    for name in sorted(os.listdir(PKG_DIR)):
        pkg_path = os.path.join(PKG_DIR, name)
        meta_path = os.path.join(pkg_path, "metadata.json")
        if not os.path.isfile(meta_path):
            continue
        meta = json.load(open(meta_path, encoding="utf-8"))
        ident = meta["identifier"]
        files = collect(pkg_path)
        if len(files) <= 1:
            print(f"  {ident} : aucun contenu, paquet ignore")
            continue

        zip_name = f"{ident}-{args.version}.zip"
        zip_path = os.path.join(DIST, zip_name)
        install_size = make_zip(pkg_path, zip_path, files)
        version = {
            "version": args.version,
            "status": args.status,
            "kicad_version": args.kicad_version,
            "download_url": f"{args.download_base}/v{args.version}/{zip_name}",
            "download_sha256": sha256(zip_path),
            "download_size": os.path.getsize(zip_path),
            "install_size": install_size,
        }
        # l'historique est conserve, la version courante remplace son homonyme
        versions = [v for v in history.get(ident, []) if v.get("version") != args.version]
        versions.append(version)
        versions.sort(key=lambda v: [int(x) for x in v["version"].split(".")])
        meta["versions"] = versions
        meta.pop("$schema", None)
        packages.append(meta)
        ids.append((ident, pkg_path))
        print(f"  {ident:48} {len(files):4} fichiers  "
              f"{version['download_size'] / 1024:8.1f} Kio")

    with open(os.path.join(DIST, "packages.json"), "w", encoding="utf-8") as f:
        json.dump({"$schema": "https://go.kicad.org/pcm/schemas/v1", "packages": packages},
                  f, ensure_ascii=False, indent=2)

    res_zip = os.path.join(DIST, "resources.zip")
    build_resources(ids, res_zip)

    repo = {
        "$schema": "https://go.kicad.org/pcm/schemas/v1",
        "name": REPO_NAME,
        "maintainer": {"name": "Barbatronic",
                       "contact": {"web": "https://github.com/Barbatronic/kicad-toolkit"}},
        "packages": resource_entry(os.path.join(DIST, "packages.json"),
                                   f"{args.base_url}/packages.json"),
        "resources": resource_entry(res_zip, f"{args.base_url}/resources.zip"),
    }
    with open(os.path.join(DIST, "repository.json"), "w", encoding="utf-8") as f:
        json.dump(repo, f, ensure_ascii=False, indent=2)

    print(f"\ndepot ecrit dans {os.path.relpath(DIST, ROOT)}/ "
          f"({len(packages)} paquets, version {args.version})")
    print(f"URL a ajouter dans KiCad : {args.base_url}/repository.json")


if __name__ == "__main__":
    main()
