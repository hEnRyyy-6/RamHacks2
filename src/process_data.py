import json
import pandas as pd
from datetime import datetime
#read in the files 
with open('RAMHACK CASEFILES 4/incident_report_case4.json', 'r') as f:
    incident_data = json.load(f)
print(incident_data)

metro_swipes_df = pd.read_csv('RAMHACK CASEFILES 4/metro_swipes_case4.csv')
print(metro_swipes_df.head())

#read in the files and make them into dataframes
with open('RAMHACK CASEFILES 4/cell_pings_case4.json','r') as f:
    cell_data = json.load(f)
cell_ping_df = pd.DataFrame(cell_data)
print(cell_ping_df.head())

with open('RAMHACK CASEFILES 4/suspects_case4.json', 'r') as f:
    suspects_data = json.load(f)
    suspects_data_df = pd.DataFrame(suspects_data)
print(suspects_data_df.head())


#cell phone pings that were around the time of the incident
#incident time is 2025-04-10T23:15:00
#convert the incident time to a datetime object
incident_time = datetime.strptime('2025-04-10T23:15:00', '%Y-%m-%dT%H:%M:%S')
cell_ping_df['timestamp']= pd.to_datetime(cell_ping_df['timestamp'])
cell_ping_df['time_diff'] = abs((cell_ping_df['timestamp'] - incident_time))
nearby_pings = cell_ping_df[cell_ping_df['time_diff'] <= pd.Timedelta(minutes=10)]
print(nearby_pings)


#merged the suspsecys data frame with the nearby pings to narrow down the suspects
suspects_with_pings = pd.merge(suspects_data_df, nearby_pings, left_on='phone_id', right_on='device_id', how='inner')
print("this are the suspects with pings")
print(suspects_with_pings)

#metro swipes that were around the time of the incident, within 30 minutes
metro_swipes_df['timestamp'] = pd.to_datetime(metro_swipes_df['timestamp'])
swipe_window = pd.Timedelta('30 minutes')
metro_swipes_df['time_diff'] = abs((metro_swipes_df['timestamp'] - incident_time))
nearby_swipes = metro_swipes_df[metro_swipes_df['time_diff'] <= swipe_window]
print("this are the metro swipes that were within 30 minutes of the incident")
print(nearby_swipes)


#suspects that were swiping their cards around the time of the incident
suspects_with_swipes = pd.merge(suspects_data_df, nearby_swipes, left_on='card_id', right_on='card_id', how='inner')
print("this are the suspects with swipes")
print(suspects_with_swipes)

#merge the suspects with pinfs and the suspects ith swiipes to get the final suspects
suspects_final = pd.merge(suspects_with_pings, suspects_with_swipes, on='phone_id', how='inner')
print("this are the final suspects")
print(suspects_final)

#convert to csv files for display
suspects_with_pings.to_csv('src/metro_swipes_final.csv', index=False)

suspects_with_swipes.to_csv('src/suspects_with_swipes_final.csv', index=False)

suspects_final.to_csv('src/suspects_final.csv', index=False)

