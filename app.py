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

# עיצוב CSS מתקדם ומקצועי (Dark Mode מודרני, כרטיסים ואפקטים)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap');
    
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
        font-family: 'Heebo', sans-serif;
    }
    
    /* כותרת ראשית יוקרתית */
    .hero-container {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        background: linear-gradient(180deg, rgba(37, 99, 235, 0.12) 0%, rgba(11, 15, 25, 0) 100%);
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

    /* עיצוב לשוניות (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 10px;
        background-color: #111827;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #1F2937;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #94A3B8;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }

    /* עיצוב שדות המספרים (כארדים) */
    div.stNumberInput {
        background-color: #111827;
        padding: 14px;
        border-radius: 12px;
        border: 1px solid #1F2937;
        margin-bottom: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        transition: border-color 0.2s ease;
    }
    div.stNumberInput:hover {
        border-color: #3B82F6;
    }
    div.stNumberInput label {
        color: #E2E8F0 !important;
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
        box-shadow: 0 8px 20px -4px rgba(37, 99, 235, 0.5);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        box-shadow: 0 12px 24px -4px rgba(37, 99, 235, 0.7);
        transform: translateY(-2px);
    }

    /* טבלאות נתונים בעיצוב דארק מודי */
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
    "🤸 גυμנסטיקה (Gymnastics)", 
    "🧮 מחשבון אחוזים (Percentage Calc)"
])

# --- טאב 1: סקירה כללית ---
with tab_overview:
    st.markdown("### 📈 מדדי ביצוע מרכזיים")
    
    wl_dict = data.get("Weightlifting", DEFAULT_DATA["Weightlifting"])
    gym_dict = data.get("Gymnastics", DEFAULT_DATA["Gymnastics"])
    
    # חישוב מדדים
    active_lifts = {k: v for k, v in wl_dict.items() if v > 0}
    max_lift_name = max(active_lifts, key=active_lifts.get) if active_lifts else "אין"
    max_lift_val = active_lifts[max_lift_name] if active_lifts else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("סה\"כ תרגילי כוח", len(wl_dict))
    col2.metric("התרגיל החזק ביותר", max_lift_name, f"{max_lift_val} ק\"ג")
    col3.metric("תרגילי גิמנסטיקה", len(gym_dict))
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 השוואת משקלי כוח (גרף)")
    if active_lifts:
        df_chart = pd.DataFrame(list(active_lifts.items()), columns=["תרגיל", "משקל (ק\"ג)"])
        df_chart = df_chart.set_index("תרגיל")
        st.bar_chart(df_chart, color="#2563EB")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # טבלאות סיכום מהירות
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**🏆 Weightlifting PRs**")
        df_wl = pd.DataFrame(list(wl_dict.items()), columns=["תרגיל", "משקל (ק\"ג)"])
        st.dataframe(df_wl[df_wl["משקל (ק\"ג)"] > 0], hide_index=True, use_container_width=True)
    with col_t2:
        st.markdown("**⭐ Gymnastics PRs**")
        df_gym = pd.DataFrame(list(gym_dict.items()), columns=["תרגיל", "חזרות"])
        st.dataframe(df_gym[df_gym["חזרות"] > 0], hide_index=True, use_container_width=True)

# --- טאב 2: משקלי עבודה ---
with tab_overview: # placeholder to keep syntax clean, actual tab is below
    pass

# We redefine tabs content cleanly:
# Let's organize the update logic for user inputs inside the tabs
updated_wl = {}
updated_gym = {}

with tab_wl:
    st.markdown("### 🏋️ ניהול משקלי עבודה (ק\"ג)")
    st.markdown("עדכן את שיאי המשקל שלך. השינויים יישמרו בענן בלחיצת כפתור.")
    cols = st.columns(2)
    items = list(wl_dict.items())
    half = len(items) // 2
    
    for i, (exercise, weight) in enumerate(items):
        target_col = cols[0] if i < half else cols[1]
        with target_col:
            val = st.number_input(exercise, value=float(weight), step=2.5, format="%.1f", key=f"wl_{exercise}")
            updated_wl[exercise] = val

with tab_gym:
    st.markdown("### 🤸 ניהול תרגילי משקל גוף (חזרות)")
    st.markdown("עדכן את מקסימום החזרות הרצוף שאתה מבצע.")
    cols_g = st.columns(2)
    gym_items = list(gym_dict.items())
    half_g = len(gym_items) // 2
    
    for i, (exercise, reps) in enumerate(gym_items):
        target_col = cols_g[0] if i < half_g else cols_g[1]
        with target_col:
            val = st.number_input(exercise, value=int(reps), step=1, key=f"gym_{exercise}")
            updated_gym[exercise] = val

# --- טאב 3: מחשבון אחוזים חכם ---
with tab_calc:
    st.markdown("### 🧮 מחשבון אחוזים לעבודה (Percentage Calculator)")
    st.markdown("בחר תרגיל וחשב באופן מיידי את משקלי העבודה שלך לאימון (לפי אחוזים מ-1RM).")
    
    calc_col1, calc_col2 = st.columns([2, 1])
    with calc_col1:
        selected_exercise = st.selectbox("בחר תרגיל מתוך השיאים שלך:", list(wl_dict.keys()))
    with calc_col2:
        custom_base = st.number_input("או הזן משקל ידני (ק\"ג):", value=float(wl_dict.get(selected_exercise, 100)), step=5.0)
    
    if custom_base > 0:
        st.markdown(f"#### תוצאות אחוזים עבור **{selected_exercise}** ({custom_base} ק\"ג):")
        
        percentages = [50, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        perc_data = []
        for p in percentages:
            calculated_weight = round((custom_base * p) / 100, 1)
            perc_data.append({"אחוז (Percentage)": f"{p}%", "משקל עבודה (ק\"ג)": calculated_weight})
        
        df_perc = pd.DataFrame(perc_data)
        st.dataframe(df_perc, hide_index=True, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- אזור כפתור שמירה מרכזי ---
st.markdown("<hr style='border-color: #1F2937; margin: 1.5rem 0;'>", unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("💾 שמור שיאים חדשים בענן", type="primary"):
        with st.spinner("מעדכן את בסיס הנתונים ב-GitHub..."):
            new_data = {
                "Weightlifting": updated_wl if updated_wl else wl_dict,
                "Gymnastics": updated_gym if updated_gym else gym_dict
            }
            success = save_data_to_github(new_data, file_sha)
            if success:
                st.toast("השיאים נשמרו בהצלחה בענן! 🎉", icon="✅")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("שגיאה בשמירת הנתונים מול GitHub.")
