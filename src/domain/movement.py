from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Movement:
    """Immutable Lagerbewegung for auditing."""
    id: str = None
    product_id: str
    product_name: str
    quantity_change: int  # positive for IN, negative for OUT
    movement_type: str  # "IN", "OUT", "CORRECTION", "INITIAL"
    reason: Optional[str] = None
    timestamp: datetime = None
    performed_by: Optional[str] = "system"

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now()
