import json
import pandas as pd
from datetime import datetime

with open('/Users/henryvelasquez/RamsHackathon/RamsHackathon/RamHacks2/RAMHACK CASEFILES 4/incident_report_case4.json', 'r') as f:
    incident_data = json.load(f)
print(incident_data)

with open('/Users/henryvelasquez/RamsHackathon/RamsHackathon/RamHacks2/RAMHACK CASEFILES 4/cell_pings_case4.json','r') as f:
    cell_data = json.load(f)
cell_ping_df = pd.DataFrame(cell_data)
print(cell_ping_df.head())

with open('/Users/henryvelasquez/RamsHackathon/RamsHackathon/RamHacks2/RAMHACK CASEFILES 4/suspects_case4.json', 'r') as f:
    suspects_data = json.load(f)
    suspects_data_df = pd.DataFrame(suspects_data)
print(suspects_data_df.head())

metro_swipes_df = pd.read_csv('/Users/henryvelasquez/RamsHackathon/RamsHackathon/RamHacks2/RAMHACK CASEFILES 4/metro_swipes_case4.csv')
print(metro_swipes_df.head())

incident_time = datetime.strptime('2025-04-10T23:15:00', '%Y-%m-%dT%H:%M:%S')
cell_ping_df['timestamp']= pd.to_datetime(cell_ping_df['timestamp'])
cell_ping_df['time_diff'] = abs((cell_ping_df['timestamp'] - incident_time))
nearby_pings = cell_ping_df[cell_ping_df['time_diff'] <= pd.Timedelta(minutes=10)]
print(nearby_pings)

suspects_with_pings = pd.merge(suspects_data_df, nearby_pings, left_on='phone_id', right_on='device_id', how='inner')
print("this are the suspects with pings")
print(suspects_with_pings)


metro_swipes_df['timestamp'] = pd.to_datetime(metro_swipes_df['timestamp'])
swipe_window = pd.Timedelta('30 minutes')
metro_swipes_df['time_diff'] = abs((metro_swipes_df['timestamp'] - incident_time))
nearby_swipes = metro_swipes_df[metro_swipes_df['time_diff'] <= swipe_window]
print("this are the metro swipes that were within 30 minutes of the incident")
print(nearby_swipes)

suspects_with_pings = pd.merge(suspects_data_df, nearby_pings, left_on='phone_id', right_on='device_id', how='inner')
print("this are the suspects with pings")
print(suspects_with_pings)


suspects_with_swipes = pd.merge(suspects_data_df, nearby_swipes, left_on='card_id', right_on='card_id', how='inner')
print("this are the suspects with swipes")
print(suspects_with_swipes)


suspects_final = pd.merge(suspects_with_pings, suspects_with_swipes, on='phone_id', how='inner')
print("this are the final suspects")
print(suspects_final)


suspects_with_pings.to_csv('/Users/henryvelasquez/RamsHackathon/RamsHackathon/RamHacks2/src/suspects_with_pings.csv', index=False)

suspects_with_swipes.to_csv('/Users/henryvelasquez/RamsHackathon/RamsHackathon/RamHacks2/src/suspects_with_swipes.csv', index=False)

suspects_final.to_csv('/Users/henryvelasquez/RamsHackathon/RamsHackathon/RamHacks2/src/suspects_final.csv', index=False)

