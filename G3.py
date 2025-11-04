import tkinter as tk
from tkinter import messagebox, font as tkfont
import math

# NOTE: Import the constant for display
# Assuming G2.py contains:
# find_route(source, destination) -> (path_list, distance_float, departure_time_str, total_time_hours_float)
# AVG_SPEED_KMH
from G2 import find_route, AVG_SPEED_KMH 

class RouteFinderApp:
    def __init__(self, master):
        self.master = master
        master.title("🛣️ Enhanced National Highway Route Planner")
        master.geometry("700x700") 
        master.minsize(650, 650)
        
        # --- Configuration and Styles (Dark Theme with Differentiated Highlights) ---
        self.bg_color = "#000000"       # Black background for the window
        self.frame_bg = "#212121"       # Dark gray for main containers
        self.output_bg = "#424242"      # Requested Grey for output/summary areas
        self.primary_color = "#6aa84f"   # Requested Light Green for headers/buttons
        self.accent_route_highlight = "#ffdd57" # Light Yellow/Gold for route cities
        self.text_color = "#ffffff"     # White for main text
        
        # Specific highlight colors for summary box
        self.color_distance = "#66ff66" # Bright Green
        self.color_time = "#66ffff"     # Bright Cyan (New highlight)
        self.color_departure = "#ff6666" # Bright Red
        
        master.config(bg=self.bg_color)
        
        self.title_font = tkfont.Font(family="Roboto", size=22, weight="bold")
        self.header_font = tkfont.Font(family="Roboto", size=14, weight="bold")
        self.main_font = tkfont.Font(family="Arial", size=11)
        self.info_font = tkfont.Font(family="Arial", size=12, weight="bold")
        
        master.grid_columnconfigure(0, weight=1)
        
        # --- Main Container Frame (Centralizes content) ---
        main_container = tk.Frame(master, bg=self.bg_color)
        main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)

        # --- Title and Header ---
        
        self.logo_label = tk.Label(main_container,
                                   text="Marwadi University | Highway Route Finder",
                                   font=tkfont.Font(family="Times New Roman", size=10, weight="bold"),
                                   bg=self.primary_color, # Light Green background
                                   fg="#000000",          # Black text for contrast
                                   pady=5)
        self.logo_label.grid(row=0, column=0, sticky="ew")
        
        self.header_label = tk.Label(main_container, 
                                     text="National Route Planner 🗺️", 
                                     font=self.title_font, 
                                     bg=self.frame_bg, 
                                     fg=self.primary_color, 
                                     pady=15)
        self.header_label.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # --- Input Frame ---
        input_frame = tk.Frame(main_container, bg=self.frame_bg, padx=25, pady=25, 
                               relief=tk.RIDGE, bd=2, highlightbackground=self.primary_color, highlightthickness=1)
        input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Source City
        self.label_source = tk.Label(input_frame, text="Source City:", font=self.header_font, fg=self.text_color, bg=self.frame_bg)
        self.label_source.grid(row=0, column=0, padx=(0, 15), pady=15, sticky="w")
        self.entry_source = tk.Entry(input_frame, width=40, font=self.main_font, relief=tk.FLAT, bd=2, bg="#333333", fg=self.text_color, insertbackground=self.text_color)
        self.entry_source.grid(row=0, column=1, padx=(10, 0), pady=15, sticky="ew")
        
        # Destination City
        self.label_dest = tk.Label(input_frame, text="Destination City:", font=self.header_font, fg=self.text_color, bg=self.frame_bg)
        self.label_dest.grid(row=1, column=0, padx=(0, 15), pady=15, sticky="w")
        self.entry_dest = tk.Entry(input_frame, width=40, font=self.main_font, relief=tk.FLAT, bd=2, bg="#333333", fg=self.text_color, insertbackground=self.text_color)
        self.entry_dest.grid(row=1, column=1, padx=(10, 0), pady=15, sticky="ew")
        
        # Find Route Button
        self.find_button = tk.Button(main_container, 
                                     text="🚀 Find Optimal Route", 
                                     command=self.find_route_action, 
                                     font=('Roboto', 14, 'bold'), 
                                     bg=self.primary_color, # Light Green button
                                     fg="#000000",          # Black text for contrast
                                     activebackground="#8fbc8f", 
                                     activeforeground="#000000",
                                     relief=tk.FLAT, 
                                     bd=0,
                                     padx=30, 
                                     pady=10,
                                     cursor="hand2")
        self.find_button.grid(row=3, column=0, pady=20, sticky="n")
        
        # --- Travel Summary Section (Output Grey BG) ---
        self.summary_frame = tk.Frame(main_container, bg=self.output_bg, padx=15, pady=15, 
                                      relief=tk.SUNKEN, bd=1, highlightbackground=self.primary_color, highlightthickness=1)
        self.summary_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)

        summary_header = tk.Label(self.summary_frame, text="--- Travel Summary ---", font=self.header_font, fg=self.accent_route_highlight, bg=self.output_bg)
        summary_header.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Est. Time Display (Top Right Corner of Summary Frame)
        self.label_time = tk.Label(self.summary_frame, text="Est. Time: ---", font=self.info_font, fg=self.color_time, bg=self.output_bg, anchor="e")
        # Placing it in a specific cell for corner look. Moved from row 1, col 1
        self.label_time.grid(row=1, column=1, padx=10, pady=5, sticky="e") 
        
        # Distance Display (Top Left)
        self.label_distance = tk.Label(self.summary_frame, text="Total Distance: ---", font=self.info_font, fg=self.color_distance, bg=self.output_bg, anchor="w") 
        self.label_distance.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        # Departure Time Display (Below, Full width) 
        self.label_departure = tk.Label(self.summary_frame, text="Suggest Leave Time: ---", font=self.info_font, fg=self.color_departure, bg=self.output_bg, pady=5)
        self.label_departure.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # --- Route Section Header ---
        self.label_route_header = tk.Label(main_container, text="Detailed Route Path:", font=self.header_font, fg=self.text_color, bg=self.bg_color)
        self.label_route_header.grid(row=5, column=0, pady=(10, 5), sticky="w", padx=20)
        
        # --- Route Section (Text Area with Scrollbar - Output Grey BG) ---
        route_frame = tk.Frame(main_container)
        route_frame.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew")
        route_frame.grid_columnconfigure(0, weight=1)
        route_frame.grid_rowconfigure(0, weight=1)

        scrollbar = tk.Scrollbar(route_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.route_text = tk.Text(route_frame, 
                                   height=8, 
                                   wrap=tk.WORD, 
                                   font=self.main_font, 
                                   bg=self.output_bg, # Output Grey background
                                   fg=self.text_color, 
                                   relief=tk.FLAT, 
                                   bd=1,
                                   yscrollcommand=scrollbar.set)
        self.route_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.route_text.yview, troughcolor=self.output_bg, bg=self.frame_bg)
        
        # --- Bindings ---
        self.entry_source.bind('<Return>', lambda event: self.entry_dest.focus_set())
        self.entry_dest.bind('<Return>', lambda event: self.find_route_action())
        self.entry_source.focus_set()


    def format_time(self, hours):
        """Formats hours into Days, Hours, Minutes string."""
        days = math.floor(hours / 24)
        remaining_hours = hours % 24
        h = math.floor(remaining_hours)
        m = math.floor((remaining_hours - h) * 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days} Day{'s' if days > 1 else ''}")
        if h > 0:
            parts.append(f"{h} Hour{'s' if h > 1 else ''}")
        # Only show minutes if it's less than a day trip
        if m > 0 and not days:
            parts.append(f"{m} Min{'s' if m > 1 else ''}")

        if not parts:
            return "Less than 1 hour"
            
        return ", ".join(parts)


    def find_route_action(self):
        """Handles the button click event: gets input, calls the logic, and displays results."""
        # Logic remains unchanged
        source = self.entry_source.get().strip().title()
        destination = self.entry_dest.get().strip().title()

        if not source or not destination:
            messagebox.showerror("Input Error", "Please enter both a **Source** and a **Destination** city.")
            return

        self.route_text.delete(1.0, tk.END)
        self.label_distance.config(text="Total Distance: Calculating...")
        self.label_time.config(text="Est. Time: Calculating...")
        self.label_departure.config(text="Suggest Leave Time: Calculating...")

        try:
            result = find_route(source, destination)
            if not result or result[0] is None:
                error_message = result[1] if isinstance(result, tuple) and len(result) > 1 else "No route found."
                messagebox.showerror("Route Error", error_message)
                self.reset_summary()
                return
                
            path, distance, departure_time, total_time_hours = result

        except Exception as e:
            messagebox.showerror("System Error", f"An unexpected error occurred during route finding: {e}")
            self.reset_summary()
            return
            
        # --- Display Summary (Updated Colors/Format) ---
        formatted_time = self.format_time(total_time_hours)
        
        self.label_distance.config(text=f"Total Distance: {distance:.2f} km 🛣️", fg=self.color_distance)
        self.label_time.config(text=f"Est. Time (@{AVG_SPEED_KMH} km/h): {formatted_time} ⏱️", fg=self.color_time)
        self.label_departure.config(text=f"Suggest Leave Time: {departure_time} (To arrive by 6 PM)", fg=self.color_departure)

        # --- Format and Display Detailed Route (Updated Highlight) ---
        route_lines = []
        num_cities = len(path)
        
        # Add a title line for the route
        route_lines.append(f"--- Shortest Route Path from {path[0]} to {path[-1]} ---")
        
        for i, city in enumerate(path):
            # City line: e.g., "1. **Ahmedabad**"
            route_lines.append(f"\n{i+1}. **{city}**")
            
            # Add the arrow for all cities except the last one
            if i < num_cities - 1:
                route_lines.append("     ↓") 
        
        route_output = "\n".join(route_lines)
        
        self.route_text.insert(tk.END, route_output)
        self.route_text.config(fg=self.text_color)
        
        # Apply tag for bolding (uses the new accent color for highlight)
        self.route_text.tag_configure("bold", font=self.info_font, foreground=self.accent_route_highlight)
        
        # Bolding city names
        for i, city in enumerate(path):
            start_index = self.route_text.search(city, f"{i+2}.0", tk.END, nocase=1) 
            if start_index:
                 end_index = f"{start_index}+{len(city)}c"
                 self.route_text.tag_add("bold", start_index, end_index)
        
        
    def reset_summary(self):
        """Resets the summary section on error."""
        self.label_distance.config(text="Total Distance: ---", fg=self.color_distance)
        self.label_time.config(text="Est. Time: ---", fg=self.color_time)
        self.label_departure.config(text="Suggest Leave Time: ---", fg=self.color_departure)


if __name__ == '__main__':
    root = tk.Tk()
    app = RouteFinderApp(root)
    root.mainloop()