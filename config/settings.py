import os

# Base directory (1 level up from config/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data Directories
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# Data files
ENROLMENT_DATA_FILES = [
    "api_data_aadhar_enrolment_0_500000.csv",
    "api_data_aadhar_enrolment_500000_1000000.csv",
    "api_data_aadhar_enrolment_1000000_1006029.csv"
]

DEMOGRAPHIC_DATA_FILES = [
    "api_data_aadhar_demographic_0_500000.csv",
    "api_data_aadhar_demographic_500000_1000000.csv",
    "api_data_aadhar_demographic_1000000_1500000.csv",
    "api_data_aadhar_demographic_1500000_2000000.csv",
    "api_data_aadhar_demographic_2000000_2071700.csv"
]

# Full paths to data files
ENROLMENT_DATA_PATHS = [os.path.join(RAW_DATA_DIR, f) for f in ENROLMENT_DATA_FILES]

DEMOGRAPHIC_DATA_DIR = os.path.join(RAW_DATA_DIR, "api_data_aadhar_demographic")
DEMOGRAPHIC_DATA_PATHS = [os.path.join(DEMOGRAPHIC_DATA_DIR, f) for f in DEMOGRAPHIC_DATA_FILES]

# Mapping dictionary for state name corrections
STATE_MAPPING = {
    # Andaman and Nicobar Islands
    'andaman and nicobar islands': 'Andaman and Nicobar Islands',
    'andaman nicobar islands': 'Andaman and Nicobar Islands',
    
    # Andhra Pradesh
    'andhra pradesh': 'Andhra Pradesh',
    
    # Arunachal Pradesh
    'arunachal pradesh': 'Arunachal Pradesh',
    
    # Assam
    'assam': 'Assam',
    
    # Bihar
    'bihar': 'Bihar',
    
    # Chandigarh
    'chandigarh': 'Chandigarh',
    
    # Chhattisgarh
    'chhattisgarh': 'Chhattisgarh',
    
    # Dadra and Nagar Haveli and Daman and Diu
    'dadra nagar haveli': 'Dadra and Nagar Haveli and Daman and Diu',
    'dadra and nagar haveli': 'Dadra and Nagar Haveli and Daman and Diu',
    'daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'dadra and nagar haveli and daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'the dadra and nagar haveli and daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'daman diu': 'Dadra and Nagar Haveli and Daman and Diu',
    
    # Delhi
    'delhi': 'Delhi',
    
    # Goa
    'goa': 'Goa',
    
    # Gujarat
    'gujarat': 'Gujarat',
    
    # Haryana
    'haryana': 'Haryana',
    
    # Himachal Pradesh
    'himachal pradesh': 'Himachal Pradesh',
    
    # Jammu and Kashmir
    'jammu and kashmir': 'Jammu and Kashmir',
    'jammu kashmir': 'Jammu and Kashmir',
    
    # Jharkhand
    'jharkhand': 'Jharkhand',
    
    # Karnataka
    'karnataka': 'Karnataka',
    
    # Kerala
    'kerala': 'Kerala',
    
    # Ladakh
    'ladakh': 'Ladakh',
    
    # Lakshadweep
    'lakshadweep': 'Lakshadweep',
    
    # Madhya Pradesh
    'madhya pradesh': 'Madhya Pradesh',
    
    # Maharashtra
    'maharashtra': 'Maharashtra',
    
    # Manipur
    'manipur': 'Manipur',
    
    # Meghalaya
    'meghalaya': 'Meghalaya',
    
    # Mizoram
    'mizoram': 'Mizoram',
    
    # Nagaland
    'nagaland': 'Nagaland',
    
    # Odisha
    'odisha': 'Odisha',
    'orissa': 'Odisha',
    
    # Puducherry
    'puducherry': 'Puducherry',
    'pondicherry': 'Puducherry',
    
    # Punjab
    'punjab': 'Punjab',
    
    # Rajasthan
    'rajasthan': 'Rajasthan',
    
    # Sikkim
    'sikkim': 'Sikkim',
    
    # Tamil Nadu
    'tamil nadu': 'Tamil Nadu',
    
    # Telangana
    'telangana': 'Telangana',
    
    # Tripura
    'tripura': 'Tripura',
    
    # Uttar Pradesh
    'uttar pradesh': 'Uttar Pradesh',
    
    # Uttarakhand
    'uttarakhand': 'Uttarakhand',
    
    # West Bengal
    'west bengal': 'West Bengal',
    'west bangal': 'West Bengal',
    'westbengal': 'West Bengal',
    'west  bengal': 'West Bengal',
    'westbengal ': 'West Bengal'
}

# District mapping for West Bengal
DISTRICT_MAPPING_WB = {
    # Cooch Behar
    'coochbehar': 'Cooch Behar',
    'cooch behar': 'Cooch Behar',
    'koch bihar': 'Cooch Behar',

    # Uttar Dinajpur
    'dinajpur uttar': 'Uttar Dinajpur',
    'uttar dinajpur': 'Uttar Dinajpur',
    'north dinajpur': 'Uttar Dinajpur',

    # Dakshin Dinajpur
    'dinajpur dakshin': 'Dakshin Dinajpur',
    'dakshin dinajpur': 'Dakshin Dinajpur',
    'south dinajpur': 'Dakshin Dinajpur',

    # Darjeeling
    'darjeeling': 'Darjeeling',
    'darjiling': 'Darjeeling',

    # Kalimpong
    'kalimpong': 'Kalimpong',

    # Jalpaiguri
    'jalpaiguri': 'Jalpaiguri',

    # Alipurduar
    'alipurduar': 'Alipurduar',

    # Malda
    'malda': 'Malda',
    'maldah': 'Malda',

    # Jhargram
    'jhargram': 'Jhargram',

    # Nadia
    'nadia': 'Nadia',

    # Murshidabad
    'murshidabad': 'Murshidabad',

    # Birbhum
    'birbhum': 'Birbhum',

    # Bankura
    'bankura': 'Bankura',

    # Purulia
    'purulia': 'Purulia',
    'puruliya': 'Purulia',

    # Kolkata
    'kolkata': 'Kolkata',

    # Hooghly
    'hooghly': 'Hooghly',
    'hugli': 'Hooghly',
    'hooghiy': 'Hooghly',

    # Howrah
    'howrah': 'Howrah',
    'haora': 'Howrah',
    'hawrah': 'Howrah',

    # North 24 Parganas
    'north 24 parganas': 'North 24 Parganas',
    '24 parganas north': 'North 24 Parganas',
    '24 Paraganas North': 'North 24 Parganas',
    'north twenty four parganas': 'North 24 Parganas',

    # South 24 Parganas
    'south 24 parganas': 'South 24 Parganas',
    '24 parganas south': 'South 24 Parganas',
    'south twenty four parganas': 'South 24 Parganas',
    'south 24 pargana': 'South 24 Parganas',

    # East Medinipur
    'east midnapore': 'Purba Medinipur',
    'east midnapur': 'Purba Medinipur',
    'purba medinipur': 'Purba Medinipur',

    # West Medinipur
    'west midnapore': 'Paschim Medinipur',
    'west medinipur': 'Paschim Medinipur',
    'medinipur west': 'Paschim Medinipur',
    'paschim medinipur': 'Paschim Medinipur',

    # Bardhaman (split districts)
    'bardhaman': 'Purba Bardhaman',
    'barddhaman': 'Purba Bardhaman',
    'burdwan': 'Purba Bardhaman',

    'purba bardhaman': 'Purba Bardhaman',
    'paschim bardhaman': 'Paschim Bardhaman'
}
