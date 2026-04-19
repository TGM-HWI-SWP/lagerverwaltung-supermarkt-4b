from datetime import datetime
from src.domain.product import Product
from src.adapters.mongodb_product_repository import MongoDBProductRepository

MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"

repo = MongoDBProductRepository(MONGO_URI)


def produkte_anzeigen(repo: MongoDBProductRepository) -> None:
    produkte = repo.load_all_products()

    if not produkte:
        print("Keine Produkte gefunden.")
        return

    print("\n=== PRODUKTE ===")
    for product in produkte:
        print(f"ID: {product.id}")
        print(f"Name: {product.name}")
        print(f"Beschreibung: {product.description}")
        print(f"Preis: {product.price}")
        print(f"Menge: {product.quantity}")
        print(f"SKU: {product.sku}")
        print(f"Kategorie: {product.category}")
        print(f"Notizen: {product.notes}")
        print("-" * 30)


def produkt_aendern(repo: MongoDBProductRepository) -> None:
    produkt_id = input("Welche Produkt-ID willst du ändern? ").strip()
    product = repo.load_product_by_id(produkt_id)

    if product is None:
        print("Produkt nicht gefunden.")
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

    neuer_name = input(f"Neuer Name [{product.name}]: ").strip()
    neue_beschreibung = input(f"Neue Beschreibung [{product.description}]: ").strip()
    neuer_preis = input(f"Neuer Preis [{product.price}]: ").strip()
    neue_menge = input(f"Neue Menge [{product.quantity}]: ").strip()
    neue_sku = input(f"Neue SKU [{product.sku}]: ").strip()
    neue_kategorie = input(f"Neue Kategorie [{product.category}]: ").strip()
    neue_notizen = input(f"Neue Notizen [{product.notes}]: ").strip()

    aktualisiertes_produkt = Product(
        product.id,
        neuer_name if neuer_name else product.name,
        neue_beschreibung if neue_beschreibung else product.description,
        float(neuer_preis) if neuer_preis else product.price,
        neue_kategorie if neue_kategorie else product.category,
        int(neue_menge) if neue_menge else product.quantity,
        product.min_stock
    )

    aktualisiertes_produkt.id = product.id
    aktualisiertes_produkt.product_id = product.id
    aktualisiertes_produkt.sku = neue_sku if neue_sku else product.sku
    aktualisiertes_produkt.notes = neue_notizen if neue_notizen else product.notes
    aktualisiertes_produkt.created_at = product.created_at
    aktualisiertes_produkt.updated_at = datetime.now()

    repo.save_product(aktualisiertes_produkt)
    print("Produkt erfolgreich aktualisiert.")


def main() -> None:
    while True:
        print("\n=== MONGO TEST MENÜ ===")
        print("1 - Produkte anzeigen")
        print("2 - Produkt ändern")
        print("3 - Beenden")

        auswahl = input("Bitte wählen: ").strip()

        if auswahl == "1":
            produkte_anzeigen(repo)
        elif auswahl == "2":
            produkt_aendern(repo)
        elif auswahl == "3":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Eingabe.")


if __name__ == "__main__":
    main()