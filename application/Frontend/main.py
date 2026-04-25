import streamlit as st
import requests
from textwrap import dedent

# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Plant Growth", layout="wide")

BACKGROUND_IMAGE = "https://images.pexels.com/photos/10796342/pexels-photo-10796342.jpeg?cs=srgb&dl=pexels-vargaphotography-10796342.jpg&fm=jpg"
VIDEO_THUMB_IMAGE = "https://images.pexels.com/photos/36375100/pexels-photo-36375100.jpeg"

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
        max-width: 1400px;
        padding-top: 1.2rem;
        padding-bottom: 1.4rem;
        margin-top: 0rem;
    }

    .predict-layout {
        display: grid;
        grid-template-columns: minmax(0, 1.02fr) minmax(360px, 0.98fr);
        gap: 1.35rem;
        align-items: start;
    }

    .panel-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 18px;
        backdrop-filter: blur(10px);
                soil_col1, soil_col2 = st.columns(2)
        padding: 1.1rem;
                with soil_col1:
    }
                    organic_matter = st.number_input("Organic Matter (%)", key="organic_matter")
        position: sticky;
                with soil_col2:
    }
                    cec = st.number_input("Cation Exchange Capacity", key="cec")

    .panel-title {
        margin: 0 0 0.85rem;
        font-size: 1rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
                row1_left, row1_right = st.columns(2)
                with row1_left:
                    air_temp = st.number_input("Air Temperature (°C)", key="air_temp")
                with row1_right:
                    soil_temp = st.number_input("Soil Temperature (°C)", key="soil_temp")
    }
                row2_left, row2_right = st.columns(2)
                with row2_left:
        grid-template-columns: repeat(2, minmax(0, 1fr));
                with row2_right:
        gap: 0.85rem;

                row3_left, row3_right = st.columns(2)
                with row3_left:
                    light = st.number_input("Light Intensity", key="light")
                with row3_right:
        background: rgba(255,255,255,0.08);

                row4_left, row4_right = st.columns(2)
                with row4_left:
        border: 1px solid rgba(255,255,255,0.12);
                with row4_right:
        border-radius: 14px;

                potassium = st.number_input("Potassium (ppm)", key="potassium")
    }

    .summary-label {
        font-size: 0.68rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
                category_col1, category_col2 = st.columns(2)

                with category_col1:
                    soil_type = st.selectbox("Soil Type", [
                        "Sandy","Loamy","Clayey","Silty","Peaty",
                        "Chalky","Saline","Laterite","Alluvial"
                    ], key="soil_type")

                with category_col2:
                    plant_category = st.selectbox("Plant Category", ["cereal","legume","vegetable"], key="plant_category")
        line-height: 1.35;
        font-weight: 700;
        color: rgba(245, 250, 236, 0.96);
    }

    .result-card {
        margin-top: 1rem;
        background: rgba(8, 28, 24, 0.68);
        border: 1px solid rgba(182, 243, 77, 0.24);
        border-radius: 18px;
        padding: 1rem 1rem 1.05rem;
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.22);
    }

    .result-state {
        margin-top: 0.5rem;
        font-size: 1rem;
        line-height: 1.5;
        font-weight: 800;
    }

    .result-muted {
        color: rgba(241, 250, 235, 0.7);
        font-size: 0.92rem;
        line-height: 1.5;
        margin-top: 0.4rem;
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
        justify-content: flex-start;
        align-items: center;
        padding-top: 0;
        margin-top: -0.35rem;
        margin-left: -0.4rem;
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
        margin-left: 0;
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
        .predict-layout {
            grid-template-columns: 1fr;
        }

        .summary-grid {
            grid-template-columns: 1fr;
        }

        .panel-card--side {
            position: static;
        }

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
        max-width: 1120px;  
        padding: 2.6rem 3.6rem;
        margin: auto;
        animation: fadeIn 0.7s ease-out;
    }}

    .predict-layout {{
        display: grid;
        grid-template-columns: minmax(0, 1.08fr) minmax(360px, 0.92fr);
        gap: 2rem;
        align-items: start;
    }}

    .panel-card {{
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 18px;
        backdrop-filter: blur(12px);
        box-shadow: 0 12px 34px rgba(0,0,0,0.34);
        padding: 1.75rem;
        color: white;
    }}

    .panel-card--side {{
        position: sticky;
        top: 1rem;
    }}

    .panel-card--summary {{
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.16);
        border-radius: 18px;
        backdrop-filter: blur(12px);
        box-shadow: 0 12px 34px rgba(0,0,0,0.34);
        padding: 1.75rem;
        color: white;
    }}

    .summary-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.35rem 1rem;
    }}

    .summary-item {{
        padding: 0.25rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.10);
    }}

    .summary-item:last-child {{
        border-bottom: none;
    }}

    .summary-key {{
        font-size: 0.65rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: rgba(224, 245, 202, 0.78);
        margin-bottom: 0.2rem;
    }}

    .summary-val {{
        font-size: 0.92rem;
        line-height: 1.3;
        font-weight: 700;
        color: #f7fbf4;
    }}

    @media (max-width: 900px) {{
        .summary-grid {{
            grid-template-columns: 1fr;
        }}
    }}

    .panel-title {{
        margin: 0 0 0.85rem;
        font-size: 1rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.92);
    }}

    .result-state {{
        margin-top: 0.5rem;
        font-size: 1rem;
        line-height: 1.5;
        font-weight: 800;
        color: rgba(248, 251, 244, 0.98);
    }}

    .result-muted {{
        color: rgba(241, 250, 235, 0.78);
        font-size: 0.92rem;
        line-height: 1.5;
        margin-top: 0.4rem;
    }}

    div[data-testid="stMetric"] {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 0.75rem 0.85rem;
    }}

    div[data-testid="stMetricLabel"] {{
        color: rgba(255,255,255,0.84) !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: #ffffff !important;
        font-weight: 800 !important;
    }}

    .summary-section {{
        margin-bottom: 0.95rem;
    }}

    .summary-section-title {{
        font-size: 0.72rem;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        color: rgba(224, 245, 202, 0.72);
        margin: 0 0 0.55rem;
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

    div[data-testid="stForm"] div[data-testid="stButton"] {{
        justify-content: center;
    }}

    div[data-testid="stFormSubmitButton"] {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}

    div[data-testid="stFormSubmitButton"] > button {{
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    div[data-testid="stButton"] > button {{
        background: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.25) !important;

        padding: 10px 28px !important;
        border-radius: 999px;

        backdrop-filter: blur(8px);

        transition: all 0.3s ease !important;

        margin: 12px auto 0 !important;
        display: inline-flex;
        width: auto !important;
        min-width: 140px;

        box-shadow: 0 0 0 rgba(0,0,0,0);
    }}

    div[data-testid="stButton"] > button:hover {{
        background: linear-gradient(135deg, #b7ff5f, #5dff7a) !important;
        color: #0f1f12 !important;
        border-color: rgba(183, 255, 95, 0.95) !important;

        box-shadow: 
            0 0 10px rgba(183, 255, 95, 0.85),
            0 0 20px rgba(93, 255, 122, 0.7),
            0 0 35px rgba(93, 255, 122, 0.45);

        transform: translateY(-2px) scale(1.05);
    }}

    div[data-testid="stButton"] > button:active {{
        transform: scale(0.97);
        box-shadow: 0 0 8px rgba(122, 216, 107, 0.6);
    }}

    @media (max-width: 900px) {{
        .predict-layout {{
            grid-template-columns: 1fr;
        }}

        .panel-card--side {{
            position: static;
        }}
    }}

    </style>
    """, unsafe_allow_html=True)


def init_predict_defaults():
    profile_version = "success_profile_v4"
    defaults = {
        "bulk_density": 1.3,
        "organic_matter": 3.8,
        "cec": 20.0,
        "buffering": 0.7,
        "air_temp": 29.2,
        "soil_temp": 23.4,
        "moisture": 39.67,
        "salinity": 0.4,
        "light": 380.0,
        "ph": 6.25,
        "nitrogen": 29.4,
        "phosphorus": 80.4,
        "potassium": 105.0,
        "soil_type": "Alluvial",
        "plant_category": "legume",
    }

    if st.session_state.get("predict_defaults_version") != profile_version:
        for key, value in defaults.items():
            st.session_state[key] = value

    st.session_state["predict_defaults_version"] = profile_version

# ================================
# HOME
# ================================
if st.session_state.page == "home":

    set_home_style()

    st.markdown('<div class="hero-shell">', unsafe_allow_html=True)
    left, right = st.columns([1.42, 0.58], gap="small")

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
    init_predict_defaults()

    st.title("Input Data Tanaman")

    left_col, right_col = st.columns([1.08, 0.92], gap="large")

    with left_col:
        with st.form("form"):

            # ================================
            # SOIL
            # ================================
            st.subheader("Soil Properties")

            soil_row1_left, soil_row1_right = st.columns(2)
            with soil_row1_left:
                bulk_density = st.number_input("Bulk Density", key="bulk_density")
            with soil_row1_right:
                buffering = st.number_input("Buffering Capacity", key="buffering")

            soil_row2_left, soil_row2_right = st.columns(2)
            with soil_row2_left:
                organic_matter = st.number_input("Organic Matter (%)", key="organic_matter")
            with soil_row2_right:
                cec = st.number_input("Cation Exchange Capacity", key="cec")

            # ================================
            # ENVIRONMENT
            # ================================
            st.subheader("🌡️ Environmental Conditions")

            env_row1_left, env_row1_right = st.columns(2)
            with env_row1_left:
                air_temp = st.number_input("Air Temperature (°C)", key="air_temp")
            with env_row1_right:
                soil_temp = st.number_input("Soil Temperature (°C)", key="soil_temp")

            env_row2_left, env_row2_right = st.columns(2)
            with env_row2_left:
                moisture = st.number_input("Soil Moisture (%)", key="moisture")
            with env_row2_right:
                salinity = st.number_input("Salinity (EC)", key="salinity")

            env_row3_left, env_row3_right = st.columns(2)
            with env_row3_left:
                light = st.number_input("Light Intensity", key="light")
            with env_row3_right:
                ph = st.number_input("Soil pH", key="ph")

            env_row4_left, env_row4_right = st.columns(2)
            with env_row4_left:
                nitrogen = st.number_input("Nitrogen (ppm)", key="nitrogen")
            with env_row4_right:
                phosphorus = st.number_input("Phosphorus (ppm)", key="phosphorus")

            potassium = st.number_input("Potassium (ppm)", key="potassium")

            # ================================
            # CATEGORY (TIDAK DIUBAH SESUAI PERMINTAANMU)
            # ================================
            st.subheader("🌿 Soil & Plant Info")

            category_left, category_right = st.columns(2)

            with category_left:
                soil_type = st.selectbox("Soil Type", [
                    "Sandy","Loamy","Clayey","Silty","Peaty",
                    "Chalky","Saline","Laterite","Alluvial"
                ], key="soil_type")

            with category_right:
                plant_category = st.selectbox("Plant Category", ["cereal","legume","vegetable"], key="plant_category")

            submit = st.form_submit_button("Predict")
    summary_items = [
        ("Air Temp", f"{air_temp} °C"),
        ("Soil Temp", f"{soil_temp} °C"),
        ("Moisture", f"{moisture} %"),
        ("Salinity", f"{salinity} EC"),
        ("Light", f"{light} PAR"),
        ("pH", f"{ph}"),
        ("Nitrogen", f"{nitrogen} ppm"),
        ("Phosphorus", f"{phosphorus} ppm"),
        ("Potassium", f"{potassium} ppm"),
        ("CEC", f"{cec}"),
        ("Bulk Density", f"{bulk_density}"),
        ("Organic Matter", f"{organic_matter} %"),
        ("Buffering", f"{buffering}"),
        ("Soil Type", soil_type),
        ("Plant Type", plant_category),
    ]

    summary_rows = [summary_items[index:index + 2] for index in range(0, len(summary_items), 2)]

    summary_html = "".join(
        '<div class="summary-grid">' + "".join(
            f'<div class="summary-item"><div class="summary-key">{label}</div><div class="summary-val">{value}</div></div>'
            for label, value in row
        ) + '</div>'
        for row in summary_rows
    )

    prediction_status = "idle"
    prediction_reason = None
    prediction_result = None
    success_percentage = 0.0
    failure_percentage = 0.0

    if submit:

        if nitrogen <= 0 or phosphorus <= 0 or potassium <= 0:
            st.error("❌ Nutrient tidak valid")
            st.stop()

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

        np_ratio = nitrogen / phosphorus
        nk_ratio = nitrogen / potassium
        ph_deviation = ph - 7
        moisture_deficit = 60 - moisture
        moisture_excess = moisture - 60
        salinity_stress = salinity * 1.5

        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=data,
                    timeout=10
                )

                response.raise_for_status()
                prediction_result = response.json()
                success_percentage = float(prediction_result.get("success_percentage", 0.0))
                failure_percentage = float(prediction_result.get("failure_percentage", 0.0))

                if "error" in prediction_result:
                    prediction_status = "error"
                    prediction_reason = prediction_result["error"]
                elif prediction_result.get("status") == "rule-based":
                    prediction_status = "rule-based"
                    prediction_reason = prediction_result.get("reason")
                else:
                    prediction_status = "success"
                    if prediction_result["prediction"] == 1:
                        prediction_reason = prediction_result.get("reason", "Model memprediksi kondisi ini masih belum optimal untuk tumbuh")
                    else:
                        prediction_reason = "Tanaman diprediksi dapat tumbuh"

            except requests.exceptions.ConnectionError:
                prediction_status = "error"
                prediction_reason = "Backend belum aktif. Jalankan server di Backend/main.py terlebih dahulu."

            except requests.exceptions.Timeout:
                prediction_status = "error"
                prediction_reason = "Request ke backend terlalu lama. Coba lagi setelah server siap."

            except requests.exceptions.HTTPError as e:
                prediction_status = "error"
                prediction_reason = f"Backend mengembalikan status error: {e.response.status_code}"

            except requests.exceptions.RequestException as e:
                prediction_status = "error"
                prediction_reason = f"Gagal menghubungi backend. {e}"

    with right_col:
        if submit and prediction_status == "success":
            if prediction_result and prediction_result.get("prediction") == 1:
                prediction_html = f'<div class="result-state">❌ {prediction_reason}</div>'
            else:
                prediction_html = '<div class="result-state">✅ Tanaman Dapat Tumbuh</div>'
        elif submit and prediction_status in {"error", "rule-based"}:
            prediction_html = f'<div class="result-state">❌ {prediction_reason}</div>'
        else:
            prediction_html = '<div class="result-muted">Isi data di sebelah kiri lalu klik Predict untuk melihat hasil prediksi di sini.</div>'

        st.markdown(
            dedent(f'''
                <div class="panel-card panel-card--side panel-card--summary">
                    <div class="panel-title">Ringkasan Data</div>
                    {summary_html}
                    <div class="panel-title" style="margin-top:1rem;">Hasil Prediksi</div>
                    {prediction_html}
                </div>
            '''),
            unsafe_allow_html=True,
        )

        if submit and prediction_status in {"success", "rule-based"}:
            percent_left, percent_right = st.columns(2)

            with percent_left:
                st.metric("Keberhasilan", f"{success_percentage:.2f}%")
                st.progress(max(0, min(100, int(round(success_percentage)))))

            with percent_right:
                st.metric("Kegagalan", f"{failure_percentage:.2f}%")
                st.progress(max(0, min(100, int(round(failure_percentage)))))

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()
