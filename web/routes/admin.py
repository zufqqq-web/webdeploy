import hmac
import logging
from pathlib import Path
from aiohttp import web
from config import settings
from services.products import ProductService
from services.orders import OrderService
from bot.utils.notifications import notify_user_status
from web.middlewares.auth import is_authenticated, set_session_cookie, clear_session_cookie

logger = logging.getLogger("PizzaHouseWebAdmin")
routes = web.RouteTableDef()
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "admin"

def render_template(filename: str) -> web.Response:
    file_path = TEMPLATES_DIR / filename
    if not file_path.exists():
        return web.Response(text=f"Template {filename} not found", status=404)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return web.Response(text=content, content_type="text/html")

def require_auth(request: web.Request, is_api: bool = False):
    if not is_authenticated(request):
        if is_api:
            raise web.HTTPUnauthorized(
                text='{"error": "Unauthorized"}',
                content_type="application/json",
            )
        raise web.HTTPFound(location="/admin/login")

# ==================================================
# СТРАНИЦЫ АДМИНКИ
# ==================================================

@routes.get("/admin/login")
async def admin_login_page(request: web.Request) -> web.Response:
    if is_authenticated(request):
        raise web.HTTPFound(location="/admin")
    return render_template("login.html")

@routes.post("/admin/login")
async def admin_login_submit(request: web.Request) -> web.Response:
    try:
        data = await request.post()
        username = str(data.get("username", "")).strip()
        password = str(data.get("password", "")).strip()
    except Exception:
        raise web.HTTPFound(location="/admin/login?error=invalid")

    if not username or not password:
        raise web.HTTPFound(location="/admin/login?error=required")

    valid_username = hmac.compare_digest(username, settings.ADMIN_USERNAME)
    valid_password = hmac.compare_digest(password, settings.ADMIN_PASSWORD)

    if not (valid_username and valid_password):
        raise web.HTTPFound(location="/admin/login?error=invalid")

    response = web.HTTPFound(location="/admin")
    set_session_cookie(response, username)
    return response

@routes.get("/admin/logout")
@routes.post("/admin/logout")
async def admin_logout(request: web.Request) -> web.Response:
    response = web.HTTPFound(location="/admin/login")
    clear_session_cookie(response)
    return response

@routes.get("/admin")
async def admin_dashboard_page(request: web.Request) -> web.Response:
    require_auth(request)
    return render_template("dashboard.html")

@routes.get("/admin/products")
async def admin_products_page(request: web.Request) -> web.Response:
    require_auth(request)
    return render_template("products.html")

@routes.get("/admin/orders")
async def admin_orders_page(request: web.Request) -> web.Response:
    require_auth(request)
    return render_template("orders.html")

# ==================================================
# API АДМИНКИ (ЗАЩИЩЕНО)
# ==================================================

@routes.get("/admin/api/stats")
async def admin_stats_api(request: web.Request) -> web.Response:
    require_auth(request, is_api=True)
    stats = OrderService.get_stats()
    recent_orders = OrderService.get_orders(limit=10)
    stats["recent_orders"] = recent_orders
    return web.json_response(stats)

@routes.get("/admin/api/products")
async def admin_products_api(request: web.Request) -> web.Response:
    require_auth(request, is_api=True)
    category = request.query.get("category")
    products = ProductService.get_all_products(category=category, active_only=False)
    return web.json_response(products)

@routes.post("/admin/api/products")
async def admin_create_product_api(request: web.Request) -> web.Response:
    require_auth(request, is_api=True)
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Invalid JSON"}, status=400)

    name = str(data.get("name", "")).strip()
    if len(name) < 2:
        return web.json_response({"error": "Название должно быть от 2 символов"}, status=400)

    try:
        product_id = ProductService.create_product(
            name=name,
            description=str(data.get("description", "")).strip(),
            ingredients=data.get("ingredients", []),
            category=str(data.get("category", "other")).strip(),
            image=str(data.get("image", "")).strip(),
            price_25=int(data.get("price_25", 0)),
            price_30=int(data.get("price_30", 0)),
            price_35=int(data.get("price_35", 0)),
            is_active=1 if data.get("is_active", True) else 0,
        )
        return web.json_response({"success": True, "id": product_id})
    except Exception as e:
        logger.exception("Ошибка добавления товара в админке: %s", e)
        return web.json_response({"error": "Не удалось создать товар"}, status=500)

@routes.put("/admin/api/products/{id}")
@routes.patch("/admin/api/products/{id}")
async def admin_update_product_api(request: web.Request) -> web.Response:
    require_auth(request, is_api=True)
    try:
        product_id = int(request.match_info["id"])
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Invalid request"}, status=400)

    try:
        success = ProductService.update_product(
            product_id=product_id,
            name=data.get("name"),
            description=data.get("description"),
            ingredients=data.get("ingredients"),
            category=data.get("category"),
            image=data.get("image"),
            price_25=data.get("price_25"),
            price_30=data.get("price_30"),
            price_35=data.get("price_35"),
            is_active=data.get("is_active"),
        )
        return web.json_response({"success": success})
    except Exception as e:
        logger.exception("Ошибка обновления товара: %s", e)
        return web.json_response({"error": "Не удалось обновить товар"}, status=500)

@routes.delete("/admin/api/products/{id}")
async def admin_delete_product_api(request: web.Request) -> web.Response:
    require_auth(request, is_api=True)
    try:
        product_id = int(request.match_info["id"])
        success = ProductService.delete_product(product_id)
        return web.json_response({"success": success})
    except Exception as e:
        logger.exception("Ошибка удаления товара: %s", e)
        return web.json_response({"error": "Не удалось удалить товар"}, status=500)

@routes.post("/admin/api/products/{id}/toggle")
async def admin_toggle_product_api(request: web.Request) -> web.Response:
    require_auth(request, is_api=True)
    try:
        product_id = int(request.match_info["id"])
        data = await request.json()
        is_active = bool(data.get("is_active", True))
        success = ProductService.toggle_product_active(product_id, is_active)
        return web.json_response({"success": success})
    except Exception as e:
        logger.exception("Ошибка переключения статуса товара: %s", e)
        return web.json_response({"error": "Не удалось изменить статус"}, status=500)

@routes.get("/admin/api/orders")
async def admin_orders_api(request: web.Request) -> web.Response:
    require_auth(request, is_api=True)
    status = request.query.get("status", "all")
    orders = OrderService.get_orders(status=status, limit=100)

    # Прикрепляем позиции к каждому заказу
    detailed_orders = []
    for order in orders:
        order_copy = dict(order)
        order_copy["items"] = OrderService.get_order_items(order["id"])
        detailed_orders.append(order_copy)

    return web.json_response(detailed_orders)

@routes.post("/admin/api/orders/{id}/status")
async def admin_update_order_status_api(request: web.Request) -> web.Response:
    require_auth(request, is_api=True)
    try:
        order_id = int(request.match_info["id"])
        data = await request.json()
        new_status = str(data.get("status", "")).strip()
    except Exception:
        return web.json_response({"error": "Invalid request"}, status=400)

    if not new_status:
        return web.json_response({"error": "Статус не указан"}, status=400)

    success = OrderService.update_order_status(order_id, new_status)
    if not success:
        return web.json_response({"error": "Заказ не найден"}, status=404)

    # Оповещаем пользователя в Telegram при смене статуса
    order = OrderService.get_order(order_id)
    bot = request.app.get("bot")
    if bot and order:
        try:
            await notify_user_status(bot, order, new_status)
        except Exception:
            logger.exception("Не удалось отправить уведомление о статусе пользователю Telegram")

    return web.json_response({"success": True})
