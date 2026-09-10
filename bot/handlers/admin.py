import asyncio
import logging
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardRemove

from config.constants import ORDER_STATUSES, CATEGORY_ALIASES
from services.products import ProductService
from services.orders import OrderService
from services.users import UserService
from bot.states.admin import AdminAddProduct, AdminBroadcast
from bot.keyboards.reply import get_main_kb
from bot.keyboards.inline import (
    admin_main_kb,
    admin_orders_filter_kb,
    admin_orders_list_kb,
    admin_order_kb,
    admin_products_kb,
    broadcast_confirm_kb,
)
from bot.utils.auth import get_message_user_id, get_callback_user_id, is_admin
from bot.utils.formatters import (
    format_price,
    format_order_details,
    format_admin_products,
)
from bot.utils.notifications import safe_edit, notify_user_status

logger = logging.getLogger("PizzaHouseBot")
router = Router(name="admin")

async def show_admin_panel(message: Message) -> None:
    await message.answer(
        "👨‍💼 Админ-панель PizzaHouse",
        reply_markup=admin_main_kb(),
    )

def admin_orders_menu_text() -> str:
    return "Выберите статус заказов:"

def admin_orders_list_text(status: str, orders: list[dict]) -> str:
    if not orders:
        if status == "all":
            return "Заказов пока нет."
        return f"Заказов со статусом «{OrderService.get_status_label(status)}» пока нет."

    if status == "all":
        title = "📋 Все заказы"
    else:
        title = f"Заказы: {OrderService.get_status_label(status)}"

    lines = [title, ""]
    for order in orders[:10]:
        lines.append(
            f"№{order['id']} • {order['client_name']} • {format_price(order['total'])}"
        )

    lines.append("")
    lines.append("Нажмите на заказ, чтобы открыть его.")
    return "\n".join(lines)

# ==================================================
# КОМАНДЫ АДМИНИСТРАТОРА
# ==================================================

@router.message(Command("admin"), StateFilter("*"))
async def cmd_admin(message: Message, state: FSMContext) -> None:
    user_id = get_message_user_id(message)

    if not is_admin(user_id):
        await message.answer("У вас нет доступа к админ-панели.")
        return

    await state.clear()
    await show_admin_panel(message)

@router.message(StateFilter(None), F.text == "👨‍💼 Админ")
async def text_admin(message: Message) -> None:
    user_id = get_message_user_id(message)

    if not is_admin(user_id):
        await message.answer("У вас нет доступа к админ-панели.")
        return

    await show_admin_panel(message)

# ==================================================
# CALLBACK-ХЕНДЛЕРЫ АДМИНИСТРАТОРА
# ==================================================

@router.callback_query(F.data == "adhome")
async def cb_admin_home(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()
    await safe_edit(call, "👨‍💼 Админ-панель PizzaHouse", admin_main_kb())
    await call.answer()

@router.callback_query(F.data == "adorders")
async def cb_admin_orders(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()
    await safe_edit(call, admin_orders_menu_text(), admin_orders_filter_kb())
    await call.answer()

@router.callback_query(F.data.startswith("adlf:"))
async def cb_admin_orders_filter(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()

    try:
        status = call.data.split(":", 1)[1]
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    orders = OrderService.get_orders(status=status, limit=30)
    text = admin_orders_list_text(status, orders)
    kb = admin_orders_list_kb(orders)

    await safe_edit(call, text, kb)
    await call.answer()

@router.callback_query(F.data.startswith("admo:"))
async def cb_admin_open_order(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()

    try:
        order_id = int(call.data.split(":", 1)[1])
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    order = OrderService.get_order(order_id)

    if order is None:
        await call.answer("Заказ не найден.", show_alert=True)
        return

    items = OrderService.get_order_items(order_id)
    text = format_order_details(order, items)
    kb = admin_order_kb(order_id, order["status"])

    await safe_edit(call, text, kb)
    await call.answer()

@router.callback_query(F.data.startswith("adst:"))
async def cb_admin_set_status(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    if not call.message:
        await call.answer()
        return

    await state.clear()

    try:
        _, order_id_raw, new_status = call.data.split(":")
        order_id = int(order_id_raw)
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    if new_status not in ORDER_STATUSES:
        await call.answer("Неизвестный статус.", show_alert=True)
        return

    order = OrderService.get_order(order_id)

    if order is None:
        await call.answer("Заказ не найден.", show_alert=True)
        return

    if order["status"] == new_status:
        await call.answer("Статус уже установлен.")
        await safe_edit(
            call,
            format_order_details(order, OrderService.get_order_items(order_id)),
            admin_order_kb(order_id, order["status"]),
        )
        return

    OrderService.update_order_status(order_id, new_status)
    order = OrderService.get_order(order_id)

    if order:
        await notify_user_status(call.message.bot, order, new_status)

        await safe_edit(
            call,
            format_order_details(order, OrderService.get_order_items(order_id)),
            admin_order_kb(order_id, order["status"]),
        )

    await call.answer("Статус обновлён")

@router.callback_query(F.data == "adprods")
async def cb_admin_products(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()

    products = ProductService.get_active_products()
    text = format_admin_products(products)
    kb = admin_products_kb(products)

    await safe_edit(call, text, kb)
    await call.answer()

@router.callback_query(F.data.startswith("adpd:"))
async def cb_admin_delete_product(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()

    try:
        product_id = int(call.data.split(":", 1)[1])
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    ProductService.deactivate_product(product_id)

    products = ProductService.get_active_products()
    text = format_admin_products(products)
    kb = admin_products_kb(products)

    await safe_edit(call, text, kb)
    await call.answer("Товар скрыт из меню")

@router.callback_query(F.data == "adadd")
async def cb_admin_add_product_start(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()
    await state.set_state(AdminAddProduct.name)

    await safe_edit(
        call,
        "🆕 Новый товар.\n\nВведите название товара:",
        InlineKeyboardMarkup(inline_keyboard=[]),
    )
    await call.answer()

# ==================================================
# FSM: ДОБАВЛЕНИЕ ТОВАРА
# ==================================================

@router.message(AdminAddProduct.name, F.text)
async def admin_product_name(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return

    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Название должно содержать минимум 2 символа.")
        return

    await state.update_data(name=name)
    await state.set_state(AdminAddProduct.description)

    await message.answer(
        "Введите описание товара:",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AdminAddProduct.description, F.text)
async def admin_product_description(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return

    description = message.text.strip()
    if description in {"-", "нет"}:
        description = ""

    await state.update_data(description=description)
    await state.set_state(AdminAddProduct.ingredients)

    await message.answer(
        "Введите ингредиенты через запятую.\n"
        "Пример: томатный соус, моцарелла, пепперони",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AdminAddProduct.ingredients, F.text)
async def admin_product_ingredients(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return

    raw_ingredients = message.text.strip()
    if raw_ingredients in {"-", "нет"}:
        ingredients = []
    else:
        ingredients = [item.strip() for item in raw_ingredients.split(",") if item.strip()]

    await state.update_data(ingredients=ingredients)
    await state.set_state(AdminAddProduct.category)

    await message.answer(
        "Введите категорию товара.\n"
        "Допустимые значения:\n"
        "pizza, combo, drinks, desserts, other\n"
        "\n"
        "Можно написать по-русски: пицца, комбо, напитки, десерты, прочее.",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AdminAddProduct.category, F.text)
async def admin_product_category(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return

    category_raw = message.text.strip().lower()
    category = CATEGORY_ALIASES.get(category_raw, "other")

    await state.update_data(category=category)
    await state.set_state(AdminAddProduct.image)

    await message.answer(
        "Отправьте ссылку на изображение товара.\n"
        "Если изображения нет, отправьте: -",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AdminAddProduct.image, F.text)
async def admin_product_image(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return

    image = message.text.strip()
    if image in {"-", "нет"}:
        image = ""

    await state.update_data(image=image)
    await state.set_state(AdminAddProduct.price_25)

    await message.answer(
        "Введите цену для размера 25 см в сумах.\n"
        "Пример: 45000",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AdminAddProduct.price_25, F.text)
async def admin_product_price_25(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return

    try:
        price_25 = int(message.text.replace(" ", ""))
        if price_25 <= 0:
            raise ValueError
    except Exception:
        await message.answer("Введите корректную цену числом, например: 45000")
        return

    await state.update_data(price_25=price_25)
    await state.set_state(AdminAddProduct.price_30)

    await message.answer(
        "Введите цену для размера 30 см в сумах:",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AdminAddProduct.price_30, F.text)
async def admin_product_price_30(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return

    try:
        price_30 = int(message.text.replace(" ", ""))
        if price_30 <= 0:
            raise ValueError
    except Exception:
        await message.answer("Введите корректную цену числом, например: 60000")
        return

    await state.update_data(price_30=price_30)
    await state.set_state(AdminAddProduct.price_35)

    await message.answer(
        "Введите цену для размера 35 см в сумах:",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AdminAddProduct.price_35, F.text)
async def admin_product_price_35(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return

    try:
        price_35 = int(message.text.replace(" ", ""))
        if price_35 <= 0:
            raise ValueError
    except Exception:
        await message.answer("Введите корректную цену числом, например: 75000")
        return

    data = await state.get_data()

    name = data.get("name", "")
    description = data.get("description", "")
    ingredients = data.get("ingredients", [])
    category = data.get("category", "other")
    image = data.get("image", "")

    try:
        product_id = ProductService.create_product(
            name=name,
            description=description,
            ingredients=ingredients,
            category=category,
            image=image,
            price_25=data["price_25"],
            price_30=data["price_30"],
            price_35=price_35,
        )
    except Exception:
        logger.exception("Не удалось добавить товар.")
        await message.answer("Ошибка при добавлении товара.")
        await state.clear()
        return

    await state.clear()

    await message.answer(
        f"✅ Товар «{name}» добавлен с ID {product_id}.",
        reply_markup=get_main_kb(get_message_user_id(message)),
    )

    await message.answer(
        "👨‍💼 Админ-панель PizzaHouse",
        reply_markup=admin_main_kb(),
    )

# ==================================================
# РАССЫЛКА
# ==================================================

@router.callback_query(F.data == "adbr")
async def cb_admin_broadcast_start(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()
    await state.set_state(AdminBroadcast.text)

    await safe_edit(
        call,
        "📣 Рассылка.\n\nОтправьте текст, который нужно разослать всем пользователям.\n\nОтмена: /cancel",
        InlineKeyboardMarkup(inline_keyboard=[]),
    )
    await call.answer()

@router.message(AdminBroadcast.text, F.text)
async def admin_broadcast_text(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return

    text = message.text.strip()
    if len(text) < 1:
        await message.answer("Текст рассылки не может быть пустым.")
        return

    if len(text) > 4000:
        await message.answer("Текст слишком длинный. Пожалуйста, отправьте текст до 4000 символов.")
        return

    await state.update_data(broadcast_text=text)
    await state.set_state(AdminBroadcast.confirm)

    preview = text if len(text) <= 1000 else text[:1000] + "..."

    await message.answer(
        "Предпросмотр рассылки:\n\n"
        f"{preview}\n\n"
        "Отправить этот текст всем пользователям?",
        reply_markup=broadcast_confirm_kb(),
    )

@router.message(AdminBroadcast.text)
async def admin_broadcast_wrong_type(message: Message, state: FSMContext) -> None:
    if not is_admin(get_message_user_id(message)):
        return
    await message.answer("Пожалуйста, отправьте текст рассылки обычным текстовым сообщением.")

@router.callback_query(F.data == "brconfirm")
async def cb_admin_broadcast_confirm(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    data = await state.get_data()
    text = data.get("broadcast_text", "")

    if not text:
        await state.clear()
        await safe_edit(call, "Текст рассылки пуст.", admin_main_kb())
        await call.answer()
        return

    user_ids = UserService.get_broadcast_user_ids()

    if not user_ids:
        await state.clear()
        await safe_edit(
            call,
            "Нет пользователей для рассылки.\n"
            "Пользователи появляются в таблице после того, как напишут боту.",
            admin_main_kb(),
        )
        await call.answer()
        return

    await call.answer("Начинаю рассылку...")

    await safe_edit(
        call,
        f"⏳ Начинаю рассылку для {len(user_ids)} пользователей...",
        InlineKeyboardMarkup(inline_keyboard=[]),
    )

    success = 0
    failed = 0

    for user_id in user_ids:
        try:
            await call.bot.send_message(user_id, text)
            success += 1
        except Exception as e:
            failed += 1
            error_text = str(e).lower()

            if (
                "blocked" in error_text
                or "forbidden" in error_text
                or "chat not found" in error_text
                or "user is deactivated" in error_text
            ):
                UserService.mark_user_blocked(user_id)

            if "too many requests" in error_text:
                await asyncio.sleep(3)

        await asyncio.sleep(0.07)

    await state.clear()

    result_text = (
        "✅ Рассылка завершена.\n\n"
        f"Всего пользователей: {len(user_ids)}\n"
        f"Отправлено успешно: {success}\n"
        f"Ошибок: {failed}"
    )

    await safe_edit(call, result_text, admin_main_kb())

@router.callback_query(F.data == "brcancel")
async def cb_admin_broadcast_cancel(call: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(get_callback_user_id(call)):
        await call.answer("Нет доступа.", show_alert=True)
        return

    await state.clear()
    await safe_edit(call, "❌ Рассылка отменена.", admin_main_kb())
    await call.answer()
