from src.domain.movement import Movement  # Import der Domain-Klasse für Typisierung und Datenstruktur
from pymongo import MongoClient  # MongoDB Client zum Verbinden mit der Datenbank


class MongoDBMovementRepository:
    """
    MongoDB-Adapter für Lagerbewegungen.
    Speichert und lädt Movement-Objekte in MongoDB.
    """

    def __init__(self, mongo_uri: str, db_name: str = "supermarkt_db") -> None: # Konstruktor: stellt DB-Verbindung her und initialisiert Attribute
        self.client = MongoClient(mongo_uri)  # baut Verbindung zur MongoDB über URI auf (inkl. Authentifizierung)
        self.db = self.client[db_name]  # wählt die Datenbank anhand des Namens aus
        self.collection = self.db["movements"]  # greift auf die Collection "movements" zu (vergleichbar mit Tabelle)

    def save_movement(self, movement: Movement) -> None:
        """
        Speichert eine Lagerbewegung in MongoDB.
        """
        self.collection.insert_one({  # fügt ein neues Dokument in die Collection ein (kein Update, immer neu)
            "movement_id": movement.movement_id,  # eigene ID statt MongoDB _id (wichtig für Domain-Logik)
            "product_id": movement.product_id,  # Referenz zum Produkt (Foreign Key ähnliche Funktion)
            "product_name": movement.product_name,
            "movement_type": movement.movement_type,  # z.B. IN, OUT → wichtig für Auswertung
            "old_quantity": movement.old_quantity,  # Bestand vor der Änderung (Audit/Nachvollziehbarkeit)
            "quantity_change": movement.quantity_change,  # Änderung (+/-)
            "new_quantity": movement.new_quantity,  # neuer Bestand nach der Änderung
            "note": movement.note,
            "created_at": movement.created_at,  # Zeitpunkt der Bewegung (wichtig für Logs/Reports)
        })

    def load_all_movements(self) -> list[dict]:
        """
        Lädt alle Bewegungen aus MongoDB.
        """
        return list(self.collection.find({}, {"_id": 0}))  # {} = kein Filter → alle Dokumente; {"_id": 0} entfernt MongoDB Standard-ID

    def load_movements_by_product_id(self, product_id: str) -> list[dict]:  # lädt alle Bewegungen für ein bestimmtes Produkt (gefiltert nach product_id)
        """
        Lädt alle Bewegungen eines bestimmten Produkts.
        """
        return list(self.collection.find({"product_id": product_id}, {"_id": 0}))  # Filter nach product_id; Projektion entfernt _id