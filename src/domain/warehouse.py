from src.domain.product import Product


class WarehouseService:

    def __init__(self, repository):
        self.repository = repository


    def create_product(self, product_id, name, description, price, category, quantity):

        product = Product(
            product_id,
            name,
            description,
            price,
            category,
            quantity
        )

        self.repository.add(product)

        return product


    def add_stock(self, product_id, amount):

        product = self.repository.get(product_id)

        if product:
            product.add_stock(amount)
            self.repository.update(product)


    def remove_stock(self, product_id, amount):

        product = self.repository.get(product_id)

        if product:
            product.remove_stock(amount)
            self.repository.update(product)


    def delete_product(self, product_id):
        self.repository.delete(product_id)


    def get_low_stock_products(self):

        products = self.repository.get_all()

        result = []

        for p in products:
            if p.is_low_stock():
                result.append(p)

        return result


    def get_total_inventory_value(self):

        products = self.repository.get_all()

        total = 0

        for p in products:
            total += p.price * p.quantity

        return total


    def get_products_by_category(self, category):

        products = self.repository.get_all()

        result = []

        for p in products:
            if p.category == category:
                result.append(p)

        return result