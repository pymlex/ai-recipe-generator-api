from pymongo import MongoClient
from config import MONGODB_URL, DATABASE_NAME
from models import User, Recipe

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

def init_db():
    for collection in ('users', 'recipes'):
        if collection not in db.list_collection_names():
            db.create_collection(collection)

def save_user(user_data: User):
    user_data_dict = user_data.dict()
    db.users.insert_one(user_data_dict)

def save_recipe(login: str, recipe_data: Recipe):
    recipe_data_dict = recipe_data.dict()
    recipe_data_dict['login'] = login
    db.recipes.insert_one(recipe_data_dict)

def get_user_by_login(login: str) -> User:
    user_data = db.users.find_one({"login": login})
    if user_data:
        return User(**user_data)
    return None

def get_recipe_by_login(login: str) -> list[Recipe]:
    recipe_data = db.recipes.find({"login": login})
    return [Recipe(**recipe) for recipe in recipe_data]
