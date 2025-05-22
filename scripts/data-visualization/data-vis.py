import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "influxdata_2025-04-05T13_21_36Z.csv"
df = pd.read_csv(file_path, skiprows=2)  # Skip metadata rows

df.columns = df.iloc[0]  # Set proper column names
df = df[1:].reset_index(drop=True)  # Remove redundant row

# Convert time column to datetime format
df["time"] = pd.to_datetime(df["time"])

# Convert numeric columns to float
numeric_columns = ["pm25", "pm10", "co2", "humidity", "temperature", "no2", "o3", "so2", "dust"]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Plot PM2.5 over time without connecting points
plt.figure(figsize=(12, 6))
plt.scatter(df["time"], df["pm25"], color="b", label="PM2.5")
plt.xlabel("Time")
plt.ylabel("PM2.5 Concentration (µg/m³)")
plt.title("PM2.5 Levels Over Time")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()  # Adjust layout to prevent label cutoff

plt.show()