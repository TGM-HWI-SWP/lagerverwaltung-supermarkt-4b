from typing import Optional
import uuid
from datetime import datetime
from src.domain.movement import Movement

class Product:
    """Core domain entity for products in supermarket warehouse."""

    def __init__(
        self,
        product_id: str,
        name: str,
        description: str,
        price: float,
        category: str,
        quantity: int = 0,
        min_stock: int = 5
    ):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Initial quantity cannot be negative")

        self.product_id = product_id
        self.name = name
        self.description = description
        self.price: float = price
        self.category = category
        self.quantity: int = quantity
        self.min_stock: int = min_stock
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_quantity(self, delta: int, reason: str, user: str) -> Movement:
        """Update quantity and return Movement. Validates no negative stock."""
        if self.quantity + delta < 0:
            raise ValueError(f"Cannot reduce stock below 0. Current: {self.quantity}, delta: {delta}")

        self.quantity += delta
        self.updated_at = datetime.now()

        movement = Movement(
            product_id=self.product_id,
            product_name=self.name,
            quantity_change=delta,
            movement_type="IN" if delta > 0 else "OUT",
            reason=reason,
            performed_by=user
        )
        return movement

    def get_total_value(self) -> float:
        """Calculate total inventory value for this product."""
        return self.price * self.quantity

    def is_low_stock(self) -> bool:
        """Check if stock is below minimum threshold."""
        return self.quantity <= self.min_stock

    def change_price(self, new_price: float) -> None:
        """Update price (business decision)."""
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        return f"Product(id={self.product_id}, name={self.name}, qty={self.quantity}, price={self.price:.2f}, cat={self.category})"
