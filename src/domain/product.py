from datetime import datetime  # für Zeitstempel (Erstellung/Update)
from src.domain.movement import Movement  # wird benötigt, um Lagerbewegungen zu erzeugen


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
            raise ValueError("Price cannot be negative")  # verhindert ungültige Preise (Businessregel)
        if quantity < 0:
            raise ValueError("Initial quantity cannot be negative")  # kein negativer Startbestand erlaubt

        self.product_id = product_id
        self.id = product_id  # Alias für bestehenden Code → gleiche ID unter anderem Namen
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.quantity = quantity
        self.min_stock = min_stock  # Mindestbestand für Warnlogik

        # Zusatzattribute für MongoDB / Tests
        self.sku = ""  # optionale Artikelnummer
        self.notes = ""  # zusätzliche Notizen
        self.created_at = datetime.now()  # Zeitpunkt der Erstellung
        self.updated_at = datetime.now()  # Zeitpunkt der letzten Änderung

    def update_quantity(self, delta: int, reason: str, user: str) -> Movement: # delta = Mengenänderung (+ für Zugang, - für Abgang)
        """Update quantity and return Movement. Validates no negative stock."""
        if self.quantity + delta < 0:
            raise ValueError(f"Cannot reduce stock below 0. Current: {self.quantity}, delta: {delta}")  # verhindert negativen Lagerbestand

        self.quantity += delta  # verändert Bestand (+ für IN, - für OUT)
        self.updated_at = datetime.now()  # aktualisiert Änderungszeitpunkt

        movement = Movement(
            product_id=self.product_id,
            product_name=self.name,
            quantity_change=delta,
            movement_type="IN" if delta > 0 else "OUT",  # bestimmt automatisch Typ basierend auf delta
            reason=reason,
            performed_by=user
        )
        return movement  # gibt Movement zurück für Speicherung/Logging

    def get_total_value(self) -> float:
        """Calculate total inventory value for this product."""
        return self.price * self.quantity  # Gesamtwert = Preis * Menge

    def is_low_stock(self) -> bool:
        """Check if stock is below minimum threshold."""
        return self.quantity <= self.min_stock  # prüft ob Bestand unter Mindestgrenze liegt

    def change_price(self, new_price: float) -> None:
        """Update price (business decision)."""
        if new_price < 0:
            raise ValueError("Price cannot be negative")  # verhindert ungültige Preisänderung
        self.price = new_price  # setzt neuen Preis
        self.updated_at = datetime.now()  # aktualisiert Änderungszeitpunkt

    def __repr__(self) -> str:
        return (
            f"Product(id={self.id}, name={self.name}, qty={self.quantity}, "  # kompakte Darstellung für Debugging
            f"price={self.price:.2f}, cat={self.category})"  # :.2f formatiert Preis auf 2 Dezimalstellen
        )