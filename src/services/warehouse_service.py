from typing import Dict, List, Optional  # Typisierung für bessere Code Qualität
from src.ports.repository_port import RepositoryPort  # Schnittstelle für Datenspeicher
from src.domain.product import Product  # Domain Objekt Produkt
from src.domain.movement import Movement  # Domain Objekt Bewegung
from src.adapters.repository import RepositoryFactory  # Factory zur Erstellung des Repositories

class WarehouseService:
    """Core business logic for supermarket warehouse management."""

    def __init__(self, repo=None):  # Konstruktor mit optionalem Repository
        if repo is None:
            self.repository = RepositoryFactory.create_repository()  # erstellt Standard Repository wenn keines übergeben wird
        else:
            self.repository = repo  # verwendet übergebenes Repository für Dependency Injection

    def create_product(
        self,
        product_id: str,  # eindeutige Produkt ID
        name: str,  # Anzeigename
        description: str,  # Beschreibung
        price: float,  # Preis pro Einheit
        category: str,  # Warengruppe
        quantity: int = 0,  # Startbestand
        performed_by: str = "system"  # wer erstellt hat
    ) -> Product:
        """Create new product with initial stock movement."""
        product = Product(product_id, name, description, price, category, quantity)  # erzeugt neues Produkt Objekt
        self.repository.add(product)  # speichert Produkt im Repository
        return product  # gibt erzeugtes Produkt zurück

    def add_stock(
        self,
        product_id: str,  # welches Produkt soll bestückt werden
        quantity: int,  # wie viel soll dazukommen
        reason: str = "Stock replenishment",  # Grund für die Einbuchung
        performed_by: str = "system"  # wer führt die Aktion aus
    ) -> Movement:
        """Add stock and log movement."""
        product = self.repository.get(product_id)  # lädt Produkt aus Repository
        if not product:
            raise ValueError(f"Product {product_id} not found")  # Fehler wenn Produkt nicht existiert
        
        movement = product.update_quantity(quantity, reason, performed_by)  # führt Bestandsänderung durch und erzeugt Movement
        self.repository.add(product)  # speichert aktualisiertes Produkt
        self.repository.save_movement(movement)  # speichert Bewegung in Historie
        return movement  # gibt erzeugte Bewegung zurück

    def remove_stock(
        self,
        product_id: str,  # welches Produkt soll entnommen werden
        quantity: int,  # wie viel soll abgezogen werden
        reason: str = "Sale",  # Grund für Ausbuchung Standard ist Verkauf
        performed_by: str = "system"  # wer führt die Aktion aus
    ) -> Movement:
        """Remove stock and log movement."""
        product = self.repository.get(product_id)  # lädt Produkt aus Repository
        if not product:
            raise ValueError(f"Product {product_id} not found")  # Fehler wenn Produkt nicht existiert
        
        movement = product.update_quantity(-quantity, reason, performed_by)  # führt negative Bestandsänderung durch
        self.repository.add(product)  # speichert aktualisiertes Produkt
        self.repository.save_movement(movement)  # speichert Bewegung in Historie
        return movement  # gibt erzeugte Bewegung zurück

    def delete_product(self, product_id: str) -> None:
        """Delete product."""
        self.repository.delete(product_id)  # löscht Produkt aus Repository

    def get_product(self, product_id: str) -> Optional[Product]:
        """Get single product."""
        return self.repository.get(product_id)  # gibt einzelnes Produkt zurück oder None

    def get_all_products(self) -> Dict[str, Product]:
        """Get all products."""
        return self.repository.get_all()  # gibt Dictionary mit allen Produkten zurück

    def get_low_stock_products(self) -> List[Product]:
        """Get products below min_stock."""
        products = list(self.repository.get_all().values())  # wandelt Dictionary in Liste um
        return [p for p in products if p.is_low_stock()]  # filtert Produkte mit niedrigem Bestand

    def get_total_inventory_value(self) -> float:
        """Total value of all inventory."""
        total = 0.0  # Startwert für Summe
        for product in self.repository.get_all().values():  # iteriert über alle Produkte
            total += product.get_total_value()  # addiert Wert jedes Produkts hinzu
        return total  # gibt Gesamtwert zurück

    def get_products_by_category(self, category: str) -> List[Product]:
        """Filter products by category."""
        products = list(self.repository.get_all().values())  # wandelt Dictionary in Liste um
        return [p for p in products if p.category == category]  # filtert nach exakter Kategorie Übereinstimmung

    def get_movements(self) -> List[Movement]:
        """Get all stock movements."""
        return self.repository.get_movements()  # gibt alle gespeicherten Bewegungen zurück

    def load_dummy_data(self, performed_by: str = "system"):
        """Load supermarket dummy data if empty."""
        if len(self.repository.get_all()) > 0:
            return  # bricht ab wenn bereits Daten vorhanden sind
        
        self.create_product("MILK001", "Vollmilch 1L", "Frische Vollmilch", 1.29, "Milchprodukte", 20, performed_by)  # Milchprodukt mit hohem Bestand
        self.create_product("BREAD001", "Vollkornbrot", "Frisches Vollkornbrot 500g", 2.49, "Backwaren", 10, performed_by)  # Backware
        self.create_product("APPLE001", "Äpfel Bio", "Bio Äpfel loose kg", 3.99, "Obst", 3, performed_by)  # Obst mit niedrigem Bestand
        self.create_product("LAPTOP001", "Gaming Laptop", "High-End Gaming Laptop", 1299.99, "Elektronik", 2, performed_by)  # teures Elektronikprodukt

