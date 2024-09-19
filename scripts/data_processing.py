import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

def load_and_clean_data(filepath):
    data = pd.read_csv(filepath)
    # Removing duplicates
    data = data.drop_duplicates(keep="first")
    return data


# Function to group categorical columns (object and bool types)
def group_categorical_columns(data):
    categorical_columns = data.select_dtypes(include=['object', 'bool']).columns
    return data[categorical_columns]


# Function to perform encoding on categorical data
def encode_categorical_data(data, encoding_type='one-hot'):
    # Get categorical columns
    categorical_data = group_categorical_columns(data)

    if encoding_type == 'one-hot':
        # One-Hot Encoding using pandas
        encoded_data = pd.get_dummies(categorical_data, drop_first=True)
    elif encoding_type == 'label':
        # Label Encoding
        encoded_data = categorical_data.apply(LabelEncoder().fit_transform)
    else:
        raise ValueError("Unknown encoding type. Choose 'one-hot' or 'label'.")

    return encoded_data

 #Function to prepare the entire dataset by encoding categorical columns
def prepare_data(data):
    # Step 1: Encode categorical data
    encoded_data = encode_categorical_data(data, encoding_type='one-hot')

    # Step 2: Drop the original categorical columns
    data = data.drop(group_categorical_columns(data), axis=1)

    # Step 3: Concatenate encoded data with the remaining columns
    data = pd.concat([data, encoded_data], axis=1)
    
    return data

# Function to group numerical columns (int64 and float64 types)
def group_numerical_columns(data):
    numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
    return data[numerical_columns]

# Function to scale the numerical columns
def scale_numerical_data(data, scaling_type='standard'):
    # Get numerical columns
    numerical_data = group_numerical_columns(data)
    
    if scaling_type == 'standard':
        # Standardize the data (mean = 0, standard deviation = 1)
        scaler = StandardScaler()
    elif scaling_type == 'minmax':
        # Min-Max Scaling (range between 0 and 1)
        scaler = MinMaxScaler()
    else:
        raise ValueError("Unknown scaling type. Choose 'standard' or 'minmax'.")
    
    # Apply scaling
    scaled_data = pd.DataFrame(scaler.fit_transform(numerical_data), columns=numerical_data.columns)
    
    return scaled_data

# Function to prepare the dataset with scaled numerical columns
def prepare_scaled_data(data, scaling_type='standard'):
    # Step 1: Scale numerical data
    scaled_numerical_data = scale_numerical_data(data, scaling_type=scaling_type)
    
    # Step 2: Drop the original numerical columns
    data = data.drop(group_numerical_columns(data), axis=1)
    
    # Step 3: Concatenate scaled data with the remaining columns
    data = pd.concat([data, scaled_numerical_data], axis=1)
    
    return data