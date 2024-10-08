from typing import Dict, Any
import asyncio
from duck_chat import DuckChat
from utils import text_to_json, extract_json_from_text
from config import AI_SERVICE
from freeGPT import Client as FreeGPTClient
from io import BytesIO
from PIL import Image
import requests

def load_prompt_template():
    """Загружает шаблон промпта из файла."""
    with open("prompt_template.txt", "r", encoding="utf-8") as file:
        return file.read()

def generate_prompt(user_data: Dict[str, Any], request: str) -> str:
    """Формирует промпт на основе данных пользователя и его запроса."""
    prompt_template = load_prompt_template()
    return prompt_template.format(
        preferences=user_data.get("preferences", "не указаны"),
        country=user_data.get("country", "не указана"),
        age=user_data.get("age", "не указан"),
        budget=user_data.get("budget", "не указан"),
        diet_restrictions=user_data.get("diet_restrictions", "нет"),
        gender=user_data.get("gender", "не указан"),
        request=request
    )

def get_recipe_text_from_freegpt(user_data: Dict[str, Any], request: str) -> Dict[str, Any]:
    """Генерирует текст рецепта с использованием FreeGPT."""
    prompt = generate_prompt(user_data, request)
    try:
        recipe_text = FreeGPTClient.create_completion("gpt3", prompt)
        recipe_json = extract_json_from_text(recipe_text)
        return recipe_json
    except Exception as e:
        print(f"Ошибка получения текста рецепта с FreeGPT: {e}")
        return {} 

def get_image_url_from_pollinations(recipe_name: str) -> str:
    prompt = recipe_name
    width = 626
    height = 418
    seed = -1 
    model = 'flux' 
    nologo = 'true'
    enhance  ='true'
    private = 'true'

    return (
        f"https://image.pollinations.ai/prompt/{prompt}?"
        f"width={width}&height={height}&model={model}&seed={seed}"
        f"&nologo={nologo}&enhance={enhance}&private={private}"
    )

async def get_recipe_from_freegpt(user_data: Dict[str, Any], request: str) -> Dict[str, Any]:
    """Получаем рецепт с текстом и изображением через FreeGPT."""
    recipe_json = get_recipe_text_from_freegpt(user_data, request)

    # Получаем изображение
    if recipe_json and "recipe_name" in recipe_json:
        image_url = get_image_url_from_pollinations(recipe_json["recipe_name"])
        recipe_json['image_url'] = image_url

    return recipe_json

async def get_recipe_from_duckai(user_data: Dict[str, Any], request: str) -> Dict[str, Any]:
    """Получаем рецепт с использованием DuckAI."""
    prompt = generate_prompt(user_data, request)
    async with DuckChat() as chat:
        recipe_text = await chat.ask_question(prompt)
    recipe_json = extract_json_from_text(recipe_text)
    recipe_json['image_url'] = get_image_url_from_pollinations(
        recipe_json["recipe_name"] +', Ингредиенты: ' + \
        "; ".join([
            f"🔹 {item['name']})" 
            for item in recipe_json.get('ingredients', [])
        ])
    )
    return recipe_json

def get_recipe_manually(user_data: Dict[str, Any], request: str) -> Dict[str, Any]:
    """Ручной вариант получения рецепта."""
    prompt = generate_prompt(user_data, request)
    print(prompt)
    return text_to_json(input("Введите рецепт: "))

async def get_recipe(user_data: Dict[str, Any], request: str) -> Dict[str, Any]:
    """Выбирает и вызывает соответствующую функцию для получения рецепта на основе настроек."""
    ai_services = {
        "duckai": get_recipe_from_duckai,
        "manual": get_recipe_manually,
        "freegpt": get_recipe_from_freegpt
    }

    service_function = ai_services.get(AI_SERVICE, get_recipe_from_duckai)
    if asyncio.iscoroutinefunction(service_function):
        return await service_function(user_data, request)
    else:
        return service_function(user_data, request)
