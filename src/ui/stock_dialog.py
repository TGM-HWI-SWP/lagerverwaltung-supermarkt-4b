from PyQt6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QPushButton, QLineEdit, QSpinBox, QLabel  # importiert alle benötigten GUI Elemente

class StockDialog(QDialog):  # Dialogfenster für Bestandsänderungen
    def __init__(self, parent=None, product_id='', operation='add'):  # Konstruktor mit optionalen Parametern
        super().__init__(parent)  # ruft den Konstruktor der Elternklasse auf
        self.setWindowTitle(f"Bestand {operation.upper()} für {product_id}")  # setzt Fenstertitel dynamisch
        self.setGeometry(100, 100, 350, 200)  # positioniert und dimensioniert das Fenster

        layout = QFormLayout()  # erstellt ein Formular Layout für Labels und Eingabefelder

        self.product_id_label = QLabel(product_id)  # zeigt die Produkt ID an
        self.quantity_field = QSpinBox(minimum=1)  # Eingabefeld für Menge mit Minimum 1
        self.reason_field = QLineEdit("UI Operation")  # Eingabefeld für Grund mit Default Text

        layout.addRow("Produkt-ID:", self.product_id_label)  # fügt Zeile mit Label hinzu
        layout.addRow("Menge:", self.quantity_field)  # fügt Menge Eingabe hinzu
        layout.addRow("Grund:", self.reason_field)  # fügt Grund Eingabe hinzu

        button_layout = QHBoxLayout()  # horizontaler Layout für Buttons
        ok_btn = QPushButton("OK")  # Bestätigungsbutton
        cancel_btn = QPushButton("Abbrechen")  # Abbruchbutton
        ok_btn.clicked.connect(self.accept)  # verbindet OK mit Dialog Annahme
        cancel_btn.clicked.connect(self.reject)  # verbindet Abbrechen mit Dialog Ablehnung
        button_layout.addWidget(ok_btn)  # fügt OK Button zum Layout hinzu
        button_layout.addWidget(cancel_btn)  # fügt Abbrechen Button zum Layout hinzu

        layout.addRow(button_layout)  # fügt Button Reihe zum Formular hinzu
        self.setLayout(layout)  # aktiviert das Layout im Dialog

    def get_data(self, operation):  # Methode zum Auslesen der Benutzereingaben
        return {
            'product_id': self.product_id_label.text(),  # gibt eingegebene Produkt ID zurück
            'quantity': self.quantity_field.value(),  # gibt eingegebene Menge zurück
            'reason': self.reason_field.text(),  # gibt eingegebenen Grund zurück
            'operation': operation  # gibt Operationstyp zurück
        }

