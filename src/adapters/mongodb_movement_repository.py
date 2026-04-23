from src.MONGO.mongo_movements import Movement
from pymongo import MongoClient


class MongoDBMovementRepository:
    """
    MongoDB-Adapter für Lagerbewegungen.
    Speichert und lädt Movement-Objekte in MongoDB.
    """

    def __init__(self, mongo_uri: str, db_name: str = "supermarkt_db") -> None:
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db["movements"]

    def save_movement(self, movement: Movement) -> None:
        """
        Speichert eine Lagerbewegung in MongoDB.
        """
        self.collection.insert_one({
            "movement_id": movement.movement_id,
            "product_id": movement.product_id,
            "product_name": movement.product_name,
            "movement_type": movement.movement_type,
            "old_quantity": movement.old_quantity,
            "quantity_change": movement.quantity_change,
            "new_quantity": movement.new_quantity,
            "note": movement.note,
            "created_at": movement.created_at,
        })

    def load_all_movements(self) -> list[dict]:
        """
        Lädt alle Bewegungen aus MongoDB.
        """
        return list(self.collection.find({}, {"_id": 0}))

    def load_movements_by_product_id(self, product_id: str) -> list[dict]:
        """
        Lädt alle Bewegungen eines bestimmten Produkts.
        """
        return list(self.collection.find({"product_id": product_id}, {"_id": 0}))