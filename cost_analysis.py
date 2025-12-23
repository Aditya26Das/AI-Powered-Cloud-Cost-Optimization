import json
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from utils import extract_json, save_json_file, load_excel_data


def analyse_costs(project_profile: dict, synthetic_bill: list):
    load_dotenv()

    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        max_new_tokens=2048,
        timeout=300
    )  # type: ignore

    model = ChatHuggingFace(llm=llm)

    with open("cost_analysis_prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    total_monthly_cost = sum(
        item["cost_inr"] * item["usage_quantity"]
        for item in synthetic_bill
    )

    budget = project_profile["budget_inr_per_month"]
    budget_variance = total_monthly_cost - budget

    service_costs = {}
    for item in synthetic_bill:
        service = item["service"]
        cost = item["cost_inr"] * item["usage_quantity"]
        service_costs[service] = service_costs.get(service, 0) + cost

    excel_data = load_excel_data()

    context = {
        "project_profile": project_profile,
        "synthetic_bill": synthetic_bill,
        "summary": {
            "total_monthly_cost_inr": total_monthly_cost,
            "budget_inr": budget,
            "budget_variance_inr": budget_variance,
            "service_wise_costs": service_costs,
        },
        "pricing_reference": excel_data,
    }

    messages = [
        {
            "role": "system",
            "content": "You are a cloud cost optimization assistant. Return ONLY valid JSON."
        },
        {
            "role": "user",
            "content": (
                "Here is the full cost analysis context:\n\n"
                f"{json.dumps(context, indent=2)}\n\n"
                "Based on this, provide cost optimization recommendations."
            )
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
