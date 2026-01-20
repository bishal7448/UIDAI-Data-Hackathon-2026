import pandas as pd
from typing import List

def unique_pincode_count(df):
    return df.groupby('district_cleaned')['pincode'].nunique().reset_index(name='unique_pincode_count')

def get_pin_district_count(df):
    return (
        df.groupby('pincode')['district_cleaned']
          .nunique()
          .reset_index(name='district_count')
    )

def flag_problematic_enrolments(df, problem_pins_df):
    """
    Merge enrolment data with problematic pincodes to flag records.
    
    Parameters:
    enrolment_df (pd.DataFrame): The enrolment DataFrame to filter
    problem_pins_df (pd.DataFrame): DataFrame containing problematic pincodes
    
    Returns:
    pd.DataFrame: Filtered DataFrame containing only records with problematic pincodes
    """
    return df.merge(
        problem_pins_df[['pincode']],
        on='pincode',
        how='inner'
    )

def aggregate_enrolments_by_district_pincode(df, age_columns: List[str]):
    """
    Aggregate enrolment counts by district and pincode.
    
    Parameters:
    df (pd.DataFrame): The enrolment DataFrame to aggregate
    age_columns (list): List of age group columns to sum. Default is ['age_0_5', 'age_5_17', 'age_18_greater']
    
    Returns:
    pd.DataFrame: Aggregated DataFrame with sums for each district-pincode combination
    """
    return df.groupby(['district_cleaned', 'pincode'])[age_columns].sum().reset_index()

def get_dominant_district_per_pincode(df, age_columns: List[str]):
    """
    Identify the dominant district for each pincode based on total enrollment.
    
    For pincodes that appear in multiple districts, this function calculates the total
    enrollment and returns only the district with the highest enrollment for each pincode.
    
    Parameters:
    df (pd.DataFrame): DataFrame with district_cleaned, pincode, and age group columns
    age_columns (list): List of age group columns to sum for total enrollment
    
    Returns:
    pd.DataFrame: Filtered DataFrame with one row per pincode (the dominant district)
    """
    # Calculate total enrollment
    df = df.copy()
    df['total_enroll'] = df[age_columns].sum(axis=1)
    
    # Get index of maximum enrollment for each pincode
    idx = df.groupby('pincode')['total_enroll'].idxmax()
    
    # Filter to keep only dominant districts
    df_filtered = df.loc[idx].sort_values('pincode')
    
    return df_filtered

def flag_multi_district_pincodes(df, pincode_column='pincode', district_column='district_cleaned', flag_column='pin_multi_district_flag'):
    """
    Flag records where a pincode appears in multiple districts.
    
    This function adds a boolean column to identify pincodes that are associated 
    with more than one district, which can indicate data quality issues.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame
    pincode_column (str): Name of the pincode column. Default is 'pincode'
    district_column (str): Name of the district column. Default is 'district_cleaned'
    flag_column (str): Name of the flag column to create. Default is 'pin_multi_district_flag'
    
    Returns:
    pd.DataFrame: DataFrame with the added flag column
    """
    df[flag_column] = (
        df.groupby(pincode_column)[district_column]
          .transform('nunique') > 1
    )
    return df