import pytest
from src.domain.product import Product
from src.domain.movement import Movement

class TestProduct:
    def test_creation_valid(self):
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 5)
        assert p.product_id == 'P001'
        assert p.price == 10.0
        assert p.quantity == 5

    def test_creation_negative_price(self):
        with pytest.raises(ValueError):
            Product('P001', 'Test', 'Desc', -1.0, 'Cat', 5)

    def test_update_quantity_increase(self):
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 5)
        movement = p.update_quantity(5, 'add', 'user')
        assert p.quantity == 10
        assert movement.movement_type == 'IN'

    def test_update_quantity_decrease(self):
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 10)
        movement = p.update_quantity(-3, 'sale', 'user')
        assert p.quantity == 7
        assert movement.movement_type == 'OUT'

    def test_update_quantity_negative_fail(self):
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 2)
        with pytest.raises(ValueError):
            p.update_quantity(-5, 'sale', 'user')

    def test_get_total_value(self):
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 5)
        assert p.get_total_value() == 50.0

    def test_low_stock(self):
        p = Product('P001', 'Test', 'Desc', 10.0, 'Cat', 3)
        assert p.is_low_stock() == True

class TestMovement:
    def test_creation(self):
        m = Movement('P001', 'Test', 5, 'IN', 'stock', datetime.now(), 'user')
        assert m.product_id == 'P001'
        assert m.quantity_change == 5
