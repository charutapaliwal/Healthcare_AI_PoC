import openai
import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from data.vectorize_data import VectorizeData

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

data_obj = VectorizeData()

def generate_diagnosis(context, input):
    prompt = f"""You are a question answering chatbot for a general physician application who analyzes user query {input} and OPTIONAL context: {context}. 
    user query may be about an existing patient as supported by the context or a general user query about certain symptoms.
    Based on this, you MUST provide answer to the query.
    REMEMBER THAT YOU ARE THE HEALTHCARE PROFESSIONAL. DO NOT ANSWER ANYTHING OUTSIDE A GENERAL PHYSICIAN'S SCOPE."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",  
        messages = [
            {'role':"system", 'content':prompt}
        ],
        temperature = 1
    )
    diagnosis = response.choices[0].message.content.strip()
    return diagnosis

if __name__ == "__main__":
    # Example patient data for testing
    user_input = input(f"Enter your query")
    example_patient = data_obj.fetch_data(user_input)
    print(generate_diagnosis(example_patient, user_input))
