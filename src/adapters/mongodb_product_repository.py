from pymongo import MongoClient
from src.domain.product import Product


class MongoDBProductRepository:
    """
    MongoDB-Adapter für die Product-Objekte.
    Speichert, lädt und löscht Produkte in MongoDB.
    """

    def __init__(self, mongo_uri: str, db_name: str = "supermarkt_db") -> None:
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db["products"]

    def save_product(self, product: Product) -> None:
        """
        Speichert ein Produkt in MongoDB.
        Falls die Produkt-ID schon existiert, wird der Datensatz aktualisiert.
        """
        self.collection.update_one(
            {"id": product.id},
            {
                "$set": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "quantity": product.quantity,
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
        """
        Lädt ein Produkt anhand seiner ID.
        """
        doc = self.collection.find_one({"id": product_id})

        if doc is None:
            return None

        return Product(
            id=doc["id"],
            name=doc["name"],
            description=doc["description"],
            price=doc["price"],
            quantity=doc["quantity"],
            sku=doc.get("sku", ""),
            category=doc.get("category", ""),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
            notes=doc.get("notes")
        )

    def load_all_products(self) -> list[Product]:
        """
        Lädt alle gültigen Produkte aus MongoDB.
        Alte oder unvollständige Dokumente ohne Pflichtfelder werden übersprungen.
        """
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

            products.append(
                Product(
                    id=doc["id"],
                    name=doc["name"],
                    description=doc["description"],
                    price=doc["price"],
                    quantity=doc["quantity"],
                    sku=doc.get("sku", ""),
                    category=doc.get("category", ""),
                    created_at=doc["created_at"],
                    updated_at=doc["updated_at"],
                    notes=doc.get("notes")
                )
            )

        return products

