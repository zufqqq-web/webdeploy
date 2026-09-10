import logging
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config.constants import CATEGORY_LABELS, MAX_QTY
from services.products import ProductService
from services.cart import CartService
from bot.keyboards.reply import get_main_kb
from bot.keyboards.inline import (
    categories_kb,
    back_to_categories_kb,
    category_products_kb,
    product_sizes_kb,
    product_qty_kb,
    added_to_cart_kb,
)
from bot.utils.auth import get_message_user_id, get_callback_user_id, is_admin
from bot.utils.formatters import format_cart, format_product, format_price, format_checkout
from bot.utils.notifications import safe_edit
from bot.utils.deeplink import parse_order_payload, start_order_flow

logger = logging.getLogger("PizzaHouseBot")
router = Router(name="user")

async def process_deep_link_order(message: Message, state: FSMContext, payload: str) -> None:
    items, source = parse_order_payload(payload)

    if not items:
        await message.answer(
            "❌ Не удалось обработать заказ.\n"
            "\n"
            "Пожалуйста, попробуйте оформить заказ ещё раз.",
            reply_markup=get_main_kb(get_message_user_id(message)),
        )
        return

    await start_order_flow(
        message,
        state,
        items,
        source=source,
        clear_cart_after=False,
    )

# ==================================================
# КОМАНДЫ
# ==================================================

@router.message(CommandStart(deep_link=True), StateFilter("*"))
async def cmd_start_deep_link(message: Message, command: CommandObject, state: FSMContext) -> None:
    await state.clear()
    args = command.args if command else None

    if args:
        await process_deep_link_order(message, state, args)
        return

    await message.answer(
        "🍕 Добро пожаловать в PizzaHouse!\n"
        "\n"
        "Свежая пицца с доставкой 🍕",
        reply_markup=get_main_kb(get_message_user_id(message)),
    )

@router.message(CommandStart(), StateFilter("*"))
async def cmd_start_plain(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "🍕 Добро пожаловать в PizzaHouse!\n"
        "\n"
        "Свежая пицца с доставкой 🍕",
        reply_markup=get_main_kb(get_message_user_id(message)),
    )

@router.message(Command("cancel"), StateFilter("*"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Действие отменено.",
        reply_markup=get_main_kb(get_message_user_id(message)),
    )

# ==================================================
# ОБЫЧНЫЕ КНОПКИ
# ==================================================

@router.message(StateFilter(None), F.text == "🍕 Меню")
async def text_menu(message: Message) -> None:
    await message.answer(
        "🍕 Меню\nВыберите категорию:",
        reply_markup=categories_kb,
    )

@router.message(StateFilter(None), F.text == "🛒 Корзина")
async def text_cart(message: Message) -> None:
    user_id = get_message_user_id(message)
    text, kb = format_cart(user_id)
    await message.answer(text, reply_markup=kb)

@router.message(StateFilter(None), F.text == "ℹ️ О пиццерии")
async def text_about(message: Message) -> None:
    await message.answer(
        "🍕 PizzaHouse\n"
        "\n"
        "Свежая пицца, напитки и десерты.\n"
        "\n"
        "🕐 Работаем ежедневно:\n"
        "10:00–23:00\n"
        "\n"
        "🚚 Доставка по городу",
        reply_markup=get_main_kb(get_message_user_id(message)),
    )

# ==================================================
# КАТЕГОРИИ И ТОВАРЫ
# ==================================================

@router.callback_query(F.data == "noop")
async def cb_noop(call: CallbackQuery) -> None:
    await call.answer()

@router.callback_query(F.data == "cat:menu")
async def cb_categories_menu(call: CallbackQuery) -> None:
    await safe_edit(call, "🍕 Меню\nВыберите категорию:", categories_kb)
    await call.answer()

@router.callback_query(F.data.startswith("cat:"))
async def cb_category(call: CallbackQuery) -> None:
    try:
        category = call.data.split(":", 1)[1]
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    if category not in CATEGORY_LABELS:
        await call.answer("Неизвестная категория.", show_alert=True)
        return

    products = ProductService.get_active_products(category)

    if not products:
        await safe_edit(
            call,
            f"{CATEGORY_LABELS[category]}\n\nПока нет доступных товаров.",
            back_to_categories_kb(),
        )
        await call.answer()
        return

    await safe_edit(
        call,
        f"{CATEGORY_LABELS[category]}\nВыберите товар:",
        category_products_kb(products),
    )
    await call.answer()

@router.callback_query(F.data.startswith("p:"))
async def cb_open_product(call: CallbackQuery) -> None:
    if not call.message:
        await call.answer()
        return

    try:
        product_id = int(call.data.split(":")[1])
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    product = ProductService.get_product(product_id)

    if product is None:
        await call.answer("Товар не найден.", show_alert=True)
        return

    await call.answer()

    text = format_product(product)
    markup = product_sizes_kb(product_id)
    sent_photo = False

    if product.get("image"):
        try:
            await call.message.answer_photo(
                photo=product["image"],
                caption=text,
                reply_markup=markup,
            )
            sent_photo = True
        except Exception:
            logger.exception("Не удалось отправить изображение товара.")

    if not sent_photo:
        await call.message.answer(text, reply_markup=markup)

@router.callback_query(F.data.startswith("bsz:"))
async def cb_back_to_sizes(call: CallbackQuery) -> None:
    try:
        product_id = int(call.data.split(":")[1])
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    product = ProductService.get_product(product_id)

    if product is None:
        await call.answer("Товар не найден.", show_alert=True)
        return

    await safe_edit(call, format_product(product), product_sizes_kb(product_id))
    await call.answer()

@router.callback_query(F.data.startswith("sz:"))
async def cb_select_size(call: CallbackQuery) -> None:
    try:
        _, product_id_raw, size_raw = call.data.split(":")
        product_id = int(product_id_raw)
        size = int(size_raw)
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    product = ProductService.get_product(product_id)
    price = ProductService.get_price(product, size)

    if product is None or price is None:
        await call.answer("Неверный товар или размер.", show_alert=True)
        return

    await safe_edit(
        call,
        format_product(product, size=size),
        product_qty_kb(product_id, size, 1),
    )
    await call.answer()

@router.callback_query(F.data.startswith("dec:"))
async def cb_decrease_qty_before_add(call: CallbackQuery) -> None:
    try:
        _, product_id_raw, size_raw, qty_raw = call.data.split(":")
        product_id = int(product_id_raw)
        size = int(size_raw)
        qty = int(qty_raw)
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    product = ProductService.get_product(product_id)
    price = ProductService.get_price(product, size)

    if product is None or price is None:
        await call.answer("Неверный товар или размер.", show_alert=True)
        return

    new_qty = max(1, qty - 1)

    await safe_edit(
        call,
        format_product(product, size=size),
        product_qty_kb(product_id, size, new_qty),
    )
    await call.answer()

@router.callback_query(F.data.startswith("inc:"))
async def cb_increase_qty_before_add(call: CallbackQuery) -> None:
    try:
        _, product_id_raw, size_raw, qty_raw = call.data.split(":")
        product_id = int(product_id_raw)
        size = int(size_raw)
        qty = int(qty_raw)
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    product = ProductService.get_product(product_id)
    price = ProductService.get_price(product, size)

    if product is None or price is None:
        await call.answer("Неверный товар или размер.", show_alert=True)
        return

    new_qty = min(MAX_QTY, qty + 1)

    await safe_edit(
        call,
        format_product(product, size=size),
        product_qty_kb(product_id, size, new_qty),
    )
    await call.answer()

@router.callback_query(F.data.startswith("add:"))
async def cb_add_to_cart(call: CallbackQuery) -> None:
    try:
        _, product_id_raw, size_raw, qty_raw = call.data.split(":")
        product_id = int(product_id_raw)
        size = int(size_raw)
        qty = int(qty_raw)
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    product = ProductService.get_product(product_id)
    price = ProductService.get_price(product, size)

    if product is None or price is None:
        await call.answer("Неверный товар или размер.", show_alert=True)
        return

    if qty < 1 or qty > MAX_QTY:
        await call.answer(f"Количество должно быть от 1 до {MAX_QTY}.", show_alert=True)
        return

    user_id = get_callback_user_id(call)

    if not CartService.add_to_cart(user_id, product_id, size, qty):
        await call.answer(
            f"Нельзя добавить больше {MAX_QTY} шт. для этой позиции.",
            show_alert=True,
        )
        return

    line_total = price * qty

    text = (
        "🛒 Добавлено в корзину:\n"
        "\n"
        f"🍕 {product['name']}\n"
        f"{size} см × {qty}\n"
        "\n"
        f"💰 Цена: {format_price(price)}\n"
        f"💵 Сумма: {format_price(line_total)}"
    )

    await call.answer("Добавлено в корзину")
    await safe_edit(call, text, added_to_cart_kb())

# ==================================================
# КОРЗИНА
# ==================================================

@router.callback_query(F.data == "cart")
async def cb_cart(call: CallbackQuery) -> None:
    user_id = get_callback_user_id(call)
    text, kb = format_cart(user_id)
    await safe_edit(call, text, kb)
    await call.answer()

@router.callback_query(F.data.startswith("cdec:"))
async def cb_cart_decrease(call: CallbackQuery) -> None:
    try:
        _, product_id_raw, size_raw = call.data.split(":")
        product_id = int(product_id_raw)
        size = int(size_raw)
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    user_id = get_callback_user_id(call)
    CartService.change_cart_qty(user_id, product_id, size, -1)

    text, kb = format_cart(user_id)
    await safe_edit(call, text, kb)
    await call.answer()

@router.callback_query(F.data.startswith("cinc:"))
async def cb_cart_increase(call: CallbackQuery) -> None:
    try:
        _, product_id_raw, size_raw = call.data.split(":")
        product_id = int(product_id_raw)
        size = int(size_raw)
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    user_id = get_callback_user_id(call)
    CartService.change_cart_qty(user_id, product_id, size, +1)

    text, kb = format_cart(user_id)
    await safe_edit(call, text, kb)
    await call.answer()

@router.callback_query(F.data.startswith("cdel:"))
async def cb_cart_delete(call: CallbackQuery) -> None:
    try:
        _, product_id_raw, size_raw = call.data.split(":")
        product_id = int(product_id_raw)
        size = int(size_raw)
    except Exception:
        await call.answer("Некорректные данные.", show_alert=True)
        return

    user_id = get_callback_user_id(call)
    CartService.delete_cart_item(user_id, product_id, size)

    text, kb = format_cart(user_id)
    await safe_edit(call, text, kb)
    await call.answer("Позиция удалена")

@router.callback_query(F.data == "cclear")
async def cb_cart_clear(call: CallbackQuery) -> None:
    user_id = get_callback_user_id(call)
    CartService.clear_cart(user_id)

    text, kb = format_cart(user_id)
    await safe_edit(call, text, kb)
    await call.answer("Корзина очищена")

@router.callback_query(F.data == "checkout")
async def cb_checkout(call: CallbackQuery) -> None:
    user_id = get_callback_user_id(call)
    text, kb = format_checkout(user_id)

    if text is None or kb is None:
        await call.answer("Корзина пуста.", show_alert=True)
        return

    await safe_edit(call, text, kb)
    await call.answer()

@router.callback_query(F.data == "proceed")
async def cb_proceed_order(call: CallbackQuery, state: FSMContext) -> None:
    if not call.message:
        await call.answer()
        return

    user_id = get_callback_user_id(call)
    items = CartService.build_order_items(user_id)

    if not items:
        await call.answer("Корзина пуста.", show_alert=True)
        return

    await call.answer("Заполните данные получателя")
    await start_order_flow(
        call.message,
        state,
        items,
        source="🤖 Telegram Bot",
        clear_cart_after=True,
    )
