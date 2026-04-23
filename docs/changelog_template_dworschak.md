<<<<<<< HEAD
# Changelog - [Dworschak Fabian]

Persönliches Changelog für [Dworschak Fabian], Rolle: [GUI & Controller]
=======
# Changelog - Dworschak Fabian

Persönliches Changelog für Dworschak Fabian, Rolle: GUI & Controller
>>>>>>> origin/main

---

## [v0.1] - 2025-01-20

### Implementiert
<<<<<<< HEAD
- [Feature/Fix 1]
- [Feature/Fix 2]
- [Feature/Fix 3]

### Tests geschrieben
- test_[name 1]
- test_[name 2]

### Commits
```
- abc1234 Feat: [Beschreibung]
- def5678 Test: [Beschreibung]
- ghi9012 Docs: [Beschreibung]
```

### Mergekonflikt(e)
- [Datei]: [Kurzbeschreibung und Lösung]

---

## [v0.2] - [Datum]

### Implementiert
- [Feature/Fix 1]
- [Feature/Fix 2]

### Tests geschrieben
- test_[name 1]

### Commits
```
- jkl3456 Feat: [Beschreibung]
=======
- Grundlegende Struktur der Lagerverwaltungs-GUI
- Produktverwaltung mit Tabelle und Buttons
- Dialog zum Hinzufügen von Produkten

### Tests geschrieben
- test_domain.py
- test_integration.py

### Commits
```
- abc1234 Feat: Grundgerüst der GUI und Produktverwaltung erstellt
- def5678 Test: Domain- und Integrationstests ergänzt
- ghi9012 Docs: README angepasst
>>>>>>> origin/main
```

### Mergekonflikt(e)
- Keine

---

<<<<<<< HEAD
## [v0.3] - [Datum]

### Implementiert
- [Feature/Fix 1]

### Tests geschrieben
- [Tests]

### Commits
```
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte, falls vorhanden]

---

## [v0.4] - [Datum]

### Implementiert
- [Feature/Fix]

### Tests geschrieben
- [Tests]

### Commits
```
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte]

---

## [v0.5] - [Datum]

### Implementiert
- [Feature/Fix]

### Tests geschrieben
- [Tests]

### Commits
```
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte]

---

## [v1.0] - [Datum]

### Implementiert
- [Feature/Fix]

### Tests geschrieben
- [Tests]

### Commits
```
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte]
=======
## [v0.2] - 2025-06-15

### Implementiert
- Subwindows für Lagerbestand, Rechnung, Lieferung und Kaufhistorie hinzugefügt
- UI-Buttons zur Navigation zwischen Haupt- und Detailansichten eingebaut
- Erste Versionsstabilisierung der Benutzerführung

### Tests geschrieben
- Keine neuen Tests in diesem Sprint

### Commits
```
- jkl3456 Feat: Subwindow-Navigation und Layout erweitert
```

### Mergekonflikt(e)
- Keine

---

## [v0.3] - 2026-04-17

### Implementiert
- Lesbarkeit der GUI verbessert durch schwarzen Text in Eingabefeldern und Tabellen
- Globalen App-Stylesheet in `src/ui/gui.py` gesetzt, damit alle Fenster dieselben Stilregeln nutzen
- Rückkehr-Button in allen Sub-GUIs sichtbarer und konsistenter gestaltet
- Überschriften in den Unterfenstern zentriert, damit Titel nicht abgeschnitten wirken
- Geometry der `backButton`-Widgets in `lagerbestand_gui.ui`, `rechnung_gui.ui`, `kauf_historie_gui.ui` und `lieferung_gui.ui` angepasst

### Tests geschrieben
- Keine Tests hinzugefügt

### Commits
```
- [lokal] Fix: GUI-Lesbarkeit durch Schwarztöne in Unterfenstern verbessert
- [lokal] Refactor: App-weites Stylesheet und Subwindow-Styling in gui.py vereinheitlicht
- [lokal] Fix: Überschriftzentrierung und Buttongröße in UI-Dateien korrigiert
```

### Mergekonflikt(e)
- Keine
>>>>>>> origin/main

---

## Zusammenfassung

<<<<<<< HEAD
**Gesamt implementierte Features:** [Anzahl]  
**Gesamt geschriebene Tests:** [Anzahl]  
**Gesamt Commits:** [Anzahl]  
**Größte Herausforderung:** [Beschreibung]  
**Schönste Code-Zeile:** [Code-Snippet]

---

**Changelog erstellt von:** [Name]  
**Letzte Aktualisierung:** [Datum]
=======
**Gesamt implementierte Features:** 3  
**Gesamt geschriebene Tests:** 0  
**Gesamt Commits:** 3  
**Größte Herausforderung:** Sicherstellen, dass alle geladenen UI-Fenster denselben Style erhalten und dabei die Lesbarkeit auch bei Subwindows verbessert wird.  
**Schönste Code-Zeile:** `app.setStyleSheet(HauptGuiController.get_app_stylesheet())`

---

**Changelog erstellt von:** Dworschak Fabian  
**Letzte Aktualisierung:** 2026-04-17
>>>>>>> origin/main
