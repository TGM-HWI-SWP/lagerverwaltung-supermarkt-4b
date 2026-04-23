from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from src.domain.product import Product
from src.domain.movement import Movement

class RepositoryPort(ABC):
    """Port for product and movement persistence."""

    @abstractmethod
    def add(self, product: Product) -> None:
        """Add or update a product."""
        pass

    @abstractmethod
    def get(self, product_id: str) -> Optional[Product]:
        """Get product by ID."""
        pass

    @abstractmethod
    def get_all(self) -> Dict[str, Product]:
        """Get all products."""
        pass

    @abstractmethod
    def delete(self, product_id: str) -> None:
        """Delete product by ID."""
        pass

    @abstractmethod
    def save_movement(self, movement: Movement) -> None:
        """Save a movement."""
        pass

    @abstractmethod
    def get_movements(self) -> List[Movement]:
        """Get all movements."""
        pass