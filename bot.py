"""
PizzaHouse Bot & Web Launcher (обратная совместимость).
Основная точка входа перемещена в main.py.
Все секреты читаются из переменных окружения (BOT_TOKEN, ADMIN_ID).
"""
import asyncio
import logging
from main import main

logger = logging.getLogger("PizzaHouse")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Приложение остановлено.")