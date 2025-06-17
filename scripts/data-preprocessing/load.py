import pandas as pd 
import os

path="../../monthly-data"
csv_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".csv")]
all_dfs = []

for file in csv_files:
    df=pd.read_csv(file, skiprows=2)
    df.columns = df.iloc[0]  
    df = df[1:].reset_index(drop=True)  

    df["time"] = pd.to_datetime(df["time"])

    numeric_columns = ["pm25", "pm10", "co2", "humidity", "temperature", "no2", "o3", "so2", "dust"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    all_dfs.append(df)

combined_df = pd.concat(all_dfs, ignore_index=True)

combined_df = combined_df.sort_values("time")
combined_df=combined_df[["pm10","pm25","time"]]
pm10_df=combined_df[["time","pm10"]]
pm25_df=combined_df[["time","pm25"]]
print(pm10_df,pm25_df)

def load_csv():
    return pm10_df,pm25_df