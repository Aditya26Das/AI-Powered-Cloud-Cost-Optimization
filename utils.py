import os
import json

def create_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), "reports", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def extract_json(text):
    start = text.index("{")
    end = text.rindex("}") + 1
    return json.loads(text[start:end])

def extract_json_list(text):
    start = text.index("[")
    end = text.rindex("]") + 1
    return json.loads(text[start:end])

def save_json_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def read_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    

