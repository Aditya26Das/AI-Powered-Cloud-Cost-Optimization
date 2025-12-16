import os
import json
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

def extract_json(text):
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        raise ValueError("No valid JSON found")

def save_json_file(file, data):
  with open(f"{file}", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    load_dotenv()    
    
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct"
    ) # type: ignore
    
    model = ChatHuggingFace(llm=llm)
    
    with open("project_profile_prompt.txt", "r", encoding="utf-8") as f:
        project_profile_prompt = f.read()
    
    user_query=input("Enter your query: ")
    messages = [
        {"role": "user", "content": user_query},
        {"role": "user", "content": project_profile_prompt}
    ]
    
    response=model.invoke(messages)
    result_project_profile = extract_json(response.content)
    save_json_file("reports/project_profile.json", result_project_profile)
    
    