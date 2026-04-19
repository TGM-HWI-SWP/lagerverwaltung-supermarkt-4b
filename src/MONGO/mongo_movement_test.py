from datetime import datetime
from src.MONGO.mongo_movements import Movement
from src.adapters.mongodb_product_repository import MongoDBProductRepository
from src.adapters.mongodb_movement_repository import MongoDBMovementRepository

MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"

product_repo = MongoDBProductRepository(MONGO_URI)
movement_repo = MongoDBMovementRepository(MONGO_URI)


def generate_movement_id() -> str:
    count = len(movement_repo.load_all_movements()) + 1
    return f"M{count:03d}"


def produkt_verkaufen() -> None:
    product_id = input("Welche Produkt-ID wurde verkauft? ").strip()
    product = product_repo.load_product_by_id(product_id)

    if product is None:
        print("Produkt nicht gefunden.")
        return

    print(f"\nProdukt gefunden: {product.name}")
    print(f"Aktueller Bestand: {product.quantity}")

    try:
        verkaufsmenge = int(input("Wie viele Stück wurden verkauft? ").strip())
    except ValueError:
        print("Ungültige Menge.")
        return

    if verkaufsmenge <= 0:
        print("Die Menge muss größer als 0 sein.")
        return

    if verkaufsmenge > product.quantity:
        print("Nicht genug Bestand vorhanden.")
        return

    alte_menge = product.quantity
    neue_menge = product.quantity - verkaufsmenge

    product.quantity = neue_menge
    product.updated_at = datetime.now()

    product_repo.save_product(product)

    movement = Movement(
        movement_id=generate_movement_id(),
        product_id=product.id,
        product_name=product.name,
        movement_type="SALE",
        old_quantity=alte_menge,
        quantity_change=-verkaufsmenge,
        new_quantity=neue_menge,
        note="Verkauf über Testmenü"
    )

    movement_repo.save_movement(movement)

    print("\nVerkauf erfolgreich gespeichert.")
    print(f"Alte Menge: {alte_menge}")
    print(f"Neue Menge: {neue_menge}")
    print(f"Movement-ID: {movement.movement_id}")


def bewegungen_anzeigen() -> None:
    movements = movement_repo.load_all_movements()

    if not movements:
        print("Keine Bewegungen gefunden.")
        return

    print("\n=== ALLE BEWEGUNGEN ===")
    for movement in movements:
        print(f"Movement-ID: {movement['movement_id']}")
        print(f"Produkt-ID: {movement['product_id']}")
        print(f"Produktname: {movement['product_name']}")
        print(f"Typ: {movement['movement_type']}")
        print(f"Alte Menge: {movement['old_quantity']}")
        print(f"Änderung: {movement['quantity_change']}")
        print(f"Neue Menge: {movement['new_quantity']}")
        print(f"Notiz: {movement['note']}")
        print(f"Datum: {movement['created_at']}")
        print("-" * 40)


def bewegungen_von_produkt_anzeigen() -> None:
    product_id = input("Für welche Produkt-ID willst du die Bewegungen sehen? ").strip()
    movements = movement_repo.load_movements_by_product_id(product_id)

    if not movements:
        print("Keine Bewegungen für dieses Produkt gefunden.")
        return

    print(f"\n=== BEWEGUNGEN FÜR {product_id} ===")
    for movement in movements:
        print(f"Movement-ID: {movement['movement_id']}")
        print(f"Typ: {movement['movement_type']}")
        print(f"Alte Menge: {movement['old_quantity']}")
        print(f"Änderung: {movement['quantity_change']}")
        print(f"Neue Menge: {movement['new_quantity']}")
        print(f"Notiz: {movement['note']}")
        print(f"Datum: {movement['created_at']}")
        print("-" * 40)


def main() -> None:
    while True:
        print("\n=== MOVEMENT TEST MENÜ ===")
        print("1 - Produkt verkaufen")
        print("2 - Alle Bewegungen anzeigen")
        print("3 - Bewegungen eines Produkts anzeigen")
        print("4 - Beenden")

        auswahl = input("Bitte wählen: ").strip()

        if auswahl == "1":
            produkt_verkaufen()
        elif auswahl == "2":
            bewegungen_anzeigen()
        elif auswahl == "3":
            bewegungen_von_produkt_anzeigen()
        elif auswahl == "4":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Eingabe.")


if __name__ == "__main__":
    main()