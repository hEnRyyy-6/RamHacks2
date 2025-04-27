import pandas as pd
import matplotlib.pyplot as plt

# Load the necessary CSV files
suspects_swipes_final_df = pd.read_csv('src/suspects_with_swipes_final.csv')  # Adjust the path
metro_swipes_df = pd.read_csv('RAMHACK CASEFILES 4/metro_swipes_case4.csv')  # Adjust the path
suspects_df = pd.read_csv('src/suspects_final.csv')  # Adjust the path

# Show basic information about the data
print("Suspects Swipes Final Data")
print(suspects_swipes_final_df.head())

# --- 1. Investigating Metro Swipes at Different Stations ---
# Plot the distribution of the number of swipes at different stations
station_counts = metro_swipes_df['station'].value_counts()

plt.figure(figsize=(10, 6))
station_counts.plot(kind='bar', color='green', alpha=0.7)
plt.title('Number of Metro Swipes at Different Stations', fontsize=16)
plt.xlabel('Station', fontsize=12)
plt.ylabel('Number of Swipes', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# --- 2. Investigating Suspects Swipes and Pings ---
# Investigating the relationship between swipes and pings for each suspect
suspects_swipes_final_df['timestamp'] = pd.to_datetime(suspects_swipes_final_df['timestamp'])

# Create a new column 'event' to distinguish between swipe and ping actions
suspects_swipes_final_df['event'] = suspects_swipes_final_df['swipe_type'].apply(lambda x: 'Swipe' if pd.notna(x) else 'Ping')

# Plot the distribution of events (swipes vs pings) over time
plt.figure(figsize=(10, 6))
plt.scatter(suspects_swipes_final_df['timestamp'], suspects_swipes_final_df['name'], c=suspects_swipes_final_df['event'].map({'Swipe': 'blue', 'Ping': 'red'}), label='Event')
plt.title('Suspects Events Timeline (Swipes and Pings)', fontsize=16)
plt.xlabel('Timestamp', fontsize=12)
plt.ylabel('Suspect Name', fontsize=12)
plt.legend(['Swipe', 'Ping'])
plt.xticks(rotation=45)
plt.show()

# --- 3. Alibi Investigation with Pings and Swipes ---
# Investigating how many suspects have both pings and swipes
suspects_with_both = suspects_swipes_final_df[suspects_swipes_final_df['event'] == 'Ping'].groupby('name').size()

plt.figure(figsize=(10, 6))
suspects_with_both.plot(kind='bar', color='purple', alpha=0.7)
plt.title('Number of Suspects with Both Pings and Swipes', fontsize=16)
plt.xlabel('Suspect', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# --- 4. Investigating Time Differences Between Pings and Swipes ---
# Calculate the time difference between the suspect's swipe and ping events
suspects_swipes_final_df['time_diff'] = suspects_swipes_final_df.groupby('name')['timestamp'].diff().abs()

# Visualizing the time differences between the ping and swipe actions
plt.figure(figsize=(10, 6))
plt.hist(suspects_swipes_final_df['time_diff'].dropna().dt.total_seconds() / 60, bins=20, color='orange', alpha=0.7)
plt.title('Time Difference Between Suspect Pings and Swipes', fontsize=16)
plt.xlabel('Time Difference (Minutes)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.show()

# --- 5. Investigating Suspect Activity Correlation with Metro Swipes ---
# Merging suspects' swipes and metro swipes data based on matching card IDs
merged_df = pd.merge(suspects_swipes_final_df, metro_swipes_df, on='card_id', how='inner')

# Plot the distribution of swipe times for merged data
plt.figure(figsize=(10, 6))
plt.scatter(merged_df['timestamp_x'], merged_df['name'], c=merged_df['swipe_type'].map({'exit': 'green', 'entry': 'red'}), label='Metro Swipe')
plt.title('Suspects Metro Swipe Timeline', fontsize=16)
plt.xlabel('Metro Swipe Timestamp', fontsize=12)
plt.ylabel('Suspect Name', fontsize=12)
plt.legend(['Exit Swipe', 'Entry Swipe'])
plt.xticks(rotation=45)
plt.show()

# --- 6. Investigating Alibis and Metro Swipes ---
# Visualizing how many suspects have an alibi and their corresponding metro swipe data
suspects_with_alibis = suspects_df[suspects_df['alibi_x'].notna()]
suspects_without_alibis = suspects_df[suspects_df['alibi_x'].isna()]

plt.figure(figsize=(8, 6))
plt.bar(['With Alibi', 'Without Alibi'], [len(suspects_with_alibis), len(suspects_without_alibis)], color=['blue', 'red'], alpha=0.7)
plt.title('Number of Suspects With and Without Alibi', fontsize=16)
plt.ylabel('Count', fontsize=12)
plt.show()
