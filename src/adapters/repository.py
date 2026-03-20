from typing import Dict, List, Optional
from src.ports.repository_port import RepositoryPort
from src.domain.product import Product
from src.domain.movement import Movement

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

class RepositoryFactory:
    """Factory for creating repository implementations."""

    @classmethod
    def create(cls, repo_type: str = "memory") -> RepositoryPort:
        if repo_type == "memory":
            return InMemoryRepository()
        elif repo_type == "sqlite":
            from .sqlite_repository import SQLiteRepository
            return SQLiteRepository("warehouse.db")
        else:
            raise ValueError(f"Unknown repository type: {repo_type}")
