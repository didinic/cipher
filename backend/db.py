from pathlib import Path
import json
JSON_PATH = Path(__file__).parent / "data" / "chat_data.json"

def read_json (): 
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    return data 