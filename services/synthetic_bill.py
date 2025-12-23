import json
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from services.utils import extract_json_list, save_json_file, load_excel_data

def generate_synthetic_bill(project_profile: dict):
    load_dotenv()
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        #repo_id="nvidia/AceMath-7B-Instruct",
        max_new_tokens=2048
    ) # type: ignore

    model = ChatHuggingFace(llm=llm)

    with open("prompts/synthetic_bill_prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
        
    excel_data = load_excel_data()
    messages = [
        {"role": "user", "content": json.dumps(project_profile)},
        {"role": "user", "content": f"\nAbove is the project profile of the current project and this is the excel data containing information about pricing of the services:\n{excel_data}"},
        {"role": "user", "content": f"Take reference from the pricing of above services from the excel sheet data and use only these prices for generating synthetic bill.\n{prompt}\nYou must never invent prices on your own. All prices must be taken only from the excel sheet data provided above.You may only reason over them. Use only realistic quantities based on the context of the project described in the project profile and the budget provided in project profile. Also take idea of the number of users for a particular service and it' size from the excel sheet data. Assign the usage_quantity to values ranging from 1 to 8. Keeping all these things in mind generate a realistic synthetic bill for the project described in the project profile."}
    ]

    response = model.invoke(messages)
    # print("Synthetic Bill Response:", response.content)
    bill = extract_json_list(response.content)

    save_json_file(
        f"reports/{project_profile['name']}/synthetic_bill.json",
        bill
    )

    return bill
