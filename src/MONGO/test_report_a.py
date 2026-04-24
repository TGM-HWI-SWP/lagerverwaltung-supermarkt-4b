from src.adapters.mongodb_product_repository import MongoDBProductRepository
from src.reports.report_a import generate_inventory_report

MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"

repo = MongoDBProductRepository(MONGO_URI)

print(generate_inventory_report(repo))