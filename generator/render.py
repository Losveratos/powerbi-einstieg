#!/usr/bin/env python3
"""Rendert die Modul-Templates mit den Kontrollzahlen eines Cases.

    python generator/render.py business

Liest content/_template/*.md, ersetzt jeden {{platzhalter}} durch den Wert aus
content/werte/<case>.yaml und schreibt das Ergebnis nach content/<case>/.

Bricht ab, wenn ein Platzhalter unbekannt ist. Damit kann keine Kontrollzahl
aus Versehen von Hand im Text landen - der Text kennt nur Platzhalter.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

WURZEL = Path(__file__).resolve().parent.parent
PLATZHALTER = re.compile(r"\{\{(\w+)\}\}")

# index.md ist die Landingpage ueber alle Cases - sie landet nicht im
# Case-Ordner, sondern eine Ebene darueber.
LANDINGPAGE = "index.md"


def rendern(text: str, werte: dict, quelle: Path) -> str:
    unbekannt: set[str] = set()

    def ersetzen(treffer: re.Match) -> str:
        name = treffer.group(1)
        if name not in werte:
            unbekannt.add(name)
            return treffer.group(0)
        return str(werte[name])

    ergebnis = PLATZHALTER.sub(ersetzen, text)
    if unbekannt:
        raise KeyError(f"{quelle.name}: unbekannte Platzhalter {sorted(unbekannt)}")
    return ergebnis


def main() -> int:
    parser = argparse.ArgumentParser(description="Templates mit Kontrollzahlen rendern")
    parser.add_argument("case", nargs="?", default="business")
    args = parser.parse_args()

    werte_pfad = WURZEL / "content" / "werte" / f"{args.case}.yaml"
    if not werte_pfad.exists():
        print(f"Kontrollzahlen fehlen - erst verify.py laufen lassen: {werte_pfad}",
              file=sys.stderr)
        return 1
    werte = yaml.safe_load(werte_pfad.read_text(encoding="utf-8"))

    vorlagen = WURZEL / "content" / "_template"
    ziel_ordner = WURZEL / "content" / args.case
    ziel_ordner.mkdir(parents=True, exist_ok=True)

    fehler = []
    geschrieben = 0
    for vorlage in sorted(vorlagen.glob("*.md")):
        try:
            inhalt = rendern(vorlage.read_text(encoding="utf-8"), werte, vorlage)
        except KeyError as e:
            fehler.append(str(e))
            continue

        if vorlage.name == LANDINGPAGE:
            ziel = WURZEL / "content" / LANDINGPAGE
            # Die Landingpage verlinkt in den Case-Ordner hinein.
            inhalt = inhalt.replace("business/", f"{args.case}/")
        else:
            ziel = ziel_ordner / vorlage.name

        ziel.write_text(inhalt, encoding="utf-8")
        print(f"  {vorlage.name:28} -> {ziel.relative_to(WURZEL)}")
        geschrieben += 1

    if fehler:
        print("\nFEHLER:", file=sys.stderr)
        for f in fehler:
            print(f"  ! {f}", file=sys.stderr)
        print("\nEntweder Tippfehler im Template, oder der Wert fehlt in "
              "verify.py.", file=sys.stderr)
        return 1

    print(f"\n{geschrieben} Seiten gerendert.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
