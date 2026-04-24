#!/usr/bin/env python3
"""
Dummy data generator for Supermarkt Businesslogik testing.
Run with: python tests/dummy_data.py [sqlite|memory]
"""

import sys  # für Kommandozeilenargumente
from src.services import WarehouseService, RepositoryFactory  # Service und Factory für Datenzugriff

def load_dummy_data(service):  # lädt Beispieldaten in den Service
    """Load typical supermarket dummy data."""
    # Supermarkt products
    service.create_product("MILK001", "Vollmilch 1L", "Frische Vollmilch", 1.29, "Milchprodukte", 20, "Aleksej")  # Milch mit hohem Bestand
    service.create_product("BREAD001", "Vollkornbrot", "Frisches Vollkornbrot 500g", 2.49, "Backwaren", 10, "Aleksej")  # Brot
    service.create_product("APPLE001", "Äpfel Bio", "Bio Äpfel lose kg", 3.99, "Obst", 3, "Aleksej")  # niedriger Bestand
    service.create_product("LAPTOP001", "Gaming Laptop", "High-End Gaming Laptop", 1299.99, "Elektronik", 2, "Aleksej")  # teure Elektronik
    
    print("Dummy data loaded: 4 products")  # Bestätigung für Konsole

def demo_operations(service):  # führt Beispieloperationen durch
    """Demo stock operations."""
    print("\n--- Demo Operations ---")
    # Stock changes
    service.add_stock("MILK001", 10, "Täglicher Nachschub", "Aleksej")  # Einbuchung Milch
    service.remove_stock("BREAD001", 2, "Verkauf", "Kunde")  # Ausbuchung Brot
    service.add_stock("APPLE001", 5, "Neue Lieferung", "Lieferant")  # Einbuchung Äpfel
    
    print("Stock operations + movements logged")  # Bestätigung
    
    print("\nLow stock:", [p.name for p in service.get_low_stock_products()])  # zeigt Produkte unter Minimum
    print("Total value:", f"{service.get_total_inventory_value():.2f} €")  # zeigt Gesamtwert formatiert
    print("Movements count:", len(service.get_movements()))  # zeigt Anzahl Bewegungen

def print_report():  # gibt Report A aus
    """Print Report A."""
    from src.reports.report_a import generate_inventory_report  # lokaler Import für Report
    print("\n--- Report A ---")
    print(generate_inventory_report(service))  # generiert und zeigt Report

if __name__ == "__main__":  # Einstiegspunkt bei direktem Aufruf
    repo_type = sys.argv[1] if len(sys.argv) > 1 else "memory"  # liest Repository Typ aus Argument oder Standard memory
    repo = RepositoryFactory.create(repo_type)  # erstellt gewünschtes Repository
    service = WarehouseService(repo)  # erzeugt Service mit Repository
    
    print(f"=== Supermarkt Dummy Data ({repo_type.upper()}) ===")
    load_dummy_data(service)  # füllt Daten
    demo_operations(service)  # führt Operationen durch
    print_report()  # zeigt Report
    

