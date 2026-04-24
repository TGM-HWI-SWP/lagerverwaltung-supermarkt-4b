from abc import ABC, abstractmethod  # ABC ermöglicht abstrakte Klassen abstractmethod erzwingt Implementierung
from typing import Dict, List, Optional  # Typisierung für Methodensignaturen
from src.domain.product import Product  # Domain Objekt das gespeichert wird
from src.domain.movement import Movement  # Domain Objekt für Bewegungen

class RepositoryPort(ABC):  # abstrakte Basisklasse für alle Repository Implementierungen
    """Port for product and movement persistence."""

    @abstractmethod  # muss von Unterklassen implementiert werden
    def add(self, product: Product) -> None:
        """Add or update a product."""
        pass  # Platzhalter wird von konkreter Klasse überschrieben

    @abstractmethod
    def get(self, product_id: str) -> Optional[Product]:
        """Get product by ID."""
        pass  # gibt Produkt zurück oder None wenn nicht gefunden

    @abstractmethod
    def get_all(self) -> Dict[str, Product]:
        """Get all products."""
        pass  # gibt Dictionary mit allen Produkten zurück

    @abstractmethod
    def delete(self, product_id: str) -> None:
        """Delete product by ID."""
        pass  # entfernt Produkt aus Speicher

    @abstractmethod
    def save_movement(self, movement: Movement) -> None:
        """Save a movement."""
        pass  # speichert einzelne Bewegung

    @abstractmethod
    def get_movements(self) -> List[Movement]:
        """Get all movements."""
        pass  # gibt Liste aller Bewegungen zurück

