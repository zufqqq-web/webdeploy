from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.constants import CATEGORY_LABELS, ORDER_STATUSES, SIZES
from services.products import ProductService
from services.orders import OrderService

def format_price(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " сум"

categories_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data=f"cat:{key}")]
        for key, label in CATEGORY_LABELS.items()
    ]
)

def back_to_categories_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Категории", callback_data="cat:menu")]
        ]
    )

def category_products_kb(products: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for product in products:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"🍕 {product['name']}",
                    callback_data=f"p:{product['id']}",
                )
            ]
        )
    rows.append([InlineKeyboardButton(text="⬅️ Категории", callback_data="cat:menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def product_sizes_kb(product_id: int) -> InlineKeyboardMarkup:
    product = ProductService.get_product(product_id)
    rows = []

    if not product:
        return InlineKeyboardMarkup(inline_keyboard=[])

    for size in SIZES:
        price = product["prices"].get(size)
        if price is None:
            continue

        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{size} см — {format_price(price)}",
                    callback_data=f"sz:{product_id}:{size}",
                )
            ]
        )

    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="cat:menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def product_qty_kb(product_id: int, size: int, qty: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"dec:{product_id}:{size}:{qty}"),
                InlineKeyboardButton(text=str(qty), callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data=f"inc:{product_id}:{size}:{qty}"),
            ],
            [
                InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data=f"add:{product_id}:{size}:{qty}")
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data=f"bsz:{product_id}")
            ],
        ]
    )

def added_to_cart_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Корзина", callback_data="cart")],
            [InlineKeyboardButton(text="➕ Добавить ещё", callback_data="cat:menu")],
        ]
    )

def checkout_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Продолжить оформление",
                    callback_data="proceed",
                )
            ],
            [
                InlineKeyboardButton(
                    text="↩️ Назад в корзину",
                    callback_data="cart",
                )
            ],
        ]
    )

def admin_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 Заказы", callback_data="adorders")],
            [InlineKeyboardButton(text="🍕 Товары", callback_data="adprods")],
            [InlineKeyboardButton(text="➕ Добавить товар", callback_data="adadd")],
            [InlineKeyboardButton(text="📣 Рассылка", callback_data="adbr")],
        ]
    )

def broadcast_confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Отправить", callback_data="brconfirm")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="brcancel")],
        ]
    )

def admin_orders_filter_kb() -> InlineKeyboardMarkup:
    rows = []
    for status, label in ORDER_STATUSES.items():
        rows.append(
            [InlineKeyboardButton(text=label, callback_data=f"adlf:{status}")]
        )
    rows.append([InlineKeyboardButton(text="📋 Все заказы", callback_data="adlf:all")])
    rows.append([InlineKeyboardButton(text="🏠 Админ-панель", callback_data="adhome")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def admin_orders_list_kb(orders: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for order in orders:
        status_label = OrderService.get_status_label(order["status"])
        text = f"№{order['id']} • {status_label} • {format_price(order['total'])}"
        rows.append(
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"admo:{order['id']}",
                )
            ]
        )
    rows.append([InlineKeyboardButton(text="⬅️ Статусы", callback_data="adorders")])
    rows.append([InlineKeyboardButton(text="🏠 Админ-панель", callback_data="adhome")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def admin_order_kb(order_id: int, current_status: str) -> InlineKeyboardMarkup:
    rows = []
    for status, label in ORDER_STATUSES.items():
        button_label = f"✅ {label}" if status == current_status else label
        rows.append(
            [
                InlineKeyboardButton(
                    text=button_label,
                    callback_data=f"adst:{order_id}:{status}",
                )
            ]
        )
    rows.append([InlineKeyboardButton(text="⬅️ К заказам", callback_data="adlf:all")])
    rows.append([InlineKeyboardButton(text="🏠 Админ-панель", callback_data="adhome")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def admin_products_kb(products: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for product in products:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"🗑 {product['name']}",
                    callback_data=f"adpd:{product['id']}",
                )
            ]
        )
    rows.append([InlineKeyboardButton(text="➕ Добавить товар", callback_data="adadd")])
    rows.append([InlineKeyboardButton(text="🏠 Админ-панель", callback_data="adhome")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
