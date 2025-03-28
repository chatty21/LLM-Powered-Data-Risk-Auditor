import requests

def analyze_risks_with_llm(summary_text):
    prompt = f"""
You are a data quality expert. Analyze this dataset summary and identify risks such as:
- PII (personally identifiable info)
- Data leakage (e.g. derived columns)
- Bias (gender, age, location)
- Class imbalance
- Missing data
- High-cardinality columns

Suggest fixes for each issue.

Dataset Summary:
{summary_text}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return result["response"]