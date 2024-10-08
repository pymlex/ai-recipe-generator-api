from fastapi import FastAPI, HTTPException
from models import User, UserLogin, RecipeRequest
from recipe_service import gather_user_data, generate_recipe
from database import save_user, get_user_by_login, init_db, save_recipe

app = FastAPI()
init_db()

@app.post("/users/")
async def create_user(user: User):
    existing_user = get_user_by_login(user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Логин уже существует.")
    
    save_user(user)
    return {"status": "User created successfully"}

@app.post("/login/")
async def login(user_login: UserLogin):
    user = get_user_by_login(user_login.login)
    if not user or user.password != user_login.password:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль.")

    return {"status": "Login successful", "login": user.login, "name": user.name}

@app.post("/recipes/")
async def create_recipe(recipe_request: RecipeRequest):
    user = get_user_by_login(recipe_request.login)
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user_data = gather_user_data(user)
    recipe_data = await generate_recipe(user_data, recipe_request.request)

    save_recipe(recipe_request.login, recipe_data)
    return {"status": "Recipe generated successfully", "recipe": recipe_data.dict()}
