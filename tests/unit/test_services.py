from src.services import WarehouseService

def test_add_to_stock():
    service = WarehouseService("memory")
    service.create_product("P001", "Laptop", "High-End", 1200.0, "Elektronik", 5)
    service.add_to_stock("P001", 3, reason="Einkauf", user="Max")
    product = service.repository.get_product("P001")
    assert product.quantity == 8