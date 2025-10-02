# AI Recipe Generator API

AI-powered REST API that generates personalised recipes based on user preferences, dietary restrictions, budget, demographics, and custom requests.  
The system integrates FreeGPT and DuckAI to produce structured JSON recipes with ingredients, instructions, calories, cuisine, health benefits, comments, rating, and automatically generated images.  
Check the [Telegram Bot](https://github.com/gopyc-code/ai-recipe-generator-telegram) implementation of this project. 

## Features
- User management with MongoDB (registration, login, storing preferences).
- Asynchronous request handling with FastAPI.
- Recipe generation via multiple AI backends:
  - **FreeGPT** for text generation
  - **DuckAI** for conversational recipe creation
  - **Manual mode** for testing
- Prompt templating for individualised results (`prompt_template.txt`).
- Automatic recipe image generation via Pollinations API.
- JSON output with full structure.
## 🗄️ Database Structure

### Users Collection (`users`)
- **name** — full name of the user  
- **login** — unique login  
- **password** — hashed password  
- **country** — country of the user  
- **age** — age in years  
- **preferences** — cuisine and food preferences  
- **diet_restrictions** — dietary limitations (e.g., vegetarian, gluten-free)  
- **budget** — average budget per meal  
- **gender** — gender  

### Recipes Collection (`recipes`)
- **login** — user login who generated the recipe  
- **recipe_name** — title of the recipe  
- **ingredients** — list of ingredients with name and amount  
- **instructions** — list of step-by-step instructions  
- **comments** — additional notes or suggestions  
- **cuisine** — cuisine type (e.g., Mediterranean, Asian)  
- **calories** — estimated calories  
- **health_benefits** — nutritional and health information  
- **image_url** — link to generated image  
- **rating** — numeric rating (default 5)

## Running the API

To start the AI Recipe Generator API locally, use **uvicorn**:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
