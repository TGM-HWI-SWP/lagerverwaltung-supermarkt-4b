from src.domain.product import Product  # Domain-Klasse für Produktobjekte
from pymongo import MongoClient  # MongoDB Client für DB-Verbindung


class MongoDBProductRepository:
    """
    MongoDB-Adapter für Product-Objekte.
    Speichert, lädt und löscht Produkte in MongoDB.
    """

    def __init__(self, mongo_uri: str, db_name: str = "supermarkt_db") -> None:  # Konstruktor: baut DB-Verbindung auf
        self.client = MongoClient(mongo_uri)  # erstellt Verbindung zur MongoDB (inkl. Authentifizierung über URI)
        self.db = self.client[db_name]  # wählt Datenbank aus
        self.collection = self.db["products"]  # greift auf "products" Collection zu

    def save_product(self, product: Product) -> None:
        self.collection.update_one(  # aktualisiert vorhandenes Dokument oder erstellt neues
            {"id": product.id},  # Filter: sucht Produkt anhand eigener ID (nicht Mongo _id)
            {
                "$set": {  # MongoDB Operator: setzt/überschreibt Felder im Dokument
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
            upsert=True  # falls kein Dokument existiert → neu erstellen (insert + update kombiniert)
        )

    def load_product_by_id(self, product_id: str) -> Product | None:  # gibt Product zurück oder None wenn nicht gefunden
        doc = self.collection.find_one({"id": product_id})  # sucht genau ein Dokument mit passender ID

        if doc is None:  # prüft ob kein Ergebnis gefunden wurde
            return None

        product = Product(  # erstellt Domain-Objekt aus DB-Daten
            doc["id"],
            doc["name"],
            doc["description"],
            doc["price"],
            doc.get("category", ""),  # .get verhindert Fehler falls Feld fehlt (Default "")
            doc["quantity"],
            doc.get("min_stock", 5)  # Default Mindestbestand = 5 falls nicht vorhanden
        )

        product.id = doc["id"]  # redundantes Setzen (Absicherung falls Konstruktor anders arbeitet)
        product.product_id = doc["id"]  # zweite ID-Referenz (Designentscheidung)
        product.sku = doc.get("sku", "")  # optionales Feld mit Default
        product.notes = doc.get("notes", "")
        product.created_at = doc.get("created_at")  # kann None sein wenn nicht gesetzt
        product.updated_at = doc.get("updated_at")

        return product

    def load_all_products(self) -> list[Product]:  # lädt alle gültigen Produkte aus DB
        products = []

        for doc in self.collection.find():  # iteriert über alle Dokumente der Collection
            if "id" not in doc:
                continue  # überspringt ungültige Datensätze ohne Pflichtfeld
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

            product = Product(  # erstellt Produktobjekt aus validiertem Dokument
                doc["id"],
                doc["name"],
                doc["description"],
                doc["price"],
                doc.get("category", ""),
                doc["quantity"],
                doc.get("min_stock", 5)
            )

            product.id = doc["id"]  # stellt sicher, dass ID korrekt gesetzt ist
            product.product_id = doc["id"]
            product.sku = doc.get("sku", "")
            product.notes = doc.get("notes", "")
            product.created_at = doc.get("created_at")
            product.updated_at = doc.get("updated_at")

            products.append(product)  # fügt fertiges Objekt zur Ergebnisliste hinzu

        return products  # gibt Liste aller gültigen Produkte zurück