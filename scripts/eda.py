import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def missing_values_table(df):
    # Total missing values
    mis_val = df.isnull().sum()

    # Percentage of missing values
    mis_val_percent = 100 * df.isnull().sum() / len(df)

    # dtype of missing values
    mis_val_dtype = df.dtypes

    # Make a table with the results
    mis_val_table = pd.concat([mis_val, mis_val_percent, mis_val_dtype], axis=1)

    # Rename the columns
    mis_val_table_ren_columns = mis_val_table.rename(
    columns={0: 'Missing Values', 1: '% of Total Values', 2: 'Dtype'})



    # Sort the table by percentage of missing descending
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)

    # Print some summary information
    print("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
          "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")

    # Return the dataframe with missing information
    return mis_val_table_ren_columns


def remove_rows_with_missing_values(df: pd.DataFrame, columns: list) -> pd.DataFrame:

    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame")
    
    # Remove rows with missing values in any of the specified columns
    df_cleaned = df.dropna(subset=columns)
    
    return df_cleaned



def fill_missing_values(df: pd.DataFrame, columns: dict) -> pd.DataFrame:
 
    
    for column, strategy in columns.items():
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame")
        
        if strategy == 'mean':
            df[column].fillna(df[column].mean(), inplace=True)
        elif strategy == 'mode':
            df[column].fillna(df[column].mode()[0], inplace=True)
        else:
            raise ValueError(f"Invalid strategy '{strategy}' for column '{column}'. Use 'mean', 'mode'.")
    
    return df




def plot_histograms(df, numerical_columns):
    """
    Plots histograms for numerical columns.
    
    Parameters:
    df: DataFrame containing the data
    numerical_columns: List of numerical columns to plot histograms for
    """
    for column in numerical_columns:
        plt.figure(figsize=(8, 5))
        plt.hist(df[column], bins=30, color='lightblue', edgecolor='black')
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()

def plot_bar_charts(df, categorical_columns):
    """
    Plots bar charts for categorical columns.
    
    Parameters:
    df: DataFrame containing the data
    categorical_columns: List of categorical columns to plot bar charts for
    """
    for column in categorical_columns:
        plt.figure(figsize=(8, 5))
        df[column].value_counts().plot(kind='bar', color='lightblue', edgecolor='black')
        plt.title(f'Bar Chart of {column}')
        plt.xlabel(column)
        plt.ylabel('Count')
        plt.show()

def univariate_analysis(df, numerical_columns, categorical_columns):
    """
    Performs univariate analysis by plotting histograms for numerical columns
    and bar charts for categorical columns.
    
    Parameters:
    df: DataFrame containing the data
    numerical_columns: List of numerical columns
    categorical_columns: List of categorical columns
    """
    print("Plotting Histograms for Numerical Variables:")
    plot_histograms(df, numerical_columns)
    
    print("Plotting Bar Charts for Categorical Variables:")
    plot_bar_charts(df, categorical_columns)
