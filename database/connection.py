import os
import sqlite3
from datetime import datetime
from pathlib import Path
from config import settings

def get_db() -> sqlite3.Connection:
    """Возвращает соединение с базой данных SQLite."""
    db_path = Path(settings.DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def now_str() -> str:
    """Возвращает текущую дату и время в строковом формате."""
    return datetime.now().strftime("%d.%m.%Y %H:%M")

def init_db() -> None:
    """
    Инициализирует таблицы базы данных, если они ещё не созданы.
    Существующие таблицы и данные НЕ удаляются и НЕ перезаписываются.
    """
    with get_db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                ingredients TEXT DEFAULT '[]',
                category TEXT DEFAULT 'pizza',
                image TEXT DEFAULT '',
                price_25 INTEGER NOT NULL DEFAULT 0,
                price_30 INTEGER NOT NULL DEFAULT 0,
                price_35 INTEGER NOT NULL DEFAULT 0,
                is_active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                username TEXT,
                client_name TEXT,
                phone TEXT,
                address TEXT,
                comment TEXT,
                source TEXT,
                status TEXT DEFAULT 'expected',
                total INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                name TEXT,
                size INTEGER,
                qty INTEGER,
                price INTEGER,
                line_total INTEGER,
                FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT DEFAULT '',
                full_name TEXT DEFAULT '',
                created_at TEXT,
                updated_at TEXT,
                is_blocked INTEGER NOT NULL DEFAULT 0
            );
            """
        )
