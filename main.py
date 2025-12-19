import os
import json
from dotenv import load_dotenv
from project_profile import generate_project_profile
from synthetic_bill import generate_synthetic_bill
from cost_analysis import analyse_costs


REPORTS_DIR = "reports"


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
    print("0. Exit")


def display_recommendations_human_readable(data):
    print("\n===== Cost Analysis Summary =====\n")

    analysis = data.get("analysis", {})
    recommendations = data.get("recommendations", [])

    if analysis:
        print("\U0001F4CA Overall Analysis")
        print(f"- Total Monthly Cost: ₹{analysis.get('total_monthly_cost')}")
        print(f"- Budget: ₹{analysis.get('budget')}")
        print(f"- Over Budget: {analysis.get('is_over_budget')}")
        print()

    if not recommendations:
        print("No recommendations available.")
        return

    print("\U0001F4A1 Recommendations:\n")
    for idx, rec in enumerate(recommendations, start=1):
        print(f"{idx}. {rec.get('title')}")
        print(f"   Service        : {rec.get('service')}")
        print(f"   Current Cost   : ₹{rec.get('current_cost')}")
        print(f"   Potential Save : ₹{rec.get('potential_savings')}")
        print(f"   Suggestion     : {rec.get('description')}")
        print("-" * 50)


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

            # Exit
            case "0":
                print("\U0001F44B Exiting CLI.")
                break

            case _:
                print("\u274C Invalid option. Try again.")


if __name__ == "__main__":
    main()
