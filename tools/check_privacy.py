#!/usr/bin/env python3
"""Cherche des données personnelles avant publication.

Le dépôt est public : ni adresse de courriel, ni chemin absolu de ma machine, ni
nom de session ne doivent s'y trouver. Le script parcourt tout le dépôt sauf .git
et dist, et rend un code de sortie non nul si quelque chose est trouvé.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORED_DIRS = {".git", "dist", "node_modules", ".github/cache", "_site", "vendor"}
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".step", ".stp", ".wrl",
              ".zip", ".gz", ".pdf", ".woff", ".woff2", ".ttf"}

# Motifs recherchés. La description sert au rapport.
PATTERNS = [
    ("adresse de courriel",
     re.compile(r"[\w.+-]+@[\w-]+\.[\w.]{2,}")),
    ("chemin personnel Unix",
     re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+")),
    ("chemin personnel Windows",
     re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9._-]+", re.IGNORECASE)),
    ("numéro de téléphone français",
     re.compile(r"(?:(?<=\s)|^)(?:\+33|0)\s?[1-9](?:[\s.-]?\d{2}){4}(?=\s|$)")),
    ("jeton ou clé d'API",
     re.compile(r"(?:ghp_[A-Za-z0-9]{36}|gh[pousr]_[A-Za-z0-9]{20,}|"
                r"AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{32,})")),
    ("coordonnées GPS précises",
     re.compile(r"\b4[0-9]\.\d{5,},\s?[0-9]\.\d{5,}\b")),
]

# Chaînes autorisées malgré un motif : elles sont publiques et voulues.
ALLOWED = {
    # noms de dépôt « organisation/projet@version » et adresses de service
    "adresse de courriel": re.compile(
        r"^(?:noreply@|support@|contact@|info@|[\w.+-]+@example\.(?:com|org)"
        r"|[\w.-]+@v\d+\.\d+(?:\.\d+)?$)"),
}

# Quelques mots à signaler pour relecture, sans bloquer la publication.
REVIEW_WORDS = ["unilasalle", "makerspace-unilasalle"]


def is_text(path):
    if os.path.splitext(path)[1].lower() in BINARY_EXT:
        return False
    try:
        with open(path, "rb") as f:
            return b"\0" not in f.read(4096)
    except OSError:
        return False


def walk():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in sorted(dirnames)
                       if d not in IGNORED_DIRS and not d.startswith(".git")]
        for fn in sorted(filenames):
            yield os.path.join(dirpath, fn)


def main():
    findings, reviews = [], []
    me = os.path.abspath(__file__)
    for path in walk():
        rel = os.path.relpath(path, ROOT)
        if not is_text(path) or os.path.abspath(path) == me:
            continue
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, pat in PATTERNS:
                for m in pat.finditer(line):
                    allow = ALLOWED.get(label)
                    if allow and allow.match(m.group(0)):
                        continue
                    findings.append((rel, lineno, label, m.group(0)))
            low = line.lower()
            for w in REVIEW_WORDS:
                if w in low:
                    reviews.append((rel, lineno, w))

    if reviews:
        print("À relire (autorisé, mais à confirmer) :")
        for rel, lineno, w in reviews:
            print(f"  {rel}:{lineno}  contient « {w} »")
        print()

    if findings:
        print(f"{len(findings)} donnée(s) personnelle(s) trouvée(s) :")
        for rel, lineno, label, value in findings:
            print(f"  {rel}:{lineno}  {label} : {value}")
        return 1

    print("Aucune donnée personnelle trouvée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
