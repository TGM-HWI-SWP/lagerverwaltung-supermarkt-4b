from PyQt6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QPushButton, QLineEdit, QSpinBox, QLabel

class StockDialog(QDialog):
    def __init__(self, parent=None, product_id='', operation='add'):
        super().__init__(parent)
        self.setWindowTitle(f"Bestand {operation.upper()} für {product_id}")
        self.setGeometry(100, 100, 350, 200)

        layout = QFormLayout()

        self.product_id_label = QLabel(product_id)
        self.quantity_field = QSpinBox(minimum=1)
        self.reason_field = QLineEdit("UI Operation")

        layout.addRow("Produkt-ID:", self.product_id_label)
        layout.addRow("Menge:", self.quantity_field)
        layout.addRow("Grund:", self.reason_field)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Abbrechen")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addRow(button_layout)
        self.setLayout(layout)

    def get_data(self, operation):
        return {
            'product_id': self.product_id_label.text(),
            'quantity': self.quantity_field.value(),
            'reason': self.reason_field.text(),
            'operation': operation
        }
