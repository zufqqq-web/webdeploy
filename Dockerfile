FROM python:3.11-slim

# Установка системных переменных
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    HOST=0.0.0.0

WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода проекта
COPY . .

# Создание каталога для базы данных (для монтирования volume в Marshub/Docker)
RUN mkdir -p /data

# Порт веб-сервера
EXPOSE 8080

# Запуск единого приложения (aiogram Long Polling + aiohttp Web Server)
CMD ["python", "main.py"]
