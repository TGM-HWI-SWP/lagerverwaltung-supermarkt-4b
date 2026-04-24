from datetime import datetime  # importiert Datum und Uhrzeit für Zeitstempel
from src.domain.movement import Movement  # importiert Movement Klasse für Lagerbewegungen


class Product:
    """Core domain entity for products in supermarket warehouse."""

    def __init__(
        self,
        product_id: str,  # eindeutige Identifikationsnummer des Produkts
        name: str,  # Anzeigename des Produkts
        description: str,  # Beschreibungstext für Details
        price: float,  # Preis pro Einheit in Euro
        category: str,  # Kategorie z. B. Milchprodukte oder Obst
        quantity: int = 0,  # aktueller Lagerbestand Standard 0
        min_stock: int = 5  # Mindestbestand für Warnlogik Standard 5
    ):
        if price < 0:
            raise ValueError("Price cannot be negative")  # verhindert ungültige negative Preise
        if quantity < 0:
            raise ValueError("Initial quantity cannot be negative")  # kein negativer Startbestand erlaubt

        self.product_id = product_id  # speichert Produkt ID
        self.id = product_id  # Alias für bestehenden Code gleiche ID unter anderem Namen
        self.name = name  # speichert Produktnamen
        self.description = description  # speichert Beschreibung
        self.price = price  # speichert Preis
        self.category = category  # speichert Kategorie
        self.quantity = quantity  # speichert aktuelle Menge
        self.min_stock = min_stock  # speichert Mindestbestand für Warnlogik

        # Zusatzattribute für MongoDB und Tests
        self.sku = ""  # optionale Artikelnummer leer als Standard
        self.notes = ""  # zusätzliche Notizen leer als Standard
        self.created_at = datetime.now()  # Zeitpunkt der Erstellung wird automatisch gesetzt
        self.updated_at = datetime.now()  # Zeitpunkt der letzten Änderung wird automatisch gesetzt

    def update_quantity(self, delta: int, reason: str, user: str) -> Movement:
        # delta = Mengenänderung positiv für Zugang negativ für Abgang
        """Update quantity and return Movement. Validates no negative stock."""
        if self.quantity + delta < 0:
            raise ValueError(f"Cannot reduce stock below 0. Current: {self.quantity}, delta: {delta}")  # verhindert negativen Lagerbestand

        self.quantity += delta  # verändert Bestand positiv für Einbuchung negativ für Ausbuchung
        self.updated_at = datetime.now()  # aktualisiert Änderungszeitpunkt auf jetzt

        movement = Movement(
            product_id=self.product_id,  # übergibt eigene ID an Movement
            product_name=self.name,  # übergibt eigenen Namen an Movement
            quantity_change=delta,  # übergibt Änderungsmenge
            movement_type="IN" if delta > 0 else "OUT",  # bestimmt automatisch Typ basierend auf Vorzeichen
            reason=reason,  # übergibt Grund der Bewegung
            performed_by=user  # wer hat die Aktion ausgeführt
        )
        return movement  # gibt erzeugte Bewegung zurück für Speicherung oder Logging

    def get_total_value(self) -> float:
        """Calculate total inventory value for this product."""
        return self.price * self.quantity  # Gesamtwert berechnet sich aus Preis multipliziert mit Menge

    def is_low_stock(self) -> bool:
        """Check if stock is below minimum threshold."""
        return self.quantity <= self.min_stock  # prüft ob aktueller Bestand kleiner gleich Mindestbestand ist

    def change_price(self, new_price: float) -> None:
        """Update price (business decision)."""
        if new_price < 0:
            raise ValueError("Price cannot be negative")  # verhindert ungültige negative Preisänderung
        self.price = new_price  # setzt neuen Preis
        self.updated_at = datetime.now()  # aktualisiert Zeitpunkt der letzten Änderung

    def __repr__(self) -> str:
        return (
            f"Product(id={self.id}, name={self.name}, qty={self.quantity}, "  # kompakte Darstellung für Debugging
            f"price={self.price:.2f}, cat={self.category})"  # Punktzweif formatiert Preis auf zwei Dezimalstellen
        )

