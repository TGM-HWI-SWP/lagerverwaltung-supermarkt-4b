from src.services import WarehouseService

def generate_inventory_report(service: WarehouseService) -> str:
    """
    Report A: Lagerbestandsuebersicht (Pflicht fuer 3er-Gruppe).
    """
    products = service.get_all_products()
    low_stock = service.get_low_stock_products()
    
    report = "=== LAGERBESTANDSREPORT A ===\\n\\n"
    report += f"Gesamtwert: {service.get_total_inventory_value():.2f} €\\n"
    report += f"Warnbestände: {len(low_stock)}\\n\\n"
    
    report += "Produkte:\\n"
    for pid, p in products.items():
        mark = "[LOW]" if p.is_low_stock() else "[OK] "
        report += f"{mark} {p.name} | {p.quantity} Stk | {p.get_total_value():.2f} € ({p.category})\\n"
    
    if low_stock:
        report += "\\nAchtung - Nachbestellen:\\n"
        for p in low_stock:
            report += f"  {p.name} ({p.quantity}/{p.min_stock})\\n"
    
    return report
