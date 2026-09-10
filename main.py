import asyncio
import logging
import sys
from aiohttp import web
from config import settings
from database import init_db
from database.seed import seed_products
from bot import create_bot
from web import create_web_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("PizzaHouse")

async def main() -> None:
    logger.info("Инициализация проекта PizzaHouse...")

    # Валидация конфигурации
    try:
        settings.validate(require_bot_token=True)
    except ValueError as e:
        logger.critical("Ошибка конфигурации при запуске:\n%s", e)
        sys.exit(1)

    # Инициализация базы данных и сидирование при пустой таблице
    init_db()
    seed_products()
    logger.info("База данных SQLite инициализирована: %s", settings.DATABASE_PATH)

    # Создание бота и диспетчера
    bot, dp = create_bot()

    # Создание веб-сервера
    app = create_web_app(bot=bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=settings.HOST, port=settings.PORT)
    await site.start()
    logger.info("Веб-сервер слушает на http://%s:%s", settings.HOST, settings.PORT)

    # Удаление возможного вебхука перед стартом Long Polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception:
        logger.exception("Не удалось удалить webhook перед началом polling.")

    logger.info("Запуск Telegram Long Polling...")
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Остановка веб-сервера и сессии бота...")
        await runner.cleanup()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Приложение PizzaHouse остановлено.")
