from PyQt6.QtWidgets import (
    QMainWindow, QComboBox, QTableWidget,
    QTableWidgetItem, QPushButton, QSpinBox,
    QLineEdit, QMessageBox
)
from PyQt6 import uic


class LieferungWindow(QMainWindow):
    def __init__(self, service, ui_path):
        super().__init__()
        uic.loadUi(ui_path, self)

        self.service = service

        # Widgets holen
        self.combo = self.findChild(QComboBox, "comboBoxProduct")
        self.table = self.findChild(QTableWidget, "tableWidget")
        self.spin = self.findChild(QSpinBox, "spinBoxMenge")
        self.grund = self.findChild(QLineEdit, "lineEditGrund")

        self.btn_ein = self.findChild(QPushButton, "pushButtonEinbuchen")
        self.btn_aus = self.findChild(QPushButton, "pushButtonAusbuchen")

        # Daten laden
        self._load_products()
        self._load_table()

        # Events
        self.combo.currentIndexChanged.connect(self.on_product_selected)
        self.btn_ein.clicked.connect(self.einbuchen)
        self.btn_aus.clicked.connect(self.ausbuchen)

    def _load_products(self):
        self.combo.clear()
        products = self.service.get_all_products()

        for pid, p in products.items():
            self.combo.addItem(p.name, pid)

    def _load_table(self):
        products = self.service.get_all_products()

        self.table.setRowCount(len(products))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Kategorie", "Menge", "Preis"]
        )

        for row, (pid, p) in enumerate(products.items()):
            self.table.setItem(row, 0, QTableWidgetItem(pid))
            self.table.setItem(row, 1, QTableWidgetItem(p.name))
            self.table.setItem(row, 2, QTableWidgetItem(p.category))
            self.table.setItem(row, 3, QTableWidgetItem(str(p.quantity)))
            self.table.setItem(row, 4, QTableWidgetItem(f"{p.price:.2f}"))

    def on_product_selected(self):
        print(self.combo.currentData())

    def einbuchen(self):
        pid = self.combo.currentData()
        menge = self.spin.value()
        grund = self.grund.text()

        try:
            self.service.add_stock(pid, menge, grund)
            QMessageBox.information(self, "OK", "Eingebucht")
            self._load_table()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))

    def ausbuchen(self):
        pid = self.combo.currentData()
        menge = self.spin.value()
        grund = self.grund.text()

        try:
            self.service.remove_stock(pid, menge, grund)
            QMessageBox.information(self, "OK", "Ausgebucht")
            self._load_table()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))

