import os
import sys
import secrets
from pathlib import Path

# Поиск и загрузка .env файла
def load_dotenv(dotenv_path: Path | None = None) -> None:
    if dotenv_path is None:
        dotenv_path = Path(__file__).resolve().parent.parent / ".env"
    
    if not dotenv_path.is_file():
        return

    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key and key not in os.environ:
                    os.environ[key] = val
    except Exception as e:
        print(f"Предупреждение: не удалось прочитать .env: {e}", file=sys.stderr)

load_dotenv()

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent

# Токен бота
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()

# Администратор Telegram
raw_admin_id = os.getenv("ADMIN_ID", "").strip()
try:
    ADMIN_ID: int = int(raw_admin_id) if raw_admin_id else 0
except ValueError:
    ADMIN_ID = 0

ADMIN_IDS: set[int] = {ADMIN_ID} if ADMIN_ID else set()

# База данных
DATABASE_PATH: str = os.getenv("DATABASE_PATH", "").strip()
if not DATABASE_PATH:
    # Проверяем data/pizza.db или pizza.db в корне
    data_db = BASE_DIR / "data" / "pizza.db"
    root_db = BASE_DIR / "pizza.db"
    if data_db.exists():
        DATABASE_PATH = str(data_db)
    else:
        DATABASE_PATH = str(root_db)

# Веб-сервер
PORT: int = int(os.getenv("PORT", "8080"))
HOST: str = os.getenv("HOST", "0.0.0.0")

# Веб-админка
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin").strip()
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "").strip()
SESSION_SECRET: str = os.getenv("SESSION_SECRET", "").strip()

if not SESSION_SECRET:
    SESSION_SECRET = secrets.token_hex(32)

def validate(require_bot_token: bool = True) -> None:
    """Валидация обязательных настроек при старте приложения"""
    errors = []
    
    if require_bot_token and not BOT_TOKEN:
        errors.append(
            "BOT_TOKEN не задан! Установите переменную окружения BOT_TOKEN в .env или параметрах запуска."
        )
    
    if not ADMIN_ID:
        print(
            "ВНИМАНИЕ: ADMIN_ID не задан или некорректен. Команды администратора в Telegram не будут доступны.",
            file=sys.stderr,
        )

    if not ADMIN_PASSWORD:
        print(
            "ВНИМАНИЕ: ADMIN_PASSWORD не задан. Для веб-админки рекомендуется задать надёжный ADMIN_PASSWORD.",
            file=sys.stderr,
        )

    if errors:
        raise ValueError("\n".join(errors))
