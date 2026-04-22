from pathlib import Path
import json
JSON_PATH = Path(__file__).parent / "data" / "chat_data.json"

def read_json (): 
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data 

def write_json (data: json):
    json_str = json.dumps(data, indent=4)
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        file.write(json_str)