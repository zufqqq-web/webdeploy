import json
import sqlite3
from database.connection import get_db

class ProductRepository:
    @staticmethod
    def row_to_dict(row: sqlite3.Row | None) -> dict | None:
        if row is None:
            return None

        try:
            ingredients = json.loads(row["ingredients"])
            if not isinstance(ingredients, list):
                ingredients = [str(ingredients)]
        except Exception:
            raw = str(row["ingredients"] or "")
            ingredients = [item.strip() for item in raw.split(",") if item.strip()]

        return {
            "id": row["id"],
            "name": row["name"],
            "description": row["description"] or "",
            "ingredients": ingredients,
            "category": row["category"] or "other",
            "image": row["image"] or "",
            "price_25": row["price_25"] or 0,
            "price_30": row["price_30"] or 0,
            "price_35": row["price_35"] or 0,
            "prices": {
                25: row["price_25"] or 0,
                30: row["price_30"] or 0,
                35: row["price_35"] or 0,
            },
            "is_active": bool(row["is_active"]),
            "active": bool(row["is_active"]),
        }

    @classmethod
    def get_all(cls, category: str | None = None, active_only: bool = False) -> list[dict]:
        query = "SELECT * FROM products WHERE 1=1"
        params: list = []

        if active_only:
            query += " AND is_active=1"

        if category:
            query += " AND category=?"
            params.append(category)

        query += " ORDER BY id"

        with get_db() as conn:
            rows = conn.execute(query, params).fetchall()

        return [cls.row_to_dict(row) for row in rows if row]

    @classmethod
    def get_active(cls, category: str | None = None) -> list[dict]:
        return cls.get_all(category=category, active_only=True)

    @classmethod
    def get_by_id(cls, product_id: int, active_only: bool = False) -> dict | None:
        query = "SELECT * FROM products WHERE id=?"
        params: list = [product_id]

        if active_only:
            query += " AND is_active=1"

        with get_db() as conn:
            row = conn.execute(query, params).fetchone()

        return cls.row_to_dict(row)

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        ingredients: list[str],
        category: str,
        image: str,
        price_25: int,
        price_30: int,
        price_35: int,
        is_active: int = 1,
    ) -> int:
        with get_db() as conn:
            cursor = conn.execute(
                """
                INSERT INTO products (
                    name,
                    description,
                    ingredients,
                    category,
                    image,
                    price_25,
                    price_30,
                    price_35,
                    is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name.strip(),
                    description.strip(),
                    json.dumps(ingredients, ensure_ascii=False),
                    category.strip(),
                    image.strip(),
                    price_25,
                    price_30,
                    price_35,
                    1 if is_active else 0,
                ),
            )
            return cursor.lastrowid

    @classmethod
    def update(
        cls,
        product_id: int,
        name: str | None = None,
        description: str | None = None,
        ingredients: list[str] | None = None,
        category: str | None = None,
        image: str | None = None,
        price_25: int | None = None,
        price_30: int | None = None,
        price_35: int | None = None,
        is_active: bool | int | None = None,
    ) -> bool:
        updates = []
        params = []

        if name is not None:
            updates.append("name=?")
            params.append(name.strip())
        if description is not None:
            updates.append("description=?")
            params.append(description.strip())
        if ingredients is not None:
            updates.append("ingredients=?")
            params.append(json.dumps(ingredients, ensure_ascii=False))
        if category is not None:
            updates.append("category=?")
            params.append(category.strip())
        if image is not None:
            updates.append("image=?")
            params.append(image.strip())
        if price_25 is not None:
            updates.append("price_25=?")
            params.append(price_25)
        if price_30 is not None:
            updates.append("price_30=?")
            params.append(price_30)
        if price_35 is not None:
            updates.append("price_35=?")
            params.append(price_35)
        if is_active is not None:
            updates.append("is_active=?")
            params.append(1 if is_active else 0)

        if not updates:
            return False

        params.append(product_id)
        query = f"UPDATE products SET {', '.join(updates)} WHERE id=?"

        with get_db() as conn:
            cursor = conn.execute(query, params)
            return cursor.rowcount > 0

    @classmethod
    def set_active(cls, product_id: int, is_active: bool) -> bool:
        with get_db() as conn:
            cursor = conn.execute(
                "UPDATE products SET is_active=? WHERE id=?",
                (1 if is_active else 0, product_id),
            )
            return cursor.rowcount > 0

    @classmethod
    def delete(cls, product_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.execute("DELETE FROM products WHERE id=?", (product_id,))
            return cursor.rowcount > 0
