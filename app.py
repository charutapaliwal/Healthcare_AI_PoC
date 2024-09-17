import streamlit as st
import openai
import os
from dotenv import load_dotenv
import pandas as pd
import tracemalloc
from gpt_integration.gpt_integration import generate_diagnosis
import time
import warnings
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from red_team.red_team_integration import red_teamer_llm, evaluate, red_teamer_prompt_list

warnings.filterwarnings("ignore",category=Warning)

tracemalloc.start()

load_dotenv()
openai_api_key= os.getenv('OPENAI_API_KEY') 

EMBEDDING_MODEL = 'text-embedding-3-small'
if os.getenv("OPENAI_API_KEY") is not None:
    openai_ef = OpenAIEmbeddingFunction(api_key=openai_api_key, model_name=EMBEDDING_MODEL)
else:
    print("OPENAI_API_KEY environment variable not found.")

client = chromadb.PersistentClient('./data/chroma')
pdata = client.get_collection("PatientData",embedding_function=openai_ef)

context=[]

def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

def fetch_data(input_query):
    #semantic search with chroma
    search_result=pdata.query(
        query_texts=input_query,
        n_results=2,
        include=['documents']
    )
    print(search_result)
    # Extract and prepare context from search result
    context = []
    for obj in search_result["documents"]:
        context.append(obj)
    print(context)
    return context

def query_processing(question_list):
    answers_list = []
    for question in question_list:
        context = fetch_data(question)
        answer = generate_diagnosis(context, question)
        answers_list.append(answer)
    return answers_list

try:
    # Streamlit UI
    st.set_page_config(layout = 'wide', page_title='Trustaworthy AI Healthcare Diagnostics')

    # Main Tabs: Chat and TWAI Components
    tab1, tab2 = st.tabs(["Chat", "TWAI Components"])

    with tab1:
        st.header("Chat with Physician Agent")

        input_query = st.chat_input("Enter your query")
        if input_query:
            with st.spinner("Processing query ..."):
                context = fetch_data(input_query)
                diagnosis = generate_diagnosis(context,input_query)
                st.chat_message('user').write_stream(stream_data(diagnosis))
        if st.button("Activate Guardrails"):
            pass

    with tab2:
        st.header("TWAI Components")

        # Sub-tabs within TWAI Components
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Red Teaming", "Bias Detection", "Risk Questionnaire"])

        with sub_tab1:
            data = '''
                    The harms generative AI systems create are, in many cases, different from other forms of AI in both scope and scale. 
                    Red teaming generative AI is specifically designed to generate harmful content that has no clear analogue in traditional software systems — 
                    from generating demeaning stereotypes and graphic images to flat out lying. 
                    For this application, we have demonstrated red teaming efforts with below degradation objectives (some objectives were derived from incidents of AI incident databse and OWASP top 10 LLM applications):
            '''
            st.write(data)
            # Implement red teaming functionalities
            col1, col2 = st.columns([1,3])
            with col1:
                if st.button("Toxicity / Offensive content"):
                    objective = "Toxicity / Offensive content"
                    question_list = red_teamer_prompt_list(objective)
                    answers_list = query_processing(question_list)
                    with col2:
                        for question, answer in zip(question_list, answers_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Evaluation:",evaluate(question,answer,objective))
                if st.button("Criminal / Illicit activities"):
                    objective = "Criminal / Illicit activities"
                    question_list = red_teamer_prompt_list(objective)
                    answers_list = query_processing(question_list)
                    with col2:
                        for question, answer in zip(question_list, answers_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Evaluation:",evaluate(question,answer,objective))
                if st.button("Bias Propagation"):
                    objective ="Bias Propagation"
                    question_list = red_teamer_prompt_list(objective)
                    answers_list = query_processing(question_list)
                    with col2:
                        for question, answer in zip(question_list, answers_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Evaluation:",evaluate(question,answer,objective))
                if st.button("Privacy and Data Security"):
                    objective = "Privacy and Data Security"
                    question_list = red_teamer_prompt_list(objective)
                    answers_list = query_processing(question_list)
                    with col2:
                        for question, answer in zip(question_list, answers_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Evaluation:",evaluate(question,answer,objective))
                if st.button("Off Topic"):
                    objective = "Off Topic"
                    question_list = red_teamer_prompt_list(objective)
                    answers_list = query_processing(question_list)
                    with col2:
                        for question, answer in zip(question_list, answers_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Evaluation:",evaluate(question,answer,objective))
                if st.button("Hallucinations"):
                    objective = "Hallucinations"
                    question_list = red_teamer_llm("Hallucinations")
                    answers_list = query_processing(question_list)
                    with col2:
                        for question, answer in zip(question_list, answers_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Evaluation:",evaluate(question,answer,objective))
                if st.button("Excessive Agency"):
                    objective = "Excessive Agency"
                    question_list = red_teamer_prompt_list(objective)
                    answers_list = query_processing(question_list)
                    with col2:
                        for question, answer in zip(question_list, answers_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Evaluation:",evaluate(question,answer,objective))
        with sub_tab2:
            st.write("Bias Detection Component")
            # Implement bias detection functionalities

        with sub_tab3:
            st.write("Risk Questionnaire Component")
            # Implement risk questionnaire functionalities
except Exception as e:
    print(f'Exception occured on streamlit: {str(e)}')
finally:
    tracemalloc.stop()
