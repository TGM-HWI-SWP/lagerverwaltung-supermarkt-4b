import uuid
from datetime import datetime
from typing import Dict, List, Optional
from src.ports.repository_port import RepositoryPort
from src.domain.product import Product
from src.domain.movement import Movement
from .mongodb_product_repository import MongoDBProductRepository
from .mongodb_movement_repository import MongoDBMovementRepository
from src.MONGO.mongo_test import MONGO_URI

class InMemoryRepository(RepositoryPort):
    """In-memory implementation for testing and quick starts."""

    def __init__(self):
        self._products: Dict[str, Product] = {}
        self._movements: List[Movement] = []

    def add(self, product: Product) -> None:
        self._products[product.product_id] = product
        # Log initial stock
        initial_movement = Movement(
            product_id=product.product_id,
            product_name=product.name,
            quantity_change=product.quantity,
            movement_type="INITIAL",
            reason="Initial stock",
            performed_by="system"
        )
        self._movements.append(initial_movement)

    def get(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def get_all(self) -> Dict[str, Product]:
        return self._products.copy()

    def delete(self, product_id: str) -> None:
        if product_id in self._products:
            del self._products[product_id]

    def save_movement(self, movement: Movement) -> None:
        self._movements.append(movement)

    def get_movements(self) -> List[Movement]:
        return self._movements.copy()


class MongoDBRepository(RepositoryPort):
    """MongoDB implementation for production data."""

    def __init__(self):
        self.product_repo = MongoDBProductRepository(MONGO_URI)
        self.movement_repo = MongoDBMovementRepository(MONGO_URI)

    def add(self, product: Product) -> None:
        self.product_repo.save_product(product)

    def get(self, product_id: str) -> Optional[Product]:
        return self.product_repo.load_product_by_id(product_id)

    def get_all(self) -> Dict[str, Product]:
        products_list = self.product_repo.load_all_products()
        return {p.id: p for p in products_list}

    def delete(self, product_id: str) -> None:
        # Mongo doesn't have direct delete in product repo, but can add if needed
        # For now, set quantity=0 or implement delete
        product = self.get(product_id)
        if product:
            product.quantity = 0
            product.category = "DELETED"
            self.product_repo.save_product(product)

    def save_movement(self, movement: Movement) -> None:
        movement_id = movement.id if movement.id is not None else str(uuid.uuid4())
        timestamp = movement.timestamp if movement.timestamp is not None else datetime.now()
        mongo_movement = {
            "movement_id": movement_id,
            "product_id": movement.product_id,
            "product_name": movement.product_name or movement.product_id,
            "movement_type": movement.movement_type,
            "old_quantity": 0,  # To be calculated if needed
            "quantity_change": movement.quantity_change,
            "new_quantity": 0,  # To be calculated
            "note": movement.reason,
            "created_at": timestamp,
        }
        self.movement_repo.collection.insert_one(mongo_movement)
        # Note: Custom Movement class from MONGO may differ; adjust if error

    def get_movements(self) -> List[Movement]:
        raw_movements = self.movement_repo.load_all_movements()
        movements = []
        for raw in raw_movements:
            # created_at from MongoDB is a BSON datetime object, not a string
            created_at = raw.get("created_at")
            if isinstance(created_at, datetime):
                timestamp = created_at
            elif isinstance(created_at, str):
                timestamp = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            else:
                timestamp = None

            m = Movement(
                product_id=raw.get("product_id", ""),
                product_name=raw.get("product_name", ""),
                quantity_change=raw.get("quantity_change", 0),
                movement_type=raw.get("movement_type", ""),
                reason=raw.get("note", ""),
                timestamp=timestamp,
            )
            movements.append(m)
        return movements


class RepositoryFactory:
    """Factory for creating repository implementations."""

    @classmethod
    def create_repository(cls, repo_type: str = "mongodb") -> RepositoryPort:  # Default to mongodb
        if repo_type == "memory":
            return InMemoryRepository()
        elif repo_type == "sqlite":
            from .sqlite_repository import SQLiteRepository
            return SQLiteRepository("warehouse.db")
        elif repo_type == "mongodb":
            return MongoDBRepository()
        else:
            raise ValueError(f"Unknown repository type: {repo_type}")

    @classmethod
    def create(cls, repo_type: str = "memory") -> RepositoryPort:
        return cls.create_repository(repo_type)
