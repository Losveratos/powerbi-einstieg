#!/usr/bin/env python3
"""Erzeugt das PBIP-Projekt fuer den Checkpoint nach Modul 2.

    python generator/build_pbip.py business

Schreibt nach powerbi/geputzt/ ein vollstaendiges Power-BI-Projekt im
PBIP/TMDL-Format: Datenquelle, die acht Power-Query-Handgriffe aus Modul 2
und die fertigen Spaltentypen - also genau den Stand, den ein Lernender nach
Modul 2 haben muss.

Damit muss der Checkpoint nicht von Hand durchgeklickt werden. In Power BI
Desktop oeffnen, aktualisieren, pruefen, dann als .pbix speichern.

Alle GUIDs sind aus dem Case-Namen abgeleitet (uuid5) - zweimal laufen lassen
erzeugt dieselbe Datei, das haelt Git-Diffs sauber.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path

import yaml

WURZEL = Path(__file__).resolve().parent.parent
NAMESPACE = uuid.UUID("6f9619ff-8b86-d011-b42d-00c04fc964ff")

# Die Spalten in der Reihenfolge der CSV, mit den Typen, die nach Modul 2
# eingestellt sein muessen. summarizeBy fuer Marge bleibt bewusst auf 'sum' -
# genau daraus entsteht in Modul 5 die absurde Zahl.
SPALTEN = [
    {"name": "Auftragsdatum", "typ": "dateTime", "summarizeBy": "none",
     "formatString": "Long Date"},
    {"name": "Region", "typ": "string", "summarizeBy": "none"},
    {"name": "Produktgruppe", "typ": "string", "summarizeBy": "none"},
    {"name": "Produkt", "typ": "string", "summarizeBy": "none"},
    {"name": "Umsatz", "typ": "double", "summarizeBy": "sum"},
    {"name": "Marge", "typ": "double", "summarizeBy": "sum"},
]


def guid(*teile: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "/".join(teile)))


def m_abfrage(csv_url: str, tabelle: str) -> str:
    """Die acht Handgriffe aus Modul 2 als Power-Query-Ausdruck.

    Die Schrittnamen sind exakt die, die Power BI Desktop auf einem deutschen
    System vergibt - der Lernende soll in der Checkpoint-Datei dieselbe
    Schrittliste sehen wie in seiner eigenen.
    """
    spalten_text = ", ".join(f'{{"Column{i}", type text}}' for i in range(1, 7))
    return f'''let
    Quelle = Csv.Document(Web.Contents("{csv_url}"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Geänderter Typ" = Table.TransformColumnTypes(Quelle,{{{spalten_text}}}),
    #"Entfernte oberste Zeilen" = Table.Skip(#"Geänderter Typ",1),
    #"Höher gestufte Header" = Table.PromoteHeaders(#"Entfernte oberste Zeilen", [PromoteAllScalars=true]),
    #"Entfernte leere Zeilen" = Table.SelectRows(#"Höher gestufte Header", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {{"", null}}))),
    #"Gekürzter Text" = Table.TransformColumns(#"Entfernte leere Zeilen",{{{{"Region", Text.Trim, type text}}}}),
    #"Großgeschrieben in jedem Wort" = Table.TransformColumns(#"Gekürzter Text",{{{{"Produktgruppe", Text.Proper, type text}}}}),
    #"Geänderter Typ1" = Table.TransformColumnTypes(#"Großgeschrieben in jedem Wort",{{{{"Auftragsdatum", type date}}}}),
    #"Geänderter Typ mit Gebietsschema" = Table.TransformColumnTypes(#"Geänderter Typ1", {{{{"Umsatz", type number}}}}, "en-US"),
    #"Geänderter Typ mit Gebietsschema1" = Table.TransformColumnTypes(#"Geänderter Typ mit Gebietsschema", {{{{"Marge", type number}}}}, "en-US")
in
    #"Geänderter Typ mit Gebietsschema1"'''


def tabelle_tmdl(tabelle: str, csv_url: str) -> str:
    zeilen = [f"table {tabelle}", f"\tlineageTag: {guid(tabelle)}", ""]

    for spalte in SPALTEN:
        zeilen.append(f"\tcolumn {spalte['name']}")
        zeilen.append(f"\t\tdataType: {spalte['typ']}")
        if "formatString" in spalte:
            zeilen.append(f"\t\tformatString: {spalte['formatString']}")
        zeilen.append(f"\t\tlineageTag: {guid(tabelle, spalte['name'])}")
        zeilen.append(f"\t\tsummarizeBy: {spalte['summarizeBy']}")
        zeilen.append(f"\t\tsourceColumn: {spalte['name']}")
        zeilen.append("")
        zeilen.append("\t\tannotation SummarizationSetBy = Automatic")
        zeilen.append("")

    zeilen.append(f"\tpartition {tabelle} = m")
    zeilen.append("\t\tmode: import")
    zeilen.append("\t\tsource =")
    for zeile in m_abfrage(csv_url, tabelle).splitlines():
        zeilen.append(f"\t\t\t\t{zeile}")
    zeilen.append("")
    zeilen.append("\tannotation PBI_ResultType = Table")
    zeilen.append("")
    return "\n".join(zeilen)


def modell_tmdl(tabelle: str) -> str:
    # __PBI_TimeIntelligenceEnabled = 1: Power BI legt fuer die Datumsspalte
    # automatisch eine Hierarchie Jahr/Quartal/Monat/Tag an. Modul 3 baut
    # darauf auf ("klick bei Jahr, Quartal und Tag auf das X").
    return f"""model Model
\tculture: de-DE
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: de-DE
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 1

annotation PBI_ProTooling = ["DevMode"]

ref table {tabelle}

ref cultureInfo de-DE
"""


def platform(typ: str, name: str) -> str:
    return json.dumps(
        {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/"
                       "gitIntegration/platformProperties/2.0.0/schema.json",
            "metadata": {"type": typ, "displayName": name},
            "config": {"version": "2.0", "logicalId": guid(typ, name)},
        },
        indent=2,
        ensure_ascii=False,
    )


def schreiben(pfad: Path, inhalt: str) -> None:
    """PBIP-Dateien muessen UTF-8 OHNE BOM sein, sonst brechen die Parser."""
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(inhalt, encoding="utf-8", newline="\r\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="PBIP-Checkpoint erzeugen")
    parser.add_argument("case", nargs="?", default="business")
    args = parser.parse_args()

    werte_pfad = WURZEL / "content" / "werte" / f"{args.case}.yaml"
    if not werte_pfad.exists():
        print(f"Kontrollzahlen fehlen - erst verify.py laufen lassen: {werte_pfad}",
              file=sys.stderr)
        return 1
    werte = yaml.safe_load(werte_pfad.read_text(encoding="utf-8"))

    tabelle = werte["tabellen_name"]
    csv_url = werte["csv_url"]
    projekt = "geputzt"
    anzeigename = f"{werte['titel']} - nach Modul 2"

    wurzel = WURZEL / "powerbi" / projekt
    sm = wurzel / f"{projekt}.SemanticModel"
    rp = wurzel / f"{projekt}.Report"

    # --- Projektdatei -------------------------------------------------------
    schreiben(wurzel / f"{projekt}.pbip", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/"
                   "pbipProperties/1.0.0/schema.json",
        "version": "1.0",
        "artifacts": [{"report": {"path": f"{projekt}.Report"}}],
        "settings": {"enableAutoRecovery": True},
    }, indent=2))

    # --- Semantisches Modell ------------------------------------------------
    schreiben(sm / ".platform", platform("SemanticModel", anzeigename))
    schreiben(sm / "definition.pbism", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/"
                   "semanticModel/definitionProperties/1.0.0/schema.json",
        "version": "4.2",
        "settings": {},
    }, indent=2))
    schreiben(sm / "definition" / "database.tmdl", "database\n\tcompatibilityLevel: 1606\n")
    schreiben(sm / "definition" / "model.tmdl", modell_tmdl(tabelle))
    schreiben(sm / "definition" / "cultures" / "de-DE.tmdl", "cultureInfo de-DE\n")
    schreiben(sm / "definition" / "tables" / f"{tabelle}.tmdl",
              tabelle_tmdl(tabelle, csv_url))

    # --- Bericht (eine leere Seite - Visuals kommen erst ab Modul 3) --------
    schreiben(rp / ".platform", platform("Report", anzeigename))
    schreiben(rp / "definition.pbir", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/"
                   "report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byPath": {"path": f"../{projekt}.SemanticModel"}},
    }, indent=2))
    schreiben(rp / "definition" / "version.json", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/"
                   "report/definition/versionMetadata/1.0.0/schema.json",
        "version": "2.0.0",
    }, indent=2))
    # Das Basis-Theme muss als Datei danebenliegen und in resourcePackages
    # deklariert sein. Fehlt es, laedt Power BI Desktop den Bericht nicht
    # ("Fehler beim Laden des Berichts") - ohne verwertbare Fehlermeldung.
    theme = "Fluent2-CY26SU07"
    schreiben(rp / "StaticResources" / "SharedResources" / "BaseThemes" / f"{theme}.json",
              (WURZEL / "generator" / "assets" / f"{theme}.json").read_text(encoding="utf-8"))
    schreiben(rp / "definition" / "report.json", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/"
                   "report/definition/report/3.3.0/schema.json",
        "themeCollection": {
            "baseTheme": {
                "name": theme,
                "reportVersionAtImport": {
                    "visual": "2.11.0", "report": "3.4.0", "page": "2.3.1",
                },
                "type": "SharedResources",
            }
        },
        "resourcePackages": [{
            "name": "SharedResources",
            "type": "SharedResources",
            "items": [{
                "name": theme,
                "path": f"BaseThemes/{theme}.json",
                "type": "BaseTheme",
            }],
        }],
        "settings": {
            "useStylableVisualContainerHeader": True,
            "defaultDrillFilterOtherVisuals": True,
            "allowChangeFilterTypes": True,
            "useEnhancedTooltips": True,
            "useDefaultAggregateDisplayName": True,
        },
    }, indent=2))
    schreiben(rp / "definition" / "pages" / "pages.json", json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/"
                   "report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": ["Seite1"],
        "activePageName": "Seite1",
    }, indent=2))
    schreiben(rp / "definition" / "pages" / "Seite1" / "page.json",
              json.dumps({
                  "$schema": "https://developer.microsoft.com/json-schemas/fabric/"
                             "item/report/definition/page/2.1.0/schema.json",
                  "name": "Seite1",
                  "displayName": "Seite 1",
                  "displayOption": "FitToPage",
                  "height": 1080,
                  "width": 1920,
              }, indent=2, ensure_ascii=False))

    print(f"geschrieben: {wurzel.relative_to(WURZEL)}")
    print(f"  Tabelle:  {tabelle} ({len(SPALTEN)} Spalten)")
    print(f"  Quelle:   {csv_url}")
    print("\nNaechster Schritt: In Power BI Desktop oeffnen "
          f"({projekt}.pbip), aktualisieren, pruefen, als .pbix speichern.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
