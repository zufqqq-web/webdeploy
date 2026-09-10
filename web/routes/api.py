import logging
from aiohttp import web
from config.constants import CATEGORY_LABELS
from services.products import ProductService
from services.orders import OrderService
from bot.utils.notifications import notify_admin_about_order

logger = logging.getLogger("PizzaHouseWeb")

routes = web.RouteTableDef()

@routes.get("/api/products")
async def get_products_api(request: web.Request) -> web.Response:
    category = request.query.get("category")
    products = ProductService.get_active_products(category=category)
    return web.json_response(products)

@routes.get("/api/products/{id}")
async def get_product_by_id_api(request: web.Request) -> web.Response:
    try:
        product_id = int(request.match_info["id"])
    except ValueError:
        return web.json_response({"error": "Invalid ID"}, status=400)

    product = ProductService.get_product(product_id, active_only=True)
    if not product:
        return web.json_response({"error": "Product not found"}, status=404)

    return web.json_response(product)

@routes.get("/api/categories")
async def get_categories_api(request: web.Request) -> web.Response:
    categories = [
        {"id": key, "name": label.split(" ", 1)[-1], "emoji": label.split(" ", 1)[0], "label": label}
        for key, label in CATEGORY_LABELS.items()
    ]
    return web.json_response(categories)

@routes.post("/api/orders")
async def create_order_api(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Invalid JSON body"}, status=400)

    client_name = str(data.get("client_name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    address = str(data.get("address", "")).strip()
    comment = str(data.get("comment", "")).strip()
    items = data.get("items", [])

    if len(client_name) < 2:
        return web.json_response({"error": "Укажите имя получателя"}, status=400)

    if sum(1 for c in phone if c.isdigit()) < 7:
        return web.json_response({"error": "Укажите корректный номер телефона"}, status=400)

    if len(address) < 4:
        return web.json_response({"error": "Укажите адрес доставки"}, status=400)

    if not items or not isinstance(items, list):
        return web.json_response({"error": "В заказе нет товаров"}, status=400)

    try:
        order_id = OrderService.create_order(
            user_id=None,
            user_name="",
            username="",
            client_name=client_name,
            phone=phone,
            address=address,
            comment=comment,
            source="🌐 Сайт",
            items=items,
        )

        if not order_id:
            return web.json_response({"error": "Не удалось создать заказ"}, status=400)

        # Оповещение администратора в Telegram, если бот доступен в app
        bot = request.app.get("bot")
        if bot:
            try:
                await notify_admin_about_order(bot, order_id)
            except Exception:
                logger.exception("Не удалось отправить уведомление о заказе в Telegram")

        return web.json_response({"success": True, "order_id": order_id})
    except Exception as e:
        logger.exception("Ошибка создания заказа через сайт: %s", e)
        return web.json_response({"error": "Внутренняя ошибка сервера"}, status=500)
