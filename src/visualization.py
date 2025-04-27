import folium

# Create a base map centered at a location
map_center = [40.730610, -73.935242]  # Coordinates for Midtown University
m = folium.Map(location=map_center, zoom_start=15)

# Plot suspect's locations (dummy example)
for suspect in suspects_data:
    folium.Marker(
        location=[suspect['latitude'], suspect['longitude']],
        popup=suspect['name']
    ).add_to(m)

# Save map to HTML
m.save('suspects_map.html')
