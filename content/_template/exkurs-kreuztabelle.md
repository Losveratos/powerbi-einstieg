# Exkurs · Warum deine Excel-Tabelle nicht passt

*Etwa 10 Minuten · Optional. Gehört nicht zum Pfad — du kannst ihn überspringen.*

Wenn du nach diesem Pfad eine eigene Excel-Datei in Power BI lädst, passiert oft
etwas Verwirrendes: Es geht nicht. Dieser Exkurs erklärt in einem Satz, warum.

## Der Kernsatz

**Menschen lesen Kreuztabellen, Maschinen lesen lange Tabellen.**

Eine Kreuztabelle sieht so aus — und für ein Auge ist sie großartig:

| Region | Januar | Februar | März |
|---|---|---|---|
| Nord | 12.400 | 11.900 | 13.100 |
| Süd | 14.200 | 15.000 | 14.800 |

Das Problem: Der Monat steht hier nicht *in* der Tabelle, sondern *über* ihr —
als Spaltenüberschrift. Power BI kann aber nur mit dem arbeiten, was in Zeilen
und Spalten steht. Es sieht drei Kennzahlen namens „Januar", „Februar", „März"
und keine Dimension „Monat". Ein Liniendiagramm über die Zeit ist damit
unmöglich.

Dieselben Daten als lange Tabelle:

| Region | Monat | Umsatz |
|---|---|---|
| Nord | Januar | 12.400 |
| Nord | Februar | 11.900 |
| Nord | März | 13.100 |
| Süd | Januar | 14.200 |
| Süd | Februar | 15.000 |
| Süd | März | 14.800 |

Unhandlich zu lesen, aber jetzt gibt es eine Spalte **Monat** — eine Dimension,
wie du sie in Modul 3 benutzt hast. Genau so wollen es alle Auswertungswerkzeuge.

## Der Handgriff dazu heißt Entpivotieren

Du brauchst das nicht auswendig zu lernen, nur wiedererkennen:

1. Datei in Power BI laden, **Start → Daten transformieren**.
2. Die Spalte anklicken, die *bleiben* soll — hier **Region**.
3. **Transformieren → Spalten entpivotieren → Andere Spalten entpivotieren**.

Power BI macht aus den Monatsspalten zwei neue Spalten: **Attribut** (der
Monatsname) und **Wert** (die Zahl). Die kannst du dann umbenennen, und die
Tabelle ist lang statt breit.

## Wenn du weitermachen willst

Dieser Pfad hatte genau **eine** Tabelle. Echte Auswertungen haben mehrere —
Aufträge, Kunden, Produkte, Kalender — die über gemeinsame Schlüssel verbunden
werden. Diese Verbindungen heißen **Beziehungen**, und die übliche Anordnung
dafür heißt **Sternschema**. Das ist der nächste Schritt, wenn dir eine Tabelle
nicht mehr reicht.

## Zurück

→ [Modul 6 · Fertig machen](06-fertig-machen.md)
