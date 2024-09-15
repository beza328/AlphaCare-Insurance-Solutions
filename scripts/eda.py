import pandas as pd

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
<<<<<<< Updated upstream
=======


def remove_rows_with_missing_values(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Remove rows from the DataFrame where any of the specified columns have missing values.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    columns (list): A list of column names to check for missing values.

    Returns:
    pd.DataFrame: A DataFrame with rows removed where any of the specified columns have missing values.
    """
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
            raise ValueError(f"Invalid strategy '{strategy}' for column '{column}'. Use 'mean', 'median', 'mode'.")
    
    return df


>>>>>>> Stashed changes
