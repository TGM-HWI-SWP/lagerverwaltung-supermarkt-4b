class ConsoleReportAdapter:

    def print_inventory(self, products):

        print("===== INVENTORY REPORT =====")

        total = 0

        for p in products:
            value = p.price * p.quantity
            total += value

            print(p.name, "| qty:", p.quantity, "| value:", value)

        print("-------------------")
        print("TOTAL:", total)