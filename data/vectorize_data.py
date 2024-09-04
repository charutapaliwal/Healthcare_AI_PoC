import weaviate
from weaviate.classes.init import Auth, AdditionalConfig, Timeout
import weaviate.classes as wvc
import os
from dotenv import load_dotenv
import pandas as pd
import json
import requests

load_dotenv()
weaviate_api_key = os.getenv('WEAVIATE_API_KEY')
weaviate_url=os.getenv('WEAVIATE_CLUSTER_URL')
openai_api_key= os.getenv('OPENAI_API_KEY')

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
    headers={'X-OpenAI-Api-Key':openai_api_key},
    skip_init_checks=True,
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    )
)
print(client.is_ready())

try:
    #define data collection (similar to createing a table in RDBMS)
    PatientData = client.collections.create(
        name='PatientData',
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        generative_config=wvc.config.Configure.Generative.openai()
    )

    #Add objects to weaviate
    df = pd.read_csv('Synthetic_Data.csv')
    df.set_index('Patient_ID', inplace=True)

    data_obj = []
    for index, row in df.iterrows():
        data_obj.append({
            'Patient_ID': index,
            'Name' : row['Name'],
            'Age': row['Age'],
            'Gender': row['Gender'],
            'Address':row['Address'],
            'SSN': row['SSN'],
            'ICD10_Code': row['ICD10_Code'],
            'Code_Description':row['Code_Description'],
            'Previous_Symptoms': row['Previous_Symptoms'],
            'Previous_Diagnosis': row['Previous_Diagnosis'],
            'Current_Medication': row['Current_Medication'],
            'Blood_Pressure': row['Blood_Pressure'],
            'Body_Mass_Index': row['Body_Mass_Index']
        })
    print("no pass")
    #add objects to target collection PatientData
    pdata=client.collections.get('PatientData')
    pdata.data.insert_many(data_obj)
    print("successfully loaded data into weaviate")
except Exception as e:
    print(f"Error while loading weaviate : {str(e)}")
finally:
    client.close()

