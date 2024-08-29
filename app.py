import streamlit as st
from data.synthetic_data import generate_synthetic_data
from gpt.gpt_integration import generate_diagnosis
from guardrails.guardrails_integration import apply_guardrails
from red_team.red_team_integration import red_team_attack
from bias_detection.model_bias import detect_model_bias
from bias_detection.data_bias import detect_data_bias
from risk_assessment.ai_risk_questionnaire import ai_risk_questionnaire
from monitoring.prometheus_monitoring import (
    start_prometheus_server, process_request,
    record_bias_alert, record_guardrail_trigger,
    record_red_teaming_alert, record_data_privacy_alert,
    record_regulatory_compliance_check
)

st.title("Trustworthy AI Healthcare Diagnostics")

# Start Prometheus monitoring server
start_prometheus_server()

# Generate synthetic data
patient_data = generate_synthetic_data()
st.write("## Synthetic Patient Data")
st.dataframe(patient_data)

# Select a patient and generate diagnosis
selected_patient = st.selectbox("Select a patient", patient_data['Patient_ID'].tolist())
patient_info = patient_data[patient_data['Patient_ID'] == selected_patient].iloc[0]
st.write(f"Patient Info: {patient_info.to_dict()}")

if st.button("Generate Diagnosis"):
    process_request()  # Record the metrics for this request
    diagnosis = generate_diagnosis(patient_info.to_dict())
    st.write(f"Generated Diagnosis: {diagnosis}")

    # Apply guardrails
    guardrail_result = apply_guardrails(diagnosis)
    st.write(f"Guardrails Result: {guardrail_result}")

    if guardrail_result.get("guardrail_triggered"):
        record_guardrail_trigger()  # Increment guardrails triggered counter

if st.button("Simulate Red Teaming"):
    process_request()  # Record the metrics for this request
    adversarial_example = red_team_attack(patient_info.to_dict())
    st.write(f"Adversarial Example Data: {adversarial_example}")
    record_red_teaming_alert()  # Increment red teaming alert counter

if st.button("Check for Model Bias"):
    process_request()  # Record the metrics for this request
    y_true = patient_data['Lab_Results'].apply(lambda x: 1 if x > 70 else 0)
    metrics, dpd = detect_model_bias(patient_data, y_true, 'Gender')
    st.write(f"Model Bias Results: {metrics}")
    st.write(f"Demographic Parity Difference: {dpd}")

    if dpd > 0.1:  # Example threshold for bias alert
        record_bias_alert()  # Increment bias alert counter

if st.button("Check for Data Bias"):
    process_request()  # Record the metrics for this request
    bias_results = detect_data_bias(patient_data)
    st.write(f"Data Bias Detection Results: {bias_results}")

if st.button("Complete AI Risk Questionnaire"):
    process_request()  # Record the metrics for this request
    risk_results = ai_risk_questionnaire()
    st.write("## Risk Assessment Results")
    st.json(risk_results)

    # Record any alerts based on the AI Risk Questionnaire results
    if risk_results['Data Privacy']['Anonymization'] == 'No':
        record_data_privacy_alert()
    if risk_results['Regulatory Compliance']['Regulatory Adherence'] == 'No':
        record_regulatory_compliance_check()
