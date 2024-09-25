# Graphical user interface for route optimization
This project is a web application that uses **Streamlit** and **Folium** to visualize routes and orders on an interactive map. The application decodes routes stored as hashed polylines, displays order locations, logistic centers, and allows users to select specific drivers' routes to be visualized.

## Installation

### Prerequisites

1. You must have **Python 3.x** installed on your system.
2. It is recommended to use a virtual environment (venv) to manage dependencies.

## Create the virtual environment
```bash
python -m venv venv
```
## Install dependencies

Install the required dependencies using the requirements.txt file:
```bash
pip install -r requirements.txt
```
## Project structure 
* ```streamlit_optimized_routes.py``` contains the main code for the application.
* ```locations.json```: JSON file with the coordinates of the orders.
* ```hashed_driver_routes.json```: JSON file with the routes in encoded polyline format.

## Running the application
To run the application, use the following command in your terminal:
```bash
streamlit run streamlit_optimized_routes.py
```
This will open the application in your default browser, where you can interact with the interface and visualize the routes on the map.

### Input data
1. ```locations.json```: contains detailed information about the orders, including the client ID, location (address, latitude, longitude), order details, and status. The structure of each entry is as follows:

   ```bash
    {
        "client_id": 298104694689,
        "location": {
            "address": "Bypass Sur",
            "lat": 40.390130799999994,
            "lon": -3.683518876417766
        },
        "order_id": "498b821e-a8c1-4876-8ecb-05912791d902",
        "order": {
            "n_objects": 5,
            "volume": 80.57954913557874,
            "weight": 16.296355287733935
        },
        "status": "active"
    },
    ...  
   ```
2. ```hashed_driver_routes.json```: contains the driver's routes encoded as polylines. These are decoded to display them on the map.

### User interface
* **Interactive map**: view the orders and logistic centers on a map
* **Driver selection**: choose specific drivers' routes to display using checkboxes in the sidebar
* **Clustered markers**: orders are shown as clustered markers to improve visualization in dense areas.

## Code explanation
### 1. Streamlit configuration
  This configures the Streamlit page to use a wide layout and sets the title of the application.
  ```bash
  st.set_page_config(layout="wide")
  st.title("Optimizador de rutas")
  ```  
### 2. Loading data
  * ```locations.json```: contains the orders coordinates.
  * ```hashed_driver_routes.json```: contains the drivers' routes encoded as polylines.
```bash
with open('locations.json', 'r') as f:
    data = json.load(f)

with open('hashed_driver_routes.json', 'r') as f:
    polylines = json.load(f)
```

### 3. Decoding routes
  The code decodes the routes in polyline format, corrects the coordinates, and stores them in the ```decoded_polylines``` dictionary.
  ```bash
  for driver, encoded_list in polylines.items():
    for encoded_polyline in encoded_list:
        decoded_polyline = polyline.decode(encoded_polyline)
        corrected_polyline = [(lat / 10, lng / 10) for lat, lng in decoded_polyline]

        if driver not in decoded_polylines:
            decoded_polylines[driver] = []
        decoded_polylines[driver].append(corrected_polyline)

 ```
### 4. Sidebar user interface
  The user can select all drivers or individual drivers via checkboxes in the sidebar.
  ```bash
  select_all = st.sidebar.checkbox("Select All Drivers", value=False)
  ```
### 5. Displaying routes and orders
  The interactive map displays the selected routes, orders, and logistic centers with markers.
  ```bash
my_map = folium.Map(location=map_center, zoom_start=map_zoom, tiles='CartoDB Positron')

# Add selected routes to the map
for i, driver in enumerate(selected_drivers):
    for corrected_polyline in decoded_polylines[driver]:
        folium.PolyLine(corrected_polyline, color=colors[i % len(colors)], weight=2.5, opacity=1).add_to(my_map)

#Creation of clustered markers
marker_cluster = MarkerCluster().add_to(my_map)

#Link the clustered markers with the orders locations
for coord in orders_coords:
    folium.Marker(coord, popup="Pedido", tooltip="Pedido").add_to(marker_cluster)
 ```
  
### 6. Rendering the map in streamlit
  The map is rendered within the Streamlit application.
  ```bash
  st_folium(my_map, width=1100, height=700)
  ```
## Example 

 
![streamlit_optimized_routes_01](https://github.com/user-attachments/assets/dbea8ba4-d72b-4fbc-b849-a84646aaa0dd)

*Figure 1 : Only some drivers selected*

![streamlit_optimized_routes_02](https://github.com/user-attachments/assets/438c35f4-ffac-494d-8b17-1838880338a4)

*Figure 2: All drivers selected*
