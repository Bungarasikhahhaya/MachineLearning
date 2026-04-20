import streamlit as st
import requests

# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Plant Growth", layout="wide")

# ================================
# STATE
# ================================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================================
# HOME STYLE
# ================================
def set_home_style():
    st.markdown("""
    <style>

    header {visibility: hidden;}
    footer {visibility: hidden;}

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    .stApp {
        background: url("https://images.pexels.com/photos/1379620/pexels-photo-1379620.jpeg") no-repeat center center fixed;
        background-size: cover;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        backdrop-filter: blur(10px);
        background: rgba(0,0,0,0.75);
        z-index: -1;
    }

    .full-center {
        position: fixed;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .title {
        font-size: 56px;
        color: white;
        font-weight: bold;
    }

    .subtitle {
        font-size: 20px;
        color: #f1f1f1;
        margin-bottom: 30px;
    }

    div.stButton {
        display: flex;
        justify-content: center;
    }

    </style>
    """, unsafe_allow_html=True)

# ================================
# PREDICT STYLE
# ================================
def set_predict_style():
    st.markdown("""
    <style>

    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* BACKGROUND */
    .stApp {
        background: url("https://images.pexels.com/photos/1379620/pexels-photo-1379620.jpeg") no-repeat center center fixed;
        background-size: cover;
    }

    /* DARK OVERLAY */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.6);
        backdrop-filter: blur(6px);
        z-index: -1;
    }

    /* CONTAINER */
    .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }

    /* TITLE */
    h1 {
        text-align: center;
        color: white;
    }

    /* === GLASS CARD (INI YANG DIPERBAIKI) === */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.08);  /* transparan */
        backdrop-filter: blur(15px);           /* efek kaca */
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }

    /* TEXT */
    label, .stMarkdown, .stSubheader {
        color: white !important;
    }

    /* INPUT BOX */
    input, select {
        background-color: rgba(0,0,0,0.6) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }

    /* NUMBER INPUT */
    div[data-baseweb="input"] {
        background-color: rgba(0,0,0,0.6) !important;
        border-radius: 10px !important;
    }

    /* DROPDOWN */
    div[data-baseweb="select"] > div {
        background-color: rgba(0,0,0,0.6) !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* BUTTON */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50, #2ecc71);
        color: white;
        border-radius: 12px;
        padding: 10px 25px;
        border: none;
    }

    .stButton > button:hover {
        transform: scale(1.05);
    }

    </style>
    """, unsafe_allow_html=True)


# ================================
# HOME PAGE
# ================================
if st.session_state.page == "home":

    set_home_style()

    st.markdown('<div class="full-center">', unsafe_allow_html=True)

    st.markdown('<div class="title">🌱 Plant Growth Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Prediksi apakah tanaman dapat tumbuh berdasarkan kondisi lingkungan</div>', unsafe_allow_html=True)

    if st.button("🚀 Start"):
        st.session_state.page = "predict"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ================================
# PREDICTION PAGE
# ================================
elif st.session_state.page == "predict":

    set_predict_style()

    st.title("Input Data Tanaman")

    with st.form("form"):

        st.subheader("🌡️ Environmental Conditions")

        col1, col2 = st.columns(2)

        with col1:
            air_temp = st.number_input("Air Temperature (°C)", value=25.0)
            soil_temp = st.number_input("Soil Temperature (°C)", value=24.0)
            moisture = st.number_input("Soil Moisture (%)", value=50.0)
            salinity = st.number_input("Salinity (EC)", value=0.3)
            light = st.number_input("Light Intensity", value=500.0)

        with col2:
            ph = st.number_input("Soil pH", value=6.5)
            nitrogen = st.number_input("Nitrogen (ppm)", value=10.0)
            phosphorus = st.number_input("Phosphorus (ppm)", value=5.0)
            potassium = st.number_input("Potassium (ppm)", value=8.0)

        st.subheader("🌿 Soil & Plant Info")

        soil_type = st.selectbox("Soil Type", ["clay", "sandy", "loam"])
        plant_category = st.selectbox("Plant Category", ["vegetable", "fruit", "grain"])
        moisture_regime = st.selectbox("Moisture Regime", ["dry", "moderate", "wet"])
        nutrient_balance = st.selectbox("Nutrient Balance", ["low", "balanced", "high"])

        submit = st.form_submit_button("Predict")

    # ================================
    # SEND TO BACKEND
    # ================================
    if submit:
        data = {
            "air_temp_c": air_temp,
            "soil_temp_c": soil_temp,
            "soil_moisture_pct": moisture,
            "salinity_ec": salinity,
            "light_intensity_par": light,
            "soil_ph": ph,
            "nitrogen_ppm": nitrogen,
            "phosphorus_ppm": phosphorus,
            "potassium_ppm": potassium,
            "soil_type": soil_type,
            "plant_category": plant_category,
            "moisture_regime": moisture_regime,
            "nutrient_balance": nutrient_balance
        }

        with st.spinner("Processing..."):

            # ================================
            # VALIDASI DI FRONTEND (SEBELUM REQUEST)
            # ================================
            if nitrogen <= 0 or phosphorus <= 0 or potassium <= 0:
                st.error("❌ Nutrient tidak valid (harus > 0)")
                st.stop()

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=data
                )

                # ================================
                # DEBUG STATUS
                # ================================
                st.write("Status Code:", response.status_code)

                # ================================
                # CEK RESPONSE
                # ================================
                result = response.json()

                # kalau backend kirim error
                if "error" in result:
                    st.error(f"❌ {result['error']}")
                    st.stop()

                # kalau sukses prediction
                if "prediction" in result:

                    if result["prediction"] == 1:
                        st.error("❌ Tanaman Tidak Dapat Tumbuh")
                    else:
                        st.success("✅ Tanaman Dapat Tumbuh")

                else:
                    st.error("Format response tidak sesuai")
                    st.write(result)

            except Exception as e:
                st.error("Tidak bisa konek ke backend")
                st.write(e)

    if st.button("⬅Back"):
        st.session_state.page = "home"
        st.rerun()
