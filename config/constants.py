"""
Константы проекта PizzaHouse.
Общие для Telegram-бота и веб-сервера.
"""

SIZES = [25, 30, 35]
MAX_QTY = 99

# Статусы заказов
STATUS_EXPECTED = "expected"
STATUS_COOKING = "cooking"
STATUS_DELIVERY = "delivery"
STATUS_COMPLETED = "completed"
STATUS_CANCELLED = "cancelled"

ORDER_STATUSES = {
    STATUS_EXPECTED: "🕒 Ожидается",
    STATUS_COOKING: "🍳 Готовится",
    STATUS_DELIVERY: "🚚 В доставке",
    STATUS_COMPLETED: "✅ Выполнен",
    STATUS_CANCELLED: "❌ Отменён",
}

# Категории меню
CATEGORY_LABELS = {
    "pizza": "🍕 Пиццы",
    "combo": "🍔 Комбо",
    "drinks": "🥤 Напитки",
    "desserts": "🍰 Десерты",
    "other": "📦 Прочее",
}

CATEGORY_ALIASES = {
    "pizza": "pizza",
    "пицца": "pizza",
    "пиццы": "pizza",
    "pizzas": "pizza",
    "combo": "combo",
    "комбо": "combo",
    "combos": "combo",
    "drink": "drinks",
    "drinks": "drinks",
    "напитки": "drinks",
    "напиток": "drinks",
    "dessert": "desserts",
    "desserts": "desserts",
    "десерт": "desserts",
    "десерты": "desserts",
    "other": "other",
    "прочее": "other",
    "другое": "other",
}
