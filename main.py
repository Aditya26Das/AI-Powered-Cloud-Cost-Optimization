import os
import json
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

def create_folder(folder_name):
    try:
        current_dir = os.getcwd()
        folder_path = os.path.join(current_dir,"reports",folder_name)

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(f"Folder '{folder_name}' created successfully.")
        else:
            print(f"Folder '{folder_name}' already exists.")

    except OSError as e:
        print(f"Error creating folder: {e}")

def extract_json(text):
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        raise ValueError("No valid JSON found")

def extract_json_list(text):
    try:
        start = text.index("[")
        end = text.rindex("]") + 1
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
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        # repo_id="meta-llama/Llama-3.1-8B-Instruct"
        # repo_id="moonshotai/Kimi-K2-Instruct",
        max_new_tokens=2048
    ) # type: ignore
    
    model = ChatHuggingFace(llm=llm)
    
    
    # Generate Project Profile
    with open("project_profile_prompt.txt", "r", encoding="utf-8") as f:
        project_profile_prompt = f.read()
    user_query=input("Enter your query: ")
    messages = [
        {"role": "user", "content": user_query},
        {"role": "user", "content": project_profile_prompt}
    ]
    response=model.invoke(messages)
    print(response.content)
    result_project_profile = extract_json(response.content)
    create_folder(f"{result_project_profile["name"]}")
    save_json_file(f"reports/{result_project_profile["name"]}/project_profile.json", result_project_profile)

    # Generate Synthetic Bill
    messages2 = []
    messages2.append({"role": "assistant", "content": json.dumps(result_project_profile)})
    with open("synthetic_bill_prompt.txt", "r", encoding="utf-8") as f:
        synthetic_bill_prompt = f.read()
    messages2.append({"role": "user", "content": f"{synthetic_bill_prompt}"})
    response=model.invoke(messages2)
    print(response.content)
    
    result_synthetic_bill = extract_json_list(response.content)
    save_json_file(f"reports/{result_project_profile['name']}/synthetic_bill.json", result_synthetic_bill)
    
    
    