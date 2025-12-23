import json
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from services.utils import extract_json, create_folder, save_json_file

def generate_project_profile(user_query: str):
    load_dotenv()

    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        max_new_tokens=2048
    ) # type: ignore

    model = ChatHuggingFace(llm=llm)

    with open("prompts/project_profile_prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    messages = [
        {"role": "user", "content": user_query},
        {"role": "user", "content": prompt}
    ]

    response = model.invoke(messages)
    profile = extract_json(response.content)

    folder = create_folder(profile["name"])
    save_json_file(f"{folder}/project_profile.json", profile)

    return profile
