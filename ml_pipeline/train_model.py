import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os


def create_lag_feat(df):
    """Create lag features for time-series prediction."""
    
    print("\n🔧 Engineering features from time-series data...")

    # Lag features: yesterday's values
    df['moisture_lag_24h'] = df['soil_moisture'].shift(24)
    df['temp_lag_24h'] = df['temp_c'].shift(24)              # FIXED: added 'h'
    df['humidity_lag_24h'] = df['humidity'].shift(24)        # FIXED: added 'h'

    # Rolling stats: avg over last 24 hours
    df['moisture_rolling_mean_24h'] = df['soil_moisture'].rolling(24).mean()
    df['temp_rolling_mean_24h'] = df['temp_c'].rolling(24).mean()

    # Target: next day's moisture (shift -24 hours forward)
    df['moisture_next_day'] = df['soil_moisture'].shift(-24)

    # Drop rows with NaN values created by shifting
    df_clean = df.dropna()

    print(f"   ✓ Created lag features for {len(df_clean)} valid samples")
    print(f"   ✓ Dropped {len(df) - len(df_clean)} incomplete rows")

    return df_clean


def train_moisture_prediction_model(csv_path='sensor_data.csv'):
    """Train Linear Regression model to predict next-day soil moisture."""
    
    print("=" * 70)
    print("AgroIntel: Soil Moisture Prediction Model Training")
    print("=" * 70)

    # Check if data exists
    if not os.path.exists(csv_path):
        print(f"\n❌ Error: '{csv_path}' not found!")
        print("   Please run 'gen_training_data.py' first.")
        return
    
    # Load the data
    print(f"\n📂 Loading training data from '{csv_path}'...")
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    print(f"   ✓ Loaded {len(df)} sensor readings")

    # Create features
    df_features = create_lag_feat(df)

    # Define features and target
    feature_columns = [
        'moisture_lag_24h', 
        'temp_lag_24h', 
        'humidity_lag_24h',
        'moisture_rolling_mean_24h',
        'temp_rolling_mean_24h',
        'soil_pH'
    ]

    X = df_features[feature_columns]
    y = df_features['moisture_next_day']

    print(f"\n📊 Dataset prepared:")
    print(f"   Features: {len(feature_columns)} columns")
    print(f"   Samples: {len(X)} rows")

    # Split data: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    print(f"\n🔀 Train-Test Split:")
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")

    # Train the model
    print(f"\n🤖 Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    print(f"   ✓ Model training complete!")

    # Make predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Evaluate performance
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)

    print(f"\n📈 Model Performance:")                        # FIXED: typo
    print(f"   Training MAE: {train_mae:.2f}% (avg error on training data)")
    print(f"   Testing MAE:  {test_mae:.2f}% (avg error on unseen data)")
    print(f"   Training R²:  {train_r2:.4f}")
    print(f"   Testing R²:   {test_r2:.4f}")

    if test_mae < 5:
        print(f"   ✅ Voila! MAE < 5% indicates high accuracy")
    elif test_mae < 10:
        print(f"   ✓ Good! MAE < 10% is acceptable")
    else:
        print(f"   ⚠️ Consider more features or a different model")

    # Feature importance
    print(f"\n🔍 Feature Importance (coefficients):")
    for feature, coef in zip(feature_columns, model.coef_):
        direction = "increases" if coef > 0 else "decreases"
        print(f"   {feature:30s}: {coef:+8.4f} {direction} next-day moisture")

    # Save the model
    model_filename = 'moisture_predictor.pkl'
    joblib.dump(model, model_filename)
    print(f"\n💾 Model saved as '{model_filename}'")
    print(f"   File size: {os.path.getsize(model_filename) / 1024:.2f} KB")

    # Save feature names for later use
    feature_info = {
        'features': feature_columns,
        'test_mae': test_mae,
        'test_r2': test_r2  
    }
    joblib.dump(feature_info, 'model_info.pkl')
    print(f"   Feature info saved as 'model_info.pkl'")

    print("\n" + "=" * 70)
    print("✅ Training complete! Model ready for predictions.")
    print("=" * 70)

    return model, test_mae


def main():
    """Main execution function."""
    train_moisture_prediction_model()


if __name__ == "__main__":
    main()
