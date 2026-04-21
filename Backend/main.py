from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# ================================
# LOAD MODEL
# ================================
model = joblib.load("../model/model1.pkl")


# ================================
# FEATURE ENGINEERING
# ================================
def feature_engineering(df):

    # ================================
    # SAFE DIVISION
    # ================================
    df["phosphorus_ppm"] = df["phosphorus_ppm"].replace(0, 0.0001)
    df["potassium_ppm"] = df["potassium_ppm"].replace(0, 0.0001)

    df["np_ratio"] = df["nitrogen_ppm"] / df["phosphorus_ppm"]
    df["nk_ratio"] = df["nitrogen_ppm"] / df["potassium_ppm"]

    # pH
    df["ph_deviation"] = df["soil_ph"] - 7

    # moisture
    df["moisture_deficit"] = 60 - df["soil_moisture_pct"]
    df["moisture_excess"] = df["soil_moisture_pct"] - 60
    df["moisture_z_by_soil"] = (df["soil_moisture_pct"] - 50) / 10

    # salinity
    df["salinity_stress"] = df["salinity_ec"] * 1.5

    # ================================
    # DEFAULT VALUE (JANGAN TIMPA INPUT USER)
    # ================================
    defaults = {
        "bulk_density": 1.3,
        "organic_matter_pct": 2.5,
        "cation_exchange_capacity": 15,
        "buffering_capacity": 10,
        "moisture_limit_dry": 30,
        "moisture_limit_wet": 80
    }

    for col, val in defaults.items():
        if col not in df.columns:
            df[col] = val

    return df


# ================================
# NORMALISASI CATEGORY
# ================================
def normalize_category(df):

    soil_map = {
        "Sandy": "sandy",
        "Loamy": "loam",
        "Clayey": "clay",
        "Silty": "loam",
        "Peaty": "loam",
        "Chalky": "clay",
        "Saline": "sandy",
        "Laterite": "clay",
        "Alluvial": "loam"
    }

    if "soil_type" in df.columns:
        df["soil_type"] = df["soil_type"].map(
            lambda x: soil_map.get(x, str(x).lower())
        )

    if "plant_category" in df.columns:
        df["plant_category"] = df["plant_category"].str.lower()

    return df


# ================================
# HOME
# ================================
@app.get("/")
def home():
    return {"message": "API is running"}


# ================================
# PREDICT
# ================================
@app.post("/predict")
def predict(data: dict):

    try:
        # ================================
        # VALIDASI DASAR
        # ================================
        if data["nitrogen_ppm"] <= 0 or data["phosphorus_ppm"] <= 0 or data["potassium_ppm"] <= 0:
            return {"error": "Nutrient tidak valid", "status": "failed"}

        # ================================
        # 🔥 RULE-BASED (PRIORITAS)
        # ================================
        if data["soil_ph"] < 4 or data["soil_ph"] > 9:
            return {
                "prediction": 1,
                "status": "rule-based",
                "reason": "pH terlalu ekstrem"
            }

        if data["soil_moisture_pct"] < 10:
            return {
                "prediction": 1,
                "status": "rule-based",
                "reason": "Tanah terlalu kering"
            }

        if data["soil_moisture_pct"] > 90:
            return {
                "prediction": 1,
                "status": "rule-based",
                "reason": "Tanah terlalu basah"
            }

        if data["air_temp_c"] < 0 or data["air_temp_c"] > 50:
            return {
                "prediction": 1,
                "status": "rule-based",
                "reason": "Suhu ekstrem"
            }

        # ================================
        # DATAFRAME
        # ================================
        df = pd.DataFrame([data])

        # ================================
        # NORMALISASI
        # ================================
        df = normalize_category(df)

        # ================================
        # FEATURE ENGINEERING
        # ================================
        df = feature_engineering(df)

        # ================================
        # HANDLE MISSING FEATURE
        # ================================
        for col in model.feature_names_in_:
            if col not in df.columns:
                df[col] = 0

        # ================================
        # ALIGN ORDER
        # ================================
        df = df[model.feature_names_in_]

        # ================================
        # PREDICT ML
        # ================================
        prediction = model.predict(df)[0]

        return {
            "prediction": int(prediction),
            "status": "ml"
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
