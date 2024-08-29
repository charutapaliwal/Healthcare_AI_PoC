import requests
from config import LLM_GUARD_API_KEY

def apply_guardrails(diagnosis):
    api_url = "https://api.llmguard.io/v1/guardrails"
    headers = {
        "Authorization": f"Bearer {LLM_GUARD_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": diagnosis,
        "rules": ["confidence_threshold", "bias_detection"]
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    # Example usage for testing
    example_diagnosis = "Possible early-stage lung cancer"
    result = apply_guardrails(example_diagnosis)
    print(result)
