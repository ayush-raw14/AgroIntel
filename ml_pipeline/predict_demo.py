import joblib
import pandas as pd
import numpy as np
import os

def load_model():

    if not os.path.exists('moisture_predictor.pkl'):
        print("  Error: Model file 'moisture_predictor.pkl' not found!")
        print("  Please run the 'train_model.py' first.")
        return None, None
    
    model = joblib.load('moisture_predictor.pkl')
    model_info = joblib.load('model_info.pkl')

    return model, model_info

def predict_next_day_moisture(model, current_readings):

    # create a dataframe with req features
    X_current = pd.DataFrame([current_readings])

    # make predictions
    predicted_moisture = model.predict(X_current)[0]

    return predicted_moisture

def gen_recommendation(current_moisture, predicted_moisture, temp):

    print("\n" + "=" * 70)
    print("  IRRIGATION RECOMMENDATION")
    print("=" * 70)
    
    print(f"\n  Current Status:")
    print(f"   Current soil moisture: {current_moisture:.1f}%")
    print(f"   Predicted tomorrow:    {predicted_moisture:.1f}%")
    print(f"   Current temperature:   {temp:.1f}°C")

    print(f"\n  AI Analysis:")

    #decision logic

    if predicted_moisture < 30:
        status = "🔴 CRITICAL"
        action = "IMMEDIATE IRRIGATION REQUIRED"
        details = f"irrigate 12-15 L/acre tomorrow morning (6-8 AM)"
        print(f"   Status: {status}")
        print(f"   Action: {action}")
        print(f"   Details: {details}")
        print(f"   Reason: Moisture predicted to drop below critical threshold")

    elif predicted_moisture < 40:
        status = "🟡 WARNING"
        action = "MONITOR CLOSELY - IRRIGATION MAY BE NEEDED"
        details = f"Prepare for irrigation in 24-48 hours"
        print(f"   Status: {status}")
        print(f"   Action: {action}")
        print(f"   Details: {details}")
        print(f"   Reason: Moisture approaching low levels")
    
    elif predicted_moisture > 70:
        status = "🔵 HIGH"
        action = "NO IRRIGATION NEEDED"
        details = f"Soil moisture is adequate. Save water and costs."
        print(f"   Status: {status}")
        print(f"   Action: {action}")
        print(f"   Details: {details}")
        print(f"   Reason: Moisture levels are optimal")
    
    else:
        status = "🟢 OPTIMAL"
        action = "NO IRRIGATION NEEDED"
        details = f"Soil moisture is in optimal range"
        print(f"   Status: {status}")
        print(f"   Action: {action}")
        print(f"   Details: {details}")
        print(f"   Reason: Moisture levels are healthy")
    
    print("\n" + "=" * 70)

def main():

    print("=" * 70)
    print("AgroIntel: Next-Day Soil Moisture Prediction Demo")
    print("=" * 70)

    # load model
    print("\n  Loading trained model...")
    model, model_info = load_model()

    if model is None:
        return
    
    print(f"  Model loaded succesfully")
    print(f"  Model MAE: {model_info['test_mae']:.2f}%")

    # simulate current sensor readings

    print("\n  Simulating current sensor readings...")
    current_readings = {
        'moisture_lag_24h': 35.5,          # Yesterday's moisture
        'temp_lag_24h': 28.3,              # Yesterday's temperature
        'humidity_lag_24h': 55.2,          # Yesterday's humidity
        'moisture_rolling_mean_24h': 37.8, # 24h average moisture
        'temp_rolling_mean_24h': 27.1,     # 24h average temperature
        'soil_pH': 6.4                     # Current pH
    }

    print(f"  Yesterday's moisture:{current_readings['moisture_lag_24h']:.1f}%")
    print(f"  Yesterday's temperature:{current_readings['temp_lag_24h']:.1f}°C")
    print(f"  24h average moisture: {current_readings['moisture_rolling_mean_24h']:.1f}%")

    # predict
    print("\n Making prediction...")
    predicted_moisture = predict_next_day_moisture(model, current_readings)
    print(f"  Prediction complete")

    # generate recommendations
    gen_recommendation(
        current_moisture = current_readings['moisture_lag_24h'],
        predicted_moisture = predicted_moisture,
        temp = current_readings['temp_lag_24h']
    )

    print("\n  Next Steps:")
    print("   1. Integrate this model into FastAPI backend")
    print("   2. Schedule daily predictions at 18:00")
    print("   3. Display recommendations on farmer dashboard")
    print("   4. Replace synthetic data with real ESP32 readings")
    
    print("\n" + "=" * 70) 

if __name__ == "__main__":
    main()
