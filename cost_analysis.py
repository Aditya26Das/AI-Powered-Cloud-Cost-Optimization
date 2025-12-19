import json
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from utils import extract_json, save_json_file

def analyse_costs(project_profile: dict, synthetic_bill: list):
    load_dotenv()
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        max_new_tokens=2048,
        timeout=300
    ) # type: ignore

    model = ChatHuggingFace(llm=llm)

    with open("cost_analysis_prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    messages = [
        {
            "role": "system",
            "content": "You are a cloud cost optimization assistant. Return ONLY valid JSON."
        },
        {
            "role": "user",
            "content": f"Project profile:\n{json.dumps(project_profile, indent=2)}"
        },
        {
            "role": "user",
            "content": f"Current cloud bill:\n{json.dumps(synthetic_bill, indent=2)}"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = model.invoke(messages)
    print("Cost Analysis Response:", response.content)
    analysis = extract_json(response.content)

    save_json_file(
        f"reports/{project_profile['name']}/cost_analysis_recommendations.json",
        analysis
    )

    return analysis
