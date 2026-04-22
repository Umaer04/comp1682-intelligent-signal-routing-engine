import requests
import pandas as pd
import sys
import time
import os 
import math

API_KEY = "YOUR_KEY_HERE" 


BASE_URL = "https://api.tfl.gov.uk"
INPUT_FILE = 'FINAL_network_with_signal.csv'
OUTPUT_FILE = 'COMPLETE_tube_network_dataset.csv' 

def get_journey_time(from_station, to_station):
    """
    Calls the TfL Journey API to get the travel time for a single segment.
    """
    try:
        from_resp = requests.get(f"{BASE_URL}/StopPoint/Search", params={"query": from_station, "modes": "tube", "app_key": API_KEY})
        from_resp.raise_for_status()
        from_id = from_resp.json()['matches'][0]['id']

        to_resp = requests.get(f"{BASE_URL}/StopPoint/Search", params={"query": to_station, "modes": "tube", "app_key": API_KEY})
        to_resp.raise_for_status()
        to_id = to_resp.json()['matches'][0]['id']

        journey_resp = requests.get(f"{BASE_URL}/Journey/JourneyResults/{from_id}/to/{to_id}", params={"journeyPreference": "LeastTime", "mode": "tube", "app_key": API_KEY})
        journey_resp.raise_for_status()
        
        journeys = journey_resp.json().get('journeys', [])
        if journeys:
            duration = journeys[0].get('duration', 0)
            return duration
        else:
            if "Waterloo" in from_station and "Bank" in to_station: return 4
            if "Bank" in from_station and "Waterloo" in to_station: return 4
            return 0 
    except Exception as err:
        print(f"  > API Error for {from_station} to {to_station}. Setting 0. Error: {err}")
        return 0

if __name__ == "__main__":
    if API_KEY == "YOUR_KEY_HERE":
        print("ERROR: No TfL API key provided.")
        print("This script is only needed if you want to rebuild the dataset from scratch.")
        print("The final submitted project runs offline using the completed CSV dataset.")
        print("To use this script locally, replace API_KEY = 'YOUR_KEY_HERE' with your own TfL API key.")
        sys.exit()

    start_index = 0
    
    if os.path.exists(OUTPUT_FILE):
        print(f"Found existing file: {OUTPUT_FILE}. Resuming...")
        df = pd.read_csv(OUTPUT_FILE)
        
        if df['Travel_Time'].isnull().any():
            start_index = df['Travel_Time'].isnull().idxmax()
            print(f"Resuming from segment {start_index}...")
        else:
            print("File is already 100% complete. All done!")
            sys.exit() 
            
    else:
        print(f"Starting from scratch. Loading {INPUT_FILE}...")
        try:
            df = pd.read_csv(INPUT_FILE)
            df['Travel_Time'] = pd.NA 
        except FileNotFoundError:
            print(f"ERROR: '{INPUT_FILE}' not found.")
            print("Please run the 'add_signal.py' script first.")
            sys.exit()

    total_rows = len(df)
    print(f"Processing segments from {start_index} to {total_rows}...")

    for index, row in df.iloc[start_index:].iterrows():
        print(f"Processing segment {index+1} of {total_rows}: {row['From_Station']} -> {row['To_Station']}")
        
        time_taken = get_journey_time(row['From_Station'], row['To_Station'])
        

        df.at[index, 'Travel_Time'] = time_taken
        

        df.to_csv(OUTPUT_FILE, index=False)
        

        time.sleep(0.5) 

    print("\n--- ALL DONE! ---")
    print(f"Your file '{OUTPUT_FILE}' is now 100% complete.")