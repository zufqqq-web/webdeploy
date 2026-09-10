from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import settings

def is_admin_user(user_id: int) -> bool:
    return bool(user_id and user_id in settings.ADMIN_IDS)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🍕 Меню"),
            KeyboardButton(text="🛒 Корзина"),
        ],
        [
            KeyboardButton(text="ℹ️ О пиццерии"),
        ],
    ],
    resize_keyboard=True,
)

admin_main_reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🍕 Меню"),
            KeyboardButton(text="🛒 Корзина"),
        ],
        [
            KeyboardButton(text="ℹ️ О пиццерии"),
            KeyboardButton(text="👨‍💼 Админ"),
        ],
    ],
    resize_keyboard=True,
)

def get_main_kb(user_id: int) -> ReplyKeyboardMarkup:
    return admin_main_reply_kb if is_admin_user(user_id) else main_kb
