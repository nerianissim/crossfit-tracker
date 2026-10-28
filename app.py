import streamlit as st
import pandas as pd
import json
import base64
import requests

# הגדרת עמוד עם תמיכה בעיצוב נקי
st.set_page_config(
    page_title="CrossFit PR Dashboard", 
    page_icon="🏆", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# הזרקת עיצוב CSS מותאם אישית למראה רשמי ומקצועי יותר (כולל יישור לימין)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Heebo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* עיצוב כפתורים */
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# כותרת ראשית מעוצבת
st.markdown('<p class="main-header">🏆 CrossFit Personal Records</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">מערכת מעקב וניהול שיאים אישיים</p>', unsafe_allow_html=True)

# טעינת הגדרות אבטחה
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
        "message": "Update CrossFit PRs via Dashboard",
        "content": encoded_content,
        "sha": sha
    }
    response = requests.put(API_URL, headers=headers, json=payload)
    return response.status_code in [200, 201]

data, file_sha = load_data_from_github()
if not data:
    st.error("❌ שגיאה בטעינת הנתונים מול GitHub. בדוק את הרשאות הטוקן ושם המאגר.")
    st.stop()

# יצירת לשוניות מעוצבות
tab1, tab2 = st.tabs(["🏋️ Weightlifting & Powerlifting", "🤸 Gymnastics & Calisthenics"])

with tab1:
    st.markdown("### משקלי עבודה (ק\"ג)")
    updated_wl = {}
    
    # חלוקה ל-2 טוריות פנימיות לנוחות צפייה ועריכה
    cols = st.columns(2)
    items = list(data["Weightlifting"].items())
    half = len(items) // 2
    
    for i, (exercise, weight) in enumerate(items):
        target_col = cols[0] if i < half else cols[1]
        with target_col:
            val = st.number_input(f"{exercise}", value=float(weight), step=2.5, format="%.1f", key=f"wl_{exercise}")
            updated_wl[exercise] = val

with tab2:
    st.markdown("### תרגילי משקל גוף וגמישות (חזרות)")
    updated_gym = {}
    
    cols_g = st.columns(2)
    gym_items = list(data["Gymnastics"].items())
    half_g = len(gym_items) // 2
    
    for i, (exercise, reps) in enumerate(gym_items):
        target_col = cols_g[0] if i < half_g else cols_g_1 = cols_g[1] if i >= half_g else cols_g[1]
        with target_col:
            val = st.number_input(f"{exercise}", value=int(reps), step=1, key=f"gym_{exercise}")
            updated_gym[exercise] = val

st.markdown("<br>", unsafe_allow_html=True)

# כפתור שמירה מרכזי בולט ונקי
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("💾 שמור שיאים חדשים", type="primary"):
        new_data = {
            "Weightlifting": updated_wl,
            "Gymnastics": updated_gym
        }
        success = save_data_to_github(new_data, file_sha)
        if success:
            st.success("השיאים עודכנו ונשמרו בהצלחה! 🎉")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("שגיאה בשמירת הנתונים מול GitHub. ודא שהטוקן תקין.")

st.divider()

# חלק סיכום נקי
st.markdown("### 📊 סיכום שיאים אישיים פעילים")
summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.markdown("**הרתמנויות - Weightlifting**")
    df_wl = pd.DataFrame(list(data["Weightlifting"].items()), columns=["תרגיל", "משקל (ק\"ג)"])
    st.dataframe(df_wl[df_wl["משקל (ק\"ג)"] > 0], hide_index=True, use_container_width=True)

with summary_col2:
    st.markdown("**גמישות - Gymnastics**")
    df_gym = pd.DataFrame(list(data["Gymnastics"].items()), columns=["תרגיל", "חזרות"])
    st.dataframe(df_gym[df_gym["חזרות"] > 0], hide_index=True, use_container_width=True)
