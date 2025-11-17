# AgroIntel: IoT Based Smart Agriculture System

## Project Overview
Low-cost precision farming platform combining IoT sensors with ML-based irrigation recommendations.

## Problem Statement

- 70% of Indian farmers use fixed irrigation schedules → **30-40% water wastage**
- Soil degradation from over/under-watering reduces crop yields by 15-25%
- Existing precision farming solutions cost ₹50,000-2,00,000 (unaffordable for small farmers)
- Need: Affordable, simple, AI-powered irrigation guidance system

## Our Solution

**AGRO-INTEL** provides farmers with:
- Real-time soil monitoring (moisture, temperature, humidity, pH)
- **AI prediction:** Next-day soil moisture forecast
- **Simple action:** "Irrigate 12-15 L/acre tomorrow at 6-8 AM" or "No irrigation needed"
- **Cost:** ₹2,500 per farm (50× cheaper than existing solutions)

## Project Structure
- `ml-pipeline/` - Machine learning model for soil moisture prediction
- `hardware/` - ESP32 firmware and sensor integration
- `backend/` - FastAPI server and database
- `frontend/` - React farmer dashboard
- `docs/` - Project documentation

## 📊 Project Status

**Current Phase:** Phase 2 - ML Pipeline Validation ✅  
**Overall Completion:** 30%

| Component | Status | Progress |
|-----------|--------|----------|
| ML Pipeline | Working (synthetic data) | 95% |
| Hardware Setup | ESP32 operational, sensors pending | 30% |
| Backend API | Planned (FastAPI) | 0% |
| Database | Planned (PostgreSQL) | 0% |
| Dashboard | Planned (HTML/JS) | 0% |

