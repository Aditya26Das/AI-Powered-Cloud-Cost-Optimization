import os
import sys
import time
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

def stream_text(text, delay=0.01):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
def list_project_folders(reports_dir):
    if not os.path.exists(reports_dir):
        return []
    return [
        f for f in os.listdir(reports_dir)
        if os.path.isdir(os.path.join(reports_dir, f))
    ]
    
def has_file(reports_dir, project, filename):
    return os.path.exists(
        os.path.join(reports_dir, project, filename)
    )
    
def display_menu():
    print("\n===== Cloud Cost CLI =====")
    print("1. Enter new project description")
    print("2. Run complete cost analysis")
    print("3. View recommendations")
    print("4. Extract HTML Report")
    print("0. Exit")
    
def display_recommendations_human_readable(data):
    clear_screen()
    stream_text("\n===== Cost Analysis Summary =====\n", 0.005)

    analysis = data.get("analysis", {})
    recommendations = data.get("recommendations", [])

    if analysis:
        stream_text("\U0001F4CA Overall Analysis", 0.01)
        stream_text(f"- Total Monthly Cost: ₹{analysis.get('total_monthly_cost')}", 0.01)
        stream_text(f"- Budget: ₹{analysis.get('budget')}", 0.01)
        stream_text(f"- Over Budget: {analysis.get('is_over_budget')}", 0.01)
        stream_text("\nPress Enter to continue...")
        input()

    if not recommendations:
        stream_text("No recommendations available.")
        return

    index = 0
    total = len(recommendations)

    while True:
        clear_screen()
        rec = recommendations[index]

        stream_text("\U0001F4A1 Recommendations\n", 0.005)
        stream_text(f"{index + 1}/{total}. {rec.get('title')}", 0.01)
        stream_text(f"   Service        : {rec.get('service')}", 0.01)
        stream_text(f"   Current Cost   : ₹{rec.get('current_cost')}", 0.01)
        stream_text(f"   Potential Save : ₹{rec.get('potential_savings')}", 0.01)
        stream_text(f"   Suggestion     : {rec.get('description')}", 0.01)
        stream_text("-" * 50, 0.003)

        stream_text(
            "Controls: [n] Next | [p] Previous | [q] Quit",
            0.005
        )

        choice = input("Your choice: ").strip().lower()

        if choice in ("n", ""):
            if index < total - 1:
                index += 1
            else:
                stream_text("You are at the last recommendation.", 0.005)
                time.sleep(1)

        elif choice == "p":
            if index > 0:
                index -= 1
            else:
                stream_text("You are at the first recommendation.", 0.005)
                time.sleep(1)

        elif choice == "q":
            stream_text("\nExited recommendations view.")
            break

        else:
            stream_text("Invalid input. Use n / p / q.", 0.005)
            time.sleep(1)
