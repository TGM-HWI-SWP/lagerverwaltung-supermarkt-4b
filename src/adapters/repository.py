class InMemoryRepository:

    def __init__(self):
        self.products = {}

    def add(self, product):
        self.products[product.product_id] = product

    def get(self, product_id):
        return self.products.get(product_id)

    def update(self, product):
        self.products[product.product_id] = product

    def delete(self, product_id):
        if product_id in self.products:
            del self.products[product_id]

    def get_all(self):
        return list(self.products.values())