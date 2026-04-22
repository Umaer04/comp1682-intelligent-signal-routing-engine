import pandas as pd
import heapq
import sys
import os

DATASET_FILE = 'COMPLETE_tube_network_dataset.csv' 
PENALTY_MINUTES = 300  

class TubeRouter:
    def __init__(self, filename):
        self.graph = {}
        self.load_data(filename)

    def load_data(self, filename):
        if not os.path.exists(filename):
            if os.path.exists(filename.replace('.csv', '')):
                filename = filename.replace('.csv', '')
            else:
                print(f"ERROR: Could not find '{filename}'.")
                sys.exit()

        try:
            df = pd.read_csv(filename)
            df.columns = [c.strip() for c in df.columns]
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit()

        print(f"Successfully loaded {len(df)} connections...")

        for _, row in df.iterrows():
            u = str(row['From_Station']).strip()
            v = str(row['To_Station']).strip()
            line = row['Line']
            
            try:
                travel_time = float(row['Travel_Time'])
            except:
                travel_time = 0.0

            if travel_time <= 0:
                travel_time = 2.5
            
            signal_val = str(row['Has_Signal']).strip().upper()
            has_signal = signal_val == 'TRUE'
            
            weight = travel_time if has_signal else (travel_time + PENALTY_MINUTES)
            
            self._add_edge(u, v, weight, travel_time, line)
            self._add_edge(v, u, weight, travel_time, line)

    def _add_edge(self, u, v, weight, time, line):
        if u not in self.graph: self.graph[u] = {}
        self.graph[u][v] = (weight, time, line)

    def find_route(self, start, end):
        queue = [(0, start, None, [])] 
        visited = set()
        INTERCHANGE_PENALTY = 5 
        
        while queue:
            cost, current_station, current_line, path = heapq.heappop(queue)
            
            state = (current_station, current_line)
            
            if state in visited: continue
            visited.add(state)
            
            path = path + [(current_station, current_line)]

            if current_station == end: 
                return self._format_output(path)

            if current_station in self.graph:
                for neighbor_station, (weight, _, neighbor_line) in self.graph[current_station].items():
                    
                    new_cost = cost + weight
                    
                    if current_line is not None and current_line != neighbor_line:
                        new_cost += INTERCHANGE_PENALTY
                        
                    neighbor_state = (neighbor_station, neighbor_line)
                    if neighbor_state not in visited:
                        heapq.heappush(queue, (new_cost, neighbor_station, neighbor_line, path))
        return None

    def _format_output(self, path):
        total_time = 0
        log = []
        for i in range(len(path) - 1):
            u, line_u = path[i]
            v, line_v = path[i+1]
            
            _, time, _ = self.graph[u][v] 
            
            if line_u is not None and line_u != line_v:
                 log.append(f"  [TRANSFER from {line_u} to {line_v}] (+5 min walking)")
                 total_time += 5

            total_time += time
            log.append(f"  * {u} -> {v} ({line_v}) [{time} min]") 
            
        return total_time, log

if __name__ == "__main__":
    router = TubeRouter(DATASET_FILE)
    print("\n--- SIGNAL ROUTER READY ---")
    while True:
        start = input("\nStart Station (or 'x' to quit): ").strip()
        if start.lower() == 'x': break
        end = input("End Station:   ").strip()
        
        result = router.find_route(start, end)
        if result:
            time, steps = result
            print(f"\nRoute Found! Total Time: {int(time)} mins")
            for step in steps: print(step)
        else:
            print("Route not found (Check spelling!)")