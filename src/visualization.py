import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium


suspects_final = pd.read_csv('path_to/suspects_final.csv')
suspects_with_pings = pd.read_csv('path_to/suspects_with_pings.csv')
suspects_with_swipes = pd.read_csv('path_to/suspects_with_swipes.csv')

