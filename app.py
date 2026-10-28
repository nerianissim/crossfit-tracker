import streamlit as st
import pandas as pd
import json
import base64
import requests

# הגדרת עמוד
st.set_page_config(
    page_title="CrossFit PR Tracker", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# עיצוב CSS נקי, יוקרתי ומותאם אישית (ללא חסימת שדות)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap');
    
    .stApp {
        background-color: #0E1117;
        color: #F8FAFC;
        font-family: 'Heebo', sans-serif;
    }
    
    /* כותרת ראשית */
    .hero-container {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #1F2937;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 2px;
        margin: 0;
    }
    .sub-title {
        font-size: 1rem;
        color: #9CA3AF;
        margin-top: 0.4rem;
    }

    /* עיצוב כפתור השמירה */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.7rem;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# כותרת ראשית מרכזית
st.markdown("""
    <div class="hero-container">
        <p class="main-title">⚡ CROSSFIT</p>
        <p class="sub-title">מערכת מעקב שיאים אישיים מתקדמת</p>
    </div>
""", unsafe_allow_html=True)

# טעינת הגדרות אבטחה מ-Secrets
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO = st.secrets["REPO_NAME"]
except Exception:
    st.error("⚠️ יש להגדיר תקינות של GITHUB_TOKEN ו-REPO ב-Streamlit Secrets.")
    st.stop()

FILE_PATH = "data.json"
API_URL = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

@st.cache_data(ttl=1)
def load_data_from_github():
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        file_content = base64.b64decode(file_info["content"]).decode("utf-8")
        return json.loads(file_content), file_info["sha"]
    return None, None

def save_data_to_github(data_dict, sha):
    updated_content = json.dumps(data_dict, indent=4, ensure_ascii=False)
    encoded_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": "Update CrossFit PRs via Pro Dashboard",
        "content": encoded_content,
        "sha": sha
    }
    response = requests.put(API_URL, headers=headers, json=payload)
    return response.status_code in [200, 201]

data, file_sha = load_data_from_github()
if not data:
    st.error("❌ שגיאה בטעינת הנתונים מול GitHub. בדוק את הרשאות הטוקן ושם המאגר.")
    st.stop()

# לשוניות ראשיות
tab1, tab2 = st.tabs(["🏋️ Weightlifting", "🤸 Gymnastics"])

with tab1:
    st.subheader("🏋️ משקלי עבודה (ק\"ג)")
    updated_wl = {}
    cols = st.columns(2)
    items = list(data["Weightlifting"].items())
    half = len(items) // 2
    
    for i, (exercise, weight) in enumerate(items):
        target_col = cols[0] if i < half else cols[1]
        with target_col:
            val = st.number_input(f"{exercise}", value=float(weight), step=2.5, format="%.1f", key=f"wl_{exercise}")
            updated_wl[exercise] = val

with tab2:
    st.subheader("🤸 תרגילי משקל גוף (חזרות)")
    updated_gym = {}
    cols_g = st.columns(2)
    gym_items = list(data["Gymnastics"].items())
    half_g = len(gym_items)
