import os
import sys
import time
import json
from dotenv import load_dotenv
from services.project_report import generate_project_report
from services.project_profile import generate_project_profile
from services.synthetic_bill import generate_synthetic_bill
from services.cost_analysis import analyse_costs

REPORTS_DIR = "reports"

def stream_text(text, delay=0.01):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def list_project_folders():
    if not os.path.exists(REPORTS_DIR):
        return []
    return [
        f for f in os.listdir(REPORTS_DIR)
        if os.path.isdir(os.path.join(REPORTS_DIR, f))
    ]

def has_file(project, filename):
    return os.path.exists(
        os.path.join(REPORTS_DIR, project, filename)
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


def main():
    load_dotenv()
    while True:
        display_menu()
        choice = input("Select an option: ").strip()

        match choice:

            # Generate Project Profile
            case "1":
                try:
                    query = input("\nEnter project description: ").strip()
                    if not query:
                        print("\u274C Description cannot be empty.")
                        continue

                    generate_project_profile(query)
                    print("\u2705 Project profile generated.")
                except Exception as e:
                    print(f"\u274C Error generating project profile: {e}")

            # Run Complete Cost Analysis
            case "2":
                try:
                    projects = list_project_folders()
                    incomplete_projects = [
                        p for p in projects
                        if not has_file(p, "cost_analysis_recommendations.json")
                    ]

                    if not incomplete_projects:
                        print("\u2705 No incomplete projects found.")
                        continue

                    print("\nIncomplete Projects:")
                    for i, p in enumerate(incomplete_projects, start=1):
                        print(f"{i}. {p}")

                    try:
                        idx = int(input("Choose project: ")) - 1
                        project = incomplete_projects[idx]
                    except (ValueError, IndexError):
                        print("\u274C Invalid selection.")
                        continue

                    profile_path = os.path.join(
                        REPORTS_DIR, project, "project_profile.json"
                    )

                    if not os.path.exists(profile_path):
                        print("\u274C project_profile.json not found.")
                        continue

                    with open(profile_path, "r", encoding="utf-8") as f:
                        project_profile = json.load(f)


                    bill_path = os.path.join(
                        REPORTS_DIR, project, "synthetic_bill.json"
                    )

                    if os.path.exists(bill_path):
                        with open(bill_path, "r", encoding="utf-8") as f:
                            synthetic_bill = json.load(f)
                        print("\u2139 Using existing synthetic bill.")
                    else:
                        synthetic_bill = generate_synthetic_bill(project_profile)
                        print("\u2705 Synthetic bill generated.")

                    analyse_costs(project_profile, synthetic_bill)
                    print("\u2705 Cost analysis completed.")

                except Exception as e:
                    print(f"\u274C Error during cost analysis: {e}")

            # View Recommendations
            case "3":
                try:
                    projects = list_project_folders()
                    completed_projects = [
                        p for p in projects
                        if (
                            has_file(p, "project_profile.json") and
                            has_file(p, "synthetic_bill.json") and
                            has_file(p, "cost_analysis_recommendations.json")
                        )
                    ]

                    if not completed_projects:
                        print("\u274C No completed projects found.")
                        continue

                    print("\nCompleted Projects:")
                    for i, p in enumerate(completed_projects, start=1):
                        print(f"{i}. {p}")

                    try:
                        idx = int(input("Choose project: ")) - 1
                        project = completed_projects[idx]
                    except (ValueError, IndexError):
                        print("\u274C Invalid selection.")
                        continue

                    rec_path = os.path.join(
                        REPORTS_DIR,
                        project,
                        "cost_analysis_recommendations.json"
                    )

                    with open(rec_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    display_recommendations_human_readable(data)
                except Exception as e:
                    print(f"\u274C Error displaying recommendations: {e}")

            # Extract HTML Report
            case "4":
                try:
                    projects = list_project_folders()
                    completed_projects = [
                        p for p in projects if (
                            has_file(p, "cost_analysis_recommendations.json") and
                            has_file(p, "project_profile.json") and
                            has_file(p, "synthetic_bill.json")
                        )
                    ]
                    
                    if not completed_projects:
                        print("\u274C No completed projects found.")
                        continue
                    
                    print("\nCompleted Projects:")
                    for i, p in enumerate(completed_projects, start=1):
                        print(f"{i}. {p}")
                    
                    try:
                        idx = int(input("Choose project: ")) - 1
                        project = completed_projects[idx]
                    except (ValueError, IndexError):
                        print("\u274C Invalid selection.")
                        continue
                    
                    output_path = generate_project_report(project)
                    print(f"\u2705 HTML report generated at: {output_path}")
                except Exception as e:
                    print(f"\u274C Error extracting HTML report: {e}")
            # Exit
            case "0":
                print("\U0001F44B Exiting CLI.")
                break

            case _:
                print("\u274C Invalid option. Try again.")


if __name__ == "__main__":
    main()
