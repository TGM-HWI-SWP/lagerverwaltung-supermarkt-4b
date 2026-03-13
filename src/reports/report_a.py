def generate_inventory_report(products):
    total_value = 0
    report_lines = []

    for p in products:
        value = p.price * p.quantity
        total_value += value
        report_lines.append(f"{p.name} → {p.quantity} → {value:.2f} €")

    report_lines.append(f"GESAMTWERT → {total_value:.2f} €")
    return "\n".join(report_lines)