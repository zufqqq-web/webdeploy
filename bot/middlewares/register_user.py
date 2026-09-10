import logging
from aiogram import BaseMiddleware
from services.users import UserService

logger = logging.getLogger("PizzaHouseBot")

class RegisterUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)

        if user:
            try:
                UserService.register_user(
                    user_id=user.id,
                    full_name=user.full_name,
                    username=user.username,
                )
            except Exception:
                logger.exception("Не удалось зарегистрировать пользователя.")

        return await handler(event, data)
