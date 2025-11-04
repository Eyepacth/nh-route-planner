# 🛣️ Enhanced National Highway Route Planner

### 👨‍💻 Author
**Ashara Ashish**  
Information Technology Department  
Marwadi University, Rajkot  
Course: *PROGRAMMING WITH PYTHON(01AI0302)*

---

## 🚀 Project Overview
The **Enhanced National Highway Route Planner** is a Python-based desktop application that helps users find the **shortest route** between two Indian cities using **Dijkstra’s Algorithm**.  
It estimates the **total distance**, **travel time**, and suggests a **departure time** to ensure the traveler arrives before **6 PM (daylight arrival)**.

This project demonstrates key Python concepts including:
- Database handling with **SQLite**
- Graph algorithms (**Dijkstra**)
- **Tkinter GUI** design
- Modular programming
- Exception handling
- Date & time manipulation

---

## 🧩 Project Structure

| File | Description |
|------|--------------|
| `G1.py` | Creates and populates the SQLite database (`nh_routes.db`) with highway routes. |
| `G2.py` | Implements Dijkstra’s algorithm and travel-time calculations. |
| `G3.py` | Provides the user interface using Tkinter to find and display routes. |
| `requirements.txt` | Contains the required Python modules. |
| `README.md` | Project documentation and instructions. |

---

## 🧠 Features
✅ Shortest path finder using **Dijkstra’s Algorithm**  
✅ **SQLite**-based database for routes  
✅ **Tkinter GUI** for user interaction  
✅ **Arrival time suggestion** (ensures arrival before 6 PM)  
✅ **Error handling** for invalid or missing inputs  
✅ Modular and maintainable code (DB + Logic + GUI separation)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/asharaashish/nh-route-planner.git
cd nh-route-planner
