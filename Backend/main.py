from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# ================================
# LOAD MODEL
# ================================
model = joblib.load("../model/model.pkl")


# ================================
# FEATURE ENGINEERING
# ================================
def feature_engineering(df):

    # 🔥 safe division (hindari error 0)
    df["np_ratio"] = df["nitrogen_ppm"] / df["phosphorus_ppm"].replace(0, 0.0001)
    df["nk_ratio"] = df["nitrogen_ppm"] / df["potassium_ppm"].replace(0, 0.0001)

    # pH
    df["ph_deviation"] = df["soil_ph"] - 7

    # moisture
    df["moisture_deficit"] = 60 - df["soil_moisture_pct"]
    df["moisture_excess"] = df["soil_moisture_pct"] - 60
    df["moisture_z_by_soil"] = (df["soil_moisture_pct"] - 50) / 10

    # salinity stress
    df["salinity_stress"] = df["salinity_ec"] * 1.5

    # soil properties (default asumsi model training)
    df["bulk_density"] = 1.3
    df["organic_matter_pct"] = 2.5
    df["cation_exchange_capacity"] = 15
    df["buffering_capacity"] = 10

    # moisture limits
    df["moisture_limit_dry"] = 30
    df["moisture_limit_wet"] = 80

    return df


# ================================
# HOME
# ================================
@app.get("/")
def home():
    return {"message": "API is running"}


# ================================
# PREDICT ENDPOINT (CLEAN VERSION)
# ================================
@app.post("/predict")
def predict(data: dict):

    try:
        # ================================
        # VALIDASI BACKEND (SAFETY LAYER)
        # ================================
        if data["nitrogen_ppm"] <= 0 or data["phosphorus_ppm"] <= 0 or data["potassium_ppm"] <= 0:
            return {
                "error": "Nutrient tidak valid",
                "status": "failed"
            }

        # ================================
        # CONVERT DATA
        # ================================
        df = pd.DataFrame([data])

        # ================================
        # FEATURE ENGINEERING
        # ================================
        df = feature_engineering(df)

        # ================================
        # ALIGN FEATURE ORDER
        # ================================
        df = df[model.feature_names_in_]

        # ================================
        # PREDICTION
        # ================================
        prediction = model.predict(df)[0]

        return {
            "prediction": int(prediction),
            "status": "success"
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
