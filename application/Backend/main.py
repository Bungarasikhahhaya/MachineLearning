from fastapi import FastAPI
import joblib
import pandas as pd
from pathlib import Path
import numpy as n

app = FastAPI()

# ================================
# LOAD MODEL
# ================================
MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "model" / "model.pkl"
model = joblib.load(MODEL_PATH)


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
    if "soil_type" in df.columns:
        df["soil_type"] = df["soil_type"].astype(str).str.title()

    if "plant_category" in df.columns:
        df["plant_category"] = df["plant_category"].str.lower()

    return df


# ================================
# FALLBACK FEATURE MATRIX
# ================================
def build_model_input(df):

    # ================================
    # DERIVED FEATURES
    # ================================
    df = df.copy()

    df["phosphorus_ppm"] = df["phosphorus_ppm"].replace(0, 0.0001)
    df["potassium_ppm"] = df["potassium_ppm"].replace(0, 0.0001)

    # Features used by the training notebook before preprocessing.
    numeric_features = [
        "bulk_density",
        "organic_matter_pct",
        "cation_exchange_capacity",
        "salinity_ec",
        "buffering_capacity",
        "soil_moisture_pct",
        "moisture_limit_dry",
        "moisture_limit_wet",
        "moisture_z_by_soil",
        "soil_temp_c",
        "air_temp_c",
        "light_intensity_par",
        "soil_ph",
        "nitrogen_ppm",
        "phosphorus_ppm",
        "potassium_ppm",
        "np_ratio",
        "nk_ratio",
        "moisture_deficit",
        "moisture_excess",
        "salinity_stress",
        "ph_deviation",
    ]

    df["np_ratio"] = df["nitrogen_ppm"] / df["phosphorus_ppm"]
    df["nk_ratio"] = df["nitrogen_ppm"] / df["potassium_ppm"]
    df["ph_deviation"] = abs(df["soil_ph"] - 6.5)
    df["moisture_deficit"] = 60 - df["soil_moisture_pct"]
    df["moisture_excess"] = df["soil_moisture_pct"] - 60
    df["salinity_stress"] = df["salinity_ec"] * df["soil_moisture_pct"]

    if "moisture_limit_dry" not in df.columns:
        df["moisture_limit_dry"] = 30
    if "moisture_limit_wet" not in df.columns:
        df["moisture_limit_wet"] = 80
    if "moisture_z_by_soil" not in df.columns:
        df["moisture_z_by_soil"] = 0

    numeric_df = df[numeric_features].copy()

    soil_dummies = pd.get_dummies(df["soil_type"], prefix="soil_type")
    plant_dummies = pd.get_dummies(df["plant_category"], prefix="plant_category")

    expected_columns = [
        *numeric_features,
        "soil_type_Alluvial",
        "soil_type_Chalky",
        "soil_type_Clayey",
        "soil_type_Laterite",
        "soil_type_Loamy",
        "soil_type_Peaty",
        "soil_type_Saline",
        "soil_type_Sandy",
        "soil_type_Silty",
        "plant_category_cereal",
        "plant_category_legume",
        "plant_category_vegetable",
    ]

    encoded = pd.concat([numeric_df, soil_dummies, plant_dummies], axis=1)

    for col in expected_columns:
        if col not in encoded.columns:
            encoded[col] = 0

    encoded = encoded[expected_columns]
    return encoded


def get_prediction_percentages(model, model_input, prediction):
    predicted_label = int(prediction)

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(model_input)[0]
        classes = list(getattr(model, "classes_", []))

        class_probability = {int(cls): float(prob) for cls, prob in zip(classes, probabilities)}

        success_probability = class_probability.get(0, float(probabilities[0] if len(probabilities) > 0 else 0.0))
        failure_probability = class_probability.get(1, float(probabilities[1] if len(probabilities) > 1 else 1.0 - success_probability))

        success_percentage = round(success_probability * 100, 2)
        failure_percentage = round(failure_probability * 100, 2)
    else:
        if predicted_label == 1:
            success_percentage = 0.0
            failure_percentage = 100.0
        else:
            success_percentage = 100.0
            failure_percentage = 0.0

    return {
        "success_percentage": success_percentage,
        "failure_percentage": failure_percentage,
    }


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
                "reason": "pH terlalu ekstrem",
                "success_percentage": 0.0,
                "failure_percentage": 100.0,
            }

        if data["soil_moisture_pct"] < 10:
            return {
                "prediction": 1,
                "status": "rule-based",
                "reason": "Tanah terlalu kering",
                "success_percentage": 0.0,
                "failure_percentage": 100.0,
            }

        if data["soil_moisture_pct"] > 90:
            return {
                "prediction": 1,
                "status": "rule-based",
                "reason": "Tanah terlalu basah",
                "success_percentage": 0.0,
                "failure_percentage": 100.0,
            }

        if data["air_temp_c"] < 0 or data["air_temp_c"] > 50:
            return {
                "prediction": 1,
                "status": "rule-based",
                "reason": "Suhu ekstrem",
                "success_percentage": 0.0,
                "failure_percentage": 100.0,
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
        # ALIGN FEATURES
        # ================================
        if hasattr(model, "feature_names_in_"):
            for col in model.feature_names_in_:
                if col not in df.columns:
                    df[col] = 0

            df = df[model.feature_names_in_]
            model_input = df
        else:
            model_input = build_model_input(df)

        # ================================
        # PREDICT ML
        # ================================
        prediction = model.predict(model_input)[0] if hasattr(model, "feature_names_in_") else model.predict(model_input.to_numpy())[0]
        percentages = get_prediction_percentages(model, model_input, prediction)

        if int(prediction) == 1:
            return {
                "prediction": 1,
                "status": "ml",
                **percentages,
                "reason": "Model memprediksi kombinasi input ini masih belum optimal untuk tumbuh"
            }

        return {
            "prediction": int(prediction),
            "status": "ml",
            **percentages
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
