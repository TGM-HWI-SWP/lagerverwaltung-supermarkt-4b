"""Central Ports - Unified interfaces for hexagonal architecture."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from ..domain.product import Product
from ..domain.movement import Movement

class RepositoryPort(ABC):
    '''Port für Datenpersistenz (Produkte und Bewegungen). English methods matching adapters.'''
    
    @abstractmethod
    def add(self, product: Product) -> None:
        '''Produkt hinzufügen/aktualisieren.'''
        pass

    @abstractmethod
    def get(self, product_id: str) -> Optional[Product]:
        '''Produkt by ID laden.'''
        pass

    @abstractmethod
    def get_all(self) -> Dict[str, Product]:
        '''Alle Produkte laden.'''
        pass

    @abstractmethod
    def delete(self, product_id: str) -> None:
        '''Produkt löschen.'''
        pass

    @abstractmethod
    def save_movement(self, movement: Movement) -> None:
        '''Lagerbewegung speichern.'''
        pass

    @abstractmethod
    def get_movements(self) -> List[Movement]:
        '''Alle Bewegungen laden.'''
        pass

class ReportPort(ABC):
    '''Port für Report-Generierung.'''
    
    @abstractmethod
    def generate_inventory_report(self) -> str:
        '''Lagerbestandsbericht generieren.'''
        pass

    @abstractmethod
    def generate_movement_report(self) -> str:
        '''Bewegungsprotokoll generieren.'''
        pass

