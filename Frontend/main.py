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

    div[data-testid="stAppViewContainer"] .main .block-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 0 !important;
        max-width: 100% !important;
    }

    div[data-testid="stAppViewContainer"] .main .block-container > div {
        width: 100%;
    }

    .stApp {
        background: url("__BG__") no-repeat center center fixed;
        background-size: cover;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        backdrop-filter: blur(12px);
        background: linear-gradient(180deg, rgba(8, 14, 10, 0.84), rgba(8, 14, 10, 0.62));
        z-index: -1;
    }

    .home-title,
    .home-subtitle {
        text-align: center;
    }

    .home-title {
        font-size: clamp(2rem, 3.8vw, 4rem);
        color: white !important;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 0.5rem;
        max-width: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    @media (min-width: 901px) {
        .home-title {
            white-space: nowrap;
        }
    }

    @media (max-width: 900px) {
        .home-title {
            white-space: normal;
        }
    }

    .home-subtitle {
        font-size: 1.05rem;
        color: rgba(255, 255, 255, 0.86) !important;
        margin: 0 auto 0.6rem;
        line-height: 1.6;
        max-width: 680px;
    }

    .home-center div.stButton {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 0.8rem;
    }

    .home-center div.stButton > button {
        margin: 0 auto;
    }

    div[data-testid="stButton"] > button,
    div[data-testid="stButton"] button,
    button[kind="secondary"] {
        background: linear-gradient(135deg, #7ad86b, #2f9e57) !important;
        background-color: #2f9e57 !important;
        color: white !important;
        border: none !important;
        border-radius: 999px !important;
        width: 100% !important;
        max-width: 260px !important;
        padding: 0.8rem 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 12px 28px rgba(47, 158, 87, 0.35) !important;
        cursor: pointer !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease !important;
    }

    div[data-testid="stButton"] > button:hover,
    div[data-testid="stButton"] button:hover,
    button[kind="secondary"]:hover {
        transform: translateY(-1px);
        filter: brightness(1.08);
        box-shadow: 0 14px 32px rgba(47, 158, 87, 0.45) !important;
    }

    </style>
    """.replace("__BG__", BACKGROUND_IMAGE), unsafe_allow_html=True)

# ================================
# PREDICT STYLE
# ================================
def set_predict_style():
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
        background: linear-gradient(180deg, rgba(5, 10, 7, 0.78), rgba(5, 10, 7, 0.56));
        backdrop-filter: blur(10px);
        z-index: -1;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1120px;
    }

    h1, h2, h3, p, label {
        color: white;
    }

    h1 {
        text-align: center;
        color: white;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }

    .page-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        max-width: 760px;
        margin: 0 auto 1.5rem;
        line-height: 1.55;
    }

    .stTitle, h1 {
        text-align: center !important;
    }

    .top-strip .small-note,
    .page-subtitle,
    .section-title {
        text-align: center;
    }

    .page-subtitle + div,
    .top-strip + h1,
    .top-strip + div {
        text-align: center;
    }

    .top-strip {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        gap: 1rem;
        margin: 0 auto 1.25rem;
        padding: 0.9rem 1.2rem;
        border-radius: 18px;
        background: rgba(8, 14, 10, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        max-width: 760px;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.45rem 0.85rem;
        border-radius: 999px;
        background: rgba(122, 216, 107, 0.16);
        color: #d8ffd2;
        font-size: 0.88rem;
        border: 1px solid rgba(122, 216, 107, 0.2);
    }

    div[data-testid="stForm"] {
        background: rgba(10, 18, 12, 0.58);
        backdrop-filter: blur(18px);
        border-radius: 24px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.34);
    }

    .section-title,
    .stSubheader {
        color: white !important;
        font-weight: 700;
        margin-top: 0.35rem;
        margin-bottom: 0.8rem;
    }

    .stMarkdown,
    label {
        color: white !important;
    }

    input, select, textarea {
        background-color: rgba(0,0,0,0.48) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.16) !important;
    }

    div[data-baseweb="input"] {
        background-color: rgba(0,0,0,0.48) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(0,0,0,0.48) !important;
        color: white !important;
        border-radius: 12px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #7ad86b, #2f9e57);
        color: white;
        border-radius: 999px;
        padding: 0.8rem 1.5rem;
        border: none;
        font-weight: 700;
        box-shadow: 0 12px 28px rgba(47, 158, 87, 0.35);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }

    .result-card {
        margin-top: 1rem;
        padding: 1rem 1.2rem;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255,255,255,0.12);
        color: white;
    }

    .small-note {
        color: rgba(255, 255, 255, 0.72);
        font-size: 0.92rem;
    }

    div[data-testid="stForm"] label {
        display: block;
        margin-bottom: 0.35rem;
    }

    div[data-testid="stForm"] {
        text-align: center;
    }

    div[data-testid="stForm"] .stNumberInput,
    div[data-testid="stForm"] .stSelectbox {
        text-align: left;
    }

    div[data-testid="stForm"] [data-testid="column"] {
        gap: 1rem;
    }

    </style>
    """.replace("__BG__", BACKGROUND_IMAGE), unsafe_allow_html=True)


# ================================
# HOME PAGE
# ================================
if st.session_state.page == "home":

    set_home_style()

    left, center, right = st.columns([0.25, 2.5, 0.25], gap="small")

    with center:
        st.markdown('<div class="home-center">', unsafe_allow_html=True)
        st.markdown('<div class="home-title">🌱 Plant Growth Prediction</div>', unsafe_allow_html=True)
        st.markdown('<div class="home-subtitle">Prediksi apakah tanaman dapat tumbuh berdasarkan kondisi lingkungan</div>', unsafe_allow_html=True)
        st.markdown('<div class="home-subtitle">Masukkan data tanah dan lingkungan, lalu sistem akan mengembalikan hasil prediksi secara otomatis.</div>', unsafe_allow_html=True)

        btn_left, btn_center, btn_right = st.columns([1, 0.7, 1])

        with btn_center:
            if st.button("🚀 Start", use_container_width=True):
                st.session_state.page = "predict"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ================================
# PREDICTION PAGE
# ================================
elif st.session_state.page == "predict":

    set_predict_style()

    st.markdown('<div class="top-strip"><div><div class="pill">🌿 Plant Growth</div><div class="small-note">Frontend Streamlit terhubung ke backend FastAPI di port 8000</div></div></div>', unsafe_allow_html=True)
    st.title("Input Data Tanaman")
    st.markdown('<div class="page-subtitle">Isi parameter lingkungan di bawah ini, lalu tekan Predict untuk melihat hasilnya.</div>', unsafe_allow_html=True)

    with st.form("form"):

        st.markdown('<div class="section-title">🌡️ Environmental Conditions</div>', unsafe_allow_html=True)

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

        st.markdown('<div class="section-title">🌿 Soil & Plant Info</div>', unsafe_allow_html=True)

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
                st.error("Tidak bisa konek ke backend. Pastikan FastAPI sudah berjalan di http://127.0.0.1:8000")
                st.caption(str(e))

    if st.button("⬅Back"):
        st.session_state.page = "home"
        st.rerun()
