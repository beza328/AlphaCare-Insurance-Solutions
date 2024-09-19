import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, ttest_ind
import os



def generate_insurance_data(num_records=1000):
    """Generate random insurance data with provinces and gender, ensuring significant differences."""
    np.random.seed(42)  # For reproducibility
    IsVATRegistered = ['True', 'False']
    Gender = ['Male', 'Female']
    LegalType = ['Individual', 'Private company', 'close Corporation', 'Partneship', 'Public company', 'Sole proprieter']

    # Define claim rates for each LegalType to create a significant difference
    claim_rates_LegalType = {
        'Individual': 0.9,  
        'Private company': 0.4,   
        'close Corporation': 0.1, 
        'Partneship': 0.1,
        'Public company': 0.1,
        'Sole proprieter': 0.1,



    }
    
    # Define claim rates for gender
    claim_rates_Gender = {
        'Male': 0.6,   # 60% claim rate for males
        'Female': 0.2,   # 20% claim rate for females
    }

    # Define claim rates for Vatregistration
    claim_rates_IsVATRegistered = {
        'True': 0.9,   # 60% claim rate for males
        'False': 0.1,   # 20% claim rate for females
    }
    
    # Generate province and gender
    LegalType_choices = np.random.choice(LegalType, num_records)
    Gender_choices = np.random.choice(Gender, num_records)
    IsVATRegistered_choices = np.random.choice(IsVATRegistered, num_records)
    
    # Generate claims based on gender
    claims = [1 if np.random.rand() < claim_rates_Gender[Gender] else 0 for Gender in Gender_choices]
    #claims = [1 if np.random.rand() < claim_rates_IsVATRegistered[IsVATRegistered] else 0 for Gender in IsVATRegistered_choices]
    data = {
        'LegalType': LegalType_choices,
        'Gender': Gender_choices,
       'IsVATRegistered': IsVATRegistered_choices,
        'Claimed': claims
    }
    
    return pd.DataFrame(data)


def save_data_to_csv(data, filename='insurance_data.csv'):
    
    """Save the generated data to a CSV file in the 'data' folder one level up."""
    # Create the path for the 'data' folder one level up
    data_folder = os.path.abspath(os.path.join(os.getcwd(), '..', 'data'))
    os.makedirs(data_folder, exist_ok=True)  # Create 'data' folder if it doesn't exist
    data.to_csv(os.path.join(data_folder, filename), index=False)


def ab_test(data):
    """Perform A/B testing using Chi-squared test for Legaltype."""
    contingency_table = pd.crosstab(data['LegalType'], data['Claimed'])
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    return chi2, p, contingency_table

def gender_analysis(data):
    """Perform t-test analysis based on gender."""
    male_claims = data[data['Gender'] == 'Male']['Claimed']
    female_claims = data[data['Gender'] == 'Female']['Claimed']
    
    t_stat, p_value = ttest_ind(male_claims, female_claims, equal_var=False)
    return t_stat, p_value  

def Vatregistered_analysis(data):
    """Perform t-test analysis based on vatregistered."""
    True_claims = data[data['IsVATRegistered'] == 'True']['Claimed']
    False_claims = data[data['IsVATRegistered'] == 'False']['Claimed']
    
    t_stat, p_value = ttest_ind(True_claims, False_claims, equal_var=False)
    return t_stat, p_value      


def save_insurance_data_to_csv(text_file_path, csv_file_name='insurance_text_data.csv'):
    """Load insurance data from a text file and save it as a CSV."""
    # Read the text file into a DataFrame
    df = pd.read_csv(text_file_path, delimiter='|')
    
    # Create the path for the 'data' folder one level up
    data_folder = os.path.abspath(os.path.join(os.getcwd(), '..', 'data'))
    os.makedirs(data_folder, exist_ok=True)  # Create 'data' folder if it doesn't exist

    # Define the full path for the CSV file
    csv_file_path = os.path.join(data_folder, csv_file_name)
    
    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    print(f"Data saved to {csv_file_path}")





