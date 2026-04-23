from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Movement:
    """Immutable Lagerbewegung for auditing."""
    product_id: str
    product_name: str
    quantity_change: int  # positive for IN, negative for OUT
    movement_type: str  # "IN", "OUT", "CORRECTION", "INITIAL"
    performed_by: str = "system"
    reason: Optional[str] = None
<<<<<<< HEAD
    timestamp: Optional[datetime] = None
    id: Optional[str] = None
=======
    timestamp: datetime = None
    performed_by: Optional[str] = "system"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
>>>>>>> origin/main

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
