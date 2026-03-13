class Product:

    def __init__(self, product_id, name, description, price, category, quantity):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.quantity = quantity
        self.min_stock = 5


    def add_stock(self, amount):
        self.quantity += amount


    def remove_stock(self, amount):
        self.quantity -= amount
        if self.quantity < 0:
            self.quantity = 0


    def change_price(self, new_price):
        self.price = new_price


    def is_low_stock(self):
        return self.quantity <= self.min_stock