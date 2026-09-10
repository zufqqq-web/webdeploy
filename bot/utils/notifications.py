import logging
from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from config import settings
from config.constants import (
    STATUS_COOKING,
    STATUS_DELIVERY,
    STATUS_COMPLETED,
    STATUS_CANCELLED,
)
from services.orders import OrderService
from bot.utils.formatters import format_admin_new_order

logger = logging.getLogger("PizzaHouseBot")

async def safe_edit(call: CallbackQuery, text: str, markup: InlineKeyboardMarkup) -> None:
    if not call.message:
        return

    try:
        if call.message.photo:
            await call.message.edit_caption(
                caption=text,
                reply_markup=markup,
            )
        else:
            await call.message.edit_text(
                text=text,
                reply_markup=markup,
            )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return

        try:
            await call.message.answer(text=text, reply_markup=markup)
        except Exception:
            logger.exception("Не удалось показать сообщение после ошибки редактирования.")
    except Exception:
        logger.exception("Ошибка при редактировании сообщения.")

async def notify_admin_about_order(bot: Bot, order_id: int) -> None:
    order = OrderService.get_order(order_id)
    if not order:
        return

    items = OrderService.get_order_items(order_id)
    text = format_admin_new_order(order, items)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"📦 Открыть заказ №{order_id}",
                    callback_data=f"admo:{order_id}",
                )
            ]
        ]
    )

    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text, reply_markup=kb)
        except Exception:
            logger.exception("Не удалось отправить новый заказ администратору %s", admin_id)

def status_notification_text(order_id: int, status: str) -> str | None:
    if status == STATUS_COOKING:
        return f"🍳 Ваш заказ №{order_id} начал готовиться!"

    if status == STATUS_DELIVERY:
        return f"🚚 Ваш заказ №{order_id} передан в доставку!"

    if status == STATUS_COMPLETED:
        return f"✅ Ваш заказ №{order_id} выполнен. Спасибо, что выбрали PizzaHouse!"

    if status == STATUS_CANCELLED:
        return f"❌ Ваш заказ №{order_id} отменён."

    return None

async def notify_user_status(bot: Bot, order: dict, status: str) -> None:
    user_id = order.get("user_id")
    if not user_id:
        return

    text = status_notification_text(order["id"], status)
    if not text:
        return

    try:
        await bot.send_message(user_id, text)
    except Exception:
        logger.exception("Не удалось отправить уведомление пользователю %s", user_id)
