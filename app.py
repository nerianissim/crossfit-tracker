import streamlit as st
import pandas as pd
import urllib.parse
import urllib.request

st.set_page_config(page_title="CrossFit PR Tracker", page_icon="🏋️‍♂️", layout="centered")

st.title("🏋️‍♂️ מעקב שיאי קרוספיט")

# הכנס כאן את ה-ID של הגיליון שלך מתוך הכתובת ב-Google Sheets
SHEET_ID = "YOUR_SPREADSHEET_ID_HERE"

@st.cache_data(ttl=1)
def load_data():
    url_wl = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Weightlifting"
    url_gym = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Gymnastics"
    df_wl = pd.read_csv(url_wl)
    df_gym = pd.read_csv(url_gym)
    return df_wl, df_gym

try:
    df_wl, df_gym = load_data()
except Exception:
    st.warning("⚠️ נא לוודא שהכנסת את ה-ID של הגיליון בקוד ושהגיליון מוגדר כציבורי לקריאה (Anyone with the link can view).")
    st.stop()

tab1, tab2 = st.tabs(["🏋️ Weightlifting & Powerlifting", "🤸 Gymnastics & Calisthenics"])

with tab1:
    st.subheader("עדכון משקלי עבודה (ק\"ג)")
    updated_wl = []
    for _, row in df_wl.iterrows():
        exercise = row["Exercise"]
        current_weight = float(row["Weight"]) if pd.notna(row["Weight"]) else 0.0
        new_weight = st.number_input(f"{exercise}", value=current_weight, step=2.5, format="%.1f", key=f"wl_{exercise}")
        updated_wl.append({"Exercise": exercise, "Weight": new_weight})
    df_wl_new = pd.DataFrame(updated_wl)

with tab2:
    st.subheader("עדכון תרגילי גמישות וממשקל גוף (חזרות)")
    updated_gym = []
    for _, row in df_gym.iterrows():
        exercise = row["Exercise"]
        current_reps = int(row["Reps"]) if pd.notna(row["Reps"]) else 0
        new_reps = st.number_input(f"{exercise}", value=current_reps, step=1, key=f"gym_{exercise}")
        updated_gym.append({"Exercise": exercise, "Reps": new_reps})
    df_gym_new = pd.DataFrame(updated_gym)

st.divider()

# הוראות להעתקה נוחה לעדכון הגיליון
st.info("💡 **איך מעדכנים את הגיליון?** שנה את המשקלים או החזרות למעלה, העתק את הטבלה המוכנה שמופיעה למטה, והדבק ב-Google Sheets.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**נתוני Weightlifting מעודכנים להעתקה:**")
    st.dataframe(df_wl_new, hide_index=True, use_container_width=True)

with col2:
    st.markdown("**נתוני Gymnastics מעודכנים להעתקה:**")
    st.dataframe(df_gym_new, hide_index=True, use_container_width=True)
