import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="CrossFit PR Tracker", page_icon="🏋️‍♂️", layout="centered")

st.title("🏋️‍♂️ מעקב שיאי קרוספיט - מחובר ל-Google Sheets")

# יצירת חיבור ל-Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# טעינת הנתונים מהגיליונות (יש לוודא ששמות הטאבים תואמים)
try:
    df_wl = conn.read(worksheet="Weightlifting", usecols=[0, 1], ttl=0)
    df_gym = conn.read(worksheet="Gymnastics", usecols=[0, 1], ttl=0)
except Exception as e:
    st.error(f"שגיאה בטעינת הנתונים מ-Google Sheets: {e}")
    st.stop()

# טאבים להפרדה
tab1, tab2 = st.tabs(["🏋️ Weightlifting & Powerlifting", "🤸 Gymnastics & Calisthenics"])

with tab1:
    st.subheader("עדכון משקלי עבודה (ק\"ג)")
    updated_wl = []
    for index, row in df_wl.iterrows():
        exercise = row["Exercise"]
        current_weight = float(row["Weight"]) if pd.notna(row["Weight"]) else 0.0
        new_weight = st.number_input(f"{exercise}", value=current_weight, step=2.5, format="%.1f", key=f"wl_{exercise}")
        updated_wl.append({"Exercise": exercise, "Weight": new_weight})
    
    df_wl_new = pd.DataFrame(updated_wl)

with tab2:
    st.subheader("עדכון תרגילי גמישות וממשקל גוף (חזרות)")
    updated_gym = []
    for index, row in df_gym.iterrows():
        exercise = row["Exercise"]
        current_reps = int(row["Reps"]) if pd.notna(row["Reps"]) else 0
        new_reps = st.number_input(f"{exercise}", value=current_reps, step=1, key=f"gym_{exercise}")
        updated_gym.append({"Exercise": exercise, "Reps": new_reps})
        
    df_gym_new = pd.DataFrame(updated_gym)

# כפתור שמירה ל-Google Sheets
if st.button("💾 שמור שיאים חדשים ל-Google Sheets", type="primary"):
    try:
        conn.update(worksheet="Weightlifting", data=df_wl_new)
        conn.update(worksheet="Gymnastics", data=df_gym_new)
        st.success("השיאים עודכנו בהצלחה ב-Google Sheets! 🎉")
        st.rerun()
    except Exception as e:
        st.error(f"שגיאה בשמירת הנתונים: {e}")

st.divider()
st.subheader("📊 סיכום שיאים נוכחי")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Weightlifting**")
    st.dataframe(df_wl[df_wl["Weight"] > 0], hide_index=True, use_container_width=True)

with col2:
    st.markdown("**Gymnastics**")
    st.dataframe(df_gym[df_gym["Reps"] > 0], hide_index=True, use_container_width=True)
