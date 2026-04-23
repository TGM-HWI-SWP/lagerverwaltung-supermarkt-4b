"""Unified Main Controller - Combines .ui buttons with full business logic integration."""

import random
import sys
from pathlib import Path
from typing import Dict
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QTableWidget,
    QTableView, QPushButton, QComboBox, QSpinBox, QLineEdit, QLabel,
    QAbstractItemView, QHeaderView, QCompleter
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QObject, QEvent, QTimer
from PyQt6 import uic

ROOT_DIR = Path(__file__).resolve().parents[1]

try:
    from src.adapters.repository import RepositoryFactory
    from src.services import WarehouseService
except ImportError:
    sys.path.insert(0, str(ROOT_DIR))
    from src.adapters.repository import RepositoryFactory
    from src.services import WarehouseService

class ComboBoxAppFilter(QObject):
    """Application-level filter that opens a QComboBox dropdown on click/focus.
    
    Installed on QApplication.instance() so it receives events BEFORE the
    target widget consumes them.
    """
    def __init__(self, combo: QComboBox, parent=None):
        super().__init__(parent)
        self.combo = combo
        self._line_edit = combo.lineEdit()

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.FocusIn):
            if obj is self.combo or obj is self._line_edit:
                self.combo.showPopup()
        return super().eventFilter(obj, event)

class ComboBoxLineEditFilter(QObject):
    """Event filter installed on a QComboBox's line edit to open dropdown on click/focus."""
    def __init__(self, combo: QComboBox, parent=None):
        super().__init__(parent)
        self.combo = combo

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.FocusIn):
            self.combo.showPopup()
        return super().eventFilter(obj, event)

class LagerbestandController(QMainWindow):
    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        self.base_dir = Path(__file__).resolve().parent
        uic.loadUi(str(self.base_dir / "lagerbestand_gui.ui"), self)
        self._setup_ui()

    def _setup_ui(self):
        back_btn = self.findChild(QPushButton, "pushButton")
        if back_btn:
            back_btn.clicked.connect(self._go_back)
        self._refresh_table()

    def _go_back(self):
        if self.parent():
            self.parent().show()
        self.close()

    def closeEvent(self, event):
        if self.parent():
            self.parent().show()
        event.accept()

    def _refresh_table(self):
        table = self.findChild(QTableView, "tableView")
        if table:
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(["ID", "Name", "Kategorie", "Bestand", "Preis", "Wert"])
            products = self.service.get_all_products()
            for product_id, product in products.items():
                model.appendRow([
                    QStandardItem(product_id),
                    QStandardItem(product.name),
                    QStandardItem(product.category),
                    QStandardItem(str(product.quantity)),
                    QStandardItem(f"{product.price:.2f}"),
                    QStandardItem(f"{product.get_total_value():.2f}")
                ])
            table.setModel(model)

class LieferungController(QMainWindow):
    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        self.base_dir = Path(__file__).resolve().parent
        uic.loadUi(str(self.base_dir / "lieferung_gui.ui"), self)
        self._setup_ui()

    def _setup_ui(self):
        back_btn = self.findChild(QPushButton, "pushButton")
        if back_btn:
            back_btn.clicked.connect(self._go_back)

        # Verbinde Bestell-Buttons
        btn_in = self.findChild(QPushButton, "pushButtonEinbuchen")
        if btn_in:
            btn_in.clicked.connect(self._handle_incoming)

        btn_out = self.findChild(QPushButton, "pushButtonAusbuchen")
        if btn_out:
            btn_out.clicked.connect(self._handle_outgoing)

        # Tabelle schreibgeschützt machen und Klick-Verhalten verbinden
        table = self.findChild(QTableWidget, "tableWidget")
        if table:
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            table.clicked.connect(self._on_table_row_clicked)

        self._refresh_table()
        self._load_products_into_combo()

    def _go_back(self):
        if self.parent():
            self.parent().show()
        self.close()

    def closeEvent(self, event):
        if self.parent():
            self.parent().show()
        event.accept()

    def _load_products_into_combo(self):
        combo = self.findChild(QComboBox, "comboBoxProduct")
        if combo:
            combo.clear()
            combo.setEditable(True)
            combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
            combo.setMaxVisibleItems(15)
            
            products = self.service.get_all_products()
            display_items = []
            for pid, product in sorted(products.items()):
                display_text = f"{product.name} ({pid}) — Bestand: {product.quantity}"
                combo.addItem(display_text, pid)
                display_items.append(display_text)

            if combo.count() > 0:
                combo.setCurrentIndex(0)

            completer = QCompleter(display_items, combo)
            completer.setCaseSensitivity(False)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
            completer.setMaxVisibleItems(15)
            combo.setCompleter(completer)
            combo.activated.connect(self._sync_combo_from_text)
            combo.currentTextChanged.connect(self._sync_combo_from_text)

            # Konfiguriere das eingebaute LineEdit
            line_edit = combo.lineEdit()
            if line_edit:
                line_edit.installEventFilter(ComboBoxLineEditFilter(combo))
                line_edit.setPlaceholderText("Produktname oder ID eingeben und Enter drücken")
                line_edit.setClearButtonEnabled(True)  # X-Button zum Löschen
                line_edit.returnPressed.connect(self._sync_combo_from_text)
                line_edit.textChanged.connect(self._sync_combo_from_text)

    def _resolve_product_id_from_input(self, user_input: str):
        """
        Resolve product ID from user input - can be:
        1. Direct product ID (e.g. '507f1f77bcf86cd799439011')
        2. Product name (e.g. 'Milch' or 'milch')
        3. Partial name (e.g. 'mil' matches 'Milch')
        """
        if not user_input:
            return None
        
        text = user_input.strip()
        products = self.service.get_all_products()
        
        # Try exact ID match first
        if text in products:
            return text
        
        # Try case-insensitive matching
        text_lower = text.lower()
        
        # Try exact name match
        for pid, product in products.items():
            if product.name.lower() == text_lower:
                return pid
        
        # Try partial name match
        for pid, product in products.items():
            if text_lower in product.name.lower():
                return pid
        
        # No match found
        return None

    def _sync_combo_from_text(self):
        """Try to match typed text to a product and update the combo selection."""
        combo = self.findChild(QComboBox, "comboBoxProduct")
        if not combo or combo.count() == 0:
            return

        text = combo.currentText().strip().lower()
        if not text:
            return

        # First, check if current selection already has matching data
        current_data = combo.currentData()
        if current_data:
            return  # Already has valid selection

        # Try to find a matching item by text
        for i in range(combo.count()):
            item_text = combo.itemText(i).lower()
            item_data = combo.itemData(i)
            
            # Match by product name
            if item_data and str(item_data).lower() == text:
                combo.setCurrentIndex(i)
                return
            
            # Match by full text
            if text in item_text:
                combo.setCurrentIndex(i)
                return

    def _refresh_table(self):
        table = self.findChild(QTableWidget, "tableWidget")
        if table:
            table.setRowCount(0)
            products = self.service.get_all_products()
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels(["ID", "Name", "Kategorie", "Bestand", "Preis", "Wert"])
            for row_idx, (product_id, product) in enumerate(products.items()):
                table.insertRow(row_idx)
                table.setItem(row_idx, 0, QTableWidgetItem(product_id))
                table.setItem(row_idx, 1, QTableWidgetItem(product.name))
                table.setItem(row_idx, 2, QTableWidgetItem(product.category))
                table.setItem(row_idx, 3, QTableWidgetItem(str(product.quantity)))
                table.setItem(row_idx, 4, QTableWidgetItem(f"{product.price:.2f}"))
                table.setItem(row_idx, 5, QTableWidgetItem(f"{product.get_total_value():.2f}"))

    def showEvent(self, event):
        self._refresh_table()
        self._load_products_into_combo()
        super().showEvent(event)

    def _on_table_row_clicked(self, index):
        """Wenn auf eine Tabellenzeile geklickt wird, Produkt in ComboBox auswählen."""
        table = self.findChild(QTableWidget, "tableWidget")
        combo = self.findChild(QComboBox, "comboBoxProduct")
        if not table or not combo:
            return

        row = index.row()
        product_id_item = table.item(row, 0)
        if product_id_item:
            product_id = product_id_item.text()
            # Finde den Index in der ComboBox anhand der userData
            for i in range(combo.count()):
                if combo.itemData(i) == product_id:
                    combo.setCurrentIndex(i)
                    break

    def _handle_incoming(self):
        self._process_movement("in")

    def _handle_outgoing(self):
        self._process_movement("out")

    def _process_movement(self, direction: str):
        combo = self.findChild(QComboBox, "comboBoxProduct")
        spin = self.findChild(QSpinBox, "spinBoxMenge")
        line = self.findChild(QLineEdit, "lineEditGrund")

        if not combo or not spin:
            QMessageBox.critical(self, "Fehler", "UI-Elemente nicht gefunden!")
            return

        # Try to get product ID from selection first
        product_id = combo.currentData()
        product_name = combo.currentText().split("(")[0].strip() if combo.currentText() else None
        
        # If no selection data, try to resolve from text input (user can type ID or name)
        if not product_id:
            user_input = combo.currentText().strip()
            if not user_input:
                QMessageBox.warning(self, "Fehler", "Bitte ein Produkt auswählen oder Produkt-ID eingeben.")
                return
            
            # Try to resolve the input (can be ID or name)
            product_id = self._resolve_product_id_from_input(user_input)
            if not product_id:
                QMessageBox.warning(self, "Fehler", f"Produkt '{user_input}' nicht gefunden.\nBitte gültige Produkt-ID oder Namen eingeben.")
                return
            
            # Get the product name from service
            try:
                products = self.service.get_all_products()
                if product_id in products:
                    product_name = products[product_id].name
                else:
                    product_name = user_input
            except:
                product_name = user_input

        quantity = spin.value()
        if quantity <= 0:
            QMessageBox.warning(self, "Fehler", "Bitte eine gültige Menge eingeben (min. 1).")
            return

        reason = line.text().strip() if line else ""

        try:
            if direction == "in":
                if not reason:
                    reason = "Wareneingang / Lieferung"
                self.service.add_stock(product_id, quantity, reason=reason)
                QMessageBox.information(
                    self, "✓ Erfolgreich",
                    f"{quantity} Stück eingebucht.\n\nProdukt: {product_name}"
                )
            else:  # out
                if not reason:
                    reason = "Verkauf"
                self.service.remove_stock(product_id, quantity, reason=reason)
                QMessageBox.information(
                    self, "✓ Erfolgreich",
                    f"{quantity} Stück ausgebucht.\n\nProdukt: {product_name}"
                )

            # Reset form
            spin.setValue(1)
            if line:
                line.clear()
            combo.setCurrentIndex(0)

            # Refresh display
            self._refresh_table()
            self._load_products_into_combo()

        except ValueError as ve:
            QMessageBox.warning(self, "Validierungsfehler", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler bei der Verarbeitung:\n{e}")

class KaufHistorieController(QMainWindow):
    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        self.base_dir = Path(__file__).resolve().parent
        uic.loadUi(str(self.base_dir / "kauf_historie_gui.ui"), self)
        self._setup_ui()

    def _setup_ui(self):
        back_btn = self.findChild(QPushButton, "pushButton")
        if back_btn:
            back_btn.clicked.connect(self._go_back)

        # Tabelle schreibgeschützt machen
        table = self.findChild(QTableWidget, "tableWidget")
        if table:
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self._refresh_table()

    def showEvent(self, event):
        self._refresh_table()
        super().showEvent(event)

    def _go_back(self):
        if self.parent():
            self.parent().show()
        self.close()

    def closeEvent(self, event):
        if self.parent():
            self.parent().show()
        event.accept()

    def _refresh_table(self):
        table = self.findChild(QTableWidget, "tableWidget")
        if table:
            table.setRowCount(0)
            movements = self.service.get_movements()
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["Produkt", "Typ", "Menge", "Grund", "Zeit"])
            for row_idx, movement in enumerate(movements[-10:]):  # Last 10
                table.insertRow(row_idx)
                table.setItem(row_idx, 0, QTableWidgetItem(movement.product_name))
                table.setItem(row_idx, 1, QTableWidgetItem(movement.movement_type))
                table.setItem(row_idx, 2, QTableWidgetItem(str(movement.quantity_change)))
                table.setItem(row_idx, 3, QTableWidgetItem(movement.reason))
                table.setItem(row_idx, 4, QTableWidgetItem(movement.timestamp.strftime('%Y-%m-%d %H:%M')))

class SupermarktMain(QMainWindow):
    """Voll integrierte Haupt-GUI mit .ui und Business Logic."""
    def __init__(self):
        super().__init__()
        print("SupermarktMain init...")
        self.base_dir = Path(__file__).resolve().parent
        print(f"UI base dir: {self.base_dir}")

        # MongoDB explizit aktivieren
        repo = RepositoryFactory.create_repository("mongodb")
        self.service = WarehouseService(repo)
        # Quick connectivity test
        self.service.get_all_products()
        print("MongoDB connected successfully")

        # Load sample products if the repository is empty.
        if not self.service.get_all_products():
            self.service.load_dummy_data()

        ui_path = self.base_dir / "haupt_gui.ui"
        print(f"Loading UI: {ui_path}")
        uic.loadUi(str(ui_path), self)
        self.setWindowTitle("Supermarkt Lagerverwaltung [MongoDB]")
        self.showMaximized()
        self.sub_windows = {}
        self._setup_main_buttons()



    def _setup_main_buttons(self):
        # Lagerbestand
        lager_btn = self.findChild(QPushButton, "pushButton")
        if lager_btn:
            lager_btn.clicked.connect(self.show_lagerbestand)

        # Lieferung
        liefer_btn = self.findChild(QPushButton, "pushButton_3")
        if liefer_btn:
            liefer_btn.clicked.connect(self.show_lieferung)

        # Random Käufe
        random_btn = self.findChild(QPushButton, "pushButton_2")
        if random_btn:
            random_btn.clicked.connect(self.show_random_purchases)

        # Kauf Historie
        kauf_btn = self.findChild(QPushButton, "pushButton_4")
        if kauf_btn:
            kauf_btn.clicked.connect(self.show_kauf_historie)

    def show_lagerbestand(self):
        if 'lager' not in self.sub_windows:
            self.sub_windows['lager'] = LagerbestandController(self.service, self)
        self.sub_windows['lager'].show()
        self.hide()

    def show_lieferung(self):
        if 'lieferung' not in self.sub_windows:
            self.sub_windows['lieferung'] = LieferungController(self.service, self)
        self.sub_windows['lieferung'].show()
        self.hide()

    def show_random_purchases(self):
        if not self.service.get_all_products():
            QMessageBox.warning(self, "Keine Produkte", "Es sind keine Produkte vorhanden, um zufällige Käufe zu erzeugen.")
            return

        product_list = [p for p in self.service.get_all_products().items() if p[1].quantity > 0]
        if not product_list:
            QMessageBox.warning(self, "Kein Lagerbestand", "Es sind keine Vorräte vorhanden, um Verkäufe zu erzeugen.")
            return

        for _ in range(min(5, len(product_list))):
            pid, product = random.choice(product_list)
            quantity = random.randint(1, min(3, product.quantity))
            try:
                self.service.remove_stock(pid, quantity, reason="Random Kauf")
            except ValueError:
                # überspringen, wenn nicht möglich
                continue

        QMessageBox.information(self, "Random Käufe", "Zufällige Käufe wurden erzeugt und in der Kaufhistorie gespeichert.")
        self.show_kauf_historie()

    def show_kauf_historie(self):
        if 'kauf' not in self.sub_windows:
            self.sub_windows['kauf'] = KaufHistorieController(self.service, self)
        self.sub_windows['kauf'].show()
        self.hide()

def main():
    print("Starting Supermarkt GUI...")
    app = QApplication(sys.argv)
    window = SupermarktMain()
    window.showMaximized()
    print("GUI shown")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

