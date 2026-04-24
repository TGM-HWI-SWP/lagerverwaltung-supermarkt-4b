# Changelog – Aleksej Pancika
# Persönliches Changelog für Aleksej Pancika
# Rolle: UI Entwickler und Business Logic Integration

## [v0.1] – 2025-03-13

### Implementiert
# GUI Grundgerüste mit Qt Designer erstellt:
# haupt_gui.ui ist Hauptfenster mit Navigation
# lagerbestand_gui.ui zeigt Lagerbestandsübersicht
# lieferung_gui.ui dient Wareneingang und ausgang
# kauf_historie_gui.ui zeigt letzte Bewegungen an
# rechnung_gui.ui ist Rechnungsansicht vorbereitet

### Tests geschrieben
# Keine Unit Tests für GUI Code nur manuelles Testen via python run_gui.py

### Commits
# 5d4a7a3 feat: business logic hinzugefügt
# 2e23e75 v0.1 project setup + business logic start
# 945796c lagerbestand_gui
# a70b4f6 lieferung_gui
# 08b78bf kauf_historie_gui
# 5449efc rechnung_gui
# 159edec haupt_gui

### Mergekonflikte
# Keine in dieser Version

## [v0.2] – 2025-03-20

### Implementiert
# MainController Version 1 bis 4 entwickelt:
# Verbindung der ui Buttons mit Python Logik
# Navigation zwischen Hauptfenster und Sub Fenstern via Parent Child Show Hide
# LagerbestandController mit schreibgeschützter Tabelle zeigt ID Name Kategorie Bestand Preis Wert
# LieferungController mit Ein und Ausbuchung über SpinBox und Grund Eingabe
# KaufHistorieController zeigt die letzten 10 Bewegungen an

### Tests geschrieben
# Test 01 als Smoke Test der GUI Startbarkeit

### Commits
# fead9af controller
# d0c595b controller v2
# 5abf64a Controller V3
# 9843061 Controller V4
# 35192ac Test-01

### Mergekonflikte
# Keine in dieser Version

## [v0.3] – 2025-04-10

### Implementiert
# Business Logic Integration:
# WarehouseService an GUI angebunden via Dependency Injection durch RepositoryFactory
# Produktliste dynamisch aus Service laden
# Einbuchen und Ausbuchen mit Validierung und Bestandsprüfung
# Automatisches Nachladen der Tabelle nach jeder Buchung
# Merge und Konfliktlösung:
# Merge von businesslogik aleksej in DB 01
# Konflikt in ui init gelöst aktuellste PyQt6 GUI Implementierung mit Business Logic Updates beibehalten

### Tests geschrieben
# Keine neuen Tests in dieser Phase

### Commits
# 76b1563 Update Business logic
# bbf38f8 Merge remote tracking branch origin businesslogik aleksej into DB 01
# 7287bb8 Resolve merge conflict in ui init Keep latest PyQt6 GUI implementation with Businesslogik updates

### Mergekonflikte
# src ui init hatte zwei parallele GUI Implementierungen alte versus neue Business Logic Version
# aktuellste Version mit WarehouseService Integration wurde beibehalten

## [v0.4] – 2025-04-17 bis 2025-04-24

### Implementiert
# Finalisierung und UX Polish:
# ComboBoxEventFilter öffnet Dropdown bei Klick oder Fokus und fokussiert sofort LineEdit zum Tippen
# Intelligente Produktauflösung Eingabe kann Produkt ID exakter Name oder Teil Name sein
# QCompleter mit PopupCompletion für schnelle Produktauswahl
# Tabellenzeilen Klick aktualisiert ComboBox Auswahl
# MongoDB zu SQLite Fallback wenn MongoDB nicht erreichbar automatisch auf lokale SQLite Datenbank umstellen mit Warn Dialog
# Dummy Daten automatisch laden wenn Repository leer ist
# Random Käufe Generator für Demozwecke
# Dropdown Fix ComboBox Objektname korrigiert zu comboBoxProduct sodass findChild wieder funktioniert

### Tests geschrieben
# Manuelle End to End Tests aller GUI Fenster

### Commits
# 0d9c7fc finalisation
# c8cc588 Resolve merge conflicts and add pymongo deps
# 9859a70 Remove TODO.md no todo files needed
# e412245 Verbinden von allem
# 9471ab9 fix dropdown funktioniert jetzt ComboBox name korrigiert

### Mergekonflikte
# pyproject.toml Dependencies pymongo und weitere DB Abhängigkeiten aus DB 01 mit GUI Code zusammengeführt
# src ui init erneut letzter Konflikt zwischen GUI 03 und businesslogik aktuelle Controller Version behalten

## Zusammenfassung

# Gesamt implementierte Features: 8 Stück
# Fünf GUI Grundgerüste Controller Business Logic Integration ComboBox EventFilter DB Fallback Random Käufe
# Gesamt geschriebene Tests: 1 Stück Smoke Test
# Gesamt Commits: mehr als 24
# Größte Herausforderung: Mergekonflikte in ui init bei paralleler GUI und Business Logic Entwicklung auflösen ohne Funktionalität zu verlieren
# Schönste Code Zeile:
# combo.installEventFilter(ComboBoxEventFilter())
# Eine Zeile die die gesamte UX der Produktauswahl von frustrierend auf flüssig gebracht hat

# Changelog erstellt von: Aleksej Pancika
# Letzte Aktualisierung: 2025-04-24

