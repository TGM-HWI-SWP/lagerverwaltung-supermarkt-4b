"""Domain Layer - Geschäftslogik und Entity-Modelle"""
# Dieses Modul enthält die Kerngeschäftslogik des Supermarkts

from .product import Product  # importiert Produkt Klasse
from .movement import Movement  # importiert Bewegungs Klasse

__all__ = ["Product", "Movement"]  # definiert öffentliche Schnittstelle beim Import mit Stern

