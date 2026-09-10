from config.constants import MAX_QTY
from services.products import ProductService

class CartService:
    # Формат в памяти: { user_id: { (product_id, size): qty } }
    _carts: dict[int, dict[tuple[int, int], int]] = {}

    @classmethod
    def get_cart(cls, user_id: int) -> dict[tuple[int, int], int]:
        return cls._carts.setdefault(user_id, {})

    @classmethod
    def add_to_cart(cls, user_id: int, product_id: int, size: int, qty: int) -> bool:
        if qty < 1 or qty > MAX_QTY:
            return False

        product = ProductService.get_product(product_id)
        price = ProductService.get_price(product, size)

        if product is None or price is None:
            return False

        cart = cls.get_cart(user_id)
        key = (product_id, size)
        current_qty = cart.get(key, 0)
        new_qty = current_qty + qty

        if new_qty > MAX_QTY:
            return False

        cart[key] = new_qty
        return True

    @classmethod
    def change_cart_qty(cls, user_id: int, product_id: int, size: int, delta: int) -> None:
        cart = cls._carts.get(user_id)
        if not cart:
            return

        key = (product_id, size)
        current_qty = cart.get(key, 0)
        new_qty = current_qty + delta

        if new_qty <= 0:
            cart.pop(key, None)
        else:
            cart[key] = min(MAX_QTY, new_qty)

    @classmethod
    def delete_cart_item(cls, user_id: int, product_id: int, size: int) -> None:
        cart = cls._carts.get(user_id)
        if cart:
            cart.pop((product_id, size), None)

    @classmethod
    def clear_cart(cls, user_id: int) -> None:
        cls._carts.pop(user_id, None)

    @classmethod
    def get_cart_total(cls, user_id: int) -> int:
        total = 0
        cart = cls._carts.get(user_id, {})

        for (product_id, size), qty in cart.items():
            product = ProductService.get_product(product_id)
            price = ProductService.get_price(product, size)

            if product is None or price is None or qty < 1:
                continue

            total += price * qty

        return total

    @classmethod
    def build_order_items(cls, user_id: int) -> list[dict]:
        items = []
        cart = cls._carts.get(user_id, {})

        for (product_id, size), qty in cart.items():
            product = ProductService.get_product(product_id)
            price = ProductService.get_price(product, size)

            if product is None or price is None or qty < 1:
                continue

            items.append({
                "product_id": product_id,
                "name": product["name"],
                "size": size,
                "qty": qty,
                "price": price,
                "line_total": price * qty,
            })

        return items
