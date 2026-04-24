import streamlit as st
import requests

# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Plant Growth", layout="wide")

BACKGROUND_IMAGE = "https://images.pexels.com/photos/1379620/pexels-photo-1379620.jpeg"
VIDEO_THUMB_IMAGE = "https://images.pexels.com/photos/1072824/pexels-photo-1072824.jpeg"

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
        background:
            radial-gradient(circle at 20% 20%, rgba(137, 219, 63, 0.18), transparent 22%),
            radial-gradient(circle at 80% 18%, rgba(137, 219, 63, 0.12), transparent 18%),
            linear-gradient(180deg, rgba(7, 41, 39, 0.72), rgba(8, 28, 24, 0.84)),
            url("__BG__") no-repeat center center fixed;
        background-size: cover;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(3, 18, 16, 0.38);
        backdrop-filter: blur(10px);
        z-index: -1;
    }

    div[data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1240px;
        padding-top: 0rem;
        padding-bottom: 0rem;
        margin-top: 0rem;
    }

    .hero-shell {
        min-height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        gap: 0.25rem;
        padding: 0rem 0 0rem;
        font-family: "Arial Black", "Franklin Gothic Heavy", "Helvetica Neue", Arial, sans-serif;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        gap: 1.6rem;
        align-items: center;
        min-height: auto;
    }

    .hero-stage {
        display: grid;
        grid-template-columns: 1.22fr 0.78fr;
        gap: 0rem;
        align-items: center;
        flex: 1;
        min-height: 0;
        margin-top: -1.6rem;
    }

    .hero-copy {
        position: relative;
        padding: 0.35rem 0 0rem 0.95rem;
        color: white;
    }

    .hero-kicker {
        color: rgba(224, 245, 202, 0.9);
        font-size: 0.72rem;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }

    .hero-title {
        margin: 0;
        font-size: clamp(4rem, 15vw, 10rem);
        line-height: 0.88;
        letter-spacing: -0.07em;
        font-weight: 900;
        color: #f7faf5;
        text-shadow: 0 12px 28px rgba(0, 0, 0, 0.35);
    }

    .hero-subtitle {
        max-width: 28rem;
        margin-top: 0.4rem;
        color: rgba(241, 250, 235, 0.82);
        font-size: 0.98rem;
        line-height: 1.45;
        font-weight: 700;
    }

    .hero-actions {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        margin-top: 0.55rem;
        flex-wrap: wrap;
    }

    .hero-note {
        color: rgba(241, 250, 235, 0.68);
        font-size: 0.86rem;
        font-weight: 700;
        margin-top: 0.1rem;
    }

    .hero-left {
        max-width: 36rem;
    }

    .hero-right {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 0;
        margin-top: -0.35rem;
        margin-left: -2.2rem;
    }

    .hero-bottom {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin-top: 0.1rem;
        padding-left: 0.85rem;
    }

    .signal-stack {
        width: 100%;
        max-width: 760px;
        display: grid;
        grid-template-columns: 1.6rem minmax(220px, 1fr) minmax(220px, 1fr);
        gap: 0.7rem 0.8rem;
        align-items: start;
    }

    .signal-rail {
        width: 1.6rem;
        min-height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(224, 245, 202, 0.9);
        letter-spacing: 0.28em;
        font-size: 0.68rem;
        text-transform: uppercase;
        writing-mode: vertical-rl;
        transform: rotate(180deg);
        opacity: 0.9;
    }

    .signal-rail::before {
        content: "";
        position: absolute;
        width: 1px;
        height: 100%;
        background: linear-gradient(180deg, transparent, rgba(182, 243, 77, 0.55), transparent);
        opacity: 0.9;
        transform: translateX(0.95rem);
    }

    .signal-card {
        background: rgba(8, 28, 24, 0.42);
        border: 1px solid rgba(182, 243, 77, 0.18);
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.18);
        backdrop-filter: blur(10px);
        border-radius: 18px;
        padding: 0.72rem 0.8rem;
        color: rgba(245, 250, 236, 0.92);
        align-self: start;
    }

    .signal-card .label {
        font-size: 0.66rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: rgba(224, 245, 202, 0.7);
        margin-bottom: 0.45rem;
    }

    .signal-card .value {
        font-size: 0.98rem;
        line-height: 1.35;
        font-weight: 800;
    }

    .video-card {
        position: relative;
        width: min(100%, 320px);
        aspect-ratio: 1 / 0.72;
        border-radius: 22px;
        overflow: hidden;
        margin-left: auto;
        box-shadow: 0 22px 56px rgba(0, 0, 0, 0.38);
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(255, 255, 255, 0.08);
    }

    .video-card img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: saturate(0.9) contrast(1.05);
    }

    .video-badge {
        position: absolute;
        inset: auto auto 1rem 1rem;
        width: 4.3rem;
        height: 4.3rem;
        border-radius: 999px;
        display: grid;
        place-items: center;
        background: linear-gradient(135deg, #b6f34d, #7fd12d);
        color: #0b2b17;
        font-size: 1.5rem;
        font-weight: 800;
        box-shadow: 0 0 0 14px rgba(182, 243, 77, 0.16);
    }

    div[data-testid="stButton"] {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        width: 100%;
    }

    div[data-testid="stButton"] > button {
        background: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.25) !important;

        padding: 0.9rem 2rem !important;
        border-radius: 999px;

        backdrop-filter: blur(8px);

        transition: all 0.3s ease !important;

        margin: 0.2rem 0 0 !important;
        display: block;
        min-width: 12rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        box-shadow: 0 10px 32px rgba(0, 0, 0, 0.18);
        font-family: inherit;
    }

    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #b6f34d, #64c93a) !important;

        box-shadow:
            0 0 10px rgba(182, 243, 77, 0.65),
            0 0 20px rgba(182, 243, 77, 0.45),
            0 0 35px rgba(182, 243, 77, 0.24);

        transform: translateY(-2px) scale(1.03);
    }

    div[data-testid="stButton"] > button:active {
        transform: scale(0.98);
        box-shadow: 0 0 8px rgba(182, 243, 77, 0.55);
    }

    div[data-testid="stButton"] > button:focus {
        outline: none;
        box-shadow: 0 0 0 0.2rem rgba(182, 243, 77, 0.22);
    }

    @media (max-width: 900px) {
        .hero-stage {
            grid-template-columns: 1fr;
            margin-top: 0;
        }

        .hero-grid {
            grid-template-columns: 1fr;
            min-height: auto;
        }

        div[data-testid="stAppViewContainer"] .main .block-container {
            padding-top: 0.5rem;
        }

        .video-card {
            margin-left: 0;
            width: min(100%, 360px);
        }

        .hero-copy {
            padding: 0.15rem 0 0.15rem 0;
        }

        .hero-right {
            padding-top: 0;
        }

        .hero-bottom {
            margin-top: 0;
            padding-left: 0;
            justify-content: center;
        }

        .signal-stack {
            max-width: 100%;
            grid-template-columns: 1fr;
        }

        .signal-rail {
            writing-mode: horizontal-tb;
            transform: none;
            width: auto;
            min-height: auto;
            padding: 0.4rem 0.6rem;
            border-radius: 999px;
            background: rgba(8, 28, 24, 0.42);
            border: 1px solid rgba(182, 243, 77, 0.18);
        }

        .signal-rail::before {
            display: none;
        }

        .signal-card {
            width: 100%;
        }

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

    st.markdown('<div class="hero-shell">', unsafe_allow_html=True)
    left, right = st.columns([1.28, 0.72], gap="small")

    with left:
        st.markdown('<div class="hero-left">', unsafe_allow_html=True)
        st.markdown('<div class="hero-kicker">Plant growth intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">GROW</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="hero-subtitle">Predict whether your plant can thrive using soil and environmental inputs.</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="hero-note">Use the model to estimate growth potential quickly.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Predict Growth"):
            st.session_state.page = "predict"
            st.rerun()

    with right:
        st.markdown('<div class="hero-right">', unsafe_allow_html=True)
        st.markdown(
            f'''
            <div class="video-card">
                <img src="{VIDEO_THUMB_IMAGE}" alt="Planting preview" />
                <div class="video-badge">▶</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-bottom">
            <div class="signal-stack">
                <div class="signal-rail">Live model</div>
                <div class="signal-card">
                    <div class="label">Inputs</div>
                    <div class="value">Soil, climate, and nutrient balance feed the prediction.</div>
                </div>
                <div class="signal-card">
                    <div class="label">Output</div>
                    <div class="value">A quick growth estimate for your plant conditions.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

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
