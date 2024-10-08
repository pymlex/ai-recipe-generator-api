from database import get_user_by_login, save_recipe
from ai_service import get_recipe
from models import Recipe, User

def gather_user_data(user: User) -> dict:
    """Собирает данные о пользователе для генерации таргетированного рецепта."""
    return {
        "preferences": user.preferences,
        "diet_restrictions": user.diet_restrictions,
        "budget": user.budget,
        "country": user.country,
        "age": user.age,
        "gender": user.gender
    }

async def generate_recipe(user_data: dict, request: str) -> Recipe:
    """Генерирует рецепт с помощью AI."""
    recipe_result = await get_recipe(user_data, request)

    return Recipe(
        recipe_name=recipe_result.get("recipe_name", ""),
        ingredients=recipe_result.get("ingredients", []),
        instructions=recipe_result.get("instructions", []),
        comments=recipe_result.get("comments", ""),
        cuisine=recipe_result.get("cuisine", ""),
        calories=recipe_result.get("calories", ""),
        health_benefits=recipe_result.get("health_benefits", ""),
        image_url=recipe_result.get("image_url", ""),
        rating=recipe_result.get("rating", 5)
    )

def save_generated_recipe(login: str, recipe_data: Recipe):
    """Сохраняет сгенерированный рецепт в базу данных."""
    save_recipe(login, recipe_data)
