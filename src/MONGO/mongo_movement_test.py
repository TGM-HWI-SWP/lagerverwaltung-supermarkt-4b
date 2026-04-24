from datetime import datetime  # für Zeitstempel beim Aktualisieren
from src.domain.movement import Movement  # Domain-Klasse für Lagerbewegungen
from src.adapters.mongodb_product_repository import MongoDBProductRepository  # Repository für Produkt-Zugriff
from src.adapters.mongodb_movement_repository import MongoDBMovementRepository  # Repository für Bewegungs-Zugriff

MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"  # MongoDB-Verbindungsstring

product_repo = MongoDBProductRepository(MONGO_URI)  # Repository für Produkte
movement_repo = MongoDBMovementRepository(MONGO_URI)  # Repository für Bewegungen


def generate_movement_id() -> str:  # erzeugt eine neue Movement-ID als Text
    count = len(movement_repo.load_all_movements()) + 1  # zählt vorhandene Bewegungen und erhöht um 1
    return f"M{count:03d}"  # formatiert ID z. B. als M001, M002, M003 (Dreistellige Zahlen)


def produkt_verkaufen() -> None:  # verkauft ein Produkt und reduziert den Bestand
    product_id = input("Welche Produkt-ID wurde verkauft? ").strip()  # liest Produkt-ID ein und entfernt Leerzeichen
    product = product_repo.load_product_by_id(product_id)  # lädt Produkt aus MongoDB

    if product is None:
        print("Produkt nicht gefunden.")  # Abbruch wenn Produkt-ID nicht existiert
        return

    print(f"\nProdukt gefunden: {product.name}")
    print(f"Aktueller Bestand: {product.quantity}")

    try:  # prüft, ob Eingabe in int umwandelbar ist
        verkaufsmenge = int(input("Wie viele Stück wurden verkauft? ").strip())  # wandelt Eingabe in Ganzzahl um
    except ValueError:
        print("Ungültige Menge.")  # Fehler wenn Eingabe keine Zahl ist
        return

    if verkaufsmenge <= 0:
        print("Die Menge muss größer als 0 sein.")  # verhindert 0 oder negative Verkaufsmenge
        return

    if verkaufsmenge > product.quantity:
        print("Nicht genug Bestand vorhanden.")  # verhindert negativen Lagerbestand
        return

    alte_menge = product.quantity  # speichert alten Bestand für Bewegungshistorie
    neue_menge = product.quantity - verkaufsmenge  # berechnet neuen Bestand nach Verkauf

    product.quantity = neue_menge  # aktualisiert Bestand im Produktobjekt
    product.updated_at = datetime.now()  # setzt Änderungszeitpunkt

    product_repo.save_product(product)  # speichert aktualisiertes Produkt in MongoDB

    movement = Movement(  # erstellt Bewegungseintrag für den Verkauf
        movement_id=generate_movement_id(),  # eindeutige ID für Bewegung
        product_id=product.id,
        product_name=product.name,
        movement_type="SALE",  # Typ der Bewegung: Verkauf
        old_quantity=alte_menge,
        quantity_change=-verkaufsmenge,  # negativ, weil Bestand sinkt
        new_quantity=neue_menge,
        note="Verkauf über Testmenü"
    )

    movement_repo.save_movement(movement)  # speichert Bewegung in MongoDB

    print("\nVerkauf erfolgreich gespeichert.")
    print(f"Alte Menge: {alte_menge}")
    print(f"Neue Menge: {neue_menge}")
    print(f"Movement-ID: {movement.movement_id}")


def produkt_einkaufen() -> None:  # kauft ein Produkt ein und erhöht den Bestand
    product_id = input("Welche Produkt-ID wurde eingekauft? ").strip()  # liest Produkt-ID ein
    product = product_repo.load_product_by_id(product_id)  # lädt Produkt aus MongoDB

    if product is None:
        print("Produkt nicht gefunden.")  # Abbruch wenn Produkt nicht existiert
        return

    print(f"\nProdukt gefunden: {product.name}")
    print(f"Aktueller Bestand: {product.quantity}")

    try:  # prüft gültige Zahleneingabe
        einkaufsmenge = int(input("Wie viele Stück wurden eingekauft? ").strip())  # wandelt Eingabe in int um
    except ValueError:
        print("Ungültige Menge.")  # Fehler bei nicht-numerischer Eingabe
        return

    if einkaufsmenge <= 0:
        print("Die Menge muss größer als 0 sein.")  # verhindert ungültige Menge
        return

    alte_menge = product.quantity  # merkt alten Bestand
    neue_menge = product.quantity + einkaufsmenge  # berechnet Bestand nach Einkauf

    product.quantity = neue_menge  # aktualisiert Bestand im Objekt
    product.updated_at = datetime.now()  # aktualisiert Änderungszeitpunkt

    product_repo.save_product(product)  # speichert Produktänderung

    movement = Movement(  # erstellt Bewegungseintrag für Einkauf
        movement_id=generate_movement_id(),  # erzeugt neue Movement-ID
        product_id=product.id,
        product_name=product.name,
        movement_type="PURCHASE",  # Typ der Bewegung: Einkauf
        old_quantity=alte_menge,
        quantity_change=einkaufsmenge,  # positiv, weil Bestand steigt
        new_quantity=neue_menge,
        note="Einkauf über Testmenü"
    )

    movement_repo.save_movement(movement)  # speichert Bewegungseintrag

    print("\nEinkauf erfolgreich gespeichert.")
    print(f"Alte Menge: {alte_menge}")
    print(f"Neue Menge: {neue_menge}")
    print(f"Movement-ID: {movement.movement_id}")


def bewegungen_anzeigen() -> None:  # zeigt alle gespeicherten Bewegungen
    movements = movement_repo.load_all_movements()  # lädt alle Bewegungen aus MongoDB

    if not movements:
        print("Keine Bewegungen gefunden.")  # Ausgabe wenn Liste leer ist
        return

    print("\n=== ALLE BEWEGUNGEN ===")
    for movement in movements:  # iteriert über alle Bewegungs-Dictionaries
        print(f"Movement-ID: {movement['movement_id']}")
        print(f"Produkt-ID: {movement['product_id']}")
        print(f"Produktname: {movement['product_name']}")
        print(f"Typ: {movement['movement_type']}")
        print(f"Alte Menge: {movement['old_quantity']}")
        print(f"Änderung: {movement['quantity_change']}")
        print(f"Neue Menge: {movement['new_quantity']}")
        print(f"Notiz: {movement['note']}")
        print(f"Datum: {movement['created_at']}")
        print("-" * 40)  # erzeugt Trennlinie mit 40 Bindestrichen


def bewegungen_von_produkt_anzeigen() -> None:  # zeigt Bewegungen für ein bestimmtes Produkt
    product_id = input("Für welche Produkt-ID willst du die Bewegungen sehen? ").strip()  # liest Filter-ID ein
    movements = movement_repo.load_movements_by_product_id(product_id)  # lädt Bewegungen passend zur Produkt-ID

    if not movements:
        print("Keine Bewegungen für dieses Produkt gefunden.")  # falls keine Bewegung existiert
        return

    print(f"\n=== BEWEGUNGEN FÜR {product_id} ===")
    for movement in movements:  # iteriert über gefilterte Bewegungen
        print(f"Movement-ID: {movement['movement_id']}")
        print(f"Typ: {movement['movement_type']}")
        print(f"Alte Menge: {movement['old_quantity']}")
        print(f"Änderung: {movement['quantity_change']}")
        print(f"Neue Menge: {movement['new_quantity']}")
        print(f"Notiz: {movement['note']}")
        print(f"Datum: {movement['created_at']}")
        print("-" * 40)  # optische Trennung der Ausgaben


def main() -> None:  # Hauptmenü des Testprogramms
    while True:  # läuft dauerhaft bis break
        print("\n=== MOVEMENT TEST MENÜ ===")
        print("1 - Produkt verkaufen")
        print("2 - Produkt einkaufen")
        print("3 - Alle Bewegungen anzeigen")
        print("4 - Bewegungen eines Produkts anzeigen")
        print("5 - Beenden")

        auswahl = input("Bitte wählen: ").strip()  # liest Menüauswahl ein

        if auswahl == "1":
            produkt_verkaufen()  # startet Verkaufslogik
        elif auswahl == "2":
            produkt_einkaufen()  # startet Einkaufslogik
        elif auswahl == "3":
            bewegungen_anzeigen()  # zeigt alle Bewegungen
        elif auswahl == "4":
            bewegungen_von_produkt_anzeigen()  # zeigt Bewegungen eines Produkts
        elif auswahl == "5":
            print("Programm beendet.")
            break  # beendet while-Schleife
        else:
            print("Ungültige Eingabe.")  # falls keine gültige Menüzahl eingegeben wurde


if __name__ == "__main__":  # startet main nur, wenn Datei direkt ausgeführt wird
    main()