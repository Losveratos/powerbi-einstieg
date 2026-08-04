#!/usr/bin/env python3
"""Erzeugt die simulierte CSV für einen Case.

    python generator/generate.py business

Ein Generator, ein Parametersatz je Case (generator/cases/<case>.yaml).
Deterministisch: gleicher Seed -> byteidentische Datei. Die Kontrollzahlen in
den Anleitungstexten hängen daran, also Seed und Zeilenzahl nie ändern.

Die CSV ist absichtlich schmutzig — jeder Fehler ist eine Lektion in Modul 2.
"""

from __future__ import annotations

import argparse
import random
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

WURZEL = Path(__file__).resolve().parent.parent


def waehle(rnd: random.Random, elemente: list[tuple[str, float]]) -> str:
    """Gewichtete Auswahl. Eigene Implementierung statt random.choices,
    damit die Zufallsfolge über Python-Versionen hinweg stabil bleibt."""
    summe = sum(gewicht for _, gewicht in elemente)
    treffer = rnd.random() * summe
    laufend = 0.0
    for name, gewicht in elemente:
        laufend += gewicht
        if treffer < laufend:
            return name
    return elemente[-1][0]


def begrenzen(wert: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, wert))


def zeilen_bauen(cfg: dict) -> list[dict]:
    rnd = random.Random(cfg["seed"])

    von = date.fromisoformat(str(cfg["zeitraum"]["von"]))
    bis = date.fromisoformat(str(cfg["zeitraum"]["bis"]))
    tage = (bis - von).days + 1

    regionen = list(cfg["regionen"].items())
    gruppen = [(name, p["gewicht"]) for name, p in cfg["produktgruppen"].items()]

    umsatz_cfg = cfg["umsatz"]
    marge_cfg = cfg["marge"]
    signal = marge_cfg["signal"]

    zeilen: list[dict] = []
    for _ in range(cfg["zeilen"]):
        # Reihenfolge der Zufallsaufrufe ist Teil des Vertrags — nicht umstellen.
        tag = von + timedelta(days=rnd.randrange(tage))
        region = waehle(rnd, regionen)
        gruppe = waehle(rnd, gruppen)
        gruppe_cfg = cfg["produktgruppen"][gruppe]
        produkt = gruppe_cfg["produkte"][rnd.randrange(len(gruppe_cfg["produkte"]))]

        roh = rnd.lognormvariate(umsatz_cfg["log_mittel"], umsatz_cfg["log_streuung"])
        umsatz = max(umsatz_cfg["min"], roh * gruppe_cfg["preisfaktor"])

        marge = marge_cfg["basis"] + gruppe_cfg["margenoffset"]
        if region == signal["region"] and tag.month >= signal["ab_monat"]:
            marge += signal["delta"]
        marge += rnd.gauss(0.0, marge_cfg["streuung"])
        marge = begrenzen(marge, marge_cfg["min"], marge_cfg["max"])

        zeilen.append(
            {
                "Auftragsdatum": tag.isoformat(),
                "Region": region,
                "Produktgruppe": gruppe,
                "Produkt": produkt,
                "Umsatz": f"{umsatz:.2f}",
                "Marge": f"{marge:.2f}",
                "_tag": tag,
            }
        )

    # Ein Systemexport kommt nach Datum sortiert — sieht echt aus und ändert
    # an den Kontrollzahlen nichts.
    zeilen.sort(key=lambda z: z["_tag"])

    # Fehler einstreuen: erst jetzt, damit die Sortierung sauber bleibt.
    fehler = cfg["fehler"]
    for zeile in zeilen:
        if rnd.random() < fehler["region_leerzeichen_anteil"]:
            zeile["Region"] = zeile["Region"] + " "
        if rnd.random() < fehler["gruppe_kleinschreibung_anteil"]:
            zeile["Produktgruppe"] = zeile["Produktgruppe"].lower()

    return zeilen


def schreiben(cfg: dict, zeilen: list[dict], ziel: Path) -> None:
    spalten = ["Auftragsdatum", "Region", "Produktgruppe", "Produkt", "Umsatz", "Marge"]
    fehler = cfg["fehler"]

    ausgabe: list[str] = [fehler["kopfzeilen_muell"], ",".join(spalten)]
    daten = [",".join(z[s] for s in spalten) for z in zeilen]

    for feld in daten:
        if '"' in feld or feld.count(",") != len(spalten) - 1:
            raise ValueError(f"Trennzeichen-Konflikt in Zeile: {feld!r}")

    # Leere Zeilen verteilt im Datenbereich (nie ganz am Anfang oder Ende).
    rnd = random.Random(cfg["seed"] + 1)
    positionen = sorted(
        rnd.sample(range(10, len(daten) - 10), fehler["leere_zeilen"]), reverse=True
    )
    for pos in positionen:
        daten.insert(pos, "")

    ausgabe.extend(daten)

    ziel.parent.mkdir(parents=True, exist_ok=True)
    with open(ziel, "w", encoding="utf-8-sig", newline="") as f:
        f.write("\r\n".join(ausgabe) + "\r\n")

    print(f"geschrieben: {ziel}")
    print(f"  Datenzeilen:    {len(zeilen)}")
    print(f"  Leerzeilen:     {fehler['leere_zeilen']} (Positionen {sorted(positionen)})")
    print(f"  Zeilen gesamt:  {len(ausgabe)}  (inkl. Müllzeile + Kopfzeile)")


def main() -> int:
    parser = argparse.ArgumentParser(description="CSV-Generator für den Einsteiger-Pfad")
    parser.add_argument("case", nargs="?", default="business")
    args = parser.parse_args()

    cfg_pfad = WURZEL / "generator" / "cases" / f"{args.case}.yaml"
    if not cfg_pfad.exists():
        print(f"Kein Parametersatz gefunden: {cfg_pfad}", file=sys.stderr)
        return 1

    cfg = yaml.safe_load(cfg_pfad.read_text(encoding="utf-8"))
    zeilen = zeilen_bauen(cfg)
    schreiben(cfg, zeilen, WURZEL / cfg["datei"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
