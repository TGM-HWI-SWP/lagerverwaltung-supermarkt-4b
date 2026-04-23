from typing import Dict, List, Optional
from src.ports.ports import RepositoryPort
from src.domain.product import Product
from src.domain.movement import Movement
from src.adapters.repository import RepositoryFactory

class WarehouseService:
    """Core business logic for supermarket warehouse management."""

    def __init__(self, repo=None):
        if repo is None:
            self.repository = RepositoryFactory.create_repository("sqlite")
        else:
            self.repository = repo

    def create_product(
        self,
        product_id: str,
        name: str,
        description: str,
        price: float,
        category: str,
        quantity: int = 0,
        performed_by: str = "system"
    ) -> Product:
        """Create new product with initial stock movement."""
        product = Product(product_id, name, description, price, category, quantity)
        self.repository.add(product)
        return product

    def add_stock(
        self,
        product_id: str,
        quantity: int,
        reason: str = "Stock replenishment",
        performed_by: str = "system"
    ) -> Movement:
        """Add stock and log movement."""
        product = self.repository.get(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        movement = product.update_quantity(quantity, reason, performed_by)
        self.repository.save_movement(movement)
        return movement

    def remove_stock(
        self,
        product_id: str,
        quantity: int,
        reason: str = "Sale",
        performed_by: str = "system"
    ) -> Movement:
        """Remove stock and log movement."""
        product = self.repository.get(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        movement = product.update_quantity(-quantity, reason, performed_by)
        self.repository.save_movement(movement)
        return movement

    def delete_product(self, product_id: str) -> None:
        """Delete product."""
        self.repository.delete(product_id)

    def get_product(self, product_id: str) -> Optional[Product]:
        """Get single product."""
        return self.repository.get(product_id)

    def get_all_products(self) -> Dict[str, Product]:
        """Get all products."""
        return self.repository.get_all()

    def get_low_stock_products(self) -> List[Product]:
        """Get products below min_stock."""
        products = list(self.repository.get_all().values())
        return [p for p in products if p.is_low_stock()]

    def get_total_inventory_value(self) -> float:
        """Total value of all inventory."""
        total = 0.0
        for product in self.repository.get_all().values():
            total += product.get_total_value()
        return total

    def get_products_by_category(self, category: str) -> List[Product]:
        """Filter products by category."""
        products = list(self.repository.get_all().values())
        return [p for p in products if p.category == category]

    def get_movements(self) -> List[Movement]:
        """Get all stock movements."""
        return self.repository.get_movements()
