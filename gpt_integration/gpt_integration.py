import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_diagnosis(patient_info):
    prompt = f"Patient data: {patient_info}. Based on this, what is the most likely diagnosis and what medication can you suggest?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",  
        messages = [
            {'role':"system", 'content':prompt}
        ],
        temperature = 0
    )
    diagnosis = response.choices[0].message.content.strip()
    return diagnosis

if __name__ == "__main__":
    # Example patient data for testing
    example_patient = {
        'Age': 45,
        'Gender': 'Male',
        'Symptoms': 'Fever, chills, cold ',
        'Previous_Diagnosis': 'None',
        'Current_Medication': 'None',
        'Blood_Pressure': '120/80',
        'BMI':23
    }
    print(generate_diagnosis(example_patient))
