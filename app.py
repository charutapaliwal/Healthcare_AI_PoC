import streamlit as st
import openai
import os
from dotenv import load_dotenv
import pandas as pd
import tracemalloc
from gpt_integration.gpt_integration import GPTIntegration
import time
import warnings
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from red_team.red_team_integration import HealthcareRedTeam
from data.vectorize_data import VectorizeData
from risk_assessment.risk_questionnaire import risk_questionnaire


warnings.filterwarnings("ignore",category=Warning)

tracemalloc.start()
load_dotenv()
openai_api_key= os.getenv('OPENAI_API_KEY') 

#chroma setup
EMBEDDING_MODEL = 'text-embedding-3-small'
if os.getenv("OPENAI_API_KEY") is not None:
    openai_ef = OpenAIEmbeddingFunction(api_key=openai_api_key, model_name=EMBEDDING_MODEL)
else:
    print("OPENAI_API_KEY environment variable not found.")

client = chromadb.PersistentClient('./data/chroma')
pdata = client.get_collection("PatientData",embedding_function=openai_ef)

#initialize instances
data_obj=VectorizeData()
gpt_obj=GPTIntegration()
red_team_obj = HealthcareRedTeam()

context=[]
eval_metrics = ""

#helper functions
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

def query_processing(question_list):
    answers_list = []
    context_list =[]
    for question in question_list:
        context_list.append(data_obj.fetch_data(question))
        answers_list.append(gpt_obj.generate_diagnosis(context, question))
    return context_list, answers_list

# streamlit implementation
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
                context = data_obj.fetch_data(input_query)
                diagnosis = gpt_obj.generate_diagnosis(context,input_query)
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
                    eval_metrics = "ToxicityMetric"
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list, answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,eval_metrics)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Criminal / Illicit activities"):
                    objective = "Criminal / Illicit activities"
                    eval_metrics = "Criminal"
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list,answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list,context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,eval_metrics)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Bias Propagation"):
                    objective ="Bias Propagation"
                    eval_metrics = 'BiasMetric'
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list,answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,eval_metrics)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Privacy and Data Security"):
                    objective = "Privacy and Data Security"
                    eval_metrics="PrivacyDataSecurity"
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list,answers_list = query_processing(question_list)
                    with col2:
                        for question, answer,context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,eval_metrics)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Off Topic"):
                    objective = "Off Topic"
                    eval_metrics = "OffTopic"
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list,answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,eval_metrics)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Hallucinations"):
                    objective = "Hallucinations"
                    eval_metrics = 'HallucinationsMetric'
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list, answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,eval_metrics)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                # if st.button("Excessive Agency"):
                #     objective = "Excessive Agency"
                #     eval_metrics = "ExcessiveAgency"
                #     question_list = red_team_obj.red_teamer_prompt_list(objective)
                #     context_list, answers_list = query_processing(question_list)
                #     with col2:
                #         for question, answer, context in zip(question_list, answers_list, context_list):
                #             st.write("Q: ",question)
                #             st.write("A:",answer)
                #             st.write("Context:", context)
                #             score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,eval_metrics)
                #             st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")

        with sub_tab2:
            st.write("Bias Detection Component")
            # Implement bias detection functionalities

        with sub_tab3:
            st.write("Risk Questionnaire Component")
            risk_questionnaire()
            # Implement risk questionnaire functionalities
except Exception as e:
    print(f'Exception occured on streamlit: {str(e)}')
finally:
    tracemalloc.stop()
