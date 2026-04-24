[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Pc_A4vY0)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23109494&assignment_repo_type=AssignmentRepo)
# Lagerverwaltungssystem - Projektvorlage
# Projekt: Supermarkt Lagerverwaltung mit PyQt6 GUI und MongoDB

## Projektueberblick
# Dieses Projekt ist ein Lagerverwaltungssystem fuer einen Supermarkt
# Es verwendet eine hexagonale Architektur mit Domain Ports Adapters und Services
# Die GUI wurde mit PyQt6 und Qt Designer entwickelt
# Die Daten werden in MongoDB Atlas gespeichert

- **Projektdauer:** 8 Wochen  # Dauer des Schulprojekts
- **Unterricht:** 2 UE pro Woche  # Unterrichtseinheiten pro Woche
- **Gruppengröße:** 4 Personen  # Teamgroesse
- **Ziel:** Professionelle Softwareentwicklung und Projektmanagement  # Lernziel

## Teammitglieder und Rollen
# Rolle 1: Projektverantwortung und Schnittstellen
# Rolle 2: Businesslogik und Report A  # Aleksej Pancika
# Rolle 3: Report B und Qualitaet
# Rolle 4: GUI und Interaktion  # Aleksej Pancika

## Projektstruktur

```
projekt/
├── src/                          # Quellcode
│   ├── domain/                   # Domain-Modelle
│   │   ├── product.py            # Produktklasse mit Validierung
│   │   ├── movement.py           # Bewegungsdatenklasse
│   │   └── warehouse.py          # Lagerverwaltung
│   ├── ports/                    # Schnittstellen (Abstraktion)
│   │   ├── repository_port.py   # Repository Schnittstelle
│   │   └── ports.py             # Report und Repository Ports
│   ├── adapters/                 # Adapter (konkrete Implementierungen)
│   │   ├── repository.py         # InMemory und MongoDB Repository
│   │   └── report.py             # Report Adapter
│   ├── services/                 # Business Logic
│   │   └── warehouse_service.py # WarehouseService mit DI
│   ├── ui/                       # Benutzeroberfläche (PyQt6)
│   │   ├── main_controller.py   # Hauptcontroller
│   │   ├── gui.py               # Legacy GUI
│   │   └── stock_dialog.py      # Bestandsdialog
│   └── reports/                  # Report-Generierung
│       └── report_a.py           # Lagerbestandsreport
├── tests/                        # Tests
│   ├── unit/                     # Unit Tests
│   │   ├── test_domain.py       # Tests fuer Domain
│   │   └── test_warehouse_service.py  # Tests fuer Service
│   └── dummy_data.py            # Dummy Daten Generator
├── docs/                         # Dokumentation
│   ├── contracts.md              # Schnittstellen-Dokumentation
│   ├── architecture.md           # Architektur-Dokumentation
│   └── changelog_pancika.md     # Changelog Aleksej Pancika
├── pyproject.toml                # Projektdefinition
└── README.md                     # Projekt-Dokumentation
```

## Installation und Setup

### Voraussetzungen
# Python 3.10 oder hoeher wird benoetigt
- Python 3.10+
- pip oder Poetry

### Entwicklungsumgebung aufbauen

```bash
# Repository klonen
git clone <repository-url>
cd projekt

# Virtuelle Umgebung erstellen
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Dependencies installieren
pip install -e .
pip install -e ".[dev]"

# Tests ausfuehren
pytest

# GUI starten
python run_gui.py
```

## Architektur

# Das Projekt folgt der Port-Adapter-Architektur (Hexagonal Architecture)
# Diese Aufteilung ermoeglicht einfaches Testen und Austauschen von Komponenten

- **Domain Layer:** Geschäftslogik und Entities (unabhängig von technischen Details)
- **Ports:** Schnittstellen für externe Abhängigkeiten (abstrakt)
- **Adapters:** Konkrete Implementierungen (In-Memory, MongoDB)
- **Services:** Geschäftsvorgänge und Use Cases
- **UI:** PyQt6 Benutzeroberfläche mit Qt Designer .ui Dateien

## GUI Starten

# Die GUI wird ueber den Hauptcontroller gestartet
# Der Controller verbindet alle Fenster mit der Businesslogik

```bash
# Haupt GUI starten
python run_gui.py

# Alternative direkt ueber Modul
python -m src.ui.main_controller
```

## Features

# Implementierte Features durch Aleksej Pancika:
# GUI Grundgeruest mit Qt Designer (.ui Dateien)
# Hauptcontroller mit Navigation zwischen Fenstern
# Lagerbestandsuebersicht mit Produkttabelle
# Ein und Ausbuchung mit ComboBox und Autocomplete
# Kaufhistorie mit letzten Bewegungen
# Random Kaeufe Generator fuer Demozwecke
# MongoDB Integration mit Fallback

## Reports

# Report A: Lagerbestandsbericht
# Zeigt aktuellen Bestand aller Produkte an
# Markiert Produkte mit niedrigem Bestand
# Berechnet Gesamtwert des Lagers

## Testing

### Unit Tests ausfuehren

```bash
pytest tests/unit/ -v
```

### Mit Coverage

```bash
pytest --cov=src tests/
```

## Bekannte Probleme

# Siehe docs/known_issues.md

## Lizenz

# Schulprojekt TGM

## Kontakt

# Projektverantwortung: Team

## Technische Hinweise

# MongoDB Atlas wird als Datenbank verwendet
# Verbindung erfolgt ueber pymongo mit mongodb+srv:// String
# Benoetigte Libraries: pymongo dnspython PyQt6

# Start der Anwendung:
```bash
python run_gui.py

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###################################################################################
-----------------------------------------------------------------------------------
****MONGODB Zugangsdaten**** Email: rajkovic.gabriel@gmx.at Passwort: GR12345GR
-----------------------------------------------------------------------------------
###################################################################################
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
