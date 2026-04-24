import pytest  # Test Framework
from src.domain.product import Product  # zu testende Produkt Klasse
from src.domain.movement import Movement  # zu testende Movement Klasse

class TestProduct:  # Testklasse für Product
    def test_creation_valid(self):  # Test für erfolgreiche Erstellung
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 5)  # erzeugt gültiges Produkt
        assert p.product_id == 'P001'  # prüft ob ID korrekt gesetzt wurde
        assert p.price == 10.0  # prüft ob Preis korrekt gesetzt wurde
        assert p.quantity == 5  # prüft ob Menge korrekt gesetzt wurde

    def test_creation_negative_price(self):  # Test für ungültigen Preis
        with pytest.raises(ValueError):  # erwartet Fehler bei negativem Preis
            Product('P001', 'Test', 'Desc', -1.0, 'Cat', 5)

    def test_update_quantity_increase(self):  # Test für Bestandserhöhung
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 5)  # Startbestand 5
        movement = p.update_quantity(5, 'add', 'user')  # fügt 5 hinzu
        assert p.quantity == 10  # erwartet neuen Bestand 10
        assert movement.movement_type == 'IN'  # erwartet Bewegungstyp IN

    def test_update_quantity_decrease(self):  # Test für Bestandsminderung
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 10)  # Startbestand 10
        movement = p.update_quantity(-3, 'sale', 'user')  # entfernt 3
        assert p.quantity == 7  # erwartet neuen Bestand 7
        assert movement.movement_type == 'OUT'  # erwartet Bewegungstyp OUT

    def test_update_quantity_negative_fail(self):  # Test für ungültige Überentnahme
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 2)  # Startbestand 2
        with pytest.raises(ValueError):  # erwartet Fehler weil 5 entnommen werden sollen
            p.update_quantity(-5, 'sale', 'user')

    def test_get_total_value(self):  # Test für Gesamtwert Berechnung
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 5)  # Preis 10 Menge 5
        assert p.get_total_value() == 50.0  # erwartet Gesamtwert 50

    def test_low_stock(self):  # Test für Mindestbestand Erkennung
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 3)  # Menge 3 Minimum 5
        assert p.is_low_stock() == True  # erwartet True weil unter Minimum

class TestMovement:  # Testklasse für Movement
    def test_creation(self):  # Test für Erstellung
        from datetime import datetime  # lokaler Import für Zeitstempel
        m = Movement('P001', 'Test', 5, 'IN', 'stock', datetime.now(), 'user')  # erzeugt Bewegung
        assert m.product_id == 'P001'  # prüft Produkt ID
        assert m.quantity_change == 5  # prüft Mengenänderung

