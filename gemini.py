import pandas as pd
import requests

def extract_nba_contracts():
    # Target URL: Spotrac's NBA contracts page (Note: URLs and table structures can change)
    url = 'https://www.spotrac.com/nba/contracts/'
    
    # Use headers to mimic a real web browser and avoid 403 Forbidden errors
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    
    print(f"Fetching data from {url}...")
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return

    try:
        # pandas read_html automatically finds all <table> tags in the HTML
        tables = pd.read_html(response.text)
        
        # Spotrac's main contract data is usually the first large table on the page
        df = tables[0]
        
        # NOTE: Column names vary based on the website's current layout. 
        # Standardize column names based on what the site outputs.
        # Let's assume the columns include 'Player', 'Type', 'Signed', and 'Salary' or 'Value'
        
        print("Data extracted successfully. Applying filters...")

        # 1. Filter out Rookie and Veteran contracts
        # We use a tilde (~) to negate the condition (meaning "Keep rows that DO NOT contain these words")
        # case=False makes the search case-insensitive, na=False handles empty cells
        types_to_exclude = 'Rookie|Vet|Minimum|Two-Way'
        
        # If the website uses 'Type' as the column header for contract type:
        if 'Type' in df.columns:
            df_filtered = df[~df['Type'].str.contains(types_to_exclude, case=False, na=False)]
        else:
            print("Warning: Could not find 'Type' column. Skipping contract type filter.")
            df_filtered = df

        # 2. Select only the necessary columns (Update these strings based on the actual table headers)
        # Often tables have multi-level headers. You may need to inspect df.columns first.
        columns_to_keep = ['Player', 'Type', 'Signed', 'Value'] # Adjust based on actual headers
        available_columns = [col for col in columns_to_keep if col in df_filtered.columns]
        
        final_df = df_filtered[available_columns]

        # 3. Export to CSV
        output_filename = 'filtered_nba_contracts.csv'
        final_df.to_csv(output_filename, index=False)
        print(f"Success! Data saved to {output_filename}")
        
    except ValueError as e:
        print("Could not find any HTML tables on the page. The website might be blocking the script or uses dynamic JavaScript loading.")
        print("Error details:", e)

if __name__ == "__main__":
    extract_nba_contracts()
    