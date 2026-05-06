# Kommentar (IGNORE)

Viel Inspiration von: https://gist.github.com/pschmidtke/7db969436727a8fd0cec5a7d4448fea7

# AUFGABE

Vergleiche den vorliegenden Änderungsvorschlag mit dem VOLLSTÄNDIGEN Stammgesetz und erstelle einen strukturierten Vorher-Nachher-Vergleich der betroffenen Gesetzestexte ("Synopse").
Das ist Ziel ist, dass ein Mensch die geplante Gesetzesänderung möglichst schnell und einfach nachvollziehen kann.

# DATENQUELLEN

Die folgenden Quellen stellen die offiziellen Quellen im Internet da.

- https://www.gesetze-im-internet.de
- https://recht.bund.de
- https://www.bgbl.de

Regeln:

- Nutze AUSSCHLIESSLICH offizielle Quellen

---

# VORGEHENSWEISE

## SCHRITT 1: Referenzen extrahieren

- Parse den Änderungsvorschlag
- Identifiziere relevante Seiten für die Änderung. Hinweis: Es können mehrere Seiten Prosa vor der eigentlichen Änderung stehen.
- Identifiziere alle ALLE Paragraphen-Nummern (NUR innerhalb relevanter Seiten). Dies können sein:
  - A) Paragraphen, die das Änderungsgesetz im Wortlaut ändert oder
     neu einfügt.
  - B) Paragraphen, die in Anwendbarkeits-Klauseln genannt werden.
     Beispiele: "es gelten die §§ X, Y, Z", "anzuwenden sind die §§ A
     bis B", "außerhalb des [Falls] gelten", "ab dem … sind …",
     "im … gelten …". Solche Klauseln sind ZÜNDSCHALTER — sie
     aktivieren Pflichten, ohne sie auszuschreiben.
  - C) Paragraphen, auf die andere Vorschriften des Stammgesetzes oder
     referenzierter Gesetze zurückverweisen.
- Normalisiere jede Referenz in das Format:
  § X Abs. Y Satz Z Nr. N
- Gebe eine strukturierte Liste der Referenzen aus, bevor du fortfährst

---

## SCHRITT 2: Aktuelles Recht abrufen

- Für jede Referenz:
  - Rufe den aktuell gültigen Gesetzestext ab
  - Speichere den Link zur Quelle für spätere Referenz
  - Verwende NUR erlaubte Quellen
- Stelle sicher:
  - Korrekte Version des Gesetzes
  - Vollständiger Wortlaut wird erfasst

---

## SCHRITT 3: Änderungen anwenden

Für jede Änderungsanweisung:

### 3.1 Operation klassifizieren

- Ersetzen → bestehenden Text ersetzen
- Einfügen → neuen Text an definierter Position hinzufügen
- Löschen → Text entfernen
- Neu nummerieren → Nummerierung konsistent anpassen
- Änderung im Inhaltsverzeichnis -> Nummerierung konsistent anpassen

### 3.2 Transformation anwenden

Ändere das geltende Stammgesetz, welches du zuvor aus den Quellen extrahiert hast wie folgt:

- Wende Änderungen NUR auf die explizit referenzierte Einheit an
- Bewahre allen unveränderten Text EXAKT
- Erhalte die rechtliche Struktur und Formatierung

---

## SCHRITT 4: Validierung

Bevor du die Ausgabe generierst, prüfe:

- Alle Referenzen wurden verarbeitet
- Keine unbeabsichtigten Abschnitte wurden geändert
- Rechtliche Struktur ist intakt
- Nummerierung ist konsistent (falls Neu-Nummerierung erfolgte)

Falls Unsicherheit besteht:

- Liste Annahmen explizit auf
- Fahre dann fort

---

## SCHRITT 5: Ausgabe erstellen

### 5.1 AUSGABEFORMAT (STRIKT)

- Alle Antworten MÜSSEN auf Deutsch sein. Verwende offiziellen Ton.
- Gib die Antwort als Markdown strukturiert zurück

- Strukturiere die Antwort wie folgt. Halte dich STRIKT an diese Struktur.
  - # Titel: Synopse
  
  - ## Untertitel: [Titel der Gesetzesänderung]
  
  - [Synopsentabelle (Format siehe unten)]
  
  - ## Untertitel: "Weiterführende Informationen"
    - Information über relevante Seiten im Änderungsvorschlag
    - Information über welche Gesetze relevant sind
    - Online-Quellen, die für die Analyse verwendet wurden: Liste der vollständigen Links
    - Falls Annahmen getroffen wurden, hier auflisten

### 5.2 Format der Synopse

- Struktur der Tabelle für die Synopse wie folgt:

| Abschnitt | Alte Fassung  | Neue Fassung | Änderungstyp |
|-----------|---------------|--------------|--------------|

- Regeln:
  - Eine Zeile pro geänderter Einheit
  - Verwende vollständigen Gesetzeswortlaut (keine Zusammenfassungen)
  - Halte die Formatierung konsistent
  - Kennzeichne den Änderungstyp klar gemäß obiger Nomenklatur (Ersetzen, Einfügen, etc)
  - Hebe Unterschiede inline hervor (**fett für Ergänzungen**, ~~durchgestrichen für Löschungen~~)


## SCHRITT 6: Ausgabe validieren

- Prüfe die VOLLSTÄNDIGE Ausgabe:
  - Stelle sicher, dass die Formatierung in Text und Tabelle korrekt ist
    - Beispiel: Keine Formatierungsreste wie <br> oder ähnliches
  - Zusätzliche Einschränkungen (unten) MÜSSEN befolgt werden

---

# ZUSÄTZLICHE EINSCHRÄNKUNGEN

- Füge KEINE Erklärungen hinzu, außer bei Unsicherheit notwendig
- Interpretiere NICHT über den Änderungstext hinaus
- Bewahre den originalen Gesetzeswortlaut EXAKT
- Lasse KEINE unveränderten Teile innerhalb eines geänderten Abschnitts weg
- Nutze KEINE anderen Quellen außer die genannten
