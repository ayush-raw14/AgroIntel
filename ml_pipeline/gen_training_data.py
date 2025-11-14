import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Calculate total number of readings

def gen_synthetic_sensor_data(days=30, freq='h'):
    if freq == 'h':
        periods = days * 24
    elif freq == '15min':
        periods = days * 24 * 4
    else:
        periods = days * 24
    
    print(f"Generating {periods} sensor readings over {days} days...")

    # Generate timestamps
    dates = pd.date_range(
        end = datetime.now(),
        periods = periods,
        freq = freq
    )

    # Set random seed for reproducibility
    np.random.seed(42)

    # Realistic Pattern for Soil Moisture Simulator : daily cycle + gradual drying + random variations
    
    base_moisture = 45 # base moisture percent
    moisture = []

    for i in range(len(dates)):
        # daily cycle
        hour_of_day = dates[i].hour
        daily_cycle = 10 * np.sin(2 * np.pi * (hour_of_day - 6)/24)

        # gradual drying
        drift = -0.02 * i

        # random sensor noise
        noise = np.random.normal(0,3)

        # calculate moisture and keep in realistic bounds (15-85%)

        current_moisture = base_moisture + daily_cycle + drift + noise

        moisture.append(max(15,min(85, current_moisture)))

        # realistic Temperature Simulation Pattern
    temp = []
    for i in range(len(dates)):
        hour_of_day = dates[i].hour

        # daily temp cycle i.e, cooling at night, hotter at noon

        daily_temp = 25 + 8 * np.sin(2*np.pi * (hour_of_day-6)/24)

        # random variations
        temp_noise = np.random.normal(0,2)

        # keep in realistic bounds (15-40 Celsius)
        current_temp = daily_temp + temp_noise
        temp.append(max(15,min(40,current_temp)))

    # humidity simulation inversely corr. with temperature
    humidity = []
    for i in range(len(dates)):
        # base humidity
        base_humidity = 60

        # inverse relation w temperature
        temp_effect = -0.5 * (temp[i]-25)

        # random variations
        humidity_noise = np.random.normal(0,5)

        # keep in realistic bounds (20-95%)
        current_humidity = base_humidity + temp_effect + humidity_noise
        humidity.append(max(20, min(95, current_humidity)))

    # soil pH simulation

    soil_pH = np.random.normal(6.5,0.3,len(dates))

    # keep in realistic bounds
    soil_pH = np.clip(soil_pH, 5.0, 8.0)

    # create dataframe df
    df = pd.DataFrame({
        'timestamp': dates,
        'soil_moisture': moisture,
        'temp_c': temp,
        'humidity': humidity,
        'soil_pH': soil_pH
    })

    # round values for realism
    df['soil_moisture'] = df['soil_moisture'].round(1)
    df['temp_c'] = df['temp_c'].round(1)
    df['humidity'] = df['humidity'].round(1)
    df['soil_pH'] = df['soil_pH'].round(2)

    return df

def main():

    print("=" * 60)
    print("AgroIntel:Synthetic Sensor Data Generator")
    print("=" * 60)

    # generate data
    df = gen_synthetic_sensor_data(days=30, freq='h')

    # display basic stats

    print("\n  Dataset Stats:")
    print(f"  Total Readings {len(df)}")
    print(f"  Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"\n  Soil Moisture: {df['soil_moisture'].min():.1f}%-{df['soil_moisture'].max():.1f}%")
    print(f"  Temperature: {df['temp_c'].min():.1f}°C - {df['temp_c'].max():.1f}°C")
    print(f"  Humidity: {df['humidity'].min():.1f}% - {df['humidity'].max():.1f}%")
    print(f"  Soil pH: {df['soil_pH'].min():.2f} - {df['soil_pH'].max():.2f}")

    # show first few rows
    print("\n  Sample Data (first 5 rows):")
    print(df.head())

    # save to a csv
    output_file = 'sensor_data.csv'
    df.to_csv(output_file, index=False)
    print(f"\n  Data saved to '{output_file}'")
    print(f"  File size: {len(df)} rows x {len(df.columns)} columns")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()



