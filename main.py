import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings as config

from src.data_processing.loading import load_data
from src.data_processing.transformation import (
    date_format_change,  
    extract_month_from_date, 
    plot_state_enrolment_heatmap
)
from src.data_processing.cleaning import clean_name, drop_columns
from src.data_processing.transformation import filter_by_state
from src.data_processing.validation import (
    get_dominant_district_per_pincode, 
    flag_multi_district_pincodes, 
    unique_pincode_count, 
    get_pin_district_count, 
    flag_problematic_enrolments, 
    aggregate_enrolments_by_district_pincode
)

def main():
    # Load Data
    print("Loading data...")
    enrolment_df = load_data(config.ENROLMENT_DATA_PATHS)
    print("*"*50)
    print("Enrolment data:")
    print(enrolment_df.head())
    
    # Date Formatting
    print("*"*50)
    print("Formatting dates...")
    enrolment_df = date_format_change(enrolment_df, 'enrolment_date')
    print("Formatted enrolment data:")
    print(enrolment_df.head())
    
    # Clean State Names
    print("*"*50)
    print("Cleaning state names...")
    enrolment_df = clean_name(enrolment_df, 'state', config.STATE_MAPPING, 'state_cleaned')
    unique_states = enrolment_df['state_cleaned'].unique()
    print(f"Unique states after cleaning: {unique_states}") # Todo: Handle this 37 -> 36
    print("Cleaned enrolment data:")
    print(enrolment_df.head())
    
    # Filter for West Bengal
    print("*"*50)
    print("Filtering for West Bengal...")
    wb_df = filter_by_state(enrolment_df, 'West Bengal')
    print(f"West Bengal data shape: {wb_df.shape}")
    print("West Bengal data:")
    print(wb_df.head())
    
    # Clean District Names for West Bengal
    print("*"*50)
    print("Cleaning district names for West Bengal...")
    # Create a copy to avoid SettingWithCopyWarning
    wb_df = wb_df.copy()
    wb_df = clean_name(wb_df, 'district', config.DISTRICT_MAPPING_WB, 'district_cleaned')
    unique_districts = wb_df['district_cleaned'].nunique()
    print(f"Unique districts in West Bengal after cleaning: {unique_districts}")
    print("Cleaned West Bengal data:")
    print(wb_df.head())
    
    # Todo: Remove Hard coding
    print("*"*50)
    print("*"*50)
    wb_df['district_cleaned'] = wb_df['district_cleaned'].replace({
        '24 Paraganas North': 'North 24 Parganas',
        '24 Paraganas South': 'South 24 Parganas'
    })
    unique_districts = wb_df['district_cleaned'].nunique()
    print(f"Unique districts in West Bengal after cleaning: {unique_districts}")
    print("Cleaned West Bengal data:")
    print(wb_df.head())
    print("*"*50)

    # Get unique pincode count
    print("*"*50)
    unique_pincode_count_df = unique_pincode_count(wb_df)
    print("Unique pincode count:")
    print(unique_pincode_count_df)

    # Get pincode district count
    print("*"*50)
    pincode_district_count_df = get_pin_district_count(wb_df)
    print("Pincode district count:")
    print(pincode_district_count_df)

    # Get problem pins
    print("*"*50)
    problem_pins = pincode_district_count_df[
    pincode_district_count_df['district_count'] > 1
    ]
    print("Problematic pins:")
    print(problem_pins[['pincode', 'district_count']])

    # Flag Problematic Enrolments
    print("*"*50)
    flagged_pincode_dominant = aggregate_enrolments_by_district_pincode(
    flag_problematic_enrolments(wb_df, problem_pins), ['age_0_5', 'age_5_17', 'age_18_greater'])
    print("Flagged problematic enrolments aggregated by district and pincode:")
    print(flagged_pincode_dominant)
    
    print("*"*50)
    dominant_districts = get_dominant_district_per_pincode(flagged_pincode_dominant, ['age_0_5', 'age_5_17', 'age_18_greater'])
    print("Dominant districts per problematic pincode:")
    print(dominant_districts)

    # Flag Multi-District Pincodes
    print("*"*50)
    wb_df = flag_multi_district_pincodes(wb_df)
    print("West Bengal data with multi-district pincode flag:")
    print(wb_df.head())

    # Extract Month from Enrolment Date
    print("*"*50)
    wb_df = extract_month_from_date(wb_df, 'enrolment_date', 'month')
    print("West Bengal data with extracted month:")
    print(wb_df.head())
    
    # Calculate total enrolments
    print("*"*50)
    wb_df['total_enroll'] = wb_df['age_0_5']+wb_df['age_5_17']+wb_df['age_18_greater']
    print("West Bengal data with total enrolments:")
    print(wb_df.head())

    # Drop unnecessary columns if needed
    print("*"*50)
    columns_to_drop = ['date','district','state']  # Replace with actual column names to drop
    wb_df_cleaned = drop_columns(wb_df, columns_to_drop)
    print("Final West Bengal data after dropping unnecessary columns:")
    print(wb_df_cleaned.head())

    # Group by district and calculate total enrolments
    print("*"*50)
    wb_df_dist_level=wb_df_cleaned.groupby('district_cleaned')[['age_0_5','age_5_17','age_18_greater','total_enroll']].sum()
    print(wb_df_dist_level.shape)
    print("West Bengal district level enrolment data:")
    print(wb_df_dist_level)
    
    # Sort by total enrolments
    print("*"*50)
    wb_df_dist_level.sort_values('total_enroll', ascending=False).reset_index()
    print("West Bengal district level enrolment data sorted by total enrolments:")
    print(wb_df_dist_level)

    # Export to Excel
    print("*"*50)
    excel_output_path = os.path.join(config.BASE_DIR, 'results', 'wb_enrolment_df_dist_level_filtered.xlsx')
    wb_df_dist_level.to_excel(excel_output_path)
    print(f"Exported district level data to: {excel_output_path}")

    # Get top 10 districts by total enrolments
    print("*"*50)
    wb_df_dist_level_top_10=wb_df_dist_level.head(10)
    print("Top 10 districts by total enrolments:")
    print(wb_df_dist_level_top_10)

    print("*"*50)
    plot_state_enrolment_heatmap(
    enrolment_df=wb_df,  # Assuming wb_df is available from previous cells. Or use original 'enrolment_df'
    state_name='West Bengal',
    geojson_path=os.path.join(config.RAW_DATA_DIR, 'west_bengal_districts.geojson'),
    output_path=os.path.join(config.BASE_DIR, 'results', 'wb_enrolment_heatmap_generic.png'),
    district_mapping=config.DISTRICT_MAPPING_WB
    )

if __name__ == "__main__":
    main()
