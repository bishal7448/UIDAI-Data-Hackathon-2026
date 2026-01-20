# Data Analysis and Methodology for Hackathon Presentation

## 1. Data Analysis Approach (The "Brain" of the Operation)

Our solution doesn't just read data; it actively interprets and refines it. We focused on three key analytical pillars:

### A. Data Hygiene (The "Digital Janitor")
Before any analysis, we scrub the data. 
- **What we do:** We standardize names (e.g., treating "Delhi" and "delhi" as the same), remove weird symbols, and fix date formats.
- **Why it matters:** Garbage in, garbage out. By standardizing district names and pincodes, we ensure that a record from *Source A* matches a record from *Source B*, even if they were typed slightly differently.

### B. Conflict Resolution (The "Tie-Breaker")
We discovered that some pincodes are associated with multiple districts in the raw data, which creates confusion.
- **The "Dominant District" Logic:** If Pincode 123456 shows up in both District A and District B, we don't guess. We count the real enrolments. If 90% of the enrolments for that pincode are in District A, we assign that pincode to District A.
- **Layman Analogy:** It’s like deciding which city a suburb belongs to based on where the majority of its residents actually vote.

### C. Geospatial Intelligence (Putting it on the Map)
Numbers in a spreadsheet are boring; maps are actionable.
- **What we do:** We merge our clean enrolment data with official digital maps (GeoJSON). 
- **The Innovation:** The system automatically harmonizes the names between our specific data and the official map files to ensure they "talk" to each other, allowing us to generate heatmaps that show exactly where the demand is.

---

## 2. Methodology (The Step-by-Step Workflow)

here is how our backend engine processes the data, step-by-step:

### Step 1: Ingestion (Loading)
*   **Action:** The system grabs raw CSV files from our data folder.
*   **Feature:** It is robust—if one file is corrupt, it flags it but handles the rest. It combines multiple dispersed files into one master dataset.

### Step 2: Purification (Cleaning)
*   **Action:** 
    *   Dates are converted to a standard format (YYYYMMDD).
    *   District names are stripped of special characters and lowercased to ensure consistency.
    *   Useless columns are dropped to focus on what matters.

### Step 3: Validation (The Quality Check)
*   **Action:** The system runs specific checks:
    *   *Pin-District Ambiguity:* It finds pincodes that are "confused" (mapped to multiple districts).
    *   *Enrolment Aggregation:* It sums up enrolments by age groups (0-5, 5-17, 18+).

### Step 4: Logic Application (The Smarts)
*   **Action:** This is where we solve the ambiguity found in Step 3. The **Dominant District Algorithm** runs here to definitively assign pincodes to the correct district based on data density, ensuring our final analytics are accurate.

### Step 5: Visualization (The Result)
*   **Action:** Finally, we generate an **Enrolment Heatmap**. 
*   **Outcome:** A color-coded map where "hotter" colors (reds/oranges) show high enrolment activity and "cooler" colors show areas needing attention. This gives judges and policymakers an instant visual understanding of the situation.
