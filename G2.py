import sqlite3
import math
from datetime import datetime, timedelta

DB_NAME = 'nh_routes.db'
# --- Global Constants for Route Planning ---
AVG_SPEED_KMH = 60  # Average driving speed for estimation
DAY_START_HOUR = 6  # 6 AM
DAY_END_HOUR = 18 # 6 PM

def standardize_city_name(city_name):
    """Cleans up and standardizes city names (Title Case, no extra spaces)."""
    return city_name.strip().title()

def get_connections():
    """Fetches all connections and distances from the database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT source_city, destination_city, distance_km FROM routes")
        connections = cursor.fetchall()
        
        graph = {}
        for src, dest, dist in connections:
            src = standardize_city_name(src)
            dest = standardize_city_name(dest)
            
            if src not in graph:
                graph[src] = {}
            if dest not in graph:
                graph[dest] = {}
                
            graph[src][dest] = dist
            graph[dest][src] = dist 

        return graph

    except sqlite3.Error:
        return None 
    finally:
        if conn:
            conn.close()

def dijkstra(graph, start_city, end_city):
    """
    Dijkstra's algorithm to find the shortest path and distance.
    (Logic remains unchanged)
    """
    if not graph:
        return None, "Error: Could not load road network data."

    distances = {city: float('inf') for city in graph}
    distances[start_city] = 0
    previous_cities = {city: None for city in graph}
    
    unvisited = [(0, start_city)]

    while unvisited:
        unvisited.sort() 
        current_distance, current_city = unvisited.pop(0)

        if current_distance > distances[current_city]:
            continue

        for neighbor, weight in graph[current_city].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_cities[neighbor] = current_city 
                unvisited.append((distance, neighbor))

    path = []
    current_city = end_city
    while current_city is not None:
        path.insert(0, current_city)
        current_city = previous_cities[current_city]

    if path and path[0] == start_city:
        return path, distances[end_city]
    else:
        return None, f"No route found between {start_city} and {end_city}. Check city spelling or database connections."

# --- SIMPLIFIED TIME LOGIC ---

def get_departure_time(total_distance):
    """
    Calculates total time and suggests the best departure time to arrive during daylight (6 AM - 6 PM).
    Returns: (suggested_departure_time, total_time_hours)
    """
    # 1. Calculate Total Time
    # Note: Includes no buffer for stops, assuming continuous driving time.
    total_time_hours = total_distance / AVG_SPEED_KMH

    # 2. Determine Optimal Departure Time
    today = datetime.now().date()
    # Target arrival is the end of the day (6 PM)
    target_arrival = datetime(today.year, today.month, today.day, DAY_END_HOUR, 0, 0)
    
    # Calculate the estimated departure time
    time_delta = timedelta(hours=total_time_hours)
    suggested_departure = target_arrival - time_delta

    # Adjust if suggested departure is illogical (too far in the past or requires overnight driving)
    now = datetime.now()
    
    if total_time_hours >= 12 and suggested_departure.hour < DAY_START_HOUR:
        # If it's a long journey requiring an overnight, suggest leaving at 6 AM today
        # (This is an assumption for simple planning)
        suggested_departure = datetime(today.year, today.month, today.day, DAY_START_HOUR, 0, 0)

    # If the suggested departure time has already passed today, suggest tomorrow morning's start time.
    if suggested_departure < now:
         # Suggest leaving tomorrow at 6 AM
         suggested_departure = datetime(today.year, today.month, today.day, DAY_START_HOUR, 0, 0) + timedelta(days=1)
    
    
    return suggested_departure.strftime("%I:%M %p"), total_time_hours
    
# --- MAIN ROUTE FINDER FUNCTION ---

def find_route(source, destination):
    """
    Finds the shortest route and calculates essential travel times.
    Returns: (path_list, distance, departure_time, total_time_hours) 
             or (None, error_message)
    """
    graph = get_connections()
    if graph is None:
        return None, "Error: Road network database not accessible or corrupt."

    start_city = standardize_city_name(source)
    end_city = standardize_city_name(destination)
    
    if start_city not in graph or end_city not in graph:
        return None, f"One or both cities not found in the network: {source} or {destination}. Check spelling or coverage."

    # 1. Find shortest path and total distance
    path, distance = dijkstra(graph, start_city, end_city)

    if not path:
        return None, distance 

    # 2. Calculate optimal departure time and total time
    departure_time, total_time_hours = get_departure_time(distance)

    # Return only the necessary calculated details (4 values total)
    return path, distance, departure_time, total_time_hours
