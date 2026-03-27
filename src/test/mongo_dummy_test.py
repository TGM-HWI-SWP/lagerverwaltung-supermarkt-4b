from src.adapters.mongodb_product_repository import MongoDBProductRepository
from src.domain.product import Product

MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:Gabi1234.@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"


def zeige_alle_produkte(repo: MongoDBProductRepository) -> None:
    products = repo.load_all_products()

    if not products:
        print("\nKeine Produkte gefunden.\n")
        return

    print("\n--- ALLE PRODUKTE ---")
    for product in products:
        print(f"ID: {product.id}")
        print(f"Name: {product.name}")
        print(f"Beschreibung: {product.description}")
        print(f"Preis: {product.price}")
        print(f"Menge: {product.quantity}")
        print(f"SKU: {product.sku}")
        print(f"Kategorie: {product.category}")
        print(f"Notizen: {product.notes}")
        print("-" * 30)
    print()


def produkt_aendern(repo: MongoDBProductRepository) -> None:
    product_id = input("Welche Produkt-ID willst du ändern? ").strip()

    product = repo.load_product_by_id(product_id)

    if product is None:
        print("\nProdukt nicht gefunden.\n")
        return

    print("\nAktuelle Daten:")
    print(f"ID: {product.id}")
    print(f"Name: {product.name}")
    print(f"Beschreibung: {product.description}")
    print(f"Preis: {product.price}")
    print(f"Menge: {product.quantity}")
    print(f"SKU: {product.sku}")
    print(f"Kategorie: {product.category}")
    print(f"Notizen: {product.notes}")
    print()

    neuer_name = input(f"Neuer Name [{product.name}]: ").strip()
    neue_beschreibung = input(f"Neue Beschreibung [{product.description}]: ").strip()
    neuer_preis = input(f"Neuer Preis [{product.price}]: ").strip()
    neue_menge = input(f"Neue Menge [{product.quantity}]: ").strip()
    neue_sku = input(f"Neue SKU [{product.sku}]: ").strip()
    neue_kategorie = input(f"Neue Kategorie [{product.category}]: ").strip()
    neue_notizen = input(f"Neue Notizen [{product.notes}]: ").strip()

    aktualisiertes_produkt = Product(
        id=product.id,
        name=neuer_name if neuer_name else product.name,
        description=neue_beschreibung if neue_beschreibung else product.description,
        price=float(neuer_preis) if neuer_preis else product.price,
        quantity=int(neue_menge) if neue_menge else product.quantity,
        sku=neue_sku if neue_sku else product.sku,
        category=neue_kategorie if neue_kategorie else product.category,
        created_at=product.created_at,
        updated_at=product.updated_at,
        notes=neue_notizen if neue_notizen else product.notes,
    )

    repo.save_product(aktualisiertes_produkt)
    print("\nProdukt erfolgreich geändert.\n")


def main() -> None:
    repo = MongoDBProductRepository(MONGO_URI)

    while True:
        print("=== MONGO TEST MENÜ ===")
        print("1 - Produkte anzeigen")
        print("2 - Produkt ändern")
        print("3 - Beenden")

        auswahl = input("Bitte wählen: ").strip()

        if auswahl == "1":
            zeige_alle_produkte(repo)
        elif auswahl == "2":
            produkt_aendern(repo)
        elif auswahl == "3":
            print("\nProgramm beendet.")
            break
        else:
            print("\nUngültige Eingabe.\n")


if __name__ == "__main__":
    main()