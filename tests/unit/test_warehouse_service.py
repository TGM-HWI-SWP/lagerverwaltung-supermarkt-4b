import pytest  # Test Framework
from src.services import WarehouseService  # zu testender Service
from src.adapters.repository import RepositoryFactory  # Factory für Test Repository

class TestWarehouseService:  # Testklasse für WarehouseService
    @pytest.fixture  # Pytest Fixture für wiederkehrende Initialisierung
    def service(self):  # erzeugt frischen Service für jeden Test
        repo = RepositoryFactory.create()  # erstellt Standard Repository
        return WarehouseService(repo)  # gibt Service mit Repository zurück

    def test_create_product(self, service):  # Test für Produkterstellung
        product = service.create_product(
            'P001', 'Testprodukt', 'Test', 10.0, 'Test', 5
        )
        assert product.product_id == 'P001'  # prüft ob ID korrekt ist
        assert product.quantity == 5  # prüft ob Startmenge korrekt ist

    def test_add_stock(self, service):  # Test für Einbuchung
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 5)  # erzeugt Produkt mit Menge 5
        movement = service.add_stock('P001', 10, 'Test', 'testuser')  # bucht 10 Stück dazu
        assert movement.quantity_change == 10  # erwartet positive Änderung
        product = service.get_product('P001')  # lädt aktualisiertes Produkt
        assert product.quantity == 15  # erwartet neue Gesamtmenge 15

    def test_remove_stock(self, service):  # Test für Ausbuchung
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 10)  # erzeugt Produkt mit Menge 10
        movement = service.remove_stock('P001', 3, 'Verkauf', 'testuser')  # bucht 3 Stück aus
        assert movement.quantity_change == -3  # erwartet negative Änderung
        product = service.get_product('P001')  # lädt aktualisiertes Produkt
        assert product.quantity == 7  # erwartet neue Gesamtmenge 7

    def test_remove_insufficient(self, service):  # Test für Überentnahme
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 5)  # erzeugt Produkt mit Menge 5
        with pytest.raises(ValueError):  # erwartet Fehler bei Entnahme von 6
            service.remove_stock('P001', 6)

    def test_low_stock(self, service):  # Test für Niedrigbestand Filter
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 2)  # unter Minimum
        service.create_product('P002', 'Test', 'Test', 10.0, 'Test', 10)  # über Minimum
        low = service.get_low_stock_products()  # fragt Produkte mit niedrigem Bestand ab
        assert len(low) == 1  # erwartet genau ein Produkt
        assert low[0].quantity == 2  # erwartet das Produkt mit Menge 2

    def test_total_value(self, service):  # Test für Gesamtwert Berechnung
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 5)  # Wert 50
        service.create_product('P002', 'Test', 'Test', 20.0, 'Test', 3)  # Wert 60
        assert service.get_total_inventory_value() == 110.0  # erwartet Summe 110

    def test_movements(self, service):  # Test für Bewegungshistorie
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 5)  # erzeugt Initiale Bewegung
        service.add_stock('P001', 5)  # erzeugt zweite Bewegung
        movements = service.get_movements()  # lädt alle Bewegungen
        assert len(movements) == 2  # erwartet zwei Bewegungen

