from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.constants import SIZES, CATEGORY_LABELS
from services.products import ProductService
from services.orders import OrderService
from services.cart import CartService

def format_price(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " сум"

def format_product(product: dict, size: int | None = None) -> str:
    lines = [
        f"🍕 {product['name']}",
        "",
        product["description"],
        "",
        "🥫 Состав:",
    ]

    for ingredient in product.get("ingredients", []):
        lines.append(f"• {ingredient}")

    if size is None:
        lines.append("")
        lines.append("📏 Размер:")

        for s in SIZES:
            price = product["prices"].get(s)
            if price is not None:
                lines.append(f"{s} см — {format_price(price)}")

        lines.append("")
        lines.append("Выберите размер:")
    else:
        price = ProductService.get_price(product, size) or 0

        lines.append("")
        lines.append(f"📏 Размер: {size} см")
        lines.append(f"💰 Цена: {format_price(price)}")
        lines.append("")
        lines.append("Количество:")

    return "\n".join(lines)

def format_cart(user_id: int) -> tuple[str, InlineKeyboardMarkup]:
    cart = CartService.get_cart(user_id)

    if not cart:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🍕 Меню", callback_data="cat:menu")]
            ]
        )
        return "🛒 Ваша корзина пуста.", kb

    lines = ["🛒 Ваша корзина", ""]
    rows = []

    for (product_id, size), qty in list(cart.items()):
        product = ProductService.get_product(product_id)
        price = ProductService.get_price(product, size)

        if product is None or price is None or qty < 1:
            continue

        line_total = price * qty

        lines.append(f"🍕 {product['name']}")
        lines.append(f"{size} см × {qty}")
        lines.append(format_price(line_total))
        lines.append("")

        rows.append(
            [
                InlineKeyboardButton(
                    text=f"🍕 {product['name']} {size} см × {qty}",
                    callback_data="noop",
                )
            ]
        )

        rows.append(
            [
                InlineKeyboardButton(
                    text="➖",
                    callback_data=f"cdec:{product_id}:{size}",
                ),
                InlineKeyboardButton(
                    text="➕",
                    callback_data=f"cinc:{product_id}:{size}",
                ),
                InlineKeyboardButton(
                    text="🗑",
                    callback_data=f"cdel:{product_id}:{size}",
                ),
            ]
        )

    lines.append("────────────────")
    lines.append(f"💰 Итого: {format_price(CartService.get_cart_total(user_id))}")

    rows.append(
        [
            InlineKeyboardButton(text="➕ Добавить ещё", callback_data="cat:menu"),
            InlineKeyboardButton(text="🗑 Очистить корзину", callback_data="cclear"),
        ]
    )

    rows.append(
        [
            InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")
        ]
    )

    return "\n".join(lines), InlineKeyboardMarkup(inline_keyboard=rows)

def format_order_items_user(items: list[dict]) -> str:
    lines = []
    for item in items:
        lines.append(f"🍕 {item['name']}")
        lines.append(f"Размер: {item['size']} см")
        lines.append(f"Количество: {item['qty']}")
        lines.append(f"Цена: {format_price(item['price'])}")
        lines.append(f"Сумма: {format_price(item['line_total'])}")
        lines.append("")
    return "\n".join(lines).strip()

def format_checkout(user_id: int):
    items = CartService.build_order_items(user_id)

    if not items:
        return None, None

    total = sum(item["line_total"] for item in items)

    text = (
        "📦 Ваш заказ\n"
        "\n"
        f"{format_order_items_user(items)}\n"
        "\n"
        "────────────────\n"
        f"💰 Итого: {format_price(total)}"
    )

    from bot.keyboards.inline import checkout_kb
    return text, checkout_kb()

def format_items_for_admin(items: list[dict]) -> str:
    lines = []
    for item in items:
        lines.append(f"🍕 {item['name']}")
        lines.append(f"📏 {item['size']} см")
        lines.append(f"🔢 × {item['qty']}")
        lines.append(f"💰 {format_price(item['price'])}")
        lines.append(f"💵 {format_price(item['line_total'])}")
        lines.append("")
    return "\n".join(lines).strip()

def format_admin_new_order(order: dict, items: list[dict]) -> str:
    username = f"@{order['username']}" if order.get("username") else "—"
    comment = order.get("comment") or "—"

    lines = [
        "🍕 НОВЫЙ ЗАКАЗ",
        "",
        f"🆔 Заказ №{order['id']}",
        f"🕒 Создан: {order['created_at']}",
        f"Источник: {order['source']}",
        "",
        f"👤 Клиент: {order['client_name']}",
        f"📞 Телефон: {order['phone']}",
        f"📍 Адрес: {order['address']}",
        f"💬 Комментарий: {comment}",
        "",
        "🧾 Telegram-аккаунт:",
        f"Имя: {order.get('user_name') or '—'}",
        f"Username: {username}",
        f"ID: {order.get('user_id') or '—'}",
        "",
        "────────────────",
        "",
        format_items_for_admin(items),
        "",
        "────────────────",
        f"💰 ИТОГО: {format_price(order['total'])}",
        "",
        f"Статус: {OrderService.get_status_label(order['status'])}",
    ]

    return "\n".join(lines)

def format_order_details(order: dict, items: list[dict]) -> str:
    username = f"@{order['username']}" if order.get("username") else "—"
    comment = order.get("comment") or "—"

    lines = [
        f"📦 Заказ №{order['id']}",
        f"Статус: {OrderService.get_status_label(order['status'])}",
        f"Создан: {order['created_at']}",
        f"Обновлён: {order['updated_at']}",
        f"Источник: {order['source']}",
        "",
        "👤 Данные получателя:",
        f"Имя: {order['client_name']}",
        f"Телефон: {order['phone']}",
        f"Адрес: {order['address']}",
        f"Комментарий: {comment}",
        "",
        "🧾 Telegram:",
        f"Имя: {order.get('user_name') or '—'}",
        f"Username: {username}",
        f"ID: {order.get('user_id') or '—'}",
        "",
        "────────────────",
        "",
        format_items_for_admin(items),
        "",
        "────────────────",
        f"💰 Итого: {format_price(order['total'])}",
    ]

    return "\n".join(lines)

def format_admin_products(products: list[dict]) -> str:
    if not products:
        return "Активных товаров пока нет."

    lines = ["🍕 Активные товары:", ""]

    for product in products:
        category_label = CATEGORY_LABELS.get(product["category"], product["category"])
        lines.append(f"{product['id']}. {product['name']}")
        lines.append(f"Категория: {category_label}")
        lines.append(
            "Цены: "
            f"25 см — {format_price(product['prices'][25])}, "
            f"30 см — {format_price(product['prices'][30])}, "
            f"35 см — {format_price(product['prices'][35])}"
        )
        lines.append("")

    lines.append("Нажмите на кнопку товара, чтобы скрыть его из меню.")
    return "\n".join(lines)
