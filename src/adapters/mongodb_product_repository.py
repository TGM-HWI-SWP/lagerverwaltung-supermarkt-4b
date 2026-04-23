from src.domain.product import Product
from pymongo import MongoClient


class MongoDBProductRepository:
    """
    MongoDB-Adapter für Product-Objekte.
    Speichert, lädt und löscht Produkte in MongoDB.
    """

    def __init__(self, mongo_uri: str, db_name: str = "supermarkt_db") -> None:
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db["products"]

    def save_product(self, product: Product) -> None:
        self.collection.update_one(
            {"id": product.id},
            {
                "$set": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "quantity": product.quantity,
                    "min_stock": product.min_stock,
                    "sku": product.sku,
                    "category": product.category,
                    "created_at": product.created_at,
                    "updated_at": product.updated_at,
                    "notes": product.notes,
                }
            },
            upsert=True
        )

    def load_product_by_id(self, product_id: str) -> Product | None:
        doc = self.collection.find_one({"id": product_id})

        if doc is None:
            return None

        product = Product(
            doc["id"],
            doc["name"],
            doc["description"],
            doc["price"],
            doc.get("category", ""),
            doc["quantity"],
            doc.get("min_stock", 5)
        )

        product.id = doc["id"]
        product.product_id = doc["id"]
        product.sku = doc.get("sku", "")
        product.notes = doc.get("notes", "")
        product.created_at = doc.get("created_at")
        product.updated_at = doc.get("updated_at")

        return product

    def load_all_products(self) -> list[Product]:
        products = []

        for doc in self.collection.find():
            if "id" not in doc:
                continue
            if "name" not in doc:
                continue
            if "description" not in doc:
                continue
            if "price" not in doc:
                continue
            if "quantity" not in doc:
                continue
            if "created_at" not in doc:
                continue
            if "updated_at" not in doc:
                continue

            product = Product(
                doc["id"],
                doc["name"],
                doc["description"],
                doc["price"],
                doc.get("category", ""),
                doc["quantity"],
                doc.get("min_stock", 5)
            )

            product.id = doc["id"]
            product.product_id = doc["id"]
            product.sku = doc.get("sku", "")
            product.notes = doc.get("notes", "")
            product.created_at = doc.get("created_at")
            product.updated_at = doc.get("updated_at")

            products.append(product)

        return products