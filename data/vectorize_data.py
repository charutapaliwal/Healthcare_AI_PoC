import chromadb
import pandas as pd
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import openai
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = 'text-embedding-3-small'
if os.getenv("OPENAI_API_KEY") is not None:
    openai_ef = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"), model_name=EMBEDDING_MODEL)
else:
    print("OPENAI_API_KEY environment variable not found.")

chroma_client = chromadb.PersistentClient()
collection = chroma_client.create_collection(name="PatientData", embedding_function=openai_ef)

try:

    df = pd.read_csv('Synthetic_Data.csv')
    df.set_index('Patient_ID', inplace=True)
    columns=len(df.columns)

    documents = []
    metadatas = []
    ids =[]
    doc_data=[]
    id=1
    for index, row in df.iterrows():
        doc_data.append(index)
        for i in range(columns):
            doc_data.append(str(row[i]))
        documents.append(' '.join(doc_data))
        metadatas.append({'item_id':index})
        ids.append(str(id))
        id+=1
        doc_data=[]

    collection.upsert(
        documents= documents,
        ids = ids
    )
    print("loaded data in chromadb")
except Exception as e:
    print(f"Error while loading chromadb : {str(e)}")


