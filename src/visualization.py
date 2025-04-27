import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


# Load the cleaned CSV files
suspects_final = pd.read_csv('path_to/suspects_final.csv')
suspects_with_pings = pd.read_csv('path_to/suspects_with_pings.csv')
suspects_with_swipes = pd.read_csv('path_to/suspects_with_swipes.csv')

# Merge the datasets
merged_data = pd.merge(suspects_with_pings, suspects_with_swipes, on='name', how='left')
merged_data = pd.merge(merged_data, suspects_final, on='name', how='left')

# Map Locations
map_center = [40.730610, -73.935242]  # Adjust coordinates as needed
m = folium.Map(location=map_center, zoom_start=15)
for _, row in merged_data.iterrows():
    folium.Marker([row['lat'], row['lon']], popup=f"{row['name']} - {row['timestamp_x']}").add_to(m)
m.save('suspects_map.html')

# Visualize Movement over Time
plt.figure(figsize=(10, 6))
for suspect in merged_data['name'].unique():
    suspect_data = merged_data[merged_data['name'] == suspect]
    plt.plot(suspect_data['timestamp_x'], suspect_data['lat'], label=f"{suspect} (Lat)")
    plt.plot(suspect_data['timestamp_y'], suspect_data['lat'], label=f"{suspect} (Swipe)")
plt.xlabel('Time')
plt.ylabel('Latitude')
plt.title('Suspects’ Movement Over Time')
plt.legend()
plt.xticks(rotation=45)
plt.show()

# Visualize Swipes
plt.figure(figsize=(10, 6))
sns.countplot(data=merged_data, x='station', hue='swipe_type', palette='Set1')
plt.xlabel('Station')
plt.ylabel('Number of Swipes')
plt.title('Metro Swipes at Each Station')
plt.xticks(rotation=45)
plt.show()

# Compare Alibis and Activities
for _, row in merged_data.iterrows():
    print(f"Name: {row['name']}")
    print(f"Alibi: {row['alibi_x']}")
    print(f"Last Known Location: {row['lat']}, {row['lon']}")
    print(f"Swipe Time: {row['timestamp_y']}")
    print(f"Swipe Type: {row['swipe_type']}")
    print(f"Time Difference: {row['time_diff_x']}")
    print("-" * 50)

# Visualize Time Differences
plt.figure(figsize=(10, 6))
sns.boxplot(data=merged_data, x='name', y='time_diff_x', palette='Set2')
plt.xlabel('Suspect')
plt.ylabel('Time Difference')
plt.title('Time Differences Between Pings and Swipes')
plt.xticks(rotation=45)
plt.show()

