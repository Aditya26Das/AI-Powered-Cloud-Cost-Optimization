import json
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from utils import extract_json_list, save_json_file

def generate_synthetic_bill(project_profile: dict):
    load_dotenv()
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        max_new_tokens=2048
    ) # type: ignore

    model = ChatHuggingFace(llm=llm)

    with open("synthetic_bill_prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    messages = [
        {"role": "assistant", "content": json.dumps(project_profile)},
        {"role": "user", "content": prompt}
    ]

    response = model.invoke(messages)
    # print("Synthetic Bill Response:", response.content)
    bill = extract_json_list(response.content)

    save_json_file(
        f"reports/{project_profile['name']}/synthetic_bill.json",
        bill
    )

    return bill
