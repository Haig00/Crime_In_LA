import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os

# 📁 Create directory to save plots
os.makedirs("plots", exist_ok=True)

# 📥 Load data and parse date columns
df = pd.read_csv("crimes.csv", parse_dates=['Date Rptd', 'DATE OCC'], dtype={'Time OCC': str})
sns.set_theme(style='whitegrid')

# --------------------------------------------------------
# 🕒 Extract hour of crime
df['TIME OCC'] = df['TIME OCC'].fillna('0000').astype(str).str.zfill(4)
df = df[df['TIME OCC'].str.isnumeric()]
df['hour_of_crime'] = df['TIME OCC'].str[:2].astype(int)

# --------------------------------------------------------
# 🎯 Question 1: Peak hour of crime
crime_by_hour = df['hour_of_crime'].value_counts().sort_index()
peak_crime_hour = crime_by_hour.idxmax()
print(f"🔹 Peak Crime Hour: {peak_crime_hour}:00")

# 📊 Plot: Crimes by hour
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x='hour_of_crime', bins=24, discrete=True, color='crimson')
plt.title("Crimes by Hour of the Day")
plt.xlabel("Hour (0–23)")
plt.ylabel("Number of Crimes")
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig("plots/crimes_by_hour.png")
plt.close()

# --------------------------------------------------------
# 🌙 Question 2: Night crime location (10 PM – 4 AM)
night_crimes = df[(df['hour_of_crime'] >= 22) | (df['hour_of_crime'] <= 3)]
peak_night_crime_location = night_crimes['AREA NAME'].value_counts().idxmax()
print(f"🔹 Peak Night Crime Location: {peak_night_crime_location}")

# 📊 Plot: Night crimes by area
plt.figure(figsize=(12, 6))
sns.countplot(data=night_crimes, x='AREA NAME', order=night_crimes['AREA NAME'].value_counts().index, color='navy')
plt.title("Night Crimes by Area (10 PM – 4 AM)")
plt.xlabel("Area Name")
plt.ylabel("Crime Count")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("plots/night_crimes_by_area.png")
plt.close()

# --------------------------------------------------------
# 🧒 Question 3: Crimes by victim age group
bins = [0, 17, 25, 34, 44, 54, 64, 150]
labels = ["0-17", "18-25", "26-34", "35-44", "45-54", "55-64", "65+"]
df['victim_age_group'] = pd.cut(df['Vict Age'], bins=bins, labels=labels, right=True)

victim_ages = df['victim_age_group'].value_counts().sort_index()
print("\n🔹 Crimes by Victim Age Group:")
print(victim_ages)

# 📊 Plot: Victim age group distribution
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='victim_age_group', order=labels, color='teal')
plt.title("Crimes by Victim Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Crimes")
plt.tight_layout()
plt.savefig("plots/victim_age_distribution.png")
plt.close()
