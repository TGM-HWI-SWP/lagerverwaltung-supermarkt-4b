from datetime import datetime
from src.domain.product import Product
from src.adapters.mongodb_product_repository import MongoDBProductRepository

# MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:Gabi12345.@cluster0.jge9ku6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"

repo = MongoDBProductRepository(MONGO_URI)


def make_product(id_, name, description, price, category, quantity, min_stock, sku, notes):
    p = Product(id_, name, description, price, category, quantity, min_stock)

    # fehlende Attribute ergänzen, damit dein Repo.save_product() funktioniert
    p.id = id_
    p.sku = sku
    p.notes = notes
    p.created_at = datetime.now()
    p.updated_at = datetime.now()

    return p


products = [
    make_product("P002", "Apfel", "Roter Apfel", 1.5, "Obst", 120, 10, "SKU-003", "Frisch geliefert"),
    make_product("P003", "Banane", "Gelbe Banane", 1.2, "Obst", 150, 10, "SKU-004", "Reif"),
    make_product("P004", "Orange", "Saftige Orange", 1.8, "Obst", 100, 10, "SKU-005", "Süß"),
    make_product("P005", "Trauben", "Süße Weintrauben", 2.4, "Obst", 80, 8, "SKU-006", "Kernlos"),
    make_product("P006", "Zitrone", "Frische Zitrone", 0.9, "Obst", 90, 10, "SKU-007", "Sauer"),

    make_product("P007", "Tomate", "Frische Tomate", 2.1, "Gemüse", 110, 10, "SKU-008", "Regional"),
    make_product("P008", "Gurke", "Grüne Gurke", 1.1, "Gemüse", 95, 10, "SKU-009", "Knackig"),
    make_product("P009", "Karotte", "Bio Karotte", 1.3, "Gemüse", 130, 12, "SKU-010", "Bio"),
    make_product("P010", "Paprika", "Rote Paprika", 1.9, "Gemüse", 85, 10, "SKU-011", "Mild"),
    make_product("P011", "Zwiebel", "Gelbe Zwiebel", 0.8, "Gemüse", 140, 15, "SKU-012", "Lagerware"),

    make_product("P012", "Milch", "Vollmilch 1L", 1.2, "Milchprodukte", 200, 20, "SKU-013", "Kühlware"),
    make_product("P013", "Joghurt", "Naturjoghurt", 0.95, "Milchprodukte", 160, 15, "SKU-014", "Ohne Zucker"),
    make_product("P014", "Butter", "Butter 250g", 2.3, "Milchprodukte", 90, 10, "SKU-015", "Marke Hausgut"),
    make_product("P015", "Käse", "Gouda Käse", 3.8, "Milchprodukte", 70, 8, "SKU-016", "Mild gereift"),
    make_product("P016", "Sahne", "Schlagsahne 250ml", 1.4, "Milchprodukte", 75, 10, "SKU-017", "Zum Kochen"),

    make_product("P017", "Brot", "Weißbrot", 1.9, "Backwaren", 100, 10, "SKU-018", "Tagesfrisch"),
    make_product("P018", "Semmel", "Frische Semmel", 0.5, "Backwaren", 220, 20, "SKU-019", "Knusprig"),
    make_product("P019", "Croissant", "Buttercroissant", 1.1, "Backwaren", 85, 10, "SKU-020", "Französische Art"),

    make_product("P020", "Wasser", "Mineralwasser 1.5L", 0.7, "Getränke", 300, 30, "SKU-021", "Still"),
    make_product("P021", "Cola", "Cola 1L", 1.6, "Getränke", 180, 20, "SKU-022", "Zuckerhaltig"),
]

for product in products:
    repo.save_product(product)

print("20 weitere Produkte gespeichert.")