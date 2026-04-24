from dataclasses import dataclass, field  # dataclass vereinfacht Klassendefinition durch automatische Methoden
from datetime import datetime  # für Zeitstempel bei Bewegungen
from typing import Optional  # erlaubt optionale Werte die auch None sein können


@dataclass  # automatisch erzeugt init repr und eq basierend auf Feldern
class Movement:
    """
    Repräsentiert eine Lagerbewegung:
    z. B. Verkauf, Nachlieferung, Korrektur
    """
    product_id: str  # ID des betroffenen Produkts
    product_name: str  # Name des betroffenen Produkts
    quantity_change: int  # positiv für Einbuchung negativ für Ausbuchung
    movement_type: str  # IN OUT CORRECTION oder INITIAL definiert Art der Bewegung
    performed_by: str = 'system'  # wer die Aktion ausgeführt hat Standard ist system
    reason: Optional[str] = None  # Grund kann fehlen daher Optional
    timestamp: Optional[datetime] = None  # Zeitpunkt kann optional gesetzt werden
    id: Optional[str] = None  # interne ID aus eigener Logik
    # MongoDB compatibility fields
    movement_id: Optional[str] = None  # zweite ID für Datenbank Kompatibilität
    old_quantity: int = 0  # Bestand vor der Änderung für Nachvollziehbarkeit
    new_quantity: int = 0  # Bestand nach der Änderung
    note: str = ""  # alternatives Feld für reason aus Datenbank
    created_at: datetime = field(default_factory=datetime.now)  # wird automatisch beim Erstellen auf jetzt gesetzt

    def __post_init__(self):  # wird nach automatischem init der dataclass ausgeführt
        if self.timestamp is None:
            self.timestamp = datetime.now()  # setzt aktuellen Zeitpunkt falls nicht vorhanden
        if self.created_at is None:
            self.created_at = datetime.now()  # Absicherung falls created_at doch None ist
        if self.movement_id is None and self.id is not None:
            self.movement_id = self.id  # synchronisiert movement_id mit id falls nur id gesetzt ist
        if self.id is None and self.movement_id is not None:
            self.id = self.movement_id  # umgekehrt setzt id aus movement_id
        if self.reason is None and self.note:
            self.reason = self.note  # übernimmt note als reason falls reason fehlt
        if not self.note and self.reason:
            self.note = self.reason  # übernimmt reason als note falls note leer ist

    def __repr__(self) -> str:
        return (
            f"Movement(id={self.id or self.movement_id}, product_id={self.product_id}, "  # nutzt id oder fallback movement_id
            f"type={self.movement_type}, change={self.quantity_change})"  # zeigt wichtigste Infos kompakt an
        )

