import json

def text_to_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}

def extract_json_from_text(text: str) -> dict:
    if '{' not in text or '}' not in text:
        return {"error": "Invalid JSON format"}
    text = text[text.find('{'):text.rfind('}') + 1]
    return text_to_json(text)
