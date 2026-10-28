import streamlit as st
import pandas as pd
import json
import base64
import requests

# הגדרת עמוד
st.set_page_config(
    page_title="CrossFit PR Tracker Pro", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# עיצוב CSS מתקדם ומקצועי (Dark Mode מודרני)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap');
    
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
        font-family: 'Heebo', sans-serif;
    }
    
    .hero-container {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        background: linear-gradient(180deg, rgba(37, 99, 235, 0.08) 0%, rgba(11, 15, 25, 0) 100%);
        border-bottom: 1px solid #1E293B;
        margin-bottom: 2rem;
        border-radius: 0 0 16px 16px;
    }
    .main-title {
        font-size: 3rem;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 2px;
        margin: 0;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #94A3B8;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 12px;
        background-color: #111827;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #1F2937;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #94A3B8;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }

    div.stNumberInput {
        background-color: #111827;
        padding: 14px;
        border-radius: 12px;
        border: 1px solid #1F2937;
        margin-bottom: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    div.stNumberInput label {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.2rem;
        padding: 0.9rem;
        border: none;
        box-shadow: 0 8px 20px -4px rgba(37, 99, 235, 0.5);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        transform: translateY(-2px);
    }

    .dataframe {
        background-color: #111827 !important;
        color: #F8FAFC !important;
        border-radius: 10px !important;
        border: 1px solid #1F2937 !important;
    }
    </style>
""", unsafe_allow_html=True)

# כותרת ראשית מרכזית
st.markdown("""
    <div class="hero-container">
        <p class="main-title">⚡ CROSSFIT</p>
        <p class="sub-title">מערכת ניהול שיאים אישיים מתקדמת</p>
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

DEFAULT_DATA = {
    "Weightlifting": {
        "Back Squat": 120, "Front Squat": 65, "Deadlift": 110, "Power Clean": 70,
        "Push Jerk": 60, "Strict Press": 50, "Push-Press": 55, "Bench Press": 60, "Power Snatch": 55
    },
    "Gymnastics": {
        "Strict Pull-Ups": 0, "Kipping Pull-Ups": 0, "Strict Handstand Push-Ups": 0,
        "Kipping Handstand Push-Ups": 0, "Ring Muscle-Ups": 0, "Toes to Bar": 0, "Bar Muscle-Ups": 0
    }
}

@st.cache_data(ttl=1)
def load_data_from_github():
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        try:
            file_content = base64.b64decode(file_info["content"]).decode("utf-8")
            data = json.loads(file_content)
            if not isinstance(data, dict) or "Weightlifting" not in data:
                return DEFAULT_DATA, file_info.get("sha")
            return data, file_info["sha"]
        except Exception:
            return DEFAULT_DATA, file_info.get("sha")
    return DEFAULT_DATA, None

def save_data_to_github(data_dict, sha):
    updated_content = json.dumps(data_dict, indent=4, ensure_ascii=False)
    encoded_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": "Update CrossFit PRs via Pro Dashboard",
        "content": encoded_content
    }
    if sha:
        payload["sha"] = sha
        
    response = requests.put(API_URL, headers=headers, json=payload)
    return response.status_code in [200, 201]

data, file_sha = load_data_from_github()

# לשוניות ראשיות
tab1, tab2 = st.tabs(["🏋️ Weightlifting", "🤸 Gymnastics"])

with tab1:
    st.markdown("### 🏋️ משקלי עבודה (ק\"ג)")
    updated_wl = {}
    cols = st.columns(2)
    items = list(data.get("Weightlifting", DEFAULT_DATA["Weightlifting"]).items())
    half = len(items) // 2
    
    for i, (exercise, weight) in enumerate(items):
        target_col = cols[0] if i < half else cols[1]
        with target_col:
            val = st.number_input(exercise, value=float(weight), step=2.5, format="%.1f", key=f"wl_{exercise}")
            updated_wl[exercise] = val

with tab2:
    st.markdown("### 🤸 תרגילי משקל גוף (חזרות)")
    updated_gym = {}
    cols_g = st.columns(2)
    gym_items = list(data.get("Gymnastics", DEFAULT_DATA["Gymnastics"]).items())
    half_g = len(gym_items) // 2
    
    for i, (exercise, reps) in enumerate(gym_items):
        target_col = cols_g[0] if i < half_g else cols_g[1]
        with target_col:
            val = st.number_input(exercise, value=int(reps), step=1, key=f"gym_{exercise}")
            updated_gym[exercise] = val

st.markdown("<br>", unsafe_allow_html=True)

# כפתור שמירה ראשי בולט ומעוצב
col_btn1, col_btn2, col_btn3 = st.columns([1, 3, 1])
with col_btn2:
    if st.button("💾 שמור שיאים חדשים במערכת", type="primary"):
        new_data = {
            "Weightlifting": updated_wl,
            "Gymnastics": updated_gym
        }
        success = save_data_to_github(new_data, file_sha)
        if success:
            st.success("השיאים עודכנו ונשמרו בהצלחה ב-GitHub! 🎉")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("שגיאה בשמירת הנתונים. ודא שהטוקן תקין.")

st.markdown("<hr style='border-color: #1F2937; margin: 2rem 0;'>", unsafe_allow_html=True)

# חלק סיכום נקי
st.markdown("### 📊 סיכום שיאים אישיים פעילים")
summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.markdown("**Weightlifting PRs**")
    df_wl = pd.DataFrame(list(updated_wl.items()), columns=["תרגיל", "משקל (ק\"ג)"])
    st.dataframe(df_wl[df_wl["משקל (ק\"ג)"] > 0], hide_index=True, use_container_width=True)

with summary_col2:
    st.markdown("**Gymnastics PRs**")
    df_gym = pd.DataFrame(list(updated_gym.items()), columns=["תרגיל", "חזרות"])
    st.dataframe(df_gym[df_gym["חזרות"] > 0], hide_index=True, use_container_width=True)
