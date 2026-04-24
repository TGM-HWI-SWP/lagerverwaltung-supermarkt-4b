import uuid  # für eindeutige IDs bei Bewegungen
from datetime import datetime  # für Zeitstempel
from typing import Dict, List, Optional  # Typisierung
from src.ports.repository_port import RepositoryPort  # Schnittstelle die implementiert wird
from src.domain.product import Product  # Domain Objekt
from src.domain.movement import Movement  # Domain Objekt
from .mongodb_product_repository import MongoDBProductRepository  # MongoDB Produkt Repository
from .mongodb_movement_repository import MongoDBMovementRepository  # MongoDB Bewegungs Repository
from src.MONGO.mongo_test import MONGO_URI  # Verbindungsstring zur Datenbank

class InMemoryRepository(RepositoryPort):  # RAM basierte Implementierung für Tests
    """In-memory implementation for testing and quick starts."""

    def __init__(self):
        self._products: Dict[str, Product] = {}  # internes Dictionary für Produkte
        self._movements: List[Movement] = []  # interne Liste für Bewegungen

    def add(self, product: Product) -> None:
        self._products[product.product_id] = product  # speichert oder überschreibt Produkt
        # Log initial stock
        initial_movement = Movement(
            product_id=product.product_id,  # ID des neuen Produkts
            product_name=product.name,  # Name des neuen Produkts
            quantity_change=product.quantity,  # Startbestand als Bewegung
            movement_type="INITIAL",  # Typ für Erstbefüllung
            reason="Initial stock",  # Grund für Initialbewegung
            performed_by="system"  # System hat initialen Bestand erzeugt
        )
        self._movements.append(initial_movement)  # fügt Initiale Bewegung zur Historie hinzu

    def get(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)  # gibt Produkt zurück oder None

    def get_all(self) -> Dict[str, Product]:
        return self._products.copy()  # gibt Kopie zurück damit externe Änderungen interne Daten nicht beeinflussen

    def delete(self, product_id: str) -> None:
        if product_id in self._products:
            del self._products[product_id]  # entfernt Produkt aus Dictionary

    def save_movement(self, movement: Movement) -> None:
        self._movements.append(movement)  # fügt Bewegung zur Liste hinzu

    def get_movements(self) -> List[Movement]:
        return self._movements.copy()  # gibt Kopie der Bewegungsliste zurück


class MongoDBRepository(RepositoryPort):  # Produktive MongoDB Implementierung
    """MongoDB implementation for production data."""

    def __init__(self):
        self.product_repo = MongoDBProductRepository(MONGO_URI)  # initialisiert Produkt Repository
        self.movement_repo = MongoDBMovementRepository(MONGO_URI)  # initialisiert Bewegungs Repository

    def add(self, product: Product) -> None:
        self.product_repo.save_product(product)  # speichert Produkt in MongoDB

    def get(self, product_id: str) -> Optional[Product]:
        return self.product_repo.load_product_by_id(product_id)  # lädt Produkt aus MongoDB

    def get_all(self) -> Dict[str, Product]:
        products_list = self.product_repo.load_all_products()  # lädt alle Produkte als Liste
        return {p.id: p for p in products_list}  # wandelt Liste in Dictionary mit ID als Schlüssel um

    def delete(self, product_id: str) -> None:
        # MongoDB hat kein direktes delete im Produkt Repository daher Soft Delete
        product = self.get(product_id)  # lädt Produkt
        if product:
            product.quantity = 0  # setzt Bestand auf Null
            product.category = "DELETED"  # markiert als gelöscht
            self.product_repo.save_product(product)  # speichert geändertes Produkt

    def save_movement(self, movement: Movement) -> None:
        movement_id = movement.id if movement.id is not None else str(uuid.uuid4())  # erzeugt UUID falls keine ID vorhanden
        timestamp = movement.timestamp if movement.timestamp is not None else datetime.now()  # nutzt aktuelle Zeit falls keine Zeit vorhanden
        mongo_movement = {
            "movement_id": movement_id,  # eindeutige Bewegungs ID
            "product_id": movement.product_id,  # Referenz zum Produkt
            "product_name": movement.product_name or movement.product_id,  # Name oder Fallback auf ID
            "movement_type": movement.movement_type,  # Art der Bewegung
            "old_quantity": 0,  # alter Bestand wird hier nicht berechnet
            "quantity_change": movement.quantity_change,  # Mengenänderung
            "new_quantity": 0,  # neuer Bestand wird hier nicht berechnet
            "note": movement.reason,  # Grund wird als Note gespeichert
            "created_at": timestamp,  # Zeitstempel
        }
        self.movement_repo.collection.insert_one(mongo_movement)  # fügt Dokument in MongoDB Collection ein
        # Hinweis: Movement Klasse aus MONGO Modul kann abweichen daher Anpassung bei Fehler

    def get_movements(self) -> List[Movement]:
        raw_movements = self.movement_repo.load_all_movements()  # lädt alle Rohdaten aus MongoDB
        movements = []
        for raw in raw_movements:  # iteriert über alle geladenen Dokumente
            # created_at aus MongoDB ist BSON datetime Objekt kein String
            created_at = raw.get("created_at")
            if isinstance(created_at, datetime):
                timestamp = created_at  # verwendet direkt wenn schon datetime
            elif isinstance(created_at, str):
                timestamp = datetime.fromisoformat(created_at.replace('Z', '+00:00'))  # konvertiert ISO String
            else:
                timestamp = None  # falls kein Zeitstempel vorhanden

            m = Movement(
                product_id=raw.get("product_id", ""),  # Produkt ID mit leerem Fallback
                product_name=raw.get("product_name", ""),  # Produktname mit leerem Fallback
                quantity_change=raw.get("quantity_change", 0),  # Änderung mit Null Fallback
                movement_type=raw.get("movement_type", ""),  # Typ mit leerem Fallback
                reason=raw.get("note", ""),  # Grund mit leerem Fallback
                timestamp=timestamp,  # konvertierter oder None Zeitstempel
            )
            movements.append(m)  # fügt konvertierte Bewegung zur Liste hinzu
        return movements  # gibt Liste aller Bewegungen zurück


class RepositoryFactory:  # Factory Klasse zur Erstellung unterschiedlicher Repository Typen
    """Factory for creating repository implementations."""

    @classmethod
    def create_repository(cls, repo_type: str = "mongodb") -> RepositoryPort:  # Standard ist MongoDB
        if repo_type == "memory":
            return InMemoryRepository()  # gibt RAM basiertes Repository zurück
        elif repo_type == "sqlite":
            from .sqlite_repository import SQLiteRepository  # lazy Import für SQLite
            return SQLiteRepository("warehouse.db")  # gibt SQLite Repository mit Dateiname zurück
        elif repo_type == "mongodb":
            return MongoDBRepository()  # gibt MongoDB Repository zurück
        else:
            raise ValueError(f"Unknown repository type: {repo_type}")  # Fehler bei unbekanntem Typ

    @classmethod
    def create(cls, repo_type: str = "memory") -> RepositoryPort:  # Kurzform mit RAM Standard
        return cls.create_repository(repo_type)  # delegiert an create_repository

