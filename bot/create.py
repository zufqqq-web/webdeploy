import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from bot.middlewares.register_user import RegisterUserMiddleware
from bot.handlers.user import router as user_router
from bot.handlers.orders import router as orders_router
from bot.handlers.admin import router as admin_router

logger = logging.getLogger("PizzaHouseBot")

def create_bot() -> tuple[Bot, Dispatcher]:
    if not settings.BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан. Укажите его в переменных окружения.")

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация middleware
    dp.message.middleware(RegisterUserMiddleware())
    dp.callback_query.middleware(RegisterUserMiddleware())

    # Подключение роутеров
    dp.include_router(orders_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # Обработка ошибок
    @dp.errors()
    async def global_error_handler(event, exception=None):
        if exception is None:
            exception = getattr(event, "exception", None)
        logger.error("Unhandled error in bot: %s", exception, exc_info=exception)
        return True

    return bot, dp
