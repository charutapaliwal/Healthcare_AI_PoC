import openai
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_diagnosis(context, input):
    prompt = f"Analyze user query {input} and Medical Data: {context}. Based on this, provide detailed answer to the query."
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
    user_input = input(f"Enter your query")
    print(generate_diagnosis(example_patient, user_input))
