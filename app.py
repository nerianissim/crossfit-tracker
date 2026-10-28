import streamlit as st
import pandas as pd
import json
import base64
import requests

st.set_page_config(page_title="CrossFit PR Tracker", page_icon="🏋️‍♂️", layout="centered")
st.title("🏋️‍♂️ מעקב שיאי קרוספיט - שמירה אוטומטית ב-GitHub")

# טעינת הגדרות מ-Streamlit Secrets
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO = st.secrets["REPO_NAME"]
except Exception:
    st.error("⚠️ יש להגדיר את ה-Secrets (GITHUB_TOKEN ו-REPO) ב-Streamlit Cloud.")
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
        "message": "Update CrossFit PRs via Streamlit app",
        "content": encoded_content,
        "sha": sha
    }
    response = requests.put(API_URL, headers=headers, json=payload)
    return response.status_code in [200, 201]

data, file_sha = load_data_from_github()
if not data:
    st.error("שגיאה בטעינת הנתונים מ-GitHub.")
    st.stop()

tab1, tab2 = st.tabs(["🏋️ Weightlifting & Powerlifting", "🤸 Gymnastics & Calisthenics"])

with tab1:
    st.subheader("עדכון משקלי עבודה (ק\"ג)")
    updated_wl = {}
    for exercise, weight in data["Weightlifting"].items():
        val = st.number_input(f"{exercise}", value=float(weight), step=2.5, format="%.1f", key=f"wl_{exercise}")
        updated_wl[exercise] = val

with tab2:
    st.subheader("עדכון תרגילי גמישות וממשקל גוף (חזרות)")
    updated_gym = {}
    for exercise, reps in data["Gymnastics"].items():
        val = st.number_input(f"{exercise}", value=int(reps), step=1, key=f"gym_{exercise}")
        updated_gym[exercise] = val

if st.button("💾 שמור שיאים חדשים ל-GitHub", type="primary", use_container_width=True):
    new_data = {
        "Weightlifting": updated_wl,
        "Gymnastics": updated_gym
    }
    success = save_data_to_github(new_data, file_sha)
    if success:
        st.success("השיאים נשמרו בהצלחה ב-GitHub! 🎉")
        st.cache_data.clear()
        st.rerun()
    else:
        st.error("שגיאה בשמירת הנתונים מול GitHub.")

st.divider()
st.subheader("📊 סיכום שיאים נוכחי")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Weightlifting**")
    df_wl = pd.DataFrame(list(data["Weightlifting"].items()), columns=["תרגיל", "משקל (ק\"ג)"])
    st.dataframe(df_wl[df_wl["משקל (ק\"ג)"] > 0], hide_index=True, use_container_width=True)

with col2:
    st.markdown("**Gymnastics**")
    df_gym = pd.DataFrame(list(data["Gymnastics"].items()), columns=["תרגיל", "חזרות"])
    st.dataframe(df_gym[df_gym["חזרות"] > 0], hide_index=True, use_container_width=True)
