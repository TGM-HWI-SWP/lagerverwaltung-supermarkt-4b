from src.adapters.mongodb_product_repository import MongoDBProductRepository  # Repository für Zugriff auf Produktdaten


def generate_inventory_report(repo: MongoDBProductRepository) -> str:  # erzeugt einen Text-Report basierend auf DB-Daten
    """
    Report A: Lagerbestandsübersicht
    """

    products = repo.load_all_products()  # lädt alle Produkte aus der Datenbank
    low_stock = [p for p in products if p.is_low_stock()]  # filtert Produkte mit niedrigem Bestand
    total_value = sum(p.get_total_value() for p in products)  # berechnet Gesamtwert aller Produkte

    report = "=== LAGERBESTANDSREPORT A ===\n\n"
    report += f"Gesamtwert: {total_value:.2f} €\n"  # :.2f formatiert Zahl auf 2 Dezimalstellen
    report += f"Warnbestände: {len(low_stock)}\n\n"  # Anzahl der Produkte unter Mindestbestand
    report += "Produkte:\n"

    for p in products:  # iteriert über alle Produkte
        mark = "[LOW]" if p.is_low_stock() else "[OK]"  # kennzeichnet Produkte mit niedrigem Bestand

        product_id = getattr(p, "id", getattr(p, "product_id", "OHNE-ID"))  # holt Attribut dynamisch, vermeidet Fehler wenn Feld fehlt
        category = getattr(p, "category", "Keine Kategorie")  # fallback falls Kategorie nicht existiert

        report += (
            f"{mark} {product_id} | {p.name} | {p.quantity} Stk | "
            f"Min: {p.min_stock} | {p.get_total_value():.2f} € ({category})\n"  # fügt formatierte Produktdaten hinzu
        )

    if low_stock:
        report += "\nAchtung - Nachbestellen:\n"  # Hinweisbereich für kritische Produkte
        for p in low_stock:  # iteriert nur über Produkte mit niedrigem Bestand
            product_id = getattr(p, "id", getattr(p, "product_id", "OHNE-ID"))  # gleiche sichere ID-Ermittlung
            report += f"  {product_id} | {p.name} ({p.quantity}/{p.min_stock})\n"  # zeigt aktuellen vs. Mindestbestand

    return report  # gibt fertigen Report als String zurück