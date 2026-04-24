class ConsoleReportAdapter:  # Adapter Klasse für Konsolen Reports

    def print_inventory(self, products):  # Methode zum Ausgeben des Lagerbestands

        print("===== INVENTORY REPORT =====")  # Ausgabe der Report Überschrift

        total = 0  # Initialisierung der Gesamtsumme

        for p in products:  # Schleife über alle übergebenen Produkte
            value = p.price * p.quantity  # berechnet Wert pro Produktzeile
            total += value  # addiert zum Gesamtwert hinzu

            print(p.name, "| qty:", p.quantity, "| value:", value)  # gibt Produktzeile aus

        print("-------------------")  # Trennlinie vor Summe
        print("TOTAL:", total)  # gibt Gesamtwert aller Produkte aus

