"""Ports - Schnittstellen für externe Abhängigkeiten (Abstraktion)"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from ..domain.product import Product
from ..domain.movement import Movement

class RepositoryPort(ABC):
    """Port für Datenpersistenz."""

    @abstractmethod
    def add(self, product: Product) -> None:
        pass

    @abstractmethod
    def get(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self) -> Dict[str, Product]:
        pass

    @abstractmethod
    def delete(self, product_id: str) -> None:
        pass

    @abstractmethod
    def save_movement(self, movement: Movement) -> None:
        pass

    @abstractmethod
    def get_movements(self) -> List[Movement]:
        pass
