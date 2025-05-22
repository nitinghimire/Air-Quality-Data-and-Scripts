import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from statsmodels.tsa.stattools import adfuller

# Directories
data_dir = "../../monthly-data"
figures_dir = "figures"
os.makedirs(figures_dir, exist_ok=True)

# Load CSV files
csv_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".csv")]
all_dfs = []

# Read and preprocess each CSV
for file_path in csv_files:
    df = pd.read_csv(file_path, skiprows=2)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df["time"] = pd.to_datetime(df["time"])
    numeric_columns = ["pm25", "pm10", "co2", "humidity", "temperature", "no2", "o3", "so2", "dust"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    all_dfs.append(df)

# Combine and sort
combined_df = pd.concat(all_dfs, ignore_index=True).sort_values("time")

# Function to perform ADF test
def adf_test(series, label):
    result = adfuller(series.dropna())
    print(f"\nADF Test for {label}")
    print(f"Test Statistic : {result[0]}")
    print(f"p-value        : {result[1]}")
    print("Critical Values:")
    for key, value in result[4].items():
        print(f"  {key} : {value}")
    if result[1] < 0.05:
        print("Likely Stationary ")
    else:
        print("Likely Non-Stationary ")

# Run tests
adf_test(combined_df["pm25"], "PM2.5")
adf_test(combined_df["pm10"], "PM10")

# Plot with rolling mean
for pollutant, color in [("pm25", "blue"), ("pm10", "green")]:
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=combined_df, x="time", y=pollutant, label=pollutant.upper(), color=color)
    sns.lineplot(data=combined_df.set_index("time")[pollutant].rolling(30).mean(), label="Rolling Mean (30d)", color="black")
    plt.title(f"{pollutant.upper()} Over Time with Rolling Mean")
    plt.xlabel("Time")
    plt.ylabel("Concentration (µg/m³)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, f"{pollutant}_adf_plot.png"))
    plt.show()
