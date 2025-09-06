import serial
import time
import datetime
import schedule
import csv
import os

# --- Configuration ---
# Replace with your actual COM port
port = 'COM5'
# The name of the CSV file to save data
csv_filename = 'sds011_data.csv'
# The location for the log data
location = 'Chandragiri Satungal'
# A shorter timeout (e.g., 5 seconds) is better for robust continuous reading
timeout = 5
# --- End Configuration ---

# AQI Calculation Function (US EPA Standard)
def calculate_aqi(pm25, pm10):
    """Calculates AQI for PM2.5 and PM10 using US EPA breakpoints."""
    def aqi_from_pm(pm, low_break, high_break, low_aqi, high_aqi):
        if pm is None:
            return None
        return round(((high_aqi - low_aqi) / (high_break - low_break)) * (pm - low_break) + low_aqi)

    # AQI calculation for PM2.5
    if pm25 <= 12.0:
        aqi25 = aqi_from_pm(pm25, 0.0, 12.0, 0, 50)
    elif pm25 <= 35.4:
        aqi25 = aqi_from_pm(pm25, 12.1, 35.4, 51, 100)
    elif pm25 <= 55.4:
        aqi25 = aqi_from_pm(pm25, 35.5, 55.4, 101, 150)
    elif pm25 <= 150.4:
        aqi25 = aqi_from_pm(pm25, 55.5, 150.4, 151, 200)
    elif pm25 <= 250.4:
        aqi25 = aqi_from_pm(pm25, 150.5, 250.4, 201, 300)
    elif pm25 > 250.4:
        aqi25 = aqi_from_pm(pm25, 250.5, 500.4, 301, 500)
    else:
        aqi25 = None

    # AQI calculation for PM10
    if pm10 <= 54:
        aqi10 = aqi_from_pm(pm10, 0, 54, 0, 50)
    elif pm10 <= 154:
        aqi10 = aqi_from_pm(pm10, 55, 154, 51, 100)
    elif pm10 <= 254:
        aqi10 = aqi_from_pm(pm10, 155, 254, 101, 150)
    elif pm10 <= 354:
        aqi10 = aqi_from_pm(pm10, 255, 354, 151, 200)
    elif pm10 > 354:
        aqi10 = aqi_from_pm(pm10, 355, 424, 201, 300)
    else:
        aqi10 = None

    if aqi25 is None and aqi10 is None:
        return None
    elif aqi25 is None:
        return aqi10
    elif aqi10 is None:
        return aqi25
    else:
        return max(aqi25, aqi10)

def log_data():
    """Reads sensor data, calculates values, and appends to CSV."""
    ser = None
    try:
        # Initialize the serial connection
        ser = serial.Serial(port, baudrate=9600, timeout=timeout)
        time.sleep(2) # Wait for the sensor to stabilize

        pm25_micrograms, pm10_micrograms, aqi = None, None, None
        
        # Read from sensor
        if ser.in_waiting >= 10:
            data = ser.read(10)
            
            if data[0] == 0xAA and data[1] == 0xC0:
                pm25_low = data[2]
                pm25_high = data[3]
                pm10_low = data[4]
                pm10_high = data[5]

                pm25_raw_val = (pm25_high << 8) | pm25_low
                pm10_raw_val = (pm10_high << 8) | pm10_low
                
                pm25_micrograms = pm25_raw_val / 10.0
                pm10_micrograms = pm10_raw_val / 10.0
                
                aqi = calculate_aqi(pm25_micrograms, pm10_micrograms)
            else:
                ser.flushInput()
                print(f"[{datetime.datetime.now()}] Invalid data packet received.")
        else:
            print(f"[{datetime.datetime.now()}] No data received from sensor.")

    except serial.SerialException as e:
        print(f"[{datetime.datetime.now()}] Serial port error: {e}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] An unexpected error occurred: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to CSV
    try:
        file_exists = os.path.isfile(csv_filename)
        with open(csv_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            if not file_exists:
                csv_writer.writerow(['Date and Time', 'PM 2.5 Value', 'PM 10 Value', 'AQI Value', 'Location'])
            
            csv_writer.writerow([
                current_datetime, 
                f"{pm25_micrograms:.2f}" if pm25_micrograms is not None else "",
                f"{pm10_micrograms:.2f}" if pm10_micrograms is not None else "",
                aqi if aqi is not None else "",
                location
            ])
            print(f"[{current_datetime}] Successfully logged data to {csv_filename}")
    except Exception as e:
        print(f"[{current_datetime}] Error writing to CSV file: {e}")

# Schedule the logging task
schedule.every(30).minutes.do(log_data)
print("Script started. Scheduling data logging every 30 minutes.")

# Run the task immediately once at startup
log_data()

try:
    # Main loop to run the scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Program stopped by user.")

