import requests
import pandas as pd
import sys
import time


API_KEY = "YOUR_KEY_HERE"


BASE_URL = "https://api.tfl.gov.uk"

def get_api_data(endpoint):
    """Fetches data from a TfL API endpoint."""
    url = f"{BASE_URL}{endpoint}"
    if '?' not in url:
        url += f"?app_key={API_KEY}"
    else:
        url += f"&app_key={API_KEY}"
        
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print(f"FATAL ERROR: API Key is invalid or not subscribed to the product.")
            print("Please check your key in the API_KEY variable.")
        else:
            print(f"HTTP error occurred: {http_err}")
        sys.exit() 
    except Exception as err:
        print(f"An error occurred: {err}")
        sys.exit() 

def build_station_dictionary():
    """
    Fetches all Tube StopPoints and creates a simple
    dictionary of {NaptanID: StationName}.
    """
    print("Step 1: Fetching station dictionary...")
    endpoint = "/StopPoint/Mode/tube"
    all_stoppoints = get_api_data(endpoint)
    
    station_dictionary = {}
    
    for station in all_stoppoints.get('stopPoints', []):
        if "NaptanMetroStation" in station.get("stopType", ""):
            naptan_id = station.get("id")
            name = station.get("commonName", "Unknown Station")
            name = name.replace("Underground Station", "").strip()
            station_dictionary[naptan_id] = name
            
    print(f"Success! Dictionary created with {len(station_dictionary)} stations.")
    return station_dictionary

def get_all_line_ids():
    """Fetches all line IDs for the 'tube' mode."""
    print("Step 2: Fetching all Tube line IDs...")
    endpoint = "/Line/Mode/tube"
    lines = get_api_data(endpoint)
    line_ids = [line['id'] for line in lines]
    print(f"Found {len(line_ids)} lines: {', '.join(line_ids)}")
    return line_ids

def build_network_segments(station_dictionary, line_ids):
    """
    Fetches the route sequence for each line and builds
    the final list of station-to-station segments.
    """
    print("Step 3: Fetching routes for each line (this will take a moment)...")
    final_data = []

    for line_name in line_ids:
        if line_name == "waterloo-city":
            print(f"  > Processing Waterloo & City (Manual Entry)...")
            final_data.append({"From_Station": "Waterloo", "To_Station": "Bank", "Line": "Waterloo & City"})
            final_data.append({"From_Station": "Bank", "To_Station": "Waterloo", "Line": "Waterloo & City"})
            continue

        print(f"  > Fetching route for: {line_name}")
        endpoint = f"/Line/{line_name}/Route/Sequence/all"
        route_data = get_api_data(endpoint)
        
        branches = route_data.get('orderedLineRoutes', [])
        
        for branch in branches:
            station_codes = branch.get('naptanIds', [])
            
            for i in range(len(station_codes) - 1):
                from_code = station_codes[i]
                to_code = station_codes[i+1]
                
                from_name = station_dictionary.get(from_code, f"CODE_NOT_FOUND: {from_code}")
                to_name = station_dictionary.get(to_code, f"CODE_NOT_FOUND: {to_code}")
                
                new_row = {
                    "From_Station": from_name,
                    "To_Station": to_name,
                    "Line": line_name
                }
                
                if new_row not in final_data:
                    final_data.append(new_row)
        
        time.sleep(0.2) 

    print("All routes processed!")
    return final_data

def save_to_csv(data):
    """Saves the final data to a CSV file."""
    print("Step 4: Saving data to CSV...")
    df = pd.DataFrame(data)
    df = df[~df['From_Station'].str.contains("CODE_NOT_FOUND")]
    df = df[~df['To_Station'].str.contains("CODE_NOT_FOUND")]
    
    df = df.drop_duplicates()
    
    df.to_csv('tube_network_segments.csv', index=False)
    print("\n--- DONE! ---")
    print("Your file 'tube_network_segments.csv' is ready in your project folder.")

if __name__ == "__main__":
    if API_KEY == "YOUR_KEY_HERE":
        print("ERROR: No TfL API key provided.")
        print("This script is only needed if you want to rebuild the dataset from scratch.")
        print("The final submitted project runs offline using the completed CSV dataset.")
        print("To use this script locally, replace API_KEY = 'YOUR_KEY_HERE' with your own TfL API key.")
        sys.exit()
    else:
        station_dict = build_station_dictionary()
        lines = get_all_line_ids()
        network_data = build_network_segments(station_dict, lines)
        save_to_csv(network_data)