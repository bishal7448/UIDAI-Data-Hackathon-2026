import re
import pandas as pd

def clean_name(df: pd.DataFrame, column_name: str, name_mapping: dict, cleaned_column_name: str) -> pd.DataFrame:
    """
    Clean and standardize names in a specified column of a DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column_name (str): The name of the column to be cleaned.
    name_mapping (dict): A dictionary mapping incorrect names to correct names.
    cleaned_column_name (str): The name of the new column to store cleaned names.

    Returns:
    pd.DataFrame: DataFrame with an additional column for cleaned names.
    """
    def clean_single_name(name):
        if pd.isna(name):
            return name
        name = str(name).lower()                     # convert to lowercase
        name = re.sub(r'[^a-z0-9\s]', ' ', name)   # remove symbols like &, -, etc. (Regex pattern: [^a-z\s])
        name = re.sub(r'\s+', ' ', name).strip()  # remove extra spaces (Regex pattern: \s+)
        if re.fullmatch(r'\d+', name): # if name is purely numeric
            return None
        return name

    cleaned = df[column_name].apply(clean_single_name)
    df[cleaned_column_name] = cleaned.map(name_mapping).fillna(df[column_name])
    return df

def drop_columns(df, columns_to_drop: list):
    """
    Drop specified columns from a DataFrame.
    
    Args:
        df: DataFrame to clean
        columns_to_drop: List of column names to drop
    
    Returns:
        DataFrame with specified columns removed
    """
    return df.drop(columns=columns_to_drop, axis=1)
