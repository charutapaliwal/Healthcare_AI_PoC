from art.attacks.evasion import FastGradientMethod
from art.estimators.classification import SklearnClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def preprocess_patient_data(patient_info):
    # Simple example: convert categorical data to numerical and normalize
    age = patient_info['Age']
    gender = 1 if patient_info['Gender'] == 'Male' else 0
    symptoms_length = len(patient_info['Symptoms'].split())
    previous_diagnosis = 1 if patient_info['Previous_Diagnosis'] != 'None' else 0
    current_medication = len(patient_info['Current_Medication'])
    lab_results = patient_info['Lab_Results']
    
    return np.array([[age, gender, symptoms_length, previous_diagnosis, current_medication, lab_results]])

# Setup the model and classifier
model = RandomForestClassifier()
# Assume the model has been trained beforehand (for demonstration purposes, we use a simple example)
# Normally, you would load a pre-trained model or train it on your data

classifier = SklearnClassifier(model=model)

# Function to simulate a red team attack
def red_team_attack(patient_info):
    # Preprocess patient info
    data = preprocess_patient_data(patient_info)

    # Create adversarial example using the Fast Gradient Method
    attack = FastGradientMethod(estimator=classifier, eps=0.1)
    adversarial_data = attack.generate(x=data)
    return adversarial_data

if __name__ == "__main__":
    # Example patient data for testing
    example_patient = {
        'Age': 45,
        'Gender': 'Male',
        'Symptoms': 'persistent cough, shortness of breath',
        'Previous_Diagnosis': 'None',
        'Current_Medication': 'None',
        'Lab_Results': 78
    }
    adversarial_example = red_team_attack(example_patient)
    print(f"Adversarial Example: {adversarial_example}")
