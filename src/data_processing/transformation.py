import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from typing import List
import os

def date_format_change(df: pd.DataFrame, date_column: str, new_format: str = '%Y%m%d') -> pd.DataFrame:
    """
    Change the format of a date column in a DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    date_column (str): The name of the date column to be reformatted.
    new_format (str): The desired date format. Default is '%Y%m%d'.

    Returns:
    pd.DataFrame: DataFrame with reformatted date column.
    """
    df[date_column] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.strftime(new_format)
    return df


def extract_month_from_date(df, date_column='enrolment_date', month_column='month'):
    """
    Extract month from a date column and add it as a new column.
    
    Args:
        df: DataFrame containing the date column
        date_column: Name of the column containing the date (default: 'enrolment_date')
        month_column: Name of the new column to store the month (default: 'month')
    
    Returns:
        DataFrame with the new month column added
    """
    df[month_column] = df[date_column].astype(str).str[4:6]
    return df

def filter_by_state(df: pd.DataFrame, state_name: str, state_column: str = 'state_cleaned') -> pd.DataFrame:
    """
    Filter the DataFrame for a specific state.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    state_name (str): The name of the state to filter by.
    state_column (str): The name of the column containing state names. Default is 'state_cleaned'.

    Returns:
    pd.DataFrame: Filtered DataFrame containing only rows for the specified state.
    """
    filtered_df = df[df[state_column] == state_name]
    return filtered_df

def filter_df_by_level(df: pd.DataFrame, filter_by: str, filter_label: List[str]) -> pd.DataFrame:
    """
    Aggregate and filter DataFrame by a specified grouping column.
    
    Groups the DataFrame by a specified column, sums the specified label columns,
    and returns the results sorted by total enrollment in descending order.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame to aggregate
    filter_by (str): The column name to group by (e.g., 'month', 'district_cleaned')
    filter_label (List[str]): List of column names to sum (e.g., ['age_0_5', 'age_5_17', 'age_18_greater', 'total_enroll'])
    
    Returns:
    pd.DataFrame: Aggregated DataFrame sorted by 'total_enroll' in descending order
    """
    return df.groupby(filter_by)[filter_label].sum().sort_values(by='total_enroll', ascending=False).reset_index()

# Generic Function to Plot Enrolment Heatmap for Any State
def plot_state_enrolment_heatmap(enrolment_df, state_name, geojson_path, output_path, district_mapping=None):
    """
    Generates and saves an enrolment heatmap for a specific state.
    
    Args:
        enrolment_df (pd.DataFrame): The raw enrolment dataframe containing 'state', 'district', 'total_enroll'.
        state_name (str): Name of the state to filter and plot (e.g., 'West Bengal').
        geojson_path (str): Path to the state's district GeoJSON file.
        output_path (str): Path where the resulting PNG plot will be saved.
        district_mapping (dict, optional): Dictionary to map/correct district names before merging.
    """
    print(f"Processing data for {state_name}...")
    
    # 1. Filter Data for State
    # Ensure state filtering is case-insensitive if needed, or rely on exact match if data is clean
    state_df = enrolment_df[enrolment_df['state_cleaned'] == state_name].copy()
    
    if state_df.empty:
        print(f"No records found for state: {state_name}")
        return
        
    # 2. Clean District Names
    # Basic cleaning: lowercase and strip
    state_df['district_cleaned'] = state_df['district'].astype(str).str.lower().str.strip()
    
    # 3. Apply Mapping if provided
    if district_mapping:
        print("Applying district mapping...")
        state_df['district_cleaned'] = state_df['district_cleaned'].map(district_mapping).fillna(state_df['district_cleaned'])
        
        # Capitalize for better matching if no mapping found (heuristic)
        # But if mapping maps to Title Case, we are good. 
        # Let's ensure the mapping values are Title Case if that's what GeoJSON has.
    
    # 4. Group by District
    dist_df = state_df.groupby('district_cleaned')['total_enroll'].sum().reset_index()
    
    # 5. Load GeoJSON
    if not os.path.exists(geojson_path):
        print(f"GeoJSON file not found at: {geojson_path}")
        return
        
    gdf = gpd.read_file(geojson_path)
    
    # Find district column in GeoJSON
    dist_col = None
    possible_cols = ['district', 'DISTRICT', 'dtname', 'DTNAME', 'district_name', 'Name', 'NAME', 'District']
    for col in possible_cols:
        if col in gdf.columns:
            dist_col = col
            break
            
    if not dist_col:
        print("Could not identify district column in GeoJSON. Available columns:", gdf.columns)
        return
        
    # Normalize GeoJSON district names for merging
    # We create a normalized column for merging, keeping original for geometry
    gdf['district_normalized'] = gdf[dist_col].astype(str).str.strip()
    # Note: We rely on the mapping to match this normalized name. 
    # If mapping outputs 'Paschim Medinipur', GeoJSON must have 'Paschim Medinipur'.
    
    # 6. Merge
    # We merge on the cleaned/mapped name from DF and the normalized name from GeoJSON
    merged = gdf.merge(dist_df, left_on='district_normalized', right_on='district_cleaned', how='left')
    
    # Check for unmatched
    unmatched_count = merged['total_enroll'].isna().sum()
    if unmatched_count > 0:
        print(f"Warning: {unmatched_count} districts in GeoJSON have no matching enrolment data.")
        unmatched_districts = merged[merged['total_enroll'].isna()]['district_normalized'].tolist()
        print("Unmatched districts:", unmatched_districts)
    
    # 7. Plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    
    # Plot all districts with base color (grey for missing data)
    merged.plot(column='total_enroll', ax=ax, legend=True,
                legend_kwds={'label': "Total Enrolment by District",
                             'orientation': "horizontal"},
                missing_kwds={'color': 'lightgrey', 'label': 'Missing values'},
                cmap='YlOrRd',
                edgecolor='black')
                
    plt.title(f'{state_name} Enrolment Heatmap', fontsize=16)
    plt.axis('off')
    
    # Save
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {output_path}")
    plt.close()
    