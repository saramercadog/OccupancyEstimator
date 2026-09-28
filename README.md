# WiFi Probe-Based Occupancy Estimation
> **Work in progress** — sensor pipeline and ML model complete; 
> MQTT, backend API, and dashboard under development.

A passive WiFi sensing system that estimates indoor occupancy in study 
spaces using probe request data captured by a Raspberry Pi. Built as a 
prototype for university campus deployment, with the goal of giving 
students real-time visibility into how busy study spaces are before 
they make the trip.

---

## Current State

### ✅ Completed
- Passive probe request capture via tshark across channels 1, 6, and 11
- 30-second scan cycles aggregated into 5-minute observation windows
- Raw observations stored in SQLite — no raw MAC addresses written to disk
- Data cleaning pipeline with faulty cycle detection and imputation
- Exploratory data analysis across three environments with varying capacities
- Gradient Boosting regression model achieving R²=0.948 on headcount prediction
- Model validated via 5-fold cross-validation on 144 calibrated observations
- Hyperparameter tuning via GridSearchCV

### 🚧 In Progress
- MQTT broker integration for multi-sensor deployment
- FastAPI backend (`/api/current`, `/api/history`, `/api/hourly`)
- Dashboard with real-time occupancy display and historical trends

---

## ML Model

**Dataset**
- 144 five-minute observation windows
- Multiple environments (room capacities: 40–600 people)
- Ground truth collected via manual headcount every 5 minutes

**Features**
- Probe counts filtered at multiple RSSI thresholds (-55 to -80 dBm)
- Unique MAC address counts at appearance thresholds (2–5 times)
- Room capacity for cross-environment generalisation

**Results**

| Model | Target | R² | MAE |
|---|---|---|---|
| Ridge | Headcount | 0.867 | 12.1 people |
| Decision Tree | Headcount | 0.823 | 12.7 people |
| Random Forest | Headcount | 0.828 | 11.6 people |
| **Gradient Boosting** | **Headcount** | **0.948** | **7.3 people** |

---

## Privacy

- Probe requests captured passively — no network connection required
- Raw MAC addresses never written to disk
- Data stored as aggregated counts per time window only
- No individual device can be tracked or identified from stored data

---

## Known Limitations

- MAC address randomisation on modern iOS and Android causes undercounting
- Model calibrated on 144 observations across 8 environments — performance 
  in new spaces may vary until recalibrated
- MQTT, backend, and dashboard not yet deployed

---

## References

- Vattapparamban et al. (2016). *Indoor Occupancy Tracking in Smart 
  Buildings Using Passive Sniffing of Probe Requests*. IEEE ICC.
- Mowla et al. (2024). *CSI-Based People Counting in WiFi Networks*. 
  IEEE COMPAS.
