"""Unified Main Controller - Combines .ui buttons with full business logic integration."""

import sys
from pathlib import Path
from typing import Dict
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QTableWidget, QPushButton, QAbstractItemView, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import uic

ROOT_DIR = Path(__file__).resolve().parents[1]

try:
    from src.adapters.repository import RepositoryFactory
    from src.services import WarehouseService
except ImportError:
    sys.path.insert(0, str(ROOT_DIR))
    from src.adapters.repository import RepositoryFactory
    from src.services import WarehouseService

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
            back_btn.clicked.connect(self.close)
        self._refresh_table()

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
            back_btn.clicked.connect(self.close)
        self._refresh_table()

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
            back_btn.clicked.connect(self.close)
        self._refresh_table()

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
        self.base_dir = Path(__file__).resolve().parent
        self.service = WarehouseService()
        uic.loadUi(str(self.base_dir / "haupt_gui.ui"), self)
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

    def show_kauf_historie(self):
        if 'kauf' not in self.sub_windows:
            self.sub_windows['kauf'] = KaufHistorieController(self.service, self)
        self.sub_windows['kauf'].show()
        self.hide()

def main():
    app = QApplication(sys.argv)
    window = SupermarktMain()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
