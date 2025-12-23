import os
import json
from jinja2 import Environment, FileSystemLoader
from services.utils import read_json_file

REPORTS_DIR = os.path.join(os.getcwd(),"reports")

def generate_project_report(project_name):
    project_dir = os.path.join(REPORTS_DIR,project_name)
    profile_path = os.path.join(project_dir, "project_profile.json")
    bill_path = os.path.join(project_dir, "synthetic_bill.json")
    cost_path = os.path.join(project_dir, "cost_analysis_recommendations.json")
    
    project_profile = read_json_file(profile_path)
    synthetic_bill = read_json_file(bill_path)
    cost_analysis_recommendations = read_json_file(cost_path)
    
    if not project_profile or not synthetic_bill or not cost_analysis_recommendations:
        raise ValueError("Required JSON files are missing.\n")
    
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("project_report.html")
    
    html = template.render(
        project_profile=project_profile,
        synthetic_bill=synthetic_bill,
        cost=cost_analysis_recommendations
    )
    
    output_path = os.path.join(project_dir, "project_report.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    return output_path
    
    