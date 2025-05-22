import pandas as pd
import matplotlib.pyplot as plt
import os

# Directories
data_dir = "../../monthly-data"
figures_dir = "figures"

# Create figures directory if it doesn't exist
os.makedirs(figures_dir, exist_ok=True)

# Get all CSV file paths in the directory
csv_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".csv")]

# List to store individual dataframes
all_dfs = []

# Process each file
for file_path in csv_files:
    df = pd.read_csv(file_path, skiprows=2)  # Skip metadata rows
    df.columns = df.iloc[0]  # Set correct column names
    df = df[1:].reset_index(drop=True)  # Remove redundant row

    # Convert time column to datetime
    df["time"] = pd.to_datetime(df["time"])

    # Convert relevant columns to numeric
    numeric_columns = ["pm25", "pm10", "co2", "humidity", "temperature", "no2", "o3", "so2", "dust"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    all_dfs.append(df)

# Concatenate all dataframes
combined_df = pd.concat(all_dfs, ignore_index=True)

# Sort by time
combined_df = combined_df.sort_values("time")

# Plot PM2.5
plt.figure(figsize=(12, 6))
plt.scatter(combined_df["time"], combined_df["pm25"], color="b", label="PM2.5", s=10)
plt.xlabel("Time")
plt.ylabel("PM2.5 Concentration (µg/m³)")
plt.title("PM2.5 Levels Over Time")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "pm25_plot.png"))
plt.show()

# Plot PM10
plt.figure(figsize=(12, 6))
plt.scatter(combined_df["time"], combined_df["pm10"], color="g", label="PM10", s=10)
plt.xlabel("Time")
plt.ylabel("PM10 Concentration (µg/m³)")
plt.title("PM10 Levels Over Time")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "pm10_plot.png"))
plt.show()
