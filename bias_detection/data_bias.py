from aequitas.group import Group
from aequitas.preprocessing import preprocess_input_df
import pandas as pd

def detect_data_bias(data, protected_columns=['Gender']):
    """
    Detects bias in the input data using Aequitas.

    Parameters:
    data (pd.DataFrame): Input data to be analyzed
    protected_columns (list): List of protected attribute columns

    Returns:
    pd.DataFrame: Bias detection results
    """
    # Preprocess input data for Aequitas
    aq_data, group_map = preprocess_input_df(data, key_columns=['Patient_ID'], protected_columns=protected_columns)

    # Create an Aequitas Group object
    g = Group()
    gdf = g.get_crosstabs(aq_data)

    return gdf

if __name__ == "__main__":
    # Example usage for testing (replace with actual data)
    data = {
        'Patient_ID': [1, 2, 3, 4],
        'Gender': ['Male', 'Female', 'Female', 'Male'],
        'Age': [34, 45, 23, 45],
        'Lab_Results': [78, 65, 88, 90]
    }
    df = pd.DataFrame(data)

    bias_results = detect_data_bias(df)
    print("Data Bias Detection Results:", bias_results)
