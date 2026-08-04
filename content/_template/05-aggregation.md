# Modul 5 · Nicht jede Zahl darf man addieren

*Etwa 20 Minuten · Hier kommt die Antwort auf die Eingangsfrage.*

## Ziel dieses Moduls

Du siehst, was passiert, wenn Power BI automatisch summiert — und findest damit
die Auffälligkeit in den Daten.

## So geht's

### Erst der Fehler

1. Klick auf eine leere Stelle der Seite.
2. Klick auf das Symbol **Karte** (das mit den Ziffern 123) — wie in Modul 3.
3. Setz im Bereich **Daten** das Häkchen bei **Marge**.
4. Schau dir die Zahl an.

   Bei dir sollte jetzt etwas Absurdes stehen — rund **{{falsche_zahl}}**.
   Wenn ja: perfekt, genau das soll passieren.

   Eine Marge von {{falsche_zahl}} gibt es nicht. Was Power BI hier gemacht hat:
   Es hat alle {{zeilen}} Margen **addiert**. Das tut es bei jeder Zahlenspalte
   automatisch, weil das bei Umsätzen ja auch richtig ist. Bei einer Marge ist
   es Unsinn — 30 % plus 30 % sind nicht 60 %.

### Dann die Reparatur

5. Schau rechts unter **Visualisierungen** in das Feld **Felder**. Dort steht
   `Summe von Marge`. Klick auf den kleinen **Pfeil nach unten** direkt daneben.
6. Es klappt eine Liste auf: **Summe · Durchschnitt · Minimum · Maximum · Anzahl**
   und weitere. Wähle **Durchschnitt**.
7. Die Zahl ist jetzt klein, etwa `0,32`. Das stimmt zwar, liest sich aber
   schlecht. Also formatieren wir die Spalte einmal richtig:
   - Klick links am Bildschirmrand auf die **Tabellenansicht** (Gittersymbol).
   - Klick oben auf die Spaltenüberschrift **Marge**.
   - Im Menüband erscheint der Reiter **Spaltentools**. Klick dort im Feld
     **Format** auf das Auswahlfeld und wähle **Prozentsatz**.
   - Stell daneben die **Dezimalstellen** auf **1**.
   - Zurück zur **Berichtsansicht** (oberstes Symbol links).

## ✅ Kontrollpunkt

> Die zweite Karte zeigt jetzt: **{{richtige_zahl}}**.
>
> Steht da etwas anderes? → Häufigste Ursache: Im Feld **Felder** steht noch
> `Summe von Marge` statt `Durchschnitt von Marge`. Prüf Schritt 5 und 6.
>
> Oder: [Checkpoint-Datei laden]({{checkpoint_visuals}}) und ab Schritt 8
> weitermachen.

### Und jetzt die eigentliche Frage: Was fällt auf?

8. Klick auf eine leere Stelle der Seite.
9. Klick auf **Liniendiagramm**.
10. Setz die Häkchen bei **Auftragsdatum** und **Marge**.
11. Reduziere die X-Achse wieder auf den Monat: Klick im Feld **X-Achse** bei
    **Jahr**, **Quartal** und **Tag** jeweils auf das **X**.
12. Stell auch hier die Aggregation um: Klick im Feld **Y-Achse** auf den Pfeil
    neben `Summe von Marge` → **Durchschnitt**.
13. Jetzt der entscheidende Handgriff: Zieh im Bereich **Daten** das Feld
    **Region** mit gedrückter Maustaste in das Feld **Legende** (rechts unter
    *Visualisierungen*). Aus einer Linie werden vier — eine je Region.
14. Schau dir das Bild an. Bis {{signal_monat_name}} laufen alle vier Linien eng
    beieinander bei rund {{signal_vorher}}. Ab {{signal_monat_name}} bricht eine
    Linie nach unten weg und bleibt unten: **{{signal_region}}**, bei rund
    {{signal_nachher}}. Die anderen drei bleiben bei rund {{signal_andere}}.

**Das ist die Antwort auf die Eingangsfrage.** Der Umsatz in {{signal_region}}
ist unauffällig — deshalb wäre es in Modul 3 niemandem aufgefallen. Aber von
jedem Euro Umsatz bleibt in {{signal_region}} seit {{signal_monat_name}}
deutlich weniger übrig.

> **Für Genaue:** Ein einfacher Durchschnitt über alle Aufträge gewichtet jeden
> Auftrag gleich — ein 50-€-Auftrag zählt so viel wie ein 5.000-€-Auftrag.
> Sauber wäre eine nach Umsatz gewichtete Marge. Für „fällt hier etwas auf?"
> reicht der Durchschnitt völlig; die gewichtete Rechnung kommt im Aufbaupfad.

## 📖 Neues Wort

**Aggregation.** Aggregation ist die Entscheidung, wie viele Zeilen zu einer
Zahl zusammengefasst werden: addieren, mitteln, zählen, größten Wert nehmen.
Power BI wählt automatisch „addieren" — das ist eine Annahme, keine Wahrheit.
Bei jeder Kennzahl, die ein Anteil, ein Preis, eine Note oder ein Stand ist,
musst du die Entscheidung selbst treffen.

## Weiter

→ [Modul 6 · Fertig machen](06-fertig-machen.md)
