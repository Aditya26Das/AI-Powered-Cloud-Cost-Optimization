import os
import json
from dotenv import load_dotenv
from services.project_report import generate_project_report
from services.project_profile import generate_project_profile
from services.synthetic_bill import generate_synthetic_bill
from services.cost_analysis import analyse_costs
from services.utils import list_project_folders, has_file, display_menu, display_recommendations_human_readable

REPORTS_DIR = "reports"

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
                    projects = list_project_folders(REPORTS_DIR)
                    incomplete_projects = [
                        p for p in projects
                        if not has_file(REPORTS_DIR, p, "cost_analysis_recommendations.json")
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
                    projects = list_project_folders(REPORTS_DIR)
                    completed_projects = [
                        p for p in projects
                        if (
                            has_file(REPORTS_DIR, p, "project_profile.json") and
                            has_file(REPORTS_DIR, p, "synthetic_bill.json") and
                            has_file(REPORTS_DIR, p, "cost_analysis_recommendations.json")
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
                    projects = list_project_folders(REPORTS_DIR)
                    completed_projects = [
                        p for p in projects if (
                            has_file(REPORTS_DIR, p, "cost_analysis_recommendations.json") and
                            has_file(REPORTS_DIR, p, "project_profile.json") and
                            has_file(REPORTS_DIR, p, "synthetic_bill.json")
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
