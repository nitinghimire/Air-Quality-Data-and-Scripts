import sys
sys.path.insert(0, '../../scripts/datapreprocessing')  # Adjust as needed
from load import load_csv

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Load preprocessed data
pm10_df, pm25_df = load_csv()

# Convert 'time' to datetime and set as index
pm10_df["time"] = pd.to_datetime(pm10_df["time"])
pm10_df = pm10_df.drop_duplicates(subset="time")
pm10_df = pm10_df.set_index("time")

# Resample to hourly frequency and interpolate missing values
pm10_df = pm10_df.resample("1H").mean()
pm10_df["pm10"] = pm10_df["pm10"].interpolate()

# Fit ARIMA model with order (2,1,2)
model = ARIMA(pm10_df["pm10"], order=(2,1,2))
results = model.fit()

# Print model summary
print(results.summary())

# Forecast (fitted values)
pm10_df["forecast"] = results.predict(start=1, end=len(pm10_df)-1, typ="levels")

# Plot actual vs forecast
plt.figure(figsize=(12, 6))
plt.plot(pm10_df.index, pm10_df["pm10"], label="Actual PM10")
plt.plot(pm10_df.index, pm10_df["forecast"], color="red", label="Forecast (ARIMA)")
plt.xlabel("Time")
plt.ylabel("PM10 Concentration (µg/m³)")
plt.title("PM10 Forecast using ARIMA(2,1,2)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
