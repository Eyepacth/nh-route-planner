import sqlite3

DB_NAME = 'nh_routes.db'

def create_and_populate_db():
    """
    Creates the SQLite database and populates it with a comprehensive set 
    of major city-to-city road distances across India (approx. 150+ routes,
    including maximum coverage for Gujarat).
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Create the 'routes' table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY,
            source_city TEXT NOT NULL,
            destination_city TEXT NOT NULL,
            distance_km REAL NOT NULL
        )
        ''')
        
        # Clear existing data to prevent duplicates upon re-running
        cursor.execute("DELETE FROM routes")
        
        # --- Comprehensive Major City Data (North, West, South, East) ---
        # Data is based on major national highway connections and shortest road distances.
        # City names are Title Cased for consistency.
        
        routes_data = [
            # ------------------------------------------------------------------
            # *** WEST INDIA: CORE AND MAX GUJARAT CITIES *** (Approx. 50+ routes)
            # ------------------------------------------------------------------
            ('Mumbai', 'Pune', 150),
            ('Mumbai', 'Nagpur', 800), # Via Samruddhi Mahamarg
            ('Mumbai', 'Ahmedabad', 530),
            ('Mumbai', 'Surat', 280),
            ('Pune', 'Nashik', 210),
            ('Ahmedabad', 'Vadodara', 100),
            ('Ahmedabad', 'Surat', 260),
            ('Ahmedabad', 'Rajkot', 215),
            ('Ahmedabad', 'Bhavnagar', 170),
            ('Ahmedabad', 'Gandhinagar', 30),
            ('Ahmedabad', 'Palanpur', 145),
            ('Ahmedabad', 'Udaipur', 260),
            ('Vadodara', 'Bharuch', 85),
            ('Vadodara', 'Rajkot', 290),
            ('Surat', 'Bharuch', 70),
            ('Surat', 'Vapi', 120),
            ('Surat', 'Bhavnagar', 220), # Via Ferry/Road approx
            
            # --- Gujarat (Saurashtra & Kutch) ---
            ('Rajkot', 'Jamnagar', 90),
            ('Rajkot', 'Junagadh', 100),
            ('Rajkot', 'Morbi', 70),
            ('Rajkot', 'Surendranagar', 110),
            ('Jamnagar', 'Dwarka', 130),
            ('Jamnagar', 'Porbandar', 100),
            ('Bhavnagar', 'Veraval', 260),
            ('Bhavnagar', 'Amreli', 130),
            ('Junagadh', 'Veraval', 85),
            ('Junagadh', 'Amreli', 105),
            ('Dwarka', 'Porbandar', 100),
            ('Bhuj', 'Kandla', 60),
            ('Bhuj', 'Gandhidham', 60),
            ('Bhuj', 'Surendranagar', 260),
            ('Kandla', 'Morbi', 150),
            ('Gandhinagar', 'Mehsana', 75),
            ('Mehsana', 'Patan', 50),
            ('Vadodara', 'Anand', 40),
            ('Anand', 'Nadiad', 20),
            ('Vadodara', 'Godhra', 75),
            ('Bharuch', 'Dediapada', 90),
            ('Valsad', 'Vapi', 25),
            ('Valsad', 'Daman', 15),

            # --- West/Central India Connections ---
            ('Pune', 'Hyderabad', 570),
            ('Nagpur', 'Raipur', 280),
            ('Nagpur', 'Bhopal', 390),
            ('Indore', 'Bhopal', 190),
            ('Indore', 'Ujjain', 55),
            ('Indore', 'Jabalpur', 500),
            ('Goa', 'Belgaum', 150),
            ('Mumbai', 'Goa', 580),
            ('Ahmedabad', 'Jaipur', 660),
            ('Mumbai', 'Jaipur', 1050),
            
            # ------------------------------------------------------------------
            # *** NORTH INDIA: *** (Approx. 40+ routes)
            # ------------------------------------------------------------------
            ('Delhi', 'Jaipur', 270),
            ('Delhi', 'Agra', 230), 
            ('Delhi', 'Amritsar', 460),
            ('Delhi', 'Chandigarh', 250),
            ('Delhi', 'Lucknow', 530),
            ('Delhi', 'Dehradun', 250),
            ('Delhi', 'Kanpur', 490),
            ('Jaipur', 'Jodhpur', 330),
            ('Jaipur', 'Ajmer', 135),
            ('Jaipur', 'Kota', 250),
            ('Lucknow', 'Kanpur', 90),
            ('Lucknow', 'Varanasi', 320),
            ('Agra', 'Gwalior', 120),
            ('Varanasi', 'Patna', 260),
            ('Chandigarh', 'Ludhiana', 100),
            ('Ludhiana', 'Amritsar', 145),
            ('Amritsar', 'Jammu', 200),
            ('Jammu', 'Srinagar', 290),
            ('Srinagar', 'Leh', 420),
            ('Ambala', 'Chandigarh', 50),
            ('Ambala', 'Delhi', 200),
            ('Jalandhar', 'Amritsar', 80),
            ('Jodhpur', 'Bikaner', 250),
            ('Bikaner', 'Jaipur', 330),
            ('Ajmer', 'Jodhpur', 200),
            ('Gwalior', 'Indore', 450),
            ('Gwalior', 'Kanpur', 280),
            ('Haridwar', 'Dehradun', 55),
            ('Rishikesh', 'Haridwar', 25),
            ('Lucknow', 'Bareilly', 230),
            ('Varanasi', 'Allahabad', 120),
            ('Patna', 'Gaya', 100),
            ('Patna', 'Ranchi', 330),
            ('Delhi', 'Shimla', 340),
            ('Delhi', 'Srinagar', 810),
            ('Agra', 'Mathura', 60),
            ('Delhi', 'Meerut', 80),
            ('Delhi', 'Hisar', 170),
            
            # ------------------------------------------------------------------
            # *** SOUTH INDIA: (Approx. 35+ routes)
            # ------------------------------------------------------------------
            ('Bengaluru', 'Chennai', 350),
            ('Bengaluru', 'Hyderabad', 575),
            ('Bengaluru', 'Pune', 830),
            ('Bengaluru', 'Kochi', 500),
            ('Bengaluru', 'Mysuru', 150),
            ('Bengaluru', 'Mangalore', 350),
            ('Chennai', 'Coimbatore', 500),
            ('Chennai', 'Madurai', 460),
            ('Chennai', 'Puducherry', 150),
            ('Chennai', 'Tiruchirappalli', 330),
            ('Hyderabad', 'Vijayawada', 270),
            ('Hyderabad', 'Visakhapatnam', 620),
            ('Vijayawada', 'Visakhapatnam', 350),
            ('Kochi', 'Thiruvananthapuram', 200),
            ('Coimbatore', 'Kochi', 190),
            ('Madurai', 'Coimbatore', 220),
            ('Madurai', 'Tiruchirappalli', 135),
            ('Pune', 'Belgaum', 390),
            ('Hyderabad', 'Nagpur', 490),
            ('Chennai', 'Nellore', 170),
            ('Coimbatore', 'Salem', 170),
            ('Salem', 'Tiruchirappalli', 140),
            ('Visakhapatnam', 'Bhubaneswar', 440),
            ('Kochi', 'Kozhikode', 180),
            ('Kozhikode', 'Mangalore', 220),
            ('Hubballi', 'Bengaluru', 400),
            ('Hubballi', 'Goa', 180),
            ('Tiruchirappalli', 'Madurai', 135),
            ('Kochi', 'Coimbatore', 190),
            ('Hyderabad', 'Warangal', 150),
            ('Guntur', 'Vijayawada', 35),
            ('Tirupati', 'Chennai', 150),
            ('Tirupati', 'Bengaluru', 250),
            ('Belgaum', 'Hubballi', 90),

            # ------------------------------------------------------------------
            # *** EAST & CENTRAL INDIA *** (Approx. 25+ routes)
            # ------------------------------------------------------------------
            ('Kolkata', 'Bhubaneswar', 440),
            ('Kolkata', 'Patna', 580),
            ('Kolkata', 'Ranchi', 400),
            ('Kolkata', 'Guwahati', 1000),
            ('Kolkata', 'Jamshedpur', 280),
            ('Bhubaneswar', 'Cuttack', 30),
            ('Ranchi', 'Jamshedpur', 130),
            ('Raipur', 'Bhubaneswar', 510),
            ('Raipur', 'Bilaspur', 115),
            ('Raipur', 'Jabalpur', 380),
            ('Guwahati', 'Shillong', 100),
            ('Guwahati', 'Agartala', 550),
            ('Bhopal', 'Sagar', 170),
            ('Bhopal', 'Jabalpur', 330),
            ('Raipur', 'Nagpur', 280),
            ('Bilaspur', 'Raipur', 115),
            ('Patna', 'Muzaffarpur', 80),
            ('Jabalpur', 'Nagpur', 270),
            ('Dhanbad', 'Kolkata', 270),
            ('Ranchi', 'Dhanbad', 170),
            
            # ------------------------------------------------------------------
            # *** PAN-INDIA MAJOR CORRIDORS ***
            # ------------------------------------------------------------------
            ('Delhi', 'Mumbai', 1400), 
            ('Kolkata', 'Mumbai', 1960), 
            ('Delhi', 'Kolkata', 1500), 
            ('Bengaluru', 'Delhi', 2160), 
            ('Chennai', 'Kolkata', 1660), 
            ('Bengaluru', 'Mumbai', 980),
            ('Chennai', 'Mumbai', 1250),
        ]

        # Insert data
        cursor.executemany("INSERT INTO routes (source_city, destination_city, distance_km) VALUES (?, ?, ?)", routes_data)
        
        conn.commit()
        print(f"Database '{DB_NAME}' created and populated with {len(routes_data)} routes.")
        
    except sqlite3.Error as e:
        print(f"An error occurred while creating the database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_and_populate_db()