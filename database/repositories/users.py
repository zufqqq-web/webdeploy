from database.connection import get_db, now_str

class UserRepository:
    @staticmethod
    def register(user_id: int, full_name: str = "", username: str = "") -> None:
        if not user_id:
            return

        timestamp = now_str()

        with get_db() as conn:
            conn.execute(
                """
                INSERT INTO users (
                    user_id,
                    username,
                    full_name,
                    created_at,
                    updated_at,
                    is_blocked
                )
                VALUES (?, ?, ?, ?, ?, 0)
                ON CONFLICT(user_id) DO UPDATE SET
                    username = excluded.username,
                    full_name = excluded.full_name,
                    updated_at = excluded.updated_at,
                    is_blocked = 0
                """,
                (
                    user_id,
                    username or "",
                    full_name or "",
                    timestamp,
                    timestamp,
                ),
            )

    @staticmethod
    def get_broadcast_ids() -> list[int]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT user_id FROM users WHERE is_blocked=0 ORDER BY user_id"
            ).fetchall()

        return [row["user_id"] for row in rows if row]

    @staticmethod
    def mark_blocked(user_id: int) -> None:
        with get_db() as conn:
            conn.execute(
                """
                UPDATE users
                SET is_blocked = 1, updated_at = ?
                WHERE user_id = ?
                """,
                (now_str(), user_id),
            )

    @staticmethod
    def get_count() -> int:
        with get_db() as conn:
            row = conn.execute("SELECT COUNT(*) as cnt FROM users").fetchone()
            return row["cnt"] if row else 0
