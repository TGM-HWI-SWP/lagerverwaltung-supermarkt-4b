from datetime import datetime


class Movement:
    """
    Repräsentiert eine Lagerbewegung:
    z. B. Verkauf, Nachlieferung, Korrektur
    """

    def __init__(
        self,
        movement_id: str,
        product_id: str,
        product_name: str,
        movement_type: str,
        old_quantity: int,
        quantity_change: int,
        new_quantity: int,
        note: str = ""
    ):
        self.movement_id = movement_id
        self.product_id = product_id
        self.product_name = product_name
        self.movement_type = movement_type
        self.old_quantity = old_quantity
        self.quantity_change = quantity_change
        self.new_quantity = new_quantity
        self.note = note
        self.created_at = datetime.now()

    def __repr__(self) -> str:
        return (
            f"Movement(id={self.movement_id}, product_id={self.product_id}, "
            f"type={self.movement_type}, change={self.quantity_change})"
        )