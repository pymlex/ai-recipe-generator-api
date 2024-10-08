from pydantic import BaseModel
from typing import List, Dict

class User(BaseModel):
    name: str
    login: str
    password: str
    country: str
    age: int
    preferences: str
    diet_restrictions: str
    budget: float
    gender: str

class UserLogin(BaseModel):
    login: str
    password: str

class RecipeRequest(BaseModel):
    login: str
    request: str

class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[Dict[str, str]]  
    instructions: List[Dict[str, str]] 
    comments: str
    cuisine: str
    calories: str
    health_benefits: str
    image_url: str
    rating: int  # Рейтинг
