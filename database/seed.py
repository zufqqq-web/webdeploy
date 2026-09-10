import json
from database.connection import get_db

PIZZA_SEED = [
    {
        "name": "Пепперони",
        "description": "Классическая пицца с пикантной пепперони и большим количеством сыра.",
        "ingredients": ["томатный соус", "моцарелла", "пепперони"],
        "category": "pizza",
        "image": "https://placehold.co/800x600/png?text=Pepperoni",
        "prices": {25: 45000, 30: 60000, 35: 75000},
    },
    {
        "name": "Маргарита",
        "description": "Классическая итальянская пицца с томатами, моцареллой и базиликом.",
        "ingredients": ["томатный соус", "моцарелла", "томаты", "базилик"],
        "category": "pizza",
        "image": "https://placehold.co/800x600/png?text=Margarita",
        "prices": {25: 38000, 30: 52000, 35: 66000},
    },
    {
        "name": "4 сыра",
        "description": "Пицца для любителей сыра: моцарелла, пармезан, дорблю и чеддер.",
        "ingredients": ["сливочный соус", "моцарелла", "пармезан", "дорблю", "чеддер"],
        "category": "pizza",
        "image": "https://placehold.co/800x600/png?text=4+Cheese",
        "prices": {25: 50000, 30: 65000, 35: 80000},
    },
    {
        "name": "Гавайская",
        "description": "Нежная курица, ананасы и сыр. Спорно, но вкусно.",
        "ingredients": ["томатный соус", "моцарелла", "курица", "ананасы"],
        "category": "pizza",
        "image": "https://placehold.co/800x600/png?text=Hawaiian",
        "prices": {25: 47000, 30: 62000, 35: 77000},
    },
    {
        "name": "BBQ Chicken",
        "description": "Курица, соус барбекю, красный лук и моцарелла.",
        "ingredients": ["соус BBQ", "моцарелла", "курица", "красный лук"],
        "category": "pizza",
        "image": "https://placehold.co/800x600/png?text=BBQ+Chicken",
        "prices": {25: 52000, 30: 68000, 35: 84000},
    },
    {
        "name": "Мясная",
        "description": "Максимально сытная пицца с несколькими видами мяса.",
        "ingredients": ["томатный соус", "моцарелла", "пепперони", "ветчина", "курица", "бекон"],
        "category": "pizza",
        "image": "https://placehold.co/800x600/png?text=Meat+Pizza",
        "prices": {25: 55000, 30: 72000, 35: 89000},
    },
]

def seed_products() -> None:
    """Заполняет базу данных начальными товарами, только если таблица пуста."""
    with get_db() as conn:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM products").fetchone()
        count = row["cnt"] if row else 0

        if count == 0:
            for pizza in PIZZA_SEED:
                conn.execute(
                    """
                    INSERT INTO products (
                        name,
                        description,
                        ingredients,
                        category,
                        image,
                        price_25,
                        price_30,
                        price_35,
                        is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """,
                    (
                        pizza["name"],
                        pizza["description"],
                        json.dumps(pizza["ingredients"], ensure_ascii=False),
                        pizza["category"],
                        pizza["image"],
                        pizza["prices"][25],
                        pizza["prices"][30],
                        pizza["prices"][35],
                    ),
                )
