from database.repositories.products import ProductRepository
from config.constants import CATEGORY_ALIASES

class ProductService:
    @staticmethod
    def normalize_category(cat: str) -> str:
        cat_clean = cat.strip().lower()
        return CATEGORY_ALIASES.get(cat_clean, "other")

    @classmethod
    def get_active_products(cls, category: str | None = None) -> list[dict]:
        if category and category != "all":
            category = cls.normalize_category(category)
        else:
            category = None
        return ProductRepository.get_active(category)

    @classmethod
    def get_all_products(cls, category: str | None = None, active_only: bool = False) -> list[dict]:
        if category and category != "all":
            category = cls.normalize_category(category)
        else:
            category = None
        return ProductRepository.get_all(category, active_only=active_only)

    @staticmethod
    def get_product(product_id: int, active_only: bool = False) -> dict | None:
        return ProductRepository.get_by_id(product_id, active_only=active_only)

    @staticmethod
    def get_price(product: dict | None, size: int) -> int | None:
        if not product:
            return None
        return product.get("prices", {}).get(size)

    @classmethod
    def create_product(
        cls,
        name: str,
        description: str,
        ingredients: list[str] | str,
        category: str,
        image: str,
        price_25: int,
        price_30: int,
        price_35: int,
        is_active: int = 1,
    ) -> int:
        if isinstance(ingredients, str):
            ingredients = [i.strip() for i in ingredients.split(",") if i.strip()]
        
        category = cls.normalize_category(category)

        return ProductRepository.create(
            name=name.strip(),
            description=description.strip(),
            ingredients=ingredients,
            category=category,
            image=image.strip(),
            price_25=int(price_25),
            price_30=int(price_30),
            price_35=int(price_35),
            is_active=1 if is_active else 0,
        )

    @classmethod
    def update_product(
        cls,
        product_id: int,
        name: str | None = None,
        description: str | None = None,
        ingredients: list[str] | str | None = None,
        category: str | None = None,
        image: str | None = None,
        price_25: int | None = None,
        price_30: int | None = None,
        price_35: int | None = None,
        is_active: bool | int | None = None,
    ) -> bool:
        if isinstance(ingredients, str):
            ingredients = [i.strip() for i in ingredients.split(",") if i.strip()]

        if category is not None:
            category = cls.normalize_category(category)

        return ProductRepository.update(
            product_id=product_id,
            name=name,
            description=description,
            ingredients=ingredients,
            category=category,
            image=image,
            price_25=int(price_25) if price_25 is not None else None,
            price_30=int(price_30) if price_30 is not None else None,
            price_35=int(price_35) if price_35 is not None else None,
            is_active=is_active,
        )

    @staticmethod
    def toggle_product_active(product_id: int, is_active: bool) -> bool:
        return ProductRepository.set_active(product_id, is_active)

    @staticmethod
    def deactivate_product(product_id: int) -> bool:
        return ProductRepository.set_active(product_id, False)

    @staticmethod
    def delete_product(product_id: int) -> bool:
        return ProductRepository.delete(product_id)
