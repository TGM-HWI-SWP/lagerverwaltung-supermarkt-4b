from datetime import datetime  # für Zeitstempel beim Update
from src.domain.product import Product  # Domain-Klasse für Produkte
from src.adapters.mongodb_product_repository import MongoDBProductRepository  # Repository für DB-Zugriff

MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"  # Verbindungsstring zur MongoDB (inkl. User, Passwort, Cluster)

repo = MongoDBProductRepository(MONGO_URI)  # erstellt Repository-Objekt für DB-Operationen


def produkte_anzeigen(repo: MongoDBProductRepository) -> None:  # zeigt alle Produkte aus der DB an
    produkte = repo.load_all_products()  # lädt alle Produkte aus MongoDB

    if not produkte:
        print("Keine Produkte gefunden.")  # Ausgabe wenn Liste leer ist
        return

    print("\n=== PRODUKTE ===")
    for product in produkte:  # iteriert über alle Produkte
        print(f"ID: {product.id}")
        print(f"Name: {product.name}")
        print(f"Beschreibung: {product.description}")
        print(f"Preis: {product.price}")
        print(f"Menge: {product.quantity}")
        print(f"SKU: {product.sku}")
        print(f"Kategorie: {product.category}")
        print(f"Notizen: {product.notes}")
        print("-" * 30)  # trennt Produkte optisch


def produkt_aendern(repo: MongoDBProductRepository) -> None:  # erlaubt Benutzer, ein Produkt zu bearbeiten
    produkt_id = input("Welche Produkt-ID willst du ändern? ").strip()  # entfernt Leerzeichen vorne/hinten
    product = repo.load_product_by_id(produkt_id)  # lädt Produkt anhand ID

    if product is None:
        print("Produkt nicht gefunden.")  # Fehlerfall wenn ID nicht existiert
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

    neuer_name = input(f"Neuer Name [{product.name}]: ").strip()  # zeigt alten Wert als Vorschlag
    neue_beschreibung = input(f"Neue Beschreibung [{product.description}]: ").strip()
    neuer_preis = input(f"Neuer Preis [{product.price}]: ").strip()
    neue_menge = input(f"Neue Menge [{product.quantity}]: ").strip()
    neue_sku = input(f"Neue SKU [{product.sku}]: ").strip()
    neue_kategorie = input(f"Neue Kategorie [{product.category}]: ").strip()
    neue_notizen = input(f"Neue Notizen [{product.notes}]: ").strip()

    aktualisiertes_produkt = Product(
        product.id,
        neuer_name if neuer_name else product.name,  # nutzt neuen Wert oder alten wenn leer
        neue_beschreibung if neue_beschreibung else product.description,
        float(neuer_preis) if neuer_preis else product.price,  # Umwandlung String → float
        neue_kategorie if neue_kategorie else product.category,
        int(neue_menge) if neue_menge else product.quantity,  # Umwandlung String → int
        product.min_stock
    )

    aktualisiertes_produkt.id = product.id  # stellt sicher, dass ID gleich bleibt
    aktualisiertes_produkt.product_id = product.id  # doppelte ID für Kompatibilität
    aktualisiertes_produkt.sku = neue_sku if neue_sku else product.sku  # übernimmt neuen oder alten Wert
    aktualisiertes_produkt.notes = neue_notizen if neue_notizen else product.notes
    aktualisiertes_produkt.created_at = product.created_at  # ursprüngliches Erstellungsdatum behalten
    aktualisiertes_produkt.updated_at = datetime.now()  # setzt neues Änderungsdatum

    repo.save_product(aktualisiertes_produkt)  # speichert Änderungen in DB (update_one mit upsert)
    print("Produkt erfolgreich aktualisiert.")


def main() -> None:  # Hauptmenü der Anwendung
    while True:  # Endlosschleife bis Benutzer beendet
        print("\n=== MONGO TEST MENÜ ===")
        print("1 - Produkte anzeigen")
        print("2 - Produkt ändern")
        print("3 - Beenden")

        auswahl = input("Bitte wählen: ").strip()  # liest Eingabe vom Benutzer

        if auswahl == "1":
            produkte_anzeigen(repo)  # zeigt Produkte
        elif auswahl == "2":
            produkt_aendern(repo)  # startet Bearbeitung
        elif auswahl == "3":
            print("Programm beendet.")
            break  # beendet Schleife → Programm endet
        else:
            print("Ungültige Eingabe.")  # Fehler bei falscher Eingabe


if __name__ == "__main__":  # sorgt dafür, dass main nur beim direkten Start ausgeführt wird
    main()