from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Movement:
    """
    Repräsentiert eine Lagerbewegung:
    z. B. Verkauf, Nachlieferung, Korrektur
    """
    product_id: str
    product_name: str
    quantity_change: int  # positive for IN, negative for OUT
    movement_type: str  # 'IN', 'OUT', 'CORRECTION', 'INITIAL'
    performed_by: str = 'system'
    reason: Optional[str] = None
    timestamp: Optional[datetime] = None
    id: Optional[str] = None
    # MongoDB compatibility fields
    movement_id: Optional[str] = None
    old_quantity: int = 0
    new_quantity: int = 0
    note: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.movement_id is None and self.id is not None:
            self.movement_id = self.id
        if self.id is None and self.movement_id is not None:
            self.id = self.movement_id
        if self.reason is None and self.note:
            self.reason = self.note
        if not self.note and self.reason:
            self.note = self.reason

    def __repr__(self) -> str:
        return (
            f"Movement(id={self.id or self.movement_id}, product_id={self.product_id}, "
            f"type={self.movement_type}, change={self.quantity_change})"
        )

