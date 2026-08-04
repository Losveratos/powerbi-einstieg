#!/usr/bin/env python3
"""Errechnet die Kontrollzahlen aus der fertigen CSV.

    python generator/verify.py business

Liest die CSV genau so, wie Power Query sie nach Modul 2 sieht (Muellzeile weg,
Kopfzeile hochgestuft, leere Zeilen weg, Region gekuerzt, Produktgruppe
normalisiert, Umsatz/Marge als Dezimalzahl) und schreibt das Ergebnis nach
content/werte/<case>.yaml.

Kontrollzahlen werden NIE von Hand in Texte geschrieben - die Templates
benutzen ausschliesslich die Platzhalter aus dieser Datei.
"""

from __future__ import annotations

import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import yaml

WURZEL = Path(__file__).resolve().parent.parent

MONATE = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
]


def de(wert: float, dezimalstellen: int = 0) -> str:
    """Deutsche Zahlenformatierung: Punkt als Tausender, Komma als Dezimal.
    Kaufmaennisch gerundet - so rundet auch Power BI."""
    quant = Decimal(1).scaleb(-dezimalstellen)
    gerundet = Decimal(repr(wert)).quantize(quant, rounding=ROUND_HALF_UP)
    englisch = f"{gerundet:,.{dezimalstellen}f}"
    ganzzahl, _, nachkomma = englisch.partition(".")
    ganzzahl = ganzzahl.replace(",", ".")
    return ganzzahl + ("," + nachkomma if nachkomma else "")


def csv_lesen(pfad: Path) -> tuple[list[dict], int, int]:
    """Gibt (bereinigte Zeilen, Rohzeilen, Spaltenzahl) zurueck."""
    text = pfad.read_text(encoding="utf-8-sig")
    roh = text.splitlines()
    # So viele Zeilen zeigt Power BI nach Modul 1 an (Muellzeile, Kopfzeile und
    # Leerzeilen sind da noch Datenzeilen).
    zeilen_roh = len(roh)

    ohne_muell = roh[1:]                       # Handgriff 1: erste Zeile entfernen
    kopf = ohne_muell[0].split(",")            # Handgriff 2: Kopfzeile hochstufen
    rest = [z for z in ohne_muell[1:] if z.strip() != ""]   # Handgriff 3

    datensaetze = []
    for zeile in rest:
        werte = zeile.split(",")
        satz = dict(zip(kopf, werte))
        satz["Region"] = satz["Region"].strip()                 # Handgriff 4
        satz["Produktgruppe"] = satz["Produktgruppe"].title()   # Handgriff 5
        satz["Monat"] = int(satz["Auftragsdatum"][5:7])         # Handgriff 6
        satz["Umsatz"] = float(satz["Umsatz"])                  # Handgriff 7
        satz["Marge"] = float(satz["Marge"])
        datensaetze.append(satz)

    return datensaetze, zeilen_roh, len(kopf)


def pruefen(daten: list[dict], cfg: dict, gesamtwert: float) -> list[str]:
    """Plausibilitaetspruefungen. Gibt eine Liste von Warnungen zurueck."""
    warnungen = []

    if round(gesamtwert) % 1000 == 0:
        warnungen.append(
            "gesamtwert ist auf Tausender gerundet - als Kontrollzahl zu glatt."
        )

    gruppen = {d["Produktgruppe"] for d in daten}
    if len(gruppen) != len(cfg["produktgruppen"]):
        warnungen.append(
            f"{len(gruppen)} Produktgruppen nach Normalisierung, "
            f"erwartet {len(cfg['produktgruppen'])}: {sorted(gruppen)}"
        )

    regionen = {d["Region"] for d in daten}
    if len(regionen) != len(cfg["regionen"]):
        warnungen.append(
            f"{len(regionen)} Regionen nach dem Kuerzen, "
            f"erwartet {len(cfg['regionen'])}: {sorted(regionen)}"
        )

    if len(daten) != cfg["zeilen"]:
        warnungen.append(f"{len(daten)} Datenzeilen, erwartet {cfg['zeilen']}.")

    signal = cfg["marge"]["signal"]
    vorher = mittel([d["Marge"] for d in daten
                     if d["Region"] == signal["region"] and d["Monat"] < signal["ab_monat"]])
    nachher = mittel([d["Marge"] for d in daten
                      if d["Region"] == signal["region"] and d["Monat"] >= signal["ab_monat"]])
    if vorher - nachher < 0.07:
        warnungen.append(
            f"Signal zu schwach: {signal['region']} faellt nur von {vorher:.3f} "
            f"auf {nachher:.3f} - im Diagramm kaum zu sehen."
        )

    return warnungen


def mittel(werte: list[float]) -> float:
    return sum(werte) / len(werte) if werte else 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description="Kontrollzahlen aus der CSV errechnen")
    parser.add_argument("case", nargs="?", default="business")
    args = parser.parse_args()

    cfg = yaml.safe_load(
        (WURZEL / "generator" / "cases" / f"{args.case}.yaml").read_text(encoding="utf-8")
    )
    csv_pfad = WURZEL / cfg["datei"]
    if not csv_pfad.exists():
        print(f"CSV fehlt - erst generate.py laufen lassen: {csv_pfad}", file=sys.stderr)
        return 1

    daten, zeilen_roh, spalten = csv_lesen(csv_pfad)

    signal = cfg["marge"]["signal"]
    signal_region = signal["region"]
    ab_monat = signal["ab_monat"]

    gesamtwert = sum(d["Umsatz"] for d in daten)
    margen = [d["Marge"] for d in daten]
    nord_umsatz = sum(d["Umsatz"] for d in daten if d["Region"] == signal_region)

    umsatz_je_region: dict[str, float] = {}
    for d in daten:
        umsatz_je_region[d["Region"]] = umsatz_je_region.get(d["Region"], 0.0) + d["Umsatz"]
    groesste_region = max(umsatz_je_region, key=lambda r: umsatz_je_region[r])

    signal_vorher = mittel(
        [d["Marge"] for d in daten if d["Region"] == signal_region and d["Monat"] < ab_monat]
    )
    signal_nachher = mittel(
        [d["Marge"] for d in daten if d["Region"] == signal_region and d["Monat"] >= ab_monat]
    )
    signal_andere = mittel([d["Marge"] for d in daten if d["Region"] != signal_region])

    repo = cfg["repo"]
    csv_url = (
        f"https://raw.githubusercontent.com/{repo['owner']}/{repo['name']}/"
        f"{repo['branch']}/{cfg['datei']}"
    )
    # Checkpoint-Dateien liegen als Release-Assets, nicht im Repo (Binaerdateien).
    # 'latest/download' bleibt stabil, auch wenn ein neues Release kommt.
    release = f"https://github.com/{repo['owner']}/{repo['name']}/releases/latest/download"

    werte = {
        # Herkunft
        "case": cfg["case"],
        "titel": cfg["titel"],
        "emoji": cfg["emoji"],
        "kurz": cfg["kurz"],
        "story": cfg["story"],
        "csv_url": csv_url,
        "datei_name": Path(cfg["datei"]).name,
        "tabellen_name": Path(cfg["datei"]).stem,
        "download_url": f"{release}/{Path(cfg['datei']).name}",
        "checkpoint_geputzt": f"{release}/{cfg['case']}_checkpoint_geputzt.pbix",
        "checkpoint_visuals": f"{release}/{cfg['case']}_checkpoint_visuals.pbix",
        "checkpoint_fertig": f"{release}/{cfg['case']}_fertig.pbix",
        # Modul 1
        "zeilen_roh": de(zeilen_roh),
        # Modul 2
        "zeilen": de(len(daten)),
        "spalten": str(spalten),
        "schritte": str(cfg["schritte"]),
        # Modul 3
        "gesamtwert": de(gesamtwert),
        "groesste_region": groesste_region,
        # Modul 4
        "filterwert": de(nord_umsatz),
        "filterregion": signal_region,
        # Modul 5
        "falsche_zahl": de(sum(margen), 2),
        "richtige_zahl": de(mittel(margen) * 100, 1) + " %",
        "signal_region": signal_region,
        "signal_monat_name": MONATE[ab_monat - 1],
        "signal_vorher": de(signal_vorher * 100, 0) + " %",
        "signal_nachher": de(signal_nachher * 100, 0) + " %",
        "signal_andere": de(signal_andere * 100, 0) + " %",
    }

    ziel = WURZEL / "content" / "werte" / f"{args.case}.yaml"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    kopf = (
        "# ERZEUGT VON generator/verify.py - NICHT VON HAND AENDERN.\n"
        f"# Quelle: {cfg['datei']} (Seed {cfg['seed']})\n"
    )
    ziel.write_text(
        kopf + yaml.safe_dump(werte, allow_unicode=True, sort_keys=True),
        encoding="utf-8",
    )

    print(f"geschrieben: {ziel}\n")
    for schluessel in sorted(werte):
        print(f"  {schluessel:20} {werte[schluessel]}")

    warnungen = pruefen(daten, cfg, gesamtwert)
    if warnungen:
        print("\nWARNUNGEN:")
        for w in warnungen:
            print(f"  ! {w}")
        return 2

    print("\nAlle Plausibilitaetspruefungen bestanden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
