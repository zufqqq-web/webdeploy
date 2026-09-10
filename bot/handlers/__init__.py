from .user import router as user_router
from .orders import router as orders_router
from .admin import router as admin_router

__all__ = ["user_router", "orders_router", "admin_router"]
