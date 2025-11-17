# AgroIntel: IoT Based Smart Agriculture System

## Project Overview
Low-cost precision farming platform combining IoT sensors with ML-based irrigation recommendations.

## Problem Statement

- 70% of Indian farmers use fixed irrigation schedules → **30-40% water wastage**
- Soil degradation from over/under-watering reduces crop yields by 15-25%
- Existing precision farming solutions cost ₹50,000-2,00,000 (unaffordable for small farmers)
- Need: Affordable, simple, AI-powered irrigation guidance system

---

## Our Solution

**AGRO-INTEL** provides farmers with:
- Real-time soil monitoring (moisture, temperature, humidity, pH)
- **AI prediction:** Next-day soil moisture forecast
- **Simple action:** "Irrigate 12-15 L/acre tomorrow at 6-8 AM" or "No irrigation needed"
- **Cost:** ₹2,500 per farm (50× cheaper than existing solutions)

---

## Project Structure
- `ml-pipeline/` - Machine learning model for soil moisture prediction
- `hardware/` - ESP32 firmware and sensor integration
- `backend/` - FastAPI server and database
- `frontend/` - React farmer dashboard
- `docs/` - Project documentation

---

## Project Status

**Current Phase:** Phase 2 - ML Pipeline Validation ✅  
**Overall Completion:** 30%

| Component | Status | Progress |
|-----------|--------|----------|
| ML Pipeline | Working (synthetic data) | ~95% |
| Hardware Setup | ESP32 operational, sensors pending | ~30% |
| Backend API | Planned (FastAPI) | 0% |
| Database | Planned (PostgreSQL) | 0% |
| Dashboard | Planned (React) | 0% |

---

## Phase 2: ML Pipeline (Current)

### Overview
We've built and validated a machine learning pipeline that predicts next-day soil moisture with 97% accuracy using synthetic data. This validates our approach before hardware deployment.

### Quick Demo

**Run the scripts:**

Step 1: Generate 30 days of synthetic sensor data by running
python gen_training_data.py

**Purpose:** Generating realistic synthetic agricultural sensor data

**What it does:**
- Creates 720 hourly readings (30 days of data)
- Simulates realistic patterns
- Saves to `sensor_data.csv`

Step 2: Train the prediction model by running
python train_model.py

**Purpose:** Trains ML model to predict next-day soil moisture

**Algorithm:** Linear Regression with time-series feature engineering

**What it does:**
- Loads `sensor_data.csv`
- Engineers time-series features (lag values, rolling averages)
- Splits data: 80% training, 20% testing
- Trains Linear Regression model
- Evaluates performance (MAE, R²)
- Saves trained model as `moisture_predictor.pkl`

Step 3: Make predictions and get recommendations by running
python predict_demo.py

**Purpose:** Demonstrates predictions with irrigation recommendations

**What it does:**
- Loads trained model
- Simulates current sensor readings (yesterday's data + rolling averages)
- Predicts tomorrow's soil moisture
- Generates actionable irrigation recommendation

**Decision Logic:**

| Predicted Moisture | Status | Action | Irrigation |
|-------------------|--------|--------|-----------|
| < 30% | 🔴 CRITICAL | Immediate irrigation required | 12-15 L/acre at 6-8 AM |
| 30-40% | 🟡 WARNING | Monitor closely | Prepare for irrigation in 24-48h |
| 40-70% | 🟢 OPTIMAL | No irrigation needed | Save water and costs |
| > 70% | 🔵 HIGH | Soil adequately moist | Recently watered |

---