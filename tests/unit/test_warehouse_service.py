import pytest
from src.services import WarehouseService
from src.adapters.repository import RepositoryFactory

class TestWarehouseService:
    @pytest.fixture
    def service(self):
        repo = RepositoryFactory.create()
        return WarehouseService(repo)

    def test_create_product(self, service):
        product = service.create_product(
            'P001', 'Testprodukt', 'Test', 10.0, 'Test', 5
        )
        assert product.product_id == 'P001'
        assert product.quantity == 5

    def test_add_stock(self, service):
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 5)
        movement = service.add_stock('P001', 10, 'Test', 'testuser')
        assert movement.quantity_change == 10
        product = service.get_product('P001')
        assert product.quantity == 15

    def test_remove_stock(self, service):
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 10)
        movement = service.remove_stock('P001', 3, 'Verkauf', 'testuser')
        assert movement.quantity_change == -3
        product = service.get_product('P001')
        assert product.quantity == 7

    def test_remove_insufficient(self, service):
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 5)
        with pytest.raises(ValueError):
            service.remove_stock('P001', 6)

    def test_low_stock(self, service):
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 2)
        service.create_product('P002', 'Test', 'Test', 10.0, 'Test', 10)
        low = service.get_low_stock_products()
        assert len(low) == 1
        assert low[0].quantity == 2

    def test_total_value(self, service):
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 5)
        service.create_product('P002', 'Test', 'Test', 20.0, 'Test', 3)
        assert service.get_total_inventory_value() == 110.0

    def test_movements(self, service):
        service.create_product('P001', 'Test', 'Test', 10.0, 'Test', 5)
        service.add_stock('P001', 5)
        movements = service.get_movements()
        assert len(movements) == 2
