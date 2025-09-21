# AI Recipe Generator API

AI-powered REST API that generates personalised recipes based on user preferences, dietary restrictions, budget, demographics, and custom requests.  
The system integrates FreeGPT and DuckAI to produce structured JSON recipes with ingredients, instructions, calories, cuisine, health benefits, comments, rating, and automatically generated images.

## ✨ Features
- User management with MongoDB (registration, login, storing preferences).
- Recipe generation via multiple AI backends:
  - **FreeGPT** for text generation
  - **DuckAI** for conversational recipe creation
  - **Manual mode** for testing
- Prompt templating for individualised results (`prompt_template.txt`).
- Automatic recipe image generation via Pollinations API.
- JSON output with full structure.

## ⚙️ Installation
```bash
git clone https://github.com/gopyc-code/ai-recipe-generator-api.git
cd ai-recipe-generator-api
pip install -r requirements.txt
