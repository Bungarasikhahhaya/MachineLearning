import streamlit as st
import requests

# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Plant Growth", layout="wide")

BACKGROUND_IMAGE = "https://images.pexels.com/photos/1379620/pexels-photo-1379620.jpeg"

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

    .stApp {
        background: url("__BG__") no-repeat center center fixed;
        background-size: cover;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        backdrop-filter: blur(12px);
        background: rgba(0,0,0,0.7);
        z-index: -1;
    }

    .title {
        text-align: center;
        font-size: 50px;
        color: white;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }

    div[data-testid="stButton"] {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

div[data-testid="stButton"] > button {
    background: rgba(255, 255, 255, 0.08) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.25) !important;

    padding: 10px 28px !important;
    border-radius: 999px;

    backdrop-filter: blur(8px);

    transition: all 0.3s ease !important;

    margin: 0 auto !important;
    display: block;
}

div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #7ad86b, #2f9e57) !important;

    box-shadow: 
        0 0 10px rgba(122, 216, 107, 0.7),
        0 0 20px rgba(122, 216, 107, 0.5),
        0 0 35px rgba(122, 216, 107, 0.3);

    transform: translateY(-2px) scale(1.05);
}

div[data-testid="stButton"] > button:active {
    transform: scale(0.97);
    box-shadow: 0 0 8px rgba(122, 216, 107, 0.6);
}

    </style>
    """.replace("__BG__", BACKGROUND_IMAGE), unsafe_allow_html=True)

# ================================
# PREDICT STYLE
# ================================
def set_predict_style():
    st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    .stApp {{
        background: url("{BACKGROUND_IMAGE}") no-repeat center center fixed;
        background-size: cover;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.5);
        backdrop-filter: blur(8px);
        z-index: -1;
    }}

    /* =========================
       CENTER CONTAINER
    ========================= */
    .block-container {{
        max-width: 850px;  
        padding: 2rem 2rem;
        margin: auto;
        animation: fadeIn 0.7s ease-out;
    }}

    /* FADE IN ANIMATION */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(12px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    /* CENTER TITLE */
    h1 {{
        text-align: center !important;
        color: white !important;
        margin-bottom: 20px;
    }}

    h2, h3, label {{
        color: white !important;
    }}

    /* =========================
       FORM CARD STYLE
    ========================= */
    div[data-testid="stForm"] {{
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.15);
        padding: 25px;
        border-radius: 18px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }}

    /* =========================
       BUTTON STYLE (PREDICT + BACK)
    ========================= */
    div[data-testid="stButton"] {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }}

    div[data-testid="stButton"] > button {{
        background: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.25) !important;

        padding: 10px 28px !important;
        border-radius: 999px;

        backdrop-filter: blur(8px);

        transition: all 0.3s ease !important;

        margin: 10px auto !important;
        display: block;

        box-shadow: 0 0 0 rgba(0,0,0,0);
    }}

    div[data-testid="stButton"] > button:hover {{
        background: linear-gradient(135deg, #7ad86b, #2f9e57) !important;

        box-shadow: 
            0 0 10px rgba(122, 216, 107, 0.7),
            0 0 20px rgba(122, 216, 107, 0.5),
            0 0 35px rgba(122, 216, 107, 0.3);

        transform: translateY(-2px) scale(1.05);
    }}

    div[data-testid="stButton"] > button:active {{
        transform: scale(0.97);
        box-shadow: 0 0 8px rgba(122, 216, 107, 0.6);
    }}

    </style>
    """, unsafe_allow_html=True)

# ================================
# HOME
# ================================
if st.session_state.page == "home":

    set_home_style()

    st.markdown('<div class="title">Plant Growth Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Prediksi pertumbuhan tanaman berbasis Machine Learning</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,1,2])

    with col2:
        if st.button("Start"):
            st.session_state.page = "predict"
            st.rerun()

# ================================
# PREDICT PAGE
# ================================
elif st.session_state.page == "predict":

    set_predict_style()

    st.title("Input Data Tanaman")

    with st.form("form"):

        # ================================
        # SOIL
        # ================================
        st.subheader("Soil Properties")

        col1, col2 = st.columns(2)

        with col1:
            bulk_density = st.number_input("Bulk Density", value=1.2)
            organic_matter = st.number_input("Organic Matter (%)", value=5.0)
            cec = st.number_input("Cation Exchange Capacity", value=10.0)

        with col2:
            buffering = st.number_input("Buffering Capacity", value=5.0)

        # ================================
        # ENVIRONMENT
        # ================================
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

        # ================================
        # CATEGORY (TIDAK DIUBAH SESUAI PERMINTAANMU)
        # ================================
        st.subheader("🌿 Soil & Plant Info")

        soil_type = st.selectbox("Soil Type", [
            "Sandy","Loamy","Clayey","Silty","Peaty",
            "Chalky","Saline","Laterite","Alluvial"
        ])

        plant_category = st.selectbox("Plant Category", ["cereal","legume","vegetable"])

        submit = st.form_submit_button("Predict")

    # ================================
    # PROCESS
    # ================================
    if submit:

        # VALIDASI
        if nitrogen <= 0 or phosphorus <= 0 or potassium <= 0:
            st.error("❌ Nutrient tidak valid")
            st.stop()

        # ================================
        # INPUT DATA
        # ================================
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
            "bulk_density": bulk_density,
            "organic_matter_pct": organic_matter,
            "cation_exchange_capacity": cec,
            "buffering_capacity": buffering
        }

        st.subheader("📥 Input Data Summary")

        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            color: white;
        ">

        <b>🌡️ Environment</b><br>
        • Air Temp: {air_temp} °C<br>
        • Soil Temp: {soil_temp} °C<br>
        • Moisture: {moisture} %<br>
        • Salinity: {salinity} EC<br>
        • Light: {light} PAR<br><br>

        <b>🧪 Soil Chemistry</b><br>
        • pH: {ph}<br>
        • Nitrogen: {nitrogen} ppm<br>
        • Phosphorus: {phosphorus} ppm<br>
        • Potassium: {potassium} ppm<br><br>

        <b>🌱 Soil Physical</b><br>
        • Bulk Density: {bulk_density}<br>
        • Organic Matter: {organic_matter} %<br>
        • CEC: {cec}<br>
        • Buffering: {buffering}<br><br>

        <b>🌿 Category</b><br>
        • Soil Type: {soil_type}<br>
        • Plant Type: {plant_category}<br>

        </div>
        """, unsafe_allow_html=True)


        # ================================
        # FEATURE ENGINEERING (AUTO)
        # ================================
        np_ratio = nitrogen / phosphorus
        nk_ratio = nitrogen / potassium
        ph_deviation = ph - 7
        moisture_deficit = 60 - moisture
        moisture_excess = moisture - 60
        salinity_stress = salinity * 1.5

        # ================================
        # REQUEST KE BACKEND
        # ================================
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=data
                )

                result = response.json()

                st.subheader("📈 Hasil Prediksi")

                # ERROR
                if "error" in result:
                    st.error(result["error"])

                # RULE BASED
                elif result.get("status") == "rule-based":
                    st.error(f"❌ Tidak Dapat Tumbuh ({result.get('reason')})")

                # NORMAL MODEL
                else:
                    if result["prediction"] == 1:
                        st.error("❌ Tanaman Tidak Dapat Tumbuh (Model)")
                    else:
                        st.success("✅ Tanaman Dapat Tumbuh")

            except Exception as e:
                st.error("Backend tidak jalan")
                st.write(e)

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()
