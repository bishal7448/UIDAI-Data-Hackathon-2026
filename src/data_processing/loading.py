import os
import pandas as pd
from typing import List

def load_data(file_paths : List[str]) -> pd.DataFrame:
    dfs = [] # List to hold individual DataFrames
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
        
        print("*"*50)
        
        print(f"Loading file: {file_path}...")

        try:
            df = pd.read_csv(file_path)
            dfs.append(df)
            print(f"Successfully loaded {file_path} with shape {df.shape}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            raise

    if not dfs:
        return pd.DataFrame()  # Return empty DataFrame
    
    combined_df = pd.concat(dfs, axis=0, ignore_index=True)
    print("*"*50)
    print(f"Combined DataFrame shape: {combined_df.shape}")
    return combined_df
