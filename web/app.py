import logging
from aiohttp import web
from web.routes.api import routes as api_routes
from web.routes.admin import routes as admin_routes
from web.routes.public import setup_public_routes

logger = logging.getLogger("PizzaHouseWeb")

def create_web_app(bot=None) -> web.Application:
    app = web.Application()
    app["bot"] = bot

    # Добавляем API и админские маршруты
    app.add_routes(api_routes)
    app.add_routes(admin_routes)

    # Добавляем статику и SPA
    setup_public_routes(app)

    return app
