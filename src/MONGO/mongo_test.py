from src.domain.product import Product  # Domain-Klasse für Produkte
from src.adapters.mongodb_product_repository import MongoDBProductRepository  # Repository für MongoDB-Zugriff


MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"  # Verbindungsstring zur MongoDB

def main() -> None:  # Einstiegspunkt des Programms
    repo = MongoDBProductRepository(MONGO_URI)  # erstellt Repository für DB-Operationen

    product = Product(  # erstellt neues Produktobjekt
        id="P001",  # ACHTUNG: Parametername passt nicht zum Konstruktor (erwartet product_id) → möglicher Fehler
        name="Apfel",
        description="Roter Apfel",
        price=1.5,
        quantity=100,
        sku="SKU-001",  # nicht im Konstruktor definiert → wird hier eigentlich nicht korrekt verarbeitet
        category="Obst",
        notes="Testprodukt"  # ebenfalls kein Konstruktor-Parameter
    )

    repo.save_product(product)  # speichert Produkt in MongoDB (update oder insert)
    print("Produkt gespeichert")

    loaded = repo.load_product_by_id("P001")  # lädt Produkt anhand ID aus DB
    print("Ein Produkt geladen:")
    print(loaded)  # nutzt __repr__ Methode der Product-Klasse

    all_products = repo.load_all_products()  # lädt alle Produkte aus DB
    print("Alle Produkte:")
    print(all_products)  # gibt Liste von Produktobjekten aus



if __name__ == "__main__":  # stellt sicher, dass main nur beim direkten Start ausgeführt wird
    main()