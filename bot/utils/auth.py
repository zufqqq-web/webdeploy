from aiogram.types import Message, CallbackQuery
from config import settings

def is_admin(user_id: int) -> bool:
    if not user_id or not settings.ADMIN_IDS:
        return False
    return user_id in settings.ADMIN_IDS

def get_message_user_id(message: Message) -> int:
    if message.from_user:
        return message.from_user.id
    if message.chat:
        return message.chat.id
    return 0

def get_callback_user_id(call: CallbackQuery) -> int:
    if call.from_user:
        return call.from_user.id
    if call.message and getattr(call.message, "chat", None):
        return call.message.chat.id
    return 0
