import streamlit as st

def calculate_risk_score(answers):
    """
    Calculate the risk score based on the answers provided.
    'Yes' = 0 points (indicating no risk)
    'No' = 1 point (indicating a risk)
    """
    score = 0
    for answer in answers:
        if answer == 'No':  # Assuming "No" means there's a risk
            score += 1
    return score

def risk_category(score):
    """
    Categorize risk based on the score.
    """
    if score >= 15:
        return "High Risk"
    elif 8 <= score < 15:
        return "Medium Risk"
    else:
        return "Low Risk"

def remediation_strategy(risk_level):
    """
    Return remediation strategies based on the risk level.
    """
    if risk_level == "High Risk":
        return """
        **Remediation for High Risk**:
        1. Immediate audit of data privacy and security policies.
        2. Introduce additional encryption for data at rest and in transit.
        3. Increase bias auditing frequency and review datasets for fairness.
        4. Implement continuous monitoring of AI outputs for harmful decisions.
        5. Ensure real-time feedback loops for clinicians and integrate human-in-the-loop (HITL) mechanisms.
        """
    elif risk_level == "Medium Risk":
        return """
        **Remediation for Medium Risk**:
        1. Conduct regular reviews of data handling and retention policies.
        2. Strengthen access control to sensitive patient information.
        3. Perform periodic bias detection audits.
        4. Implement ongoing model accuracy validation and test on edge cases.
        5. Introduce explainability tools for clinicians to better understand AI decisions.
        """
    else:
        return "Your system is operating under Low Risk. Continue monitoring and best practices."

def risk_questionnaire():
    """
    Display the AI Risk Questionnaire and collect user responses.
    Include scoring and risk categorization functionality.
    """
    st.subheader("AI Risk Questionnaire for Chat with Physician Agent")

    # Data Privacy and Security Section
    st.write("### Data Privacy and Security")
    privacy_anonymization = st.radio("Is patient data anonymized before processing?", ('Yes', 'No'))
    data_encryption = st.radio("Is patient data securely encrypted during storage and transmission?", ('Yes', 'No'))
    access_control = st.radio("Is access to patient data restricted to authorized personnel only?", ('Yes', 'No'))
    data_retention = st.radio("Is there a clear data retention and deletion policy for patient records?", ('Yes', 'No'))
    data_logging = st.radio("Are all access and modifications to patient data logged and auditable?", ('Yes', 'No'))

    # Bias and Fairness Section
    st.write("### Bias and Fairness")
    bias_auditing = st.radio("Are training datasets audited for biases related to age, gender, or ethnicity?", ('Yes', 'No'))
    fairness_monitoring = st.radio("Is there ongoing monitoring to detect biases in AI-generated diagnoses?", ('Yes', 'No'))
    diversity_check = st.radio("Are datasets used for model training representative of diverse patient populations?", ('Yes', 'No'))

    # Transparency and Explainability Section
    st.write("### Transparency and Explainability")
    decision_explainability = st.radio("Can the AI system’s diagnostic decisions be fully explained to physicians?", ('Yes', 'No'))
    patient_understanding = st.radio("Is there a mechanism for patients to understand how their diagnosis was generated by the AI?", ('Yes', 'No'))
    clinician_feedback = st.radio("Can clinicians provide feedback on the AI's decisions for continuous improvement?", ('Yes', 'No'))
    model_opacity = st.radio("Does the system avoid using black-box models that are hard to interpret?", ('Yes', 'No'))

    # Model Accuracy and Performance Section
    st.write("### Model Accuracy and Performance")
    diagnosis_accuracy = st.radio("Is the accuracy of the AI model’s diagnostic recommendations continuously evaluated?", ('Yes', 'No'))
    real_time_monitoring = st.radio("Is there real-time monitoring of model performance in clinical environments?", ('Yes', 'No'))
    handling_edge_cases = st.radio("Are there safeguards in place for handling edge cases or ambiguous diagnoses?", ('Yes', 'No'))
    false_positive_rate = st.radio("Is the false positive rate of AI recommendations within acceptable thresholds?", ('Yes', 'No'))
    peer_review = st.radio("Has the AI system been peer-reviewed or validated by external medical experts?", ('Yes', 'No'))

    # Ethics and Patient Safety Section
    st.write("### Ethics and Patient Safety")
    patient_consent = st.radio("Is patient consent obtained before using their data in model training?", ('Yes', 'No'))
    ethical_implications = st.radio("Have the ethical implications of using AI in healthcare been fully considered?", ('Yes', 'No'))
    patient_safety = st.radio("Is there a mechanism to override AI-generated recommendations when patient safety is at risk?", ('Yes', 'No'))
    clinician_override = st.radio("Can physicians easily override AI-generated diagnoses when necessary?", ('Yes', 'No'))

    # Regulatory Compliance Section
    st.write("### Regulatory Compliance")
    hipaa_compliance = st.radio("Is the AI system fully compliant with healthcare regulations such as HIPAA?", ('Yes', 'No'))
    data_audits = st.radio("Are regular audits conducted to ensure compliance with data protection regulations?", ('Yes', 'No'))
    third_party_assessment = st.radio("Has the AI system undergone third-party security and compliance assessments?", ('Yes', 'No'))

    # Guardrails and Monitoring Section
    st.write("### Guardrails and Monitoring")
    continuous_monitoring = st.radio("Is there continuous monitoring of AI model outputs to detect harmful recommendations?", ('Yes', 'No'))
    alert_system = st.radio("Does the system generate alerts if the AI outputs a potentially harmful or incorrect recommendation?", ('Yes', 'No'))
    updates_and_patches = st.radio("Is there a process in place to update or patch the AI model when issues are found?", ('Yes', 'No'))

    # Collect all answers
    answers = [
        privacy_anonymization, data_encryption, access_control, data_retention, data_logging,
        bias_auditing, fairness_monitoring, diversity_check,
        decision_explainability, patient_understanding, clinician_feedback, model_opacity,
        diagnosis_accuracy, real_time_monitoring, handling_edge_cases, false_positive_rate, peer_review,
        patient_consent, ethical_implications, patient_safety, clinician_override,
        hipaa_compliance, data_audits, third_party_assessment,
        continuous_monitoring, alert_system, updates_and_patches
    ]

    # Calculate the risk score
    score = calculate_risk_score(answers)
    risk_level = risk_category(score)

    # Display the results
    st.write(f"### Your Risk Score: {score}")
    st.write(f"### Risk Level: {risk_level}")
    
    if risk_level in ["High Risk", "Medium Risk"]:
        st.write(remediation_strategy(risk_level))

    # Show success message after submission
    if st.button("Submit Questionnaire"):
        st.success(f"Risk Assessment Completed! You are in the {risk_level} category.")
