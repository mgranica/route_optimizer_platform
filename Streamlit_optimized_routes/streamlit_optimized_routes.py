import folium
import streamlit as st
from streamlit_folium import st_folium
import polyline
import json
from folium.plugins import MarkerCluster

# Streamlit configuration
st.set_page_config(layout="wide")
st.title("Optimizador de rutas")

# Read the JSON file that contains the orders
with open('locations.json', 'r') as f:
    data = json.load(f)

# Retrieve the coordinates from the orders JSON
orders_coords = [(entry['location']['lat'], entry['location']['lon']) for entry in data]

# Load the routes in the form of a hash
with open('hashed_driver_routes.json', 'r') as f:
    polylines = json.load(f)


colors = [
    'darkblue', 'green', 'red', 'purple', 'brown', 'black', 'darkorange', 'cyan', 'magenta', 'darkslategray', 'darkviolet',
    'yellow', 'indigo', 'crimson', 'navy', 'orange', 'maroon', 'blue'
]


map_center = [40.42113845039438, -3.6950987993307467]
map_zoom = 11

# The decoded routes will be stored in this dict
decoded_polylines = {}

# Decode all the polylines and correct the coordinates
for driver, encoded_list in polylines.items():
    for encoded_polyline in encoded_list:
        decoded_polyline = polyline.decode(encoded_polyline)
        corrected_polyline = [(lat / 10, lng / 10) for lat, lng in decoded_polyline]

        # Add the polyline to the dictionary
        if driver not in decoded_polylines:
            decoded_polylines[driver] = []
        decoded_polylines[driver].append(corrected_polyline)

# Sidebar with checkboxes
st.sidebar.title("Seleccionar Drivers")
select_all = st.sidebar.checkbox("Todos los drivers", value=False)

drivers = list(decoded_polylines.keys())
selected_drivers = []
if select_all:
    selected_drivers = drivers
else:
    for driver in drivers:
        if st.sidebar.checkbox(driver, value=False):
            selected_drivers.append(driver)

# Create the map
my_map = folium.Map(location=map_center, zoom_start=map_zoom, tiles='CartoDB Positron')

# Add selected routes to the map
for i, driver in enumerate(selected_drivers):
    color = colors[i % len(colors)]
    if driver in decoded_polylines:
        for corrected_polyline in decoded_polylines[driver]:
            folium.PolyLine(corrected_polyline, color=color, weight=2.5, opacity=1).add_to(my_map)

#Creation of clustered markers
marker_cluster = MarkerCluster().add_to(my_map)

#Link the clustered markers with the orders locations
for coord in orders_coords:
    folium.Marker(coord, popup="Pedido", tooltip="Pedido").add_to(marker_cluster)

# Add a marker at each logistics center
tooltip = "Centro logístico"
folium.Marker([40.54510, -3.61184], popup="Centro logístico San Sebastián de los Reyes", tooltip=tooltip, icon=folium.Icon(color='green')).add_to(my_map)
folium.Marker([40.350370, -3.855863], popup="Centro logístico Alcorcón", tooltip=tooltip, icon=folium.Icon(color='red')).add_to(my_map)
folium.Marker([40.36977, -3.59670], popup="Centro logístico Vallecas", tooltip=tooltip, icon=folium.Icon(color='blue')).add_to(my_map)


st_folium(my_map, width=1100, height=700)
