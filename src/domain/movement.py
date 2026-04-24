from dataclasses import dataclass, field  # dataclass vereinfacht Klassen (automatisch __init__, __repr__, etc.)
from datetime import datetime  # für Zeitstempel
from typing import Optional  # erlaubt optionale (None) Werte


@dataclass
class Movement:
    """
    Repräsentiert eine Lagerbewegung:
    z. B. Verkauf, Nachlieferung, Korrektur
    """
    product_id: str
    product_name: str
    quantity_change: int  # positive for IN, negative for OUT → wichtig für Richtung der Bewegung
    movement_type: str  # 'IN', 'OUT', 'CORRECTION', 'INITIAL' → definiert Art der Bewegung
    performed_by: str = 'system'  # wer die Aktion ausgeführt hat (Default: system)
    reason: Optional[str] = None  # Grund kann fehlen (None erlaubt)
    timestamp: Optional[datetime] = None  # Zeitpunkt kann optional gesetzt werden
    id: Optional[str] = None  # interne ID (z. B. aus eigener Logik)
    # MongoDB compatibility fields
    movement_id: Optional[str] = None  # zweite ID für DB-Kompatibilität (Redundanz)
    old_quantity: int = 0  # Bestand vor der Änderung (für Nachvollziehbarkeit)
    new_quantity: int = 0  # Bestand nach der Änderung
    note: str = ""  # alternative Bezeichnung für reason (DB-Feld)
    created_at: datetime = field(default_factory=datetime.now)  # wird automatisch beim Erstellen gesetzt

    def __post_init__(self):  # wird nach automatischem __init__ der dataclass ausgeführt
        if self.timestamp is None:
            self.timestamp = datetime.now()  # setzt aktuellen Zeitpunkt falls nicht vorhanden
        if self.created_at is None:
            self.created_at = datetime.now()  # Absicherung falls created_at doch None ist
        if self.movement_id is None and self.id is not None:
            self.movement_id = self.id  # synchronisiert movement_id mit id falls nur id gesetzt ist
        if self.id is None and self.movement_id is not None:
            self.id = self.movement_id  # umgekehrt: setzt id aus movement_id
        if self.reason is None and self.note:
            self.reason = self.note  # übernimmt note als reason falls reason fehlt
        if not self.note and self.reason:
            self.note = self.reason  # übernimmt reason als note falls note leer ist

    def __repr__(self) -> str:  # definiert wie das Objekt als String dargestellt wird (z. B. beim print)
        return (
            f"Movement(id={self.id or self.movement_id}, product_id={self.product_id}, "  # nutzt id oder fallback movement_id
            f"type={self.movement_type}, change={self.quantity_change})"  # zeigt wichtigste Infos kompakt an
        )
    