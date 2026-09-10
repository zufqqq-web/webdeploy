from database.repositories.orders import OrderRepository
from config.constants import ORDER_STATUSES, STATUS_EXPECTED

class OrderService:
    @staticmethod
    def get_status_label(status: str) -> str:
        return ORDER_STATUSES.get(status, status)

    @classmethod
    def create_order(
        cls,
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

        # Нормализация позиций заказа
        validated_items = []
        for item in items:
            product_id = item.get("product_id")
            name = item.get("name", "Товар")
            size = int(item.get("size", 0))
            qty = int(item.get("qty", 1))
            price = int(item.get("price", 0))
            line_total = int(item.get("line_total", price * qty))

            if qty < 1:
                continue

            validated_items.append({
                "product_id": product_id,
                "name": name,
                "size": size,
                "qty": qty,
                "price": price,
                "line_total": line_total,
            })

        if not validated_items:
            return None

        return OrderRepository.create(
            user_id=user_id,
            user_name=user_name,
            username=username,
            client_name=client_name,
            phone=phone,
            address=address,
            comment=comment,
            source=source,
            items=validated_items,
            status=status,
        )

    @staticmethod
    def get_order(order_id: int) -> dict | None:
        return OrderRepository.get_by_id(order_id)

    @staticmethod
    def get_order_items(order_id: int) -> list[dict]:
        return OrderRepository.get_items(order_id)

    @staticmethod
    def get_orders(status: str | None = None, limit: int = 50) -> list[dict]:
        return OrderRepository.get_list(status=status, limit=limit)

    @staticmethod
    def update_order_status(order_id: int, status: str) -> bool:
        return OrderRepository.update_status(order_id, status)

    @staticmethod
    def get_stats() -> dict:
        return OrderRepository.get_stats()
