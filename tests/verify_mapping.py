import pandas as pd
import geopandas as gpd

def verify():
    print("Verifying Mapping...")
    
    # 1. Load Original Data
    # Note: efficient way would be to load the updated notebook and extract the mapping,
    # but that's complex. I'll just use the mapping I defined in my plan here to simulate the notebook logic.
    # Actually, I should probably try to run the notebook code? No, that's brittle headless.
    # I will replicate the cleaning logic here.
    
    df = pd.read_excel("wb_enrolment_df_dist_level_filtered.xlsx")
    
    district_mapping_wb = {
        'coochbehar': 'Koch Bihar',
        'cooch behar': 'Koch Bihar',
        'koch bihar': 'Koch Bihar',
        'dinajpur uttar': 'Uttar Dinajpur',
        'uttar dinajpur': 'Uttar Dinajpur',
        'north dinajpur': 'Uttar Dinajpur',
        'dinajpur dakshin': 'Dakshin Dinajpur',
        'dakshin dinajpur': 'Dakshin Dinajpur',
        'south dinajpur': 'Dakshin Dinajpur',
        'south  dinajpur': 'Dakshin Dinajpur',
        'darjeeling': 'Darjiling',
        'darjiling': 'Darjiling',
        'kalimpong': 'Darjiling',
        'jalpaiguri': 'Jalpaiguri',
        'alipurduar': 'Jalpaiguri',
        'malda': 'Maldah',
        'maldah': 'Maldah',
        'jhargram': 'Paschim Medinipur',
        'nadia': 'Nadia',
        'murshidabad': 'Murshidabad',
        'birbhum': 'Birbhum',
        'bankura': 'Bankura',
        'purulia': 'Puruliya',
        'puruliya': 'Puruliya',
        'kolkata': 'Kolkata',
        'hooghly': 'Hugli',
        'hugli': 'Hugli',
        'hooghiy': 'Hugli',
        'howrah': 'Haora',
        'haora': 'Haora',
        'hawrah': 'Haora',
        'north 24 parganas': 'North Twenty Four Parganas',
        '24 parganas north': 'North Twenty Four Parganas',
        '24 Paraganas North': 'North Twenty Four Parganas',
        'north twenty four parganas': 'North Twenty Four Parganas',
        'north 24 pgs': 'North Twenty Four Parganas',
        'south 24 parganas': 'South Twenty Four Parganas',
        '24 parganas south': 'South Twenty Four Parganas',
        'south twenty four parganas': 'South Twenty Four Parganas',
        'south 24 pargana': 'South Twenty Four Parganas',
        'south 24 pgs': 'South Twenty Four Parganas',
        'east midnapore': 'Purba Medinipur',
        'east midnapur': 'Purba Medinipur',
        'purba medinipur': 'Purba Medinipur',
        'west midnapore': 'Paschim Medinipur',
        'west medinipur': 'Paschim Medinipur',
        'medinipur west': 'Paschim Medinipur',
        'paschim medinipur': 'Paschim Medinipur',
        'bardhaman': 'Purba Barddhaman',
        'barddhaman': 'Purba Barddhaman',
        'burdwan': 'Purba Barddhaman',
        'purba bardhaman': 'Purba Barddhaman',
        'east bardhaman': 'Purba Barddhaman',
        'paschim bardhaman': 'Paschim Barddhaman',
        'west bardhaman': 'Paschim Barddhaman'
    }
    
    # Apply mapping
    # Note: The dataframe 'district_cleaned' might already be partially clean or raw 'district'.
    # Looking at prev output, 'district_cleaned' had values like "North 24 Parganas", "Malda", "Uttar Dinajpur".
    # These match keys in my mapping (when lowercased).
    
    mapped_districts = []
    
    unmapped_original = []
    
    for d in df['district_cleaned'].unique():
        d_lower = str(d).strip().lower()
        if d_lower in district_mapping_wb:
            mapped_districts.append(district_mapping_wb[d_lower])
        else:
            mapped_districts.append(d) # Keep original if not found? Or mark error.
            unmapped_original.append(d)
            
    mapped_districts = set(mapped_districts)
    
    # 2. Load GeoJSON
    geojson_path = "../data/raw/west_bengal_districts.geojson"
    gdf = gpd.read_file(geojson_path)
    
    # Find district column
    dist_col = None
    for col in ['district', 'DISTRICT', 'dtname', 'DTNAME', 'district_name', 'Name', 'NAME']:
        if col in gdf.columns:
            dist_col = col
            break
            
    if not dist_col:
        print("Error: Could not find district column in GeoJSON")
        return

    geo_districts = set(gdf[dist_col].unique())
    
    # 3. Check Mismatch
    unmatched = mapped_districts - geo_districts
    
    if len(unmatched) == 0:
        print("SUCCESS: All enrolment districts are mapped to GeoJSON districts!")
    else:
        print(f"FAILURE: Found {len(unmatched)} unmatched districts after mapping.")
        print("Unmatched:", unmatched)
        
    print(f"\nMapped Enrolment Districts: {sorted(list(mapped_districts))}")

if __name__ == "__main__":
    verify()
