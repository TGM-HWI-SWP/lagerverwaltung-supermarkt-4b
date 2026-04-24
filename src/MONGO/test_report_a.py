from src.adapters.mongodb_product_repository import MongoDBProductRepository  # Repository für Zugriff auf Produktdaten aus MongoDB
from src.reports.report_a import generate_inventory_report  # Funktion zur Erstellung des Lagerreports

MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"  # Verbindungsstring zur Datenbank

repo = MongoDBProductRepository(MONGO_URI)  # initialisiert Repository mit DB-Verbindung

print(generate_inventory_report(repo))  # erzeugt Report basierend auf DB-Daten und gibt ihn in der Konsole aus