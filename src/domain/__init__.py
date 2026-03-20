"""Domain Layer - Geschäftslogik und Entity-Modelle"""

from .product import Product
from .movement import Movement
from .warehouse import WarehouseService  # Service in domain (legacy)

__all__ = ["Product", "Movement", "WarehouseService"]
