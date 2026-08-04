# Modul 3 · Erste Antworten

*Etwa 25 Minuten*

## Ziel dieses Moduls

Drei Bilder auf der Seite, die drei Fragen beantworten: wie viel insgesamt, wer,
und wann.

## So geht's

Klick links am Bildschirmrand auf das oberste der drei Symbole: die
**Berichtsansicht**. Du siehst eine leere weiße Seite. Rechts stehen zwei
Bereiche: **Visualisierungen** (die Symbolsammlung) und **Daten** (deine
Tabelle).

### Bild 1 — die große Zahl: Wie viel insgesamt?

1. Klick auf eine leere Stelle der weißen Seite.
2. Klick im Bereich **Visualisierungen** auf das Symbol **Karte** — es sieht aus
   wie ein Kästchen mit den Ziffern **123** darin.

<!-- BILD: modul-03-karte | Der Bereich „Visualisierungen“ — markiert ist das Symbol „Karte“. -->

   (Achtung: Es gibt auch ein Symbol mit einer Weltkugel, das ebenfalls „Karte"
   heißt. Das ist eine Landkarte — nimm das mit den Ziffern.)
3. Auf der Seite erscheint ein leeres graues Kästchen.
4. Klapp im Bereich **Daten** die Tabelle **{{tabellen_name}}** auf und setz das
   Häkchen bei **Umsatz**. In dem Kästchen erscheint eine Zahl.
5. Die Zahl steht dort abgekürzt: **{{gesamtwert_kurz}}** Power BI kürzt große
   Zahlen von sich aus — „Mio." heißt Millionen. Das ist so in Ordnung und
   bleibt auch so; für die Frage „wie viel insgesamt?" reicht diese Genauigkeit
   völlig.
6. Schieb das Kästchen nach links oben und zieh es an einer Ecke etwas größer,
   damit die Zahl gut lesbar ist.

### Bild 2 — die Balken: Wer?

7. Klick auf eine leere Stelle der Seite.
8. Klick im Bereich **Visualisierungen** auf **Gestapeltes Balkendiagramm**
   (waagerechte Balken).
9. Setz im Bereich **Daten** die Häkchen bei **Region** und bei **Umsatz**.
   Power BI legt Region auf die Y-Achse und Umsatz auf die X-Achse.
10. Power BI sortiert die Balken von sich aus nach Größe — der längste steht
    oben. Sollte das bei dir anders sein: Fahr mit der Maus über das Diagramm,
    klick oben rechts auf die **drei Punkte (…)** → **Achse sortieren** →
    **Umsatz**, und noch einmal **… → Achse sortieren → Absteigend sortieren**.

### Bild 3 — die Linie: Wann?

11. Klick auf eine leere Stelle der Seite.
12. Klick auf **Liniendiagramm**.
13. Setz die Häkchen bei **Auftragsdatum** und **Umsatz**.
14. Power BI zeigt jetzt nur einen einzigen Punkt — es fasst alles zum Jahr
    zusammen. Schau rechts unter **Visualisierungen** in das Feld **X-Achse**:
    Dort steht `Auftragsdatum` mit vier Einträgen darunter — **Jahr, Quartal,
    Monat, Tag**. Klick bei **Jahr**, **Quartal** und **Tag** jeweils auf das
    **X**. Übrig bleibt **Monat** — und die Linie zeigt zwölf Punkte, Januar bis
    Dezember.
15. Schieb die drei Bilder so, dass sie sich nicht überlappen. Ordentlich ist:
    die Karte oben links, das Balkendiagramm rechts daneben, die Linie darunter
    über die ganze Breite.

## 📖 Neues Wort

**Dimension und Kennzahl.** Eine **Kennzahl** ist das, was du misst — hier der
Umsatz. Eine **Dimension** ist das, wonach du sie aufteilst — hier die Region
oder der Monat. Jedes Diagramm, das du je bauen wirst, ist eine Kennzahl,
aufgeteilt nach einer Dimension.

## ✅ Kontrollpunkt

> Die Karte zeigt: **{{gesamtwert_kurz}}**
> Im Balkendiagramm steht **{{groesste_region}}** ganz oben.
>
> Steht dort stattdessen **{{gesamtwert_falsch}}** → Dann wurde in Modul 2 der Umsatz ohne
> **Gebietsschema Englisch (USA)** umgewandelt. Power BI hat den Punkt als
> Tausendertrennzeichen gelesen, dadurch sind alle Beträge hundertmal zu groß.
> Geh zurück zu Modul 2, Handgriff 7.
>
> Steht dort eine viel kleinere Zahl oder „(Leer)"? → Dann ist statt der Summe
> die Anzahl eingestellt. Klick rechts im Feld **Wert** auf den kleinen Pfeil
> neben **Umsatz** und wähle **Summe**.
>
> Willst du es ganz genau wissen: Die Summe auf den Euro beträgt
> **{{gesamtwert}}**. Sehen kannst du sie, indem du in der Tabellenansicht
> die Spalte **Umsatz** anklickst und unter **Spaltentools** die
> **Dezimalstellen** auf `0` stellst — nötig ist das aber nicht.
>
> Oder: [Checkpoint-Datei laden]({{checkpoint_geputzt}}) und ab Schritt 1 dieses
> Moduls neu anfangen.

## Weiter

→ [Modul 4 · Filtern](04-filtern.md)
