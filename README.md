# 🎯 AI-Powered Cloud Cost Optimizer

**Cloud Cost Optimizer** is an LLM-based tool that analyzes cloud infrastructure costs and generates actionable optimization recommendations based on a user’s project requirements, expected user load, and monthly budget. It helps teams understand cost drivers, identify inefficiencies, and make budget-aware architectural decisions early in the design phase.

---

## 🚀 Features

- 📄 Takes user text input through CLI menu.
- 🧠 Uses LLM to generate project profile in JSON format.
- ✨ Generates synthetic bill.
- 📄 Takes in synthetically generated cloud pricing excel sheet and then based on this it generated accurate recommendations and cost analysis using LLM.
- ✅ Also generates HTML report.

---

## 🛠️ Tech Stack

| Technology           | Tools Used                                |
|----------------|--------------------------------------------------|
|Language used | Python 3.12 |
| Frontend       | CLI Menu                               |
| LLM used       | meta-llama/Meta-Llama-3-8B-Instruct Hugging face inference  |
| Extras   | LangChain   |
|Environment |.env for Huggingface API Key|

---

## 📂 Folder Structure

```bash
AI-Powered-Cloud-Cost-Optimizer/
├── main.py                          
├── services/                        
│   ├── __init__.py
│   ├── cost_analysis.py             
│   ├── project_profile.py           
│   ├── synthetic_bill.py            
│   ├── project_report.py            
│   └── utils.py                     
├── templates/
│   └── project_report.html          
├── prompts/
│   ├── cost_analysis_prompt.txt     
│   ├── project_profile_prompt.txt   
│   └── synthetic_bill_prompt.txt    
├── reports/                     # output is generated in this directory
│   └── .gitkeep                     
├── artifacts/                   # sample input and output    
├── .python-version                  
├── cloud_pricing_reference_synthetic.xlsx  
├── pyproject.toml                   
├── uv.lock                          
├── README.md                        
├── .gitignore                       
└── .env                             
```
---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/Aditya26Das/AI-Powered-Cloud-Cost-Optimization.git
cd AI-Powered-Cloud-Cost-Optimization
```

### 2. Set up the Environment

**For Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**For macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Sync the Environment
```bash
uv sync
```

### 4. Configure Environment Variables
Generate a Hugging Face access token and add it to a `.env` file in the root directory:
```bash
HF_TOKEN=your_token_here
```

### 5. Run the Application
```bash
uv run main.py
```

## Using the CLI Example

### Menu Options
```
========================================
   Cost Analysis CLI
========================================
1. Generate Project Profile
2. Run Complete Cost Analysis
3. View Recommendations
4. Generate & View HTML Report
0. Exit
========================================
```

### Step 1: Generate Project Profile

Select option `1` and enter your project description:
```
Select an option: 1

Enter project description: An e-commerce platform with 10,000 daily active users, 
serving product catalogs, handling transactions, and using EC2, RDS, S3, and CloudFront.
```

### Step 2: Run Complete Cost Analysis

Select option `2` and choose your project:
```
Select an option: 2

Incomplete Projects:
1. E-commerce-application

Choose project: 1
```

### Step 3: View Recommendations

Select option `3` and choose your project:
```
Select an option: 3

Completed Projects:
1. E-commerce-application

Choose project: 1
```

### Step 4: Generate & View HTML Report

Select option `4` and choose your project:
```
Select an option: 4

Completed Projects:
1. E-commerce-application

Choose project: 1
```

The report will open in your browser. Press **Enter** to stop the server.

### Step 5: Exit

Select option `0` to exit the CLI.

