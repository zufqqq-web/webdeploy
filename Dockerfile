# ---- Stage 1: сборка фронтенда (webn) ----
FROM node:20-alpine AS frontend-build

WORKDIR /frontend

# Копируем только манифесты для кеширования установки зависимостей
COPY webn/package*.json ./
RUN npm ci

# Копируем остальной код фронтенда и собираем
COPY webn/ ./
RUN npm run build
# Ожидается, что результат сборки окажется в /frontend/dist


# ---- Stage 2: бэкенд (Python) ----
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    HOST=0.0.0.0

WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода проекта (бэкенд)
COPY . .

# Подкладываем собранный фронтенд именно туда, где его ждёт web/public.py:
# DIST_DIR = <repo_root>/webn/dist
COPY --from=frontend-build /frontend/dist ./webn/dist

# Каталог для базы данных (для монтирования volume в Marshub/Docker)
RUN mkdir -p /data

EXPOSE 8080

CMD ["python", "main.py"]