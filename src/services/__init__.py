class WarehouseService:
    def __init__(self, repository_type="memory"):
        self.repository = RepositoryFactory.create_repository(repository_type)
        self.products = {}  # nur für Testzwecke

    def create_product(self, product_id, name, description, price, category, initial_quantity):
        self.products[product_id] = {
            "name": name,
            "description": description,
            "price": price,
            "category": category,
            "quantity": initial_quantity
        }

    def add_to_stock(self, product_id, quantity, reason, user):
        self.products[product_id]["quantity"] += quantity

    def remove_from_stock(self, product_id, quantity, reason, user):
        self.products[product_id]["quantity"] -= quantity

    def get_total_inventory_value(self):
        return sum(p["quantity"] * p["price"] for p in self.products.values())

    def get_low_stock_products(self, min_quantity):
        return {pid: p for pid, p in self.products.items() if p["quantity"] < min_quantity}

    def generate_inventory_report(self):
        report = "LAGERBESTAND\n"
        for pid, p in self.products.items():
            report += f"{p['name']} → {p['quantity']} → {p['quantity']*p['price']}€\n"
        report += f"GESAMTWERT → {self.get_total_inventory_value()}€"
        return report