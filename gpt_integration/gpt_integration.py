import openai
import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from data.vectorize_data import VectorizeData

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

data_obj = VectorizeData()

prompt = """You are a question answering chatbot for a general physician application who analyzes user query {input} and OPTIONAL context: {context}. 
            user query may be about an existing patient as supported by the context or a general user query about certain symptoms.
            Based on this, you MUST provide answer to the query.
            REMEMBER THAT YOU ARE THE HEALTHCARE PROFESSIONAL."""

class GPTIntegration():
    def __init__(self) -> None:
        self.response = " "
        self.diagnosis = " "
    def generate_diagnosis(self,context, input):
        self.response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",  
            messages = [
                {'role':"system", 'content':prompt.format(context = context, input=input)}
            ],
            temperature = 1
        )
        self.diagnosis = self.response.choices[0].message.content.strip()
        return self.diagnosis

if __name__ == "__main__":
    # Example patient data for testing
    model = GPTIntegration()
    user_input = input(f"Enter your query")
    example_patient = data_obj.fetch_data(user_input)
    print(model.generate_diagnosis(example_patient, user_input))
