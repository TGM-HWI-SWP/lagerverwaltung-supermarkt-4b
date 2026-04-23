#!/usr/bin/env python3
"""
Dummy data generator for Supermarkt Businesslogik testing.
Run with: python tests/dummy_data.py [sqlite|memory]
"""

import sys
from src.services import WarehouseService, RepositoryFactory

def load_dummy_data(service):
    """Load typical supermarket dummy data."""
    # Supermarkt products
    service.create_product("MILK001", "Vollmilch 1L", "Frische Vollmilch", 1.29, "Milchprodukte", 20, "Aleksej")
    service.create_product("BREAD001", "Vollkornbrot", "Frisches Vollkornbrot 500g", 2.49, "Backwaren", 10, "Aleksej")
    service.create_product("APPLE001", "Äpfel Bio", "Bio Äpfel lose kg", 3.99, "Obst", 3, "Aleksej")  # Low stock
    service.create_product("LAPTOP001", "Gaming Laptop", "High-End Gaming Laptop", 1299.99, "Elektronik", 2, "Aleksej")
    
    print("✅ Dummy data loaded: 4 products")

def demo_operations(service):
    """Demo stock operations."""
    print("\n--- Demo Operations ---")
    # Stock changes
    service.add_stock("MILK001", 10, "Täglicher Nachschub", "Aleksej")
    service.remove_stock("BREAD001", 2, "Verkauf", "Kunde")
    service.add_stock("APPLE001", 5, "Neue Lieferung", "Lieferant")
    
    print("✅ Stock operations + movements logged")
    
    print("\nLow stock:", [p.name for p in service.get_low_stock_products()])
    print("Total value:", f"{service.get_total_inventory_value():.2f} €")
    print("Movements count:", len(service.get_movements()))

def print_report():
    """Print Report A."""
    from src.reports.report_a import generate_inventory_report
    print("\n--- Report A ---")
    print(generate_inventory_report(service))

if __name__ == "__main__":
    repo_type = sys.argv[1] if len(sys.argv) > 1 else "memory"
    repo = RepositoryFactory.create(repo_type)
    service = WarehouseService(repo)
    
    print(f"=== Supermarkt Dummy Data ({repo_type.upper()}) ===")
    load_dummy_data(service)
    demo_operations(service)
    print_report()
    

