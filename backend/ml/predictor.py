from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "ml" / "models"

model = joblib.load(MODEL_DIR / "gb_best_people.joblib")
features = list(
    joblib.load(MODEL_DIR / "selected_features_people.joblib")
)

if list(model.feature_names_in_) != features:
    raise ValueError("Model feature order mismatch")


def predict_occupancy(
    measurement: dict,
    max_capacity: int
) -> float:

    data = {
        **measurement,
        "max_capacity": max_capacity
    }

    X = pd.DataFrame(
        [{feature: data[feature] for feature in features}],
        columns=features
    )

    prediction = model.predict(X)

    return float(prediction[0])