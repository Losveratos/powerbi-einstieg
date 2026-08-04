#!/usr/bin/env python3
"""Schneidet die Rohscreenshots zu und setzt rote Markierungsrahmen.

    python generator/annotate.py

Liest site/img/raw/*.png (aufgenommen mit generator/shot.ps1, 1920x1200) und
schreibt die fertigen Bilder nach site/img/.

Pro Modul genau EIN roter Rahmen um die Stelle, auf die es ankommt - mehr
Markierungen lenken nur ab. Alle Koordinaten beziehen sich auf das ungeschnittene
Rohbild; zugeschnitten wird erst danach.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

WURZEL = Path(__file__).resolve().parent.parent
ROH = WURZEL / "site" / "img" / "raw"
ZIEL = WURZEL / "site" / "img"

ROT = (214, 42, 34)
RAHMENBREITE = 5
RADIUS = 10

# (Zielname, Quelldatei, Markierung oder None, Ausschnitt oder None)
BILDER = [
    ("modul-01-daten-abrufen", "modul-01-daten-abrufen",
     (145, 100, 240, 215), (0, 55, 1450, 330)),

    ("modul-02-transformieren", "modul-01-daten-abrufen",
     (352, 108, 590, 140), (0, 55, 1450, 330)),

    ("modul-03-karte", "modul-01-daten-abrufen",
     (1553, 528, 1597, 570), (1370, 240, 1660, 800)),

    ("modul-04-datenschnitt", "modul-04-datenschnitt",
     (60, 468, 265, 625), (0, 250, 1340, 880)),

    ("modul-05-aggregation", "modul-05-aggregation",
     (1638, 508, 1912, 550), (1330, 300, 1920, 900)),

    ("modul-06-export", "modul-06-export",
     (370, 315, 650, 365), (0, 55, 700, 400)),

    # Vorschaubild: Stand NACH Modul 4, ohne Markierung. Bewusst nicht der
    # Endstand - sonst nimmt es Modul 5 die Wirkung.
    ("vorschau-nach-modul-4", "modul-01-daten-abrufen",
     None, (60, 245, 1340, 1010)),
]


def bearbeiten(ziel: str, quelle: str, markierung, ausschnitt) -> str:
    pfad = ROH / f"{quelle}.png"
    if not pfad.exists():
        return f"FEHLT: {pfad.name}"

    bild = Image.open(pfad).convert("RGB")

    if markierung:
        zeichner = ImageDraw.Draw(bild)
        # Zweiter, hellerer Rahmen aussenrum - so bleibt die Markierung auch
        # auf dunklem Untergrund sichtbar.
        x0, y0, x1, y1 = markierung
        zeichner.rounded_rectangle(
            (x0 - 2, y0 - 2, x1 + 2, y1 + 2), radius=RADIUS + 2,
            outline=(255, 255, 255), width=2,
        )
        zeichner.rounded_rectangle(
            markierung, radius=RADIUS, outline=ROT, width=RAHMENBREITE,
        )

    if ausschnitt:
        bild = bild.crop(ausschnitt)

    ZIEL.mkdir(parents=True, exist_ok=True)
    ausgabe = ZIEL / f"{ziel}.png"
    bild.save(ausgabe, optimize=True)
    kb = ausgabe.stat().st_size // 1024
    return f"{ausgabe.name:32} {bild.width}x{bild.height}  {kb} KB"


def main() -> int:
    if not ROH.exists():
        print(f"Keine Rohbilder gefunden: {ROH}", file=sys.stderr)
        return 1
    for eintrag in BILDER:
        print("  " + bearbeiten(*eintrag))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
