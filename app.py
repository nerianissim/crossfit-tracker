import streamlit as st
import pandas as pd
import json
import base64
import requests

# הגדרת עמוד
st.set_page_config(
    page_title="CrossFit PR Pro Suite", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# עיצוב CSS מתקדם ומקצועי למצב בהיר (Light Mode נקי ויוקרתי)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap');
    
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
        font-family: 'Heebo', sans-serif;
    }
    
    /* כותרת ראשית יוקרתית בהירה */
    .hero-container {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        background: linear-gradient(180deg, rgba(37, 99, 235, 0.06) 0%, rgba(248, 250, 252, 0) 100%);
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 2rem;
        border-radius: 0 0 16px 16px;
    }
    .main-title {
        font-size: 3rem;
        font-weight: 900;
        color: #0F172A;
        letter-spacing: 2px;
        margin: 0;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #64748B;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* עיצוב לשוניות (Tabs) בהירות */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 10px;
        background-color: #FFFFFF;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #64748B;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }

    /* עיצוב שדות המספרים (כארדים לבנים נקיים) */
    div.stNumberInput {
        background-color: #FFFFFF;
        padding: 14px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 14px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    div.stNumberInput:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
    }
    div.stNumberInput label {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    /* כפתור שמירה מקצועי ובולט */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.2rem;
        padding: 0.9rem;
        border: none;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
    }

    /* טבלאות נתונים במצב בהיר */
    .dataframe {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# כותרת ראשית מרכזית
st.markdown("""
    <div class="hero-container">
        <p class="main-title">⚡ CROSSFIT PRO</p>
        <p class="sub-title">מערכת ניהול שיאים אישיים ומדדי ביצוע</p>
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
        "Back Squat": 120, "Front Squat": 95, "Deadlift": 150, "Power Clean": 85,
        "Clean & Jerk": 80, "Snatch": 70, "Strict Press": 60, "Bench Press": 90
    },
    "Gymnastics": {
        "Strict Pull-Ups": 15, "Kipping Pull-Ups": 40, "Strict Handstand Push-Ups": 10,
        "Ring Muscle-Ups": 5, "Toes to Bar": 30, "Bar Muscle-Ups": 8
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

# יצירת לשוניות ניווט מתקדמות
tab_overview, tab_wl, tab_gym, tab_calc = st.tabs([
    "📊 סקירה כללית (Overview)", 
    "🏋️ משקלי עבודה (Weightlifting)", 
    "🤸 ג׳ימנסטיקה (Gymnastics)", 
    "🧮 מחשבון אחוזים (Percentage Calc)"
])

wl_dict = data.get("Weightlifting", DEFAULT_DATA["Weightlifting"])
gym_dict = data.get("Gymnastics", DEFAULT_DATA["Gymnastics"])

# --- טאב 1: סקירה כללית ---
with tab_overview:
    st.markdown("### 📈 מדדי ביצוע מרכזיים")
    
    active_lifts = {k: v for k, v in wl_dict.items() if v > 0}
    max_lift_name = max(active_lifts, key=active_lifts.get) if active_lifts else "אין"
    max_lift_val = active_lifts[max_lift_name] if active_lifts else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("סה\"כ תרגילי כוח", len(wl_dict))
    col2.metric("התרגיל החזק ביותר", max_lift_name, f"{max_lift_val} ק\"ג")
    col3.metric("תרגילי ג׳ימנסטיקה", len(gym_dict))
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 השוואת משקלי כוח (גרף)")
    if active_lifts:
        df_chart = pd.DataFrame(list(active_lifts.items()), columns=["תרגיל", "משקל (ק\"ג)"])
        df_chart = df_chart.set_index("תרגיל")
        st.bar_chart(df_chart, color="#2563EB")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**🏆 Weightlifting PRs**")
        df_wl = pd.DataFrame(list(wl_dict.items()), columns=["תרגיל", "משקל (ק\"ג)"])
        st.dataframe(df_wl[df_wl["משקל (ק\"ג)"] > 0], hide_index=True, use_container_width=True)
    with col_t2:
        st.markdown("**⭐ Gymnastics PRs**")
        df_gym = pd.DataFrame(list(gym_dict.items()), columns=["תרגיל", "חזרות"])
        st.dataframe(df_gym[df_gym["חזרות"] > 0], hide_index=True, use_container_width=True)

updated_wl = {}
updated_gym = {}

# --- טאב 2: משקלי עבודה ---
with tab_wl:
    st.markdown("### 🏋️ ניהול משקלי עבודה (ק\"ג)")
    st.markdown("עדכן את שיאי המשקל שלך. השינויים יישמרו בענן בלחיצת כפתור.")
    cols = st.columns(2)
    items = list(wl_dict.items())
    half = len(items) // 2
    
    for i, (exercise, weight) in enumerate(items):
        target_col = cols[0] if i < half else cols[1]
        with target_col:
            val = st.number_input(exercise, value=float(weight), step=2.5, format="%.1f", key
