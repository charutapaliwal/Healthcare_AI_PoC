import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_diagnosis(patient_info):
    prompt = f"Patient data: {patient_info}. Based on this, what is the most likely diagnosis?"
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-4 model
        prompt=prompt,
        max_tokens=150
    )
    diagnosis = response.choices[0].text.strip()
    return diagnosis

if __name__ == "__main__":
    # Example patient data for testing
    example_patient = {
        'Age': 45,
        'Gender': 'Male',
        'Symptoms': 'persistent cough, shortness of breath',
        'Previous_Diagnosis': 'None',
        'Current_Medication': 'None',
        'Lab_Results': 78
    }
    print(generate_diagnosis(example_patient))
