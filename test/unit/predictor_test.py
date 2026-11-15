from backend.ml.predictor import predict_occupancy

measurement = {
    "total_probes": 310,
    "unique_mac_addresses": 92,
    "probes_rssi_80": 12,
    "probes_rssi_75": 18,
    "unique_mac_2plus": 41
}

prediction = predict_occupancy(
    measurement=measurement,
    max_capacity=50
)

print("Predicted occupancy:", prediction)