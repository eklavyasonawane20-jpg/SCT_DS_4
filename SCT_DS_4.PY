# ---------------------------------------------------
# Task 04: Accident Data Analysis (Custom Dataset)
# ---------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import random
from IPython.display import display  # Jupyter/Colab me map dikhane ke liye

# ===============================
# Step 1: Prepare Custom Dataset
# ===============================

# Dhule ka center point
base_lat, base_lon = 21.1899, 74.9040

# Dhule ke 20 random points (thoda spread karke)
dhule_locations = [[base_lat + random.uniform(-0.002, 0.002),
                    base_lon + random.uniform(-0.002, 0.002)] for _ in range(20)]

# Extra jagah ke points
sakri = [[20.9015, 74.5201], [20.9015, 74.5201]]
ner = [[20.7429, 74.9431]]
svkm_dhule = [[21.1905, 74.9050], [21.1905, 74.9050]]

# Sabko ek jagah jodna
points_all = dhule_locations + sakri + ner + svkm_dhule

# Dataset create karna
records = {
    "Accident_ID": range(1, 26),
    "Road_Conditions": [
        "Dry","Wet","Icy","Snow","Dry",
        "Wet","Dry","Snow","Icy","Dry",
        "Dry","Wet","Dry","Snow","Icy",
        "Dry","Wet","Dry","Snow","Icy",   # Dhule 20
        "Wet","Dry",                       # Sakri 2
        "Dry",                             # Ner 1
        "Dry","Dry"                        # SVKM Dhule 2
    ],
    "Weather_Conditions": [
        "Clear","Rain","Fog","Snow","Clear",
        "Rain","Clear","Snow","Fog","Clear",
        "Rain","Clear","Snow","Clear","Rain",
        "Fog","Clear","Clear","Rain","Snow",  # Dhule 20
        "Rain","Clear",                        # Sakri
        "Fog",                                 # Ner
        "Clear","Clear"                        # SVKM Dhule
    ],
    "Time": [
        "08:15","09:30","22:00","18:45","14:20",
        "16:10","07:50","21:10","23:40","12:30",
        "13:50","17:25","20:15","19:40","08:00",
        "05:30","06:45","11:10","15:00","09:10",   # Dhule 20
        "10:20","12:15",                             # Sakri
        "14:40",                                     # Ner
        "16:30","18:20"                              # SVKM Dhule
    ],
    "Latitude": [loc[0] for loc in points_all],
    "Longitude": [loc[1] for loc in points_all],
    "Contributing_Factor": [
        "Speeding","Alcohol","Distracted Driving","Weather","Speeding",
        "Alcohol","Speeding","Distracted Driving","Weather","Speeding",
        "Speeding","Alcohol","Distracted Driving","Weather","Speeding",
        "Alcohol","Speeding","Distracted Driving","Weather","Speeding",  # Dhule
        "Alcohol","Speeding",                                             # Sakri
        "Distracted Driving",                                             # Ner
        "Weather","Speeding"                                              # SVKM Dhule
    ]
}

df = pd.DataFrame(records)

# Save CSV
df.to_csv("Accident_Dataset_Custom_AllPoints.csv", index=False)
print("✅ Custom Accident Dataset ready!")
print(df)

# ===============================
# Step 2: Visualization
# ===============================

# Road Condition wise
plt.figure(figsize=(8,5))
sns.countplot(data=df, x="Road_Conditions", order=df["Road_Conditions"].value_counts().index, palette="Set2")
plt.title("Accidents by Road Conditions")
plt.xticks(rotation=45)
plt.show()

# Weather wise
plt.figure(figsize=(8,5))
sns.countplot(data=df, x="Weather_Conditions", order=df["Weather_Conditions"].value_counts().index, palette="Set3")
plt.title("Accidents by Weather Conditions")
plt.xticks(rotation=45)
plt.show()

# Hour wise
df["Hour"] = pd.to_datetime(df["Time"], errors="coerce").dt.hour
plt.figure(figsize=(10,5))
sns.countplot(data=df, x="Hour", palette="Set1")
plt.title("Accidents by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Accidents")
plt.show()

# Contributing Factors
plt.figure(figsize=(10,5))
sns.countplot(data=df, y="Contributing_Factor", order=df["Contributing_Factor"].value_counts().index, palette="Pastel1")
plt.title("Top Contributing Factors in Accidents")
plt.show()

# ===============================
# Step 3: Accident Hotspot Map
# ===============================

center_point = [df["Latitude"].mean(), df["Longitude"].mean()]
accident_map = folium.Map(location=center_point, zoom_start=10)

color_scheme = {
    "Speeding": "red",
    "Alcohol": "blue",
    "Distracted Driving": "green",
    "Weather": "orange"
}

# Har accident map par plot karna
for _, r in df.iterrows():
    info = f"""
    <b>Accident ID:</b> {r['Accident_ID']}<br>
    <b>Road:</b> {r['Road_Conditions']}<br>
    <b>Weather:</b> {r['Weather_Conditions']}<br>
    <b>Factor:</b> {r['Contributing_Factor']}
    """
    folium.CircleMarker(
        location=[r["Latitude"], r["Longitude"]],
        radius=6,
        color=color_scheme.get(r["Contributing_Factor"], "gray"),
        fill=True,
        fill_opacity=0.7,
        popup=info
    ).add_to(accident_map)

# Notebook me direct show karne ke liye
display(accident_map)

# HTML file bhi save ho jaye
accident_map.save("accident_hotspots_all_points.html")
print("✅ Accident Hotspot Map saved as accident_hotspots_all_points.html")
