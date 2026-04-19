from src.domain.product import Product
from src.adapters.mongodb_product_repository import MongoDBProductRepository


MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"
def main() -> None:
    repo = MongoDBProductRepository(MONGO_URI)

    product = Product(
        id="P001",
        name="Apfel",
        description="Roter Apfel",
        price=1.5,
        quantity=100,
        sku="SKU-001",
        category="Obst",
        notes="Testprodukt"
    )

    repo.save_product(product)
    print("Produkt gespeichert")

    loaded = repo.load_product_by_id("P001")
    print("Ein Produkt geladen:")
    print(loaded)

    all_products = repo.load_all_products()
    print("Alle Produkte:")
    print(all_products)



if __name__ == "__main__":
    main()