from src.adapters.repository import RepositoryFactory

class WarehouseService:
    def __init__(self, repository_type="memory"):
        self.repository = RepositoryFactory.create_repository(repository_type)

    def create_product(self, product_id, name, description, price, category, initial_quantity):
        # Produkt erstellen und speichern
        pass

    def add_to_stock(self, product_id, quantity, reason, user):
        pass

    def remove_from_stock(self, product_id, quantity, reason, user):
        pass

    def get_total_inventory_value(self):
        pass

    def get_low_stock_products(self, min_quantity):
        pass

    def generate_inventory_report(self):
        pass