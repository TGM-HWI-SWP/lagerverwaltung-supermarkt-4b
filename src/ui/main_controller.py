"""Unified Main Controller - Combines .ui buttons with full business logic integration."""
# Haupt Controller Datei die alle GUI Fenster mit der Businesslogik verbindet

import random  # für zufällige Käufe im Demo Modus
import sys  # für Systemfunktionen und Pfad Anpassungen
from pathlib import Path  # für plattformunabhängige Pfadangaben
from typing import Dict  # Typisierung für Dictionary Rückgaben
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QTableWidget,
    QTableView, QPushButton, QComboBox, QSpinBox, QLineEdit, QLabel,
    QAbstractItemView, QHeaderView, QCompleter
)  # importiert alle benötigten GUI Elemente aus PyQt6
from PyQt6.QtGui import QStandardItemModel, QStandardItem  # für Tabellen Modelle
from PyQt6.QtCore import Qt, QObject, QEvent, QTimer  # für Event Handling und Timer
from PyQt6 import uic  # zum Laden von Qt Designer .ui Dateien

ROOT_DIR = Path(__file__).resolve().parents[1]  # geht zwei Ebenen hoch zum Projekt Root

try:
    from src.adapters.repository import RepositoryFactory  # Factory für Repository Erstellung
    from src.services import WarehouseService  # Haupt Service für Geschäftslogik
except ImportError:  # Fallback wenn Import über src nicht funktioniert
    sys.path.insert(0, str(ROOT_DIR))  # fügt Projekt Root zum Python Pfad hinzu
    from src.adapters.repository import RepositoryFactory  # erneuter Importversuch
    from src.services import WarehouseService  # erneuter Importversuch

from src.domain.lieferung_window import LieferungWindow  # separates Fenster für Lieferungen

class ComboBoxAppFilter(QObject):  # Event Filter auf Applikationsebene
    """Application-level filter that opens a QComboBox dropdown on click/focus."""
    def __init__(self, combo: QComboBox, parent=None):  # Konstruktor mit ComboBox Referenz
        super().__init__(parent)  # ruft QObject Konstruktor auf
        self.combo = combo  # speichert Referenz zur ComboBox
        self._line_edit = combo.lineEdit()  # speichert Referenz zum internen Eingabefeld

    def eventFilter(self, obj, event):  # wird bei jedem Event aufgerufen
        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.FocusIn):  # bei Mausklick oder Fokus
            if obj is self.combo or obj is self._line_edit:  # nur wenn Event von unserer ComboBox kommt
                self.combo.showPopup()  # öffnet Dropdown Liste
        return super().eventFilter(obj, event)  # übergibt Event an weitere Filter

class ComboBoxLineEditFilter(QObject):  # Event Filter nur für das Eingabefeld der ComboBox
    """Event filter installed on a QComboBox's line edit to open dropdown on click/focus."""
    def __init__(self, combo: QComboBox, parent=None):  # Konstruktor mit ComboBox Referenz
        super().__init__(parent)  # ruft QObject Konstruktor auf
        self.combo = combo  # speichert Referenz zur ComboBox

    def eventFilter(self, obj, event):  # wird bei jedem Event aufgerufen
        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.FocusIn):  # bei Mausklick oder Fokus
            self.combo.showPopup()  # öffnet Dropdown Liste
        return super().eventFilter(obj, event)  # übergibt Event an weitere Filter

class LagerbestandController(QMainWindow):  # Fenster für Lagerbestandsübersicht
    def __init__(self, service, parent=None):  # Konstruktor mit Service und optionalem Elternfenster
        super().__init__(parent)  # ruft QMainWindow Konstruktor auf
        self.service = service  # speichert Referenz zum WarehouseService
        self.base_dir = Path(__file__).resolve().parent  # Verzeichnis der aktuellen Datei
        uic.loadUi(str(self.base_dir / "lagerbestand_gui.ui"), self)  # lädt Qt Designer Datei
        self._setup_ui()  # initialisiert Benutzeroberfläche

    def _setup_ui(self):  # verbindet UI Elemente mit Logik
        back_btn = self.findChild(QPushButton, "pushButton")  # sucht Zurück Button
        if back_btn:
            back_btn.clicked.connect(self._go_back)  # verbindet Klick mit Zurück Funktion
        self._refresh_table()  # füllt Tabelle beim Start

    def _go_back(self):  # Navigation zurück zum Hauptfenster
        if self.parent():  # prüft ob Elternfenster existiert
            self.parent().show()  # zeigt Hauptfenster wieder an
        self.close()  # schließt aktuelles Fenster

    def closeEvent(self, event):  # wird beim Schließen des Fensters aufgerufen
        if self.parent():  # prüft ob Elternfenster existiert
            self.parent().show()  # zeigt Hauptfenster wieder an
        event.accept()  # bestätigt das Schließen

    def showEvent(self, event):  # wird beim Anzeigen des Fensters aufgerufen
        self._refresh_table()  # aktualisiert Tabelle bei jedem Anzeigen
        super().showEvent(event)  # ruft Original Methode auf

    def _refresh_table(self):  # aktualisiert die Produkttabelle
        table = self.findChild(QTableView, "tableView")  # sucht Tabelle im UI
        if table:  # nur wenn Tabelle gefunden wurde
            model = QStandardItemModel()  # erstellt neues Tabellen Modell
            model.setHorizontalHeaderLabels(["ID", "Name", "Kategorie", "Bestand", "Preis", "Wert"])  # setzt Spaltenüberschriften
            products = self.service.get_all_products()  # lädt alle Produkte aus Service
            for product_id, product in products.items():  # iteriert über alle Produkte
                model.appendRow([  # fügt Zeile zum Modell hinzu
                    QStandardItem(product_id),  # Spalte 0: Produkt ID
                    QStandardItem(product.name),  # Spalte 1: Name
                    QStandardItem(product.category),  # Spalte 2: Kategorie
                    QStandardItem(str(product.quantity)),  # Spalte 3: Bestand als Text
                    QStandardItem(f"{product.price:.2f}"),  # Spalte 4: Preis formatiert
                    QStandardItem(f"{product.get_total_value():.2f}")  # Spalte 5: Gesamtwert formatiert
                ])
            table.setModel(model)  # weist Modell der Tabelle zu

class LieferungController(QMainWindow):  # Fenster für Ein und Ausbuchung
    def __init__(self, service, parent=None):  # Konstruktor mit Service und optionalem Elternfenster
        super().__init__(parent)  # ruft QMainWindow Konstruktor auf
        self.service = service  # speichert Referenz zum WarehouseService
        self.base_dir = Path(__file__).resolve().parent  # Verzeichnis der aktuellen Datei
        uic.loadUi(str(self.base_dir / "lieferung_gui.ui"), self)  # lädt Qt Designer Datei
        self._setup_ui()  # initialisiert Benutzeroberfläche

    def _setup_ui(self):  # verbindet UI Elemente mit Logik
        back_btn = self.findChild(QPushButton, "pushButton")  # sucht Zurück Button
        if back_btn:
            back_btn.clicked.connect(self._go_back)  # verbindet Klick mit Zurück Funktion

        # Verbinde Bestell Buttons
        btn_in = self.findChild(QPushButton, "pushButtonEinbuchen")  # sucht Einbuchungsbutton
        if btn_in:
            btn_in.clicked.connect(self._handle_incoming)  # verbindet mit Einbuchungslogik

        btn_out = self.findChild(QPushButton, "pushButtonAusbuchen")  # sucht Ausbuchungsbutton
        if btn_out:
            btn_out.clicked.connect(self._handle_outgoing)  # verbindet mit Ausbuchungslogik

        # Tabelle schreibgeschützt machen und Klick Verhalten verbinden
        table = self.findChild(QTableWidget, "tableWidget")  # sucht Tabelle im UI
        if table:
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # deaktiviert Bearbeitung
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # ganze Zeilen auswählbar
            table.clicked.connect(self._on_table_row_clicked)  # verbindet Zeilenklick mit Auswahl

        self._refresh_table()  # füllt Tabelle beim Start
        self._load_products_into_combo()  # füllt ComboBox beim Start

    def _go_back(self):  # Navigation zurück zum Hauptfenster
        if self.parent():  # prüft ob Elternfenster existiert
            self.parent().show()  # zeigt Hauptfenster wieder an
        self.close()  # schließt aktuelles Fenster

    def closeEvent(self, event):  # wird beim Schließen des Fensters aufgerufen
        if self.parent():  # prüft ob Elternfenster existiert
            self.parent().show()  # zeigt Hauptfenster wieder an
        event.accept()  # bestätigt das Schließen

    def _load_products_into_combo(self):  # füllt die Produktauswahl Dropdown
        combo = self.findChild(QComboBox, "comboBoxProduct")  # sucht ComboBox im UI
        if combo:  # nur wenn ComboBox gefunden wurde
            combo.clear()  # leert bestehende Einträge
            combo.setEditable(True)  # ermöglicht Texteingabe
            combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)  # verhindert Hinzufügen neuer Einträge
            combo.setMaxVisibleItems(15)  # zeigt maximal 15 Einträge im Dropdown
            
            products = self.service.get_all_products()  # lädt alle Produkte
            display_items = []  # sammelt Anzeigetexte für Completer
            for pid, product in sorted(products.items()):  # sortiert nach ID
                display_text = f"{product.name} ({pid}) — Bestand: {product.quantity}"  # Format: Name (ID) — Bestand: X
                combo.addItem(display_text, pid)  # fügt Eintrag mit Produkt ID als Daten hinzu
                display_items.append(display_text)  # sammelt für Completer

            if combo.count() > 0:  # wenn Produkte vorhanden sind
                combo.setCurrentIndex(0)  # wählt ersten Eintrag vor

            completer = QCompleter(display_items, combo)  # erstellt Autovervollständigung
            completer.setCaseSensitivity(False)  # Groß und Kleinschreibung egal
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)  # zeigt Popup Vorschläge
            completer.setMaxVisibleItems(15)  # maximal 15 Vorschläge
            combo.setCompleter(completer)  # weist Completer der ComboBox zu
            combo.activated.connect(self._sync_combo_from_text)  # verbindet Auswahl mit Synchronisation
            combo.currentTextChanged.connect(self._sync_combo_from_text)  # verbindet Textänderung mit Synchronisation

            # Konfiguriere das eingebaute LineEdit
            line_edit = combo.lineEdit()  # holt internes Eingabefeld
            if line_edit:  # nur wenn Eingabefeld existiert
                line_edit.installEventFilter(ComboBoxLineEditFilter(combo))  # installiert Event Filter für Dropdown
                line_edit.setPlaceholderText("Produktname oder ID eingeben und Enter drücken")  # Hinweistext
                line_edit.setClearButtonEnabled(True)  # zeigt X Button zum Löschen
                line_edit.returnPressed.connect(self._sync_combo_from_text)  # Enter drücken synchronisiert Auswahl
                line_edit.textChanged.connect(self._sync_combo_from_text)  # Textänderung synchronisiert Auswahl

    def _resolve_product_id_from_input(self, user_input: str):  # löst Produkt ID aus Benutzereingabe auf
        """Resolve product ID from user input."""
        if not user_input:  # leere Eingabe
            return None  # keine Auflösung möglich
        
        text = user_input.strip()  # entfernt Leerzeichen am Anfang und Ende
        products = self.service.get_all_products()  # lädt alle Produkte
        
        if text in products:  # prüft ob Eingabe direkt eine Produkt ID ist
            return text  # gibt ID zurück
        
        text_lower = text.lower()  # wandelt in Kleinbuchstaben um für Vergleich
        
        for pid, product in products.items():  # iteriert über alle Produkte
            if product.name.lower() == text_lower:  # exakter Name matcht
                return pid  # gibt zugehörige ID zurück
        
        for pid, product in products.items():  # iteriert über alle Produkte
            if text_lower in product.name.lower():  # Teilstring kommt im Namen vor
                return pid  # gibt erste passende ID zurück
        
        return None  # gibt None zurück wenn nichts gefunden wurde

    def _sync_combo_from_text(self):  # synchronisiert ComboBox Auswahl mit getipptem Text
        """Try to match typed text to a product and update the combo selection."""
        combo = self.findChild(QComboBox, "comboBoxProduct")  # sucht ComboBox
        if not combo or combo.count() == 0:  # prüft ob ComboBox leer ist
            return  # bricht ab wenn nichts zu tun

        text = combo.currentText().strip().lower()  # holt aktuellen Text in Kleinbuchstaben
        if not text:  # leerer Text
            return  # bricht ab

        current_data = combo.currentData()  # holt Daten des aktuell ausgewählten Eintrags
        if current_data:  # wenn bereits gültige Auswahl vorhanden
            return  # bricht ab da bereits korrekt

        for i in range(combo.count()):  # iteriert über alle ComboBox Einträge
            item_text = combo.itemText(i).lower()  # holt Text des Eintrags in Kleinbuchstaben
            item_data = combo.itemData(i)  # holt Daten des Eintrags
            
            if item_data and str(item_data).lower() == text:  # Daten passen zum Text
                combo.setCurrentIndex(i)  # wählt diesen Eintrag
                return  # beendet Suche
            
            if text in item_text:  # Text kommt im Eintrag vor
                combo.setCurrentIndex(i)  # wählt diesen Eintrag
                return  # beendet Suche

    def _refresh_table(self):  # aktualisiert die Produkttabelle
        table = self.findChild(QTableWidget, "tableWidget")  # sucht Tabelle im UI
        if table:  # nur wenn Tabelle gefunden wurde
            table.setRowCount(0)  # leert alle Zeilen
            products = self.service.get_all_products()  # lädt alle Produkte
            table.setColumnCount(6)  # setzt sechs Spalten
            table.setHorizontalHeaderLabels(["ID", "Name", "Kategorie", "Bestand", "Preis", "Wert"])  # Spaltenüberschriften
            for row_idx, (product_id, product) in enumerate(products.items()):  # iteriert über Produkte
                table.insertRow(row_idx)  # fügt neue Zeile ein
                table.setItem(row_idx, 0, QTableWidgetItem(product_id))  # Spalte 0: ID
                table.setItem(row_idx, 1, QTableWidgetItem(product.name))  # Spalte 1: Name
                table.setItem(row_idx, 2, QTableWidgetItem(product.category))  # Spalte 2: Kategorie
                table.setItem(row_idx, 3, QTableWidgetItem(str(product.quantity)))  # Spalte 3: Bestand
                table.setItem(row_idx, 4, QTableWidgetItem(f"{product.price:.2f}"))  # Spalte 4: Preis formatiert
                table.setItem(row_idx, 5, QTableWidgetItem(f"{product.get_total_value():.2f}"))  # Spalte 5: Wert formatiert

    def showEvent(self, event):  # wird beim Anzeigen des Fensters aufgerufen
        self._refresh_table()  # aktualisiert Tabelle
        self._load_products_into_combo()  # aktualisiert Produktliste
        super().showEvent(event)  # ruft Original Methode auf

    def _on_table_row_clicked(self, index):  # wird bei Klick auf Tabellenzeile aufgerufen
        """Wenn auf eine Tabellenzeile geklickt wird, Produkt in ComboBox auswählen."""
        table = self.findChild(QTableWidget, "tableWidget")  # sucht Tabelle
        combo = self.findChild(QComboBox, "comboBoxProduct")  # sucht ComboBox
        if not table or not combo:  # prüft ob beide Elemente existieren
            return  # bricht ab wenn nicht

        row = index.row()  # holt Zeilennummer
        product_id_item = table.item(row, 0)  # holt Item aus erster Spalte (ID)
        if product_id_item:  # wenn Item existiert
            product_id = product_id_item.text()  # holt Text (Produkt ID)
            for i in range(combo.count()):  # iteriert über alle ComboBox Einträge
                if combo.itemData(i) == product_id:  # vergleicht gespeicherte Daten
                    combo.setCurrentIndex(i)  # wählt passenden Eintrag
                    break  # beendet Schleife nach Fund

    def _handle_incoming(self):  # Handler für Einbuchung Button
        self._process_movement("in")  # ruft Verarbeitung mit Richtung in auf

    def _handle_outgoing(self):  # Handler für Ausbuchung Button
        self._process_movement("out")  # ruft Verarbeitung mit Richtung out auf

    def _process_movement(self, direction: str):  # zentrale Methode für Ein und Ausbuchung
        combo = self.findChild(QComboBox, "comboBoxProduct")  # sucht Produktauswahl
        spin = self.findChild(QSpinBox, "spinBoxMenge")  # sucht Mengeneingabe
        line = self.findChild(QLineEdit, "lineEditGrund")  # sucht Grund Eingabe

        if not combo or not spin:  # prüft ob Pflichtfelder vorhanden
            QMessageBox.critical(self, "Fehler", "UI-Elemente nicht gefunden!")  # Fehlermeldung
            return  # bricht ab

        product_id = combo.currentData()  # holt Daten der aktuellen Auswahl
        product_name = combo.currentText().split("(")[0].strip() if combo.currentText() else None  # extrahiert Namensteil
        
        if not product_id:  # wenn keine Auswahl vorhanden
            user_input = combo.currentText().strip()  # holt eingegebenen Text
            if not user_input:  # wenn leer
                QMessageBox.warning(self, "Fehler", "Bitte ein Produkt auswählen oder Produkt-ID eingeben.")  # Hinweis
                return  # bricht ab
            
            product_id = self._resolve_product_id_from_input(user_input)  # versucht Auflösung
            if not product_id:  # wenn keine Auflösung möglich
                QMessageBox.warning(self, "Fehler", f"Produkt '{user_input}' nicht gefunden.\nBitte gültige Produkt-ID oder Namen eingeben.")  # Fehlermeldung
                return  # bricht ab
            
            try:  # versucht Namen aus Service zu holen
                products = self.service.get_all_products()  # lädt alle Produkte
                if product_id in products:  # wenn ID existiert
                    product_name = products[product_id].name  # holt richtigen Namen
                else:
                    product_name = user_input  # Fallback auf Eingabe
            except:  # bei Fehler
                product_name = user_input  # Fallback auf Eingabe

        quantity = spin.value()  # holt eingegebene Menge
        if quantity <= 0:  # prüft ob Menge gültig
            QMessageBox.warning(self, "Fehler", "Bitte eine gültige Menge eingeben (min. 1).")  # Hinweis
            return  # bricht ab

        reason = line.text().strip() if line else ""  # holt Grund oder leerer String

        try:  # versucht Buchung durchzuführen
            if direction == "in":  # bei Einbuchung
                if not reason:  # wenn kein Grund angegeben
                    reason = "Wareneingang / Lieferung"  # setzt Standardgrund
                self.service.add_stock(product_id, quantity, reason=reason)  # führt Einbuchung durch
                QMessageBox.information(  # Erfolgsmeldung
                    self, "Erfolgreich",
                    f"{quantity} Stück eingebucht.\n\nProdukt: {product_name}"
                )
            else:  # out  bei Ausbuchung
                if not reason:  # wenn kein Grund angegeben
                    reason = "Verkauf"  # setzt Standardgrund
                self.service.remove_stock(product_id, quantity, reason=reason)  # führt Ausbuchung durch
                QMessageBox.information(  # Erfolgsmeldung
                    self, "Erfolgreich",
                    f"{quantity} Stück ausgebucht.\n\nProdukt: {product_name}"
                )

            spin.setValue(1)  # setzt Menge zurück auf 1
            if line:  # wenn Grund Eingabe existiert
                line.clear()  # leert Grund
            combo.setCurrentIndex(0)  # setzt Auswahl zurück

            self._refresh_table()  # aktualisiert Tabelle
            self._load_products_into_combo()  # aktualisiert ComboBox

        except ValueError as ve:  # bei Validierungsfehler
            QMessageBox.warning(self, "Validierungsfehler", str(ve))  # zeigt Fehlermeldung
        except Exception as e:  # bei unerwartetem Fehler
            QMessageBox.critical(self, "Fehler", f"Fehler bei der Verarbeitung:\n{e}")  # zeigt Fehlermeldung

class KaufHistorieController(QMainWindow):  # Fenster für Bewegungshistorie
    def __init__(self, service, parent=None):  # Konstruktor mit Service und optionalem Elternfenster
        super().__init__(parent)  # ruft QMainWindow Konstruktor auf
        self.service = service  # speichert Referenz zum WarehouseService
        self.base_dir = Path(__file__).resolve().parent  # Verzeichnis der aktuellen Datei
        uic.loadUi(str(self.base_dir / "kauf_historie_gui.ui"), self)  # lädt Qt Designer Datei
        self._setup_ui()  # initialisiert Benutzeroberfläche

    def _setup_ui(self):  # verbindet UI Elemente mit Logik
        back_btn = self.findChild(QPushButton, "pushButton")  # sucht Zurück Button
        if back_btn:
            back_btn.clicked.connect(self._go_back)  # verbindet Klick mit Zurück Funktion

        table = self.findChild(QTableWidget, "tableWidget")  # sucht Tabelle
        if table:
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # deaktiviert Bearbeitung
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # ganze Zeilen auswählbar

        self._refresh_table()  # füllt Tabelle beim Start

    def showEvent(self, event):  # wird beim Anzeigen aufgerufen
        self._refresh_table()  # aktualisiert Tabelle
        super().showEvent(event)  # ruft Original Methode auf

    def _go_back(self):  # Navigation zurück zum Hauptfenster
        if self.parent():  # prüft ob Elternfenster existiert
            self.parent().show()  # zeigt Hauptfenster wieder an
        self.close()  # schließt aktuelles Fenster

    def closeEvent(self, event):  # wird beim Schließen aufgerufen
        if self.parent():  # prüft ob Elternfenster existiert
            self.parent().show()  # zeigt Hauptfenster wieder an
        event.accept()  # bestätigt das Schließen

    def _refresh_table(self):  # aktualisiert die Bewegungstabelle
        table = self.findChild(QTableWidget, "tableWidget")  # sucht Tabelle
        if table:  # nur wenn Tabelle gefunden
            table.setRowCount(0)  # leert alle Zeilen
            movements = self.service.get_movements()  # lädt alle Bewegungen
            table.setColumnCount(5)  # setzt fünf Spalten
            table.setHorizontalHeaderLabels(["Produkt", "Typ", "Menge", "Grund", "Zeit"])  # Spaltenüberschriften
            for row_idx, movement in enumerate(movements[-10:]):  # zeigt nur letzte 10 Bewegungen
                table.insertRow(row_idx)  # fügt neue Zeile ein
                table.setItem(row_idx, 0, QTableWidgetItem(movement.product_name))  # Spalte 0: Produktname
                table.setItem(row_idx, 1, QTableWidgetItem(movement.movement_type))  # Spalte 1: Bewegungstyp
                table.setItem(row_idx, 2, QTableWidgetItem(str(movement.quantity_change)))  # Spalte 2: Änderung
                table.setItem(row_idx, 3, QTableWidgetItem(movement.reason))  # Spalte 3: Grund
                table.setItem(row_idx, 4, QTableWidgetItem(movement.timestamp.strftime('%Y-%m-%d %H:%M')))  # Spalte 4: Zeit formatiert

class SupermarktMain(QMainWindow):  # Hauptfenster der Anwendung
    """Voll integrierte Haupt-GUI mit .ui und Business Logic."""
    def __init__(self):  # Konstruktor
        super().__init__()  # ruft QMainWindow Konstruktor auf
        print("SupermarktMain init...")  # Debug Ausgabe
        self.base_dir = Path(__file__).resolve().parent  # Verzeichnis der aktuellen Datei
        print(f"UI base dir: {self.base_dir}")  # Debug Ausgabe

        repo = RepositoryFactory.create_repository("mongodb")  # erstellt MongoDB Repository
        self.service = WarehouseService(repo)  # erzeugt Service mit Repository
        self.service.get_all_products()  # Test ob Verbindung funktioniert
        print("MongoDB connected successfully")  # Erfolgsmeldung

        if not self.service.get_all_products():  # prüft ob Produkte vorhanden
            self.service.load_dummy_data()  # lädt Beispieldaten

        ui_path = self.base_dir / "haupt_gui.ui"  # Pfad zur Haupt UI Datei
        print(f"Loading UI: {ui_path}")  # Debug Ausgabe
        uic.loadUi(str(ui_path), self)  # lädt Qt Designer Datei
        self.setWindowTitle("Supermarkt Lagerverwaltung [MongoDB]")  # Fenstertitel
        self.showMaximized()  # maximiert Fenster beim Start
        self.sub_windows = {}  # Dictionary für geöffnete Unterfenster
        self._setup_main_buttons()  # verbindet Hauptbuttons

    def _setup_main_buttons(self):  # verbindet Buttons des Hauptfensters
        lager_btn = self.findChild(QPushButton, "pushButton")  # sucht Lagerbestand Button
        if lager_btn:
            lager_btn.clicked.connect(self.show_lagerbestand)  # verbindet mit Anzeige Funktion

        liefer_btn = self.findChild(QPushButton, "pushButton_3")  # sucht Lieferung Button
        if liefer_btn:
            liefer_btn.clicked.connect(self.show_lieferung)  # verbindet mit Anzeige Funktion

        random_btn = self.findChild(QPushButton, "pushButton_2")  # sucht Random Button
        if random_btn:
            random_btn.clicked.connect(self.show_random_purchases)  # verbindet mit Demo Funktion

        kauf_btn = self.findChild(QPushButton, "pushButton_4")  # sucht Historie Button
        if kauf_btn:
            kauf_btn.clicked.connect(self.show_kauf_historie)  # verbindet mit Anzeige Funktion

    def show_lagerbestand(self):  # zeigt Lagerbestandsfenster
        if 'lager' not in self.sub_windows:  # prüft ob Fenster bereits existiert
            self.sub_windows['lager'] = LagerbestandController(self.service, self)  # erstellt neues Fenster
        self.sub_windows['lager'].show()  # zeigt Fenster an
        self.hide()  # versteckt Hauptfenster

    def show_lieferung(self):  # zeigt Lieferungsfenster
        self.lieferung_window = LieferungWindow(  # erstellt Lieferungsfenster
            self.service,  # übergibt Service
            str(self.base_dir / "lieferung_gui.ui")  # übergibt Pfad zur UI Datei
        )
        back_button = self.lieferung_window.findChild(QPushButton, "pushButton")  # sucht Zurück Button
        if back_button:
            back_button.clicked.connect(self._back_from_lieferung)  # verbindet mit Zurück Funktion
        self.lieferung_window.show()  # zeigt Fenster an
        self.hide()  # versteckt Hauptfenster

    def _back_from_lieferung(self):  # kommt von Lieferungsfenster zurück
        self.lieferung_window.close()  # schließt Lieferungsfenster
        self.show()  # zeigt Hauptfenster wieder an

    def show_random_purchases(self):  # erzeugt zufällige Demo Käufe
        if not self.service.get_all_products():  # prüft ob Produkte vorhanden
            QMessageBox.warning(self, "Keine Produkte", "Es sind keine Produkte vorhanden, um zufällige Käufe zu erzeugen.")  # Warnung
            return  # bricht ab

        product_list = [p for p in self.service.get_all_products().items() if p[1].quantity > 0]  # filtert Produkte mit Bestand
        if not product_list:  # wenn nichts auf Lager
            QMessageBox.warning(self, "Kein Lagerbestand", "Es sind keine Vorräte vorhanden, um Verkäufe zu erzeugen.")  # Warnung
            return  # bricht ab

        for _ in range(min(5, len(product_list))):  # maximal 5 zufällige Käufe
            pid, product = random.choice(product_list)  # wählt zufälliges Produkt
            quantity = random.randint(1, min(3, product.quantity))  # wählt zufällige Menge zwischen 1 und 3 oder Lagerbestand
            try:
                self.service.remove_stock(pid, quantity, reason="Random Kauf")  # führt Verkauf durch
            except ValueError:
                continue  # nächster Durchlauf bei Fehler

        QMessageBox.information(self, "Random Käufe", "Zufällige Käufe wurden erzeugt und in der Kaufhistorie gespeichert.")  # Erfolgsmeldung
        self.show_kauf_historie()  # zeigt direkt Historie an

    def show_kauf_historie(self):  # zeigt Kaufhistorie Fenster
        if 'kauf' not in self.sub_windows:  # prüft ob Fenster bereits existiert
            self.sub_windows['kauf'] = KaufHistorieController(self.service, self)  # erstellt neues Fenster
        self.sub_windows['kauf'].show()  # zeigt Fenster an
        self.hide()  # versteckt Hauptfenster

def main():  # Haupteinstiegspunkt der Anwendung
    print("Starting Supermarkt GUI...")  # Debug Ausgabe beim Start
    app = QApplication(sys.argv)  # erzeugt Qt Applikation mit Kommandozeilenargumenten
    window = SupermarktMain()  # erzeugt Hauptfenster
    window.showMaximized()  # zeigt Fenster maximiert an
    print("GUI shown")  # Debug Ausgabe wenn GUI angezeigt wird
    sys.exit(app.exec())  # startet Event Loop und beendet bei Schließen


if __name__ == "__main__":  # prüft ob Datei direkt gestartet wird
    main()  # ruft Hauptfunktion auf
