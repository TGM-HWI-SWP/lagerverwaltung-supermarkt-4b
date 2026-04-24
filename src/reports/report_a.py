from src.adapters.mongodb_product_repository import MongoDBProductRepository


def generate_inventory_report(repo: MongoDBProductRepository) -> str:
    """
    Report A: Lagerbestandsübersicht
    """

    products = repo.load_all_products()
    low_stock = [p for p in products if p.is_low_stock()]
    total_value = sum(p.get_total_value() for p in products)

    report = "=== LAGERBESTANDSREPORT A ===\n\n"
    report += f"Gesamtwert: {total_value:.2f} €\n"
    report += f"Warnbestände: {len(low_stock)}\n\n"
    report += "Produkte:\n"

    for p in products:
        mark = "[LOW]" if p.is_low_stock() else "[OK]"

        product_id = getattr(p, "id", getattr(p, "product_id", "OHNE-ID"))
        category = getattr(p, "category", "Keine Kategorie")

        report += (
            f"{mark} {product_id} | {p.name} | {p.quantity} Stk | "
            f"Min: {p.min_stock} | {p.get_total_value():.2f} € ({category})\n"
        )

    if low_stock:
        report += "\nAchtung - Nachbestellen:\n"
        for p in low_stock:
            product_id = getattr(p, "id", getattr(p, "product_id", "OHNE-ID"))
            report += f"  {product_id} | {p.name} ({p.quantity}/{p.min_stock})\n"

    return report