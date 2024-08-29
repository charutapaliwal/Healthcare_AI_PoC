import pandas as pd
from faker import Faker

def generate_synthetic_data(num_records=100):
    fake = Faker()
    data = []

    for _ in range(num_records):
        record = {
            'Patient_ID': fake.uuid4(),
            'Age': fake.random_int(min=18, max=85),
            'Gender': fake.random_element(elements=('Male', 'Female')),
            'Symptoms': fake.sentence(nb_words=6),
            'Previous_Diagnosis': fake.random_element(elements=('None', 'Diabetes', 'Hypertension')),
            'Current_Medication': fake.word(),
            'Lab_Results': fake.random_int(min=10, max=100)
        }
        data.append(record)

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # For testing and standalone execution
    df = generate_synthetic_data()
    print(df.head())
