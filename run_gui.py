#!/usr/bin/env python3
"""
Standalone Supermarkt GUI Runner
"""
import sys  # importiert Systemfunktionen für Programmstart
sys.path.insert(0, '.')  # fügt aktuelles Verzeichnis zum Pfad hinzu damit Imports funktionieren

from src.ui.main_controller import main  # importiert die Hauptfunktion aus dem Controller

if __name__ == "__main__":  # prüft ob Datei direkt gestartet wird
    main()  # startet die GUI Anwendung

