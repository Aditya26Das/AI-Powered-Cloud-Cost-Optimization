import os
import json
from langchain_community.document_loaders import UnstructuredExcelLoader

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
    
def load_excel_data(file_path="cloud_pricing_reference_synthetic.xlsx"):
    loader = UnstructuredExcelLoader(os.path.join(os.getcwd(), file_path), mode="elements")
    docs = loader.load()
    return docs[0].page_content