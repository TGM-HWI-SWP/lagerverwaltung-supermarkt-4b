import sqlite3
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from src.ports.ports import RepositoryPort
from src.domain.product import Product
from src.domain.movement import Movement

class SQLiteRepository(RepositoryPort):
    """SQLite persistence adapter."""

    def __init__(self, db_path: str = "warehouse.db"):
        self.db_path = Path(db_path)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cursor = self._conn.cursor()
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT,
                quantity INTEGER NOT NULL DEFAULT 0,
                min_stock INTEGER NOT NULL DEFAULT 5,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        # Movements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movements (
                id TEXT PRIMARY KEY,
                product_id TEXT,
                product_name TEXT,
                quantity_change INTEGER,
                movement_type TEXT,
                reason TEXT,
                timestamp TEXT,
                performed_by TEXT,
                FOREIGN KEY(product_id) REFERENCES products(product_id)
            )
        ''')
        self._conn.commit()

    def add(self, product: Product) -> None:
        cursor = self._conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO products 
            (product_id, name, description, price, category, quantity, min_stock, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product.product_id, product.name, product.description, product.price,
            product.category, product.quantity, product.min_stock,
            product.created_at.isoformat(), product.updated_at.isoformat()
        ))
        # Initial movement
        initial = Movement(
            product_id=product.product_id, product_name=product.name,
            quantity_change=product.quantity, movement_type="INITIAL",
            reason="Initial stock", performed_by="system"
        )
        self.save_movement(initial)
        self._conn.commit()

    def get(self, product_id: str) -> Optional[Product]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        if row:
<<<<<<< HEAD
            # Skip product_id, pass explicitly: product_id=row[0], name=row[1], desc=row[2], price=row[3], category=row[4], quantity=row[5], min_stock=row[6]
            return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
=======
            # Map row to Product constructor: product_id, name, desc, price, cat, qty, min_stock ignored for constructor
            product = Product(
                product_id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                category=row[4],
                quantity=row[5]
            )
            product.min_stock = row[6]  # Set manually
            return product
>>>>>>> origin/main
        return None

    def get_all(self) -> Dict[str, Product]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        products = {}
        for row in rows:
            product_id = row[0]
<<<<<<< HEAD
            product = Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
=======
            product = Product(
                product_id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                category=row[4],
                quantity=row[5]
            )
            product.min_stock = row[6]
>>>>>>> origin/main
            products[product_id] = product
        return products

    def delete(self, product_id: str) -> None:
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        self._conn.commit()

    def save_movement(self, movement: Movement) -> None:
        cursor = self._conn.cursor()
        cursor.execute('''
            INSERT INTO movements 
            (id, product_id, product_name, quantity_change, movement_type, reason, timestamp, performed_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            movement.id, movement.product_id, movement.product_name,
            movement.quantity_change, movement.movement_type,
            movement.reason, movement.timestamp.isoformat(), movement.performed_by
        ))
        self._conn.commit()

    def get_movements(self) -> List[Movement]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM movements ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        movements = []
        for row in rows:
            movements.append(Movement(*row[1:]))  # Skip id if auto
        return movements

    def __del__(self):
        if hasattr(self, '_conn'):
            self._conn.close()
