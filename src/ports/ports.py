"""Central Ports - Unified interfaces for hexagonal architecture."""
# Dieses Modul definiert zentrale Schnittstellen für die hexagonale Architektur

from abc import ABC, abstractmethod  # für abstrakte Klassen und Methoden
from typing import Dict, List, Optional  # Typisierung für Rückgabewerte

from ..domain.product import Product  # importiert Produkt aus Domain
from ..domain.movement import Movement  # importiert Movement aus Domain

class RepositoryPort(ABC):  # abstrakte Schnittstelle für Datenpersistenz
    '''Port für Datenpersistenz (Produkte und Bewegungen). English methods matching adapters.'''
    
    @abstractmethod
    def add(self, product: Product) -> None:
        '''Produkt hinzufügen oder aktualisieren.'''
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

class ReportPort(ABC):  # abstrakte Schnittstelle für Report Generierung
    '''Port für Report Generierung.'''
    
    @abstractmethod
    def generate_inventory_report(self) -> str:
        '''Lagerbestandsbericht generieren.'''
        pass

    @abstractmethod
    def generate_movement_report(self) -> str:
        '''Bewegungsprotokoll generieren.'''
        pass

