import logging
from urllib.parse import unquote
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from config.constants import MAX_QTY
from services.products import ProductService
from bot.keyboards.reply import get_main_kb
from bot.states.order import OrderStates
from bot.utils.auth import get_message_user_id

logger = logging.getLogger("PizzaHouseBot")

def normalize_payload(payload: str) -> tuple[str, str]:
    payload = unquote(payload.strip())
    source = "📱 Telegram Mini App"

    lower_payload = payload.lower()

    if lower_payload.startswith("s-"):
        payload = payload[2:]
        source = "🌐 Сайт"
    elif lower_payload.startswith("m-"):
        payload = payload[2:]
        source = "📱 Telegram Mini App"

    return payload, source

def parse_order_payload(raw_payload: str) -> tuple[list[dict] | None, str]:
    """
    Формат:
        m-1_30_2
        s-1_30_2-2_25_1

    Где:
        m- — заказ из Telegram Mini App;
        s- — заказ с сайта;
        1 — product_id;
        30 — размер;
        2 — количество.
    """
    payload, source = normalize_payload(raw_payload)

    try:
        if not payload:
            return None, source

        if len(payload) > 500:
            return None, source

        parts = payload.split("-")

        if not parts or len(parts) > 50:
            return None, source

        aggregated: dict[tuple[int, int], int] = {}

        for part in parts:
            if not part:
                return None, source

            fields = part.split("_")

            if len(fields) != 3:
                return None, source

            product_id = int(fields[0])
            size = int(fields[1])
            qty = int(fields[2])

            product = ProductService.get_product(product_id, active_only=True)

            if product is None:
                return None, source

            price = ProductService.get_price(product, size)

            if price is None:
                return None, source

            if qty < 1 or qty > MAX_QTY:
                return None, source

            key = (product_id, size)
            new_qty = aggregated.get(key, 0) + qty

            if new_qty > MAX_QTY:
                return None, source

            aggregated[key] = new_qty

        items = []

        for (product_id, size), qty in aggregated.items():
            product = ProductService.get_product(product_id, active_only=True)
            price = ProductService.get_price(product, size)

            if product is None or price is None:
                return None, source

            items.append(
                {
                    "product_id": product_id,
                    "name": product["name"],
                    "size": size,
                    "qty": qty,
                    "price": price,
                    "line_total": price * qty,
                }
            )

        if not items:
            return None, source

        return items, source

    except Exception:
        logger.exception("Ошибка парсинга deep link payload.")
        return None, source

async def start_order_flow(
    message: Message,
    state: FSMContext,
    items: list[dict],
    source: str,
    clear_cart_after: bool = False,
) -> None:
    if not items:
        await message.answer(
            "В заказе нет товаров.",
            reply_markup=get_main_kb(get_message_user_id(message)),
        )
        return

    await state.clear()
    await state.update_data(
        items=items,
        source=source,
        clear_cart_after=clear_cart_after,
    )
    await state.set_state(OrderStates.name)

    await message.answer(
        "📝 Оформление заказа.\n"
        "\n"
        "Введите имя получателя:",
        reply_markup=ReplyKeyboardRemove(),
    )
