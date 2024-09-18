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


# Scatter ploting
def plot_scatter_car_insurance(df, x_col, y_col, hue_col='VehicleType'):
    """
    Creates a scatter plot to show relationships between TotalPremium and TotalClaims,
    color-coded by VehicleType (or another car insurance-specific variable).

    Parameters:
    df: DataFrame containing the data
    x_col: Column name for the x-axis (e.g., TotalPremium)
    y_col: Column name for the y-axis (e.g., TotalClaims)
    hue_col: Column name to color code the scatter points (default is VehicleType)
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_col, y=y_col, hue=hue_col, data=df, palette="coolwarm", alpha=0.7)
    plt.title(f'Scatter Plot of {x_col} vs {y_col} (colored by {hue_col})')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend(title=hue_col, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def plot_car_insurance_correlation_matrix(df):
    """
    Plots a correlation matrix heatmap for numerical car insurance-specific variables.
    
    Parameters:
    df: DataFrame containing the data
    """
    # List of car insurance-specific numerical columns
    numerical_columns = ['TotalPremium', 'TotalClaims', 'SumInsured', 'cubiccapacity', 'kilowatts', 'RegistrationYear']
    
    # Compute the correlation matrix
    corr_matrix = df[numerical_columns].corr()

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Matrix for Car Insurance Variables')
    plt.show()




def car_insurance_analysis(df):
    """
    Performs bivariate and multivariate analysis for car insurance-specific variables.
    """
    print('Analyzing relationship between TotalPremium and TotalClaims by VehicleType...')
    plot_scatter_car_insurance(df, 'TotalPremium', 'TotalClaims', 'VehicleType')
    
    print('Calculating correlation matrix for car insurance variables...')
    plot_car_insurance_correlation_matrix(df)


def analyze_geography_trends(df, group_by_col):
    """
    Analyzes trends in car insurance data by geography.

    Parameters:
    df: DataFrame containing the data
    group_by_col: Column name representing geographic areas (e.g., Province, PostalCode)
    
    Returns:
    summary_df: DataFrame containing summary statistics grouped by geographic region
    """
    # Group by the geographic column
    grouped = df.groupby(group_by_col).agg({
        'TotalPremium': ['mean', 'median', 'sum'],
        'TotalClaims': ['mean', 'median', 'sum'],
        'make': lambda x: x.value_counts().idxmax(),  # Most common car make
        'CoverType': lambda x: x.value_counts().idxmax()  # Most common cover type
    }).reset_index()
    
    # Rename columns for clarity
    grouped.columns = [group_by_col, 'AvgPremium', 'MedianPremium', 'TotalPremiumSum',
                       'AvgClaims', 'MedianClaims', 'TotalClaimsSum', 'MostCommonAutoMake', 'MostCommonCoverType']

    return grouped

def plot_premium_by_geography(summary_df, group_by_col):
    """
    Plots a bar chart showing average premium by geography.
    
    Parameters:
    summary_df: DataFrame with summary statistics for each geographic region
    group_by_col: Column representing the geographic areas (e.g., Province, PostalCode)
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(x=group_by_col, y='AvgPremium', data=summary_df, palette='coolwarm')
    plt.title(f'Average Premium by {group_by_col}')
    plt.xlabel(group_by_col)
    plt.ylabel('Average Premium')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def plot_cover_type_distribution(df, group_by_col):
    """
    Plots the distribution of CoverType across different geographic areas.
    
    Parameters:
    df: DataFrame containing the data
    group_by_col: Column representing geographic areas (e.g., Province, PostalCode)
    """
    cover_type_counts = df.groupby([group_by_col, 'CoverType']).size().unstack().fillna(0)
    cover_type_counts.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='coolwarm')
    
    plt.title(f'Distribution of Cover Types by {group_by_col}')
    plt.xlabel(group_by_col)
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Cover Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()


def calculate_claim_frequency(df):
    """
    Groups by PolicyID to calculate the number of claims per policy.
    
    Args:
    df (pd.DataFrame): DataFrame containing car insurance data.
    
    Returns:
    pd.DataFrame: A DataFrame with PolicyID and corresponding ClaimFrequency.
    """
    claim_frequency = df.groupby('PolicyID')['TotalClaims'].count().reset_index(name='ClaimFrequency')
    return claim_frequency

# Function to plot the distribution of claim frequency
def plot_claim_frequency_distribution(claim_frequency):
    """
    Plots a histogram to show the distribution of claim frequency.
    
    Args:
    claim_frequency (pd.DataFrame): DataFrame containing the claim frequency per policy.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(claim_frequency['ClaimFrequency'], bins=30, kde=True)
    plt.title('Distribution of Claim Frequency per Policy')
    plt.xlabel('Number of Claims per Policy')
    plt.ylabel('Frequency')
    plt.show()

# Function to print summary statistics for claim frequency
def claim_frequency_statistics(claim_frequency):
    """
    Prints the summary statistics of the claim frequency data.
    
    Args:
    claim_frequency (pd.DataFrame): DataFrame containing the claim frequency per policy.
    """
    stats = claim_frequency['ClaimFrequency'].describe()
    print(stats)
    return stats

# Main execution
def main(df):
    # Step 1: Calculate claim frequency
    claim_frequency = calculate_claim_frequency(df)
    
    # Step 2: Plot the distribution of claim frequency
    plot_claim_frequency_distribution(claim_frequency)
    
    # Step 3: Display summary statistics
    claim_frequency_statistics(claim_frequency)

# Assuming df is already defined as your car insurance DataFrame
    main(df)



def preprocess_and_group_by_month(df):
    """
    Converts the TransactionMonth to datetime, then groups by month to calculate total claims.
    
    Args:
    df (pd.DataFrame): DataFrame containing the car insurance data.
    
    Returns:
    pd.DataFrame: DataFrame with monthly total claims.
    """
    # Convert TransactionMonth to datetime
    df['TransactionMonth'] = pd.to_datetime(df['TransactionMonth'])
    
    # Group by TransactionMonth and sum the TotalClaims per month
    monthly_claims = df.groupby('TransactionMonth')['TotalClaims'].sum().reset_index()
    
    return monthly_claims

# Function to plot the trend of total claims over time
def plot_total_claims_trend(monthly_claims):
    """
    Plots a line chart to show the trend of total claims over time.
    
    Args:
    monthly_claims (pd.DataFrame): DataFrame containing the monthly total claims.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_claims['TransactionMonth'], monthly_claims['TotalClaims'], marker='o', linestyle='-', color='b')
    plt.title('Trend of Total Claims Over Time')
    plt.xlabel('Transaction Month')
    plt.ylabel('Total Claims')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Main function to perform the trend analysis on TotalClaims
def trend_analysis(df):
    """
    Performs trend analysis on the TotalClaims column over time.
    
    Args:
    df (pd.DataFrame): DataFrame containing car insurance data.
    """
    # Step 1: Preprocess and group data by month
    monthly_claims = preprocess_and_group_by_month(df)
    
    # Step 2: Plot the trend of total claims over time
    plot_total_claims_trend(monthly_claims)     

    trend_analysis(df)



 # Function to summarize total claims by demographic attribute
def summarize_total_claims_by_demographic(df, demographic_col):
    """
    Summarizes total claims by a given demographic attribute.
    
    Args:
    df (pd.DataFrame): DataFrame containing car insurance data
    demographic_col (str): The column representing a demographic attribute
    
    Returns:
    pd.DataFrame: Summary of total claims grouped by demographic attribute
    """
    # Group by demographic column and calculate total and average claims
    summary = df.groupby(demographic_col)['TotalClaims'].agg(['sum', 'mean', 'count']).reset_index()
    summary.columns = [demographic_col, 'TotalClaims', 'AverageClaims', 'CustomerCount']
    
    return summary
 # Function to plot total claims by demographic
def plot_total_claims_by_demographic(df, demographic_col):
    """
    Plots the total claims grouped by a demographic attribute.
    
    Args:
    df (pd.DataFrame): DataFrame containing car insurance data
    demographic_col (str): The column representing a demographic attribute
    """
    # Get summary of total claims
    demographic_summary = summarize_total_claims_by_demographic(df, demographic_col)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=demographic_col, y='TotalClaims', data=demographic_summary, palette='Blues_d')
    plt.title(f'Total Claims by {demographic_col}')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Total Claims')
    plt.xlabel(demographic_col)
    plt.tight_layout()
    plt.show()
    
    # Optional: boxplot to visualize claims distribution within each demographic group
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=demographic_col, y='TotalClaims', data=df, palette='coolwarm')
    plt.title(f'Claims Distribution by {demographic_col}')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Total Claims')
    plt.xlabel(demographic_col)
    plt.tight_layout()
    plt.show()

# Main function to analyze and plot claims by demographic attributes
def analyze_customer_demographics(df, demographic_cols):
    """
    Analyzes total claims by various demographic attributes.
    
    Args:
    df (pd.DataFrame): DataFrame containing car insurance data
    demographic_cols (list): List of demographic columns to analyze
    """
    for col in demographic_cols:
        print(f"Analyzing Total Claims by {col}")
        plot_total_claims_by_demographic(df, col)

    # Define the demographic columns you want to analyze
    demographic_columns = ['Gender', 'MaritalStatus', 'Province', 'Country']

    # Execute the analysis
    analyze_customer_demographics(df, demographic_columns)
         