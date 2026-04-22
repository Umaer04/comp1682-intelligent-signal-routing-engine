import pandas as pd

print("Loading signal_stations.txt...")
try:
    with open('signal_stations.txt', 'r', encoding='utf-8') as f:
        signal_stations = set(line.strip() for line in f)
    print(f"Loaded {len(signal_stations)} signal-enabled stations.")
except FileNotFoundError:
    print("ERROR: 'signal_stations.txt' not found.")
    print("Please make sure 'signal_stations.txt' is in the same folder and has the station list.")
    exit()

print("Loading tube_network_segments.csv...")
try:
    df = pd.read_csv('tube_network_segments.csv')
except FileNotFoundError:
    print("ERROR: 'tube_network_segments.csv' not found.")
    print("Please run the 'build_network.py' script first.")
    exit()

print("Cross-referencing and building 'has_signal' column...")
has_signal_column = []


for index, row in df.iterrows():
    from_station = str(row['From_Station'])
    to_station = str(row['To_Station'])
    
    if from_station.strip() in signal_stations and to_station.strip() in signal_stations:
        has_signal_column.append(True)
    else:
        has_signal_column.append(False)

df['has_signal'] = has_signal_column

df.to_csv('FINAL_network_with_signal.csv', index=False)

print("\n--- DONE! ---")
print("Your file 'FINAL_network_with_signal.csv' is ready.")
print("This is your complete, master dataset for the project.")