from pathlib import Path
from aiohttp import web

routes = web.RouteTableDef()
DIST_DIR = Path(__file__).resolve().parent.parent.parent / "webn" / "dist"

def setup_public_routes(app: web.Application) -> None:
    if DIST_DIR.exists() and (DIST_DIR / "index.html").exists():
        # Добавляем раздачу assets
        assets_dir = DIST_DIR / "assets"
        if assets_dir.exists():
            app.router.add_static("/assets", str(assets_dir), name="assets")

        # Добавляем раздачу favicon/public если есть
        for item in DIST_DIR.iterdir():
            if item.is_file() and item.name != "index.html":
                def make_file_handler(file_path):
                    async def handler(request):
                        return web.FileResponse(file_path)
                    return handler
                app.router.add_get(f"/{item.name}", make_file_handler(item))

        # Корневой маршрут
        async def index_handler(request: web.Request) -> web.Response:
            return web.FileResponse(DIST_DIR / "index.html")

        app.router.add_get("/", index_handler)
    else:
        async def fallback_handler(request: web.Request) -> web.Response:
            html = """
            <!DOCTYPE html>
            <html lang="ru">
            <head>
              <meta charset="UTF-8">
              <title>PizzaHouse</title>
              <style>
                body { background: #0c0a09; color: #fff; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; text-align: center; }
                .box { background: #1c1917; padding: 2rem; border-radius: 20px; border: 1px solid #292524; }
                a { color: #f59e0b; text-decoration: none; font-weight: bold; }
              </style>
            </head>
            <body>
              <div class="box">
                <h1>🍕 PizzaHouse</h1>
                <p>Бэкенд запущен успешно!</p>
                <p style="margin-top: 1rem;"><a href="/admin">Перейти в панель управления →</a></p>
              </div>
            </body>
            </html>
            """
            return web.Response(text=html, content_type="text/html")

        app.router.add_get("/", fallback_handler)
