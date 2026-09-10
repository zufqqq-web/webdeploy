from .api import routes as api_routes
from .admin import routes as admin_routes
from .public import setup_public_routes

__all__ = ["api_routes", "admin_routes", "setup_public_routes"]
