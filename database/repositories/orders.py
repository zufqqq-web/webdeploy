from database.connection import get_db, now_str
from config.constants import STATUS_EXPECTED

class OrderRepository:
    @staticmethod
    def create(
        user_id: int | None,
        user_name: str,
        username: str,
        client_name: str,
        phone: str,
        address: str,
        comment: str,
        source: str,
        items: list[dict],
        status: str = STATUS_EXPECTED,
    ) -> int | None:
        if not items:
            return None

        total = sum(item["line_total"] for item in items)
        created_at = now_str()

        with get_db() as conn:
            cursor = conn.execute(
                """
                INSERT INTO orders (
                    user_id,
                    user_name,
                    username,
                    client_name,
                    phone,
                    address,
                    comment,
                    source,
                    status,
                    total,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    user_name or "",
                    username or "",
                    client_name or "",
                    phone or "",
                    address or "",
                    comment or "",
                    source or "🤖 Telegram Bot",
                    status,
                    total,
                    created_at,
                    created_at,
                ),
            )

            order_id = cursor.lastrowid

            for item in items:
                conn.execute(
                    """
                    INSERT INTO order_items (
                        order_id,
                        product_id,
                        name,
                        size,
                        qty,
                        price,
                        line_total
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        order_id,
                        item.get("product_id"),
                        item.get("name", ""),
                        item.get("size", 0),
                        item.get("qty", 1),
                        item.get("price", 0),
                        item.get("line_total", 0),
                    ),
                )

        return order_id

    @staticmethod
    def get_by_id(order_id: int) -> dict | None:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_items(order_id: int) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM order_items WHERE order_id=? ORDER BY id",
                (order_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def get_list(status: str | None = None, limit: int = 50) -> list[dict]:
        query = "SELECT * FROM orders"
        params: list = []

        if status and status != "all":
            query += " WHERE status=?"
            params.append(status)

        query += " ORDER BY id DESC"
        if limit:
            query += " LIMIT ?"
            params.append(limit)

        with get_db() as conn:
            rows = conn.execute(query, params).fetchall()

        return [dict(row) for row in rows]

    @staticmethod
    def update_status(order_id: int, status: str) -> bool:
        with get_db() as conn:
            cursor = conn.execute(
                "UPDATE orders SET status=?, updated_at=? WHERE id=?",
                (status, now_str(), order_id),
            )
            return cursor.rowcount > 0

    @staticmethod
    def get_stats() -> dict:
        """Возвращает статистику по заказам для дашборда админки."""
        with get_db() as conn:
            total_orders_row = conn.execute("SELECT COUNT(*) as cnt, COALESCE(SUM(total), 0) as revenue FROM orders").fetchone()
            total_orders = total_orders_row["cnt"] if total_orders_row else 0
            revenue = total_orders_row["revenue"] if total_orders_row else 0

            status_rows = conn.execute("SELECT status, COUNT(*) as cnt FROM orders GROUP BY status").fetchall()
            status_counts = {row["status"]: row["cnt"] for row in status_rows}

            products_count_row = conn.execute("SELECT COUNT(*) as cnt FROM products WHERE is_active=1").fetchone()
            active_products = products_count_row["cnt"] if products_count_row else 0

        return {
            "total_orders": total_orders,
            "revenue": revenue,
            "status_counts": status_counts,
            "active_products": active_products,
        }
