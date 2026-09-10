import logging
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from services.orders import OrderService
from services.cart import CartService
from bot.states.order import OrderStates
from bot.keyboards.reply import get_main_kb
from bot.utils.auth import get_message_user_id
from bot.utils.notifications import notify_admin_about_order

logger = logging.getLogger("PizzaHouseBot")
router = Router(name="orders")

@router.message(OrderStates.name, F.text)
async def order_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()

    if len(name) < 2:
        await message.answer("Пожалуйста, укажите имя получателя (минимум 2 символа).")
        return

    await state.update_data(client_name=name)
    await state.set_state(OrderStates.phone)

    await message.answer(
        "Введите номер телефона получателя:",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(OrderStates.phone, F.text)
async def order_phone(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()
    digits_count = sum(1 for char in phone if char.isdigit())

    if digits_count < 7:
        await message.answer("Пожалуйста, укажите корректный номер телефона.")
        return

    await state.update_data(phone=phone)
    await state.set_state(OrderStates.address)

    await message.answer(
        "Введите адрес доставки:",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(OrderStates.address, F.text)
async def order_address(message: Message, state: FSMContext) -> None:
    address = message.text.strip()

    if len(address) < 5:
        await message.answer("Пожалуйста, укажите корректный адрес доставки.")
        return

    await state.update_data(address=address)
    await state.set_state(OrderStates.comment)

    await message.answer(
        "Отправьте комментарий к заказу.\n"
        "Если комментария нет, напишите: -",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(OrderStates.comment, F.text)
async def order_comment(message: Message, state: FSMContext) -> None:
    text = message.text.strip()

    if text.lower() in {"-", "none", "нет", "/skip", "без комментария"}:
        comment = ""
    else:
        comment = text

    data = await state.get_data()
    items = data.get("items", [])
    source = data.get("source", "🤖 Telegram Bot")
    clear_cart_after = data.get("clear_cart_after", False)

    user = message.from_user
    user_id = user.id if user else get_message_user_id(message)
    user_name = user.full_name if user else ""
    username = user.username if user else ""

    client_name = data.get("client_name", "")
    phone = data.get("phone", "")
    address = data.get("address", "")

    try:
        order_id = OrderService.create_order(
            user_id=user_id,
            user_name=user_name,
            username=username,
            client_name=client_name,
            phone=phone,
            address=address,
            comment=comment,
            source=source,
            items=items,
        )
    except Exception:
        logger.exception("Не удалось создать заказ.")
        await message.answer("Произошла ошибка при создании заказа. Попробуйте ещё раз.")
        return

    if order_id is None:
        await message.answer("В заказе нет товаров.")
        return

    if clear_cart_after:
        CartService.clear_cart(user_id)

    await state.clear()

    await notify_admin_about_order(message.bot, order_id)

    await message.answer(
        f"✅ Заказ №{order_id} принят!\n"
        "\n"
        "Статус: 🕒 Ожидается.\n"
        "Мы сообщим вам, когда статус заказа изменится.",
        reply_markup=get_main_kb(user_id),
    )
