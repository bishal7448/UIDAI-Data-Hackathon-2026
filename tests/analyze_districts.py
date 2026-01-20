import pandas as pd
import geopandas as gpd
import os

def analyze():
    print("Loading Data...")
    try:
        # Load Excel
        df = pd.read_excel("wb_enrolment_df_dist_level_filtered.xlsx")
        print("Excel df loaded. Columns:", df.columns)
        enrol_districts = set(df['district_cleaned'].unique())
        print(f"Enrolment Districts ({len(enrol_districts)}):", sorted(list(enrol_districts)))
        
        # Load GeoJSON
        geojson_path = "../data/raw/west_bengal_districts.geojson"
        if not os.path.exists(geojson_path):
            print(f"GeoJSON not found at {geojson_path}")
            return
            
        gdf = gpd.read_file(geojson_path)
        print("GeoJSON loaded. Columns:", gdf.columns)
        
        # Assuming GeoJSON has a district name column. Often it's 'district' or 'dtname' or similar.
        # I'll print the first few rows to see columns if I'm not sure, but looking at notebook code might help.
        # Notebook output in previous turn showed 'district_name' and 'district_normalized' in gdf in cell 587.
        # But 'district_normalized' might be created in the notebook. 
        # I'll check available columns.
        
        print("GeoJSON columns:", gdf.columns.tolist())
        
        # Try to find the district column
        dist_col = None
        for col in ['district', 'DISTRICT', 'dtname', 'DTNAME', 'district_name', 'Name', 'NAME']:
            if col in gdf.columns:
                dist_col = col
                break
        
        if dist_col:
            geo_districts = set(gdf[dist_col].unique())
            print(f"Geo Districts ({len(geo_districts)}):", sorted(list(geo_districts)))
            
            # Find unmatched
            unmatched_in_geo = geo_districts - enrol_districts
            unmatched_in_enrol = enrol_districts - geo_districts
            
            print(f"\nDistricts in GeoJSON but NOT in Enrolment ({len(unmatched_in_geo)}):")
            for d in sorted(list(unmatched_in_geo)):
                print(f" - {d}")
                
            print(f"\nDistricts in Enrolment but NOT in GeoJSON ({len(unmatched_in_enrol)}):")
            for d in sorted(list(unmatched_in_enrol)):
                print(f" - {d}")
        else:
            print("Could not identify district column in GeoJSON.")
            print(gdf.head())

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze()
