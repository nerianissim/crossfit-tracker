import streamlit as st
import pandas as pd

st.set_page_config(page_title="CrossFit PR Tracker", page_icon="🏋️‍♂️", layout="centered")

st.title("🏋️‍♂️ שיאים אישיים - CrossFit PRs")

# נתונים התחלתיים מתוך התמונה
default_weightlifting = {
    "Back Squat": 120.0,
    "Front Squat": 65.0,
    "Overhead Squat": 0.0,
    "Deadlift": 110.0,
    "Power Clean": 70.0,
    "Squat Clean": 0.0,
    "Squat Snatch": 0.0,
    "Clean & Jerk": 0.0,
    "Push Jerk": 60.0,
    "Split Jerk": 0.0,
    "Strict Press": 50.0,
    "Push-Press": 55.0,
    "Bench Press": 60.0,
    "Power Snatch": 55.0,
}

default_gymnastics = {
    "Strict Pull-Ups": 0,
    "Kipping Pull-Ups": 0,
    "Strict Handstand Push-Ups": 0,
    "Kipping Handstand Push-Ups": 0,
    "Strict Chest to Bar Pull-Ups": 0,
    "Kipping Chest to Bar Pull-Ups": 0,
    "Ring Muscle-Ups": 0,
    "Toes to Bar": 0,
    "Bar Muscle-Ups": 0,
}

# טאבים להפרדה נוחה
tab1, tab2 = st.tabs(["🏋️ Weightlifting & Powerlifting", "🤸 Gymnastics & Calisthenics"])

with tab1:
    st.subheader("משקלי עבודה (ק\"ג)")
    wl_data = {}
    for exercise, weight in default_weightlifting.items():
        val = st.number_input(f"{exercise}", value=weight, step=2.5, format="%.1f", key=exercise)
        wl_data[exercise] = val

with tab2:
    st.subheader("תרגילי גמישות וממשקל גוף (חזרות max)")
    gym_data = {}
    for exercise, reps in default_gymnastics.items():
        val = st.number_input(f"{exercise}", value=reps, step=1, key=exercise)
        gym_data[exercise] = val

st.divider()
st.subheader("📊 סיכום שיאים עדכני")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Weightlifting**")
    df_wl = pd.DataFrame(list(wl_data.items()), columns=["תרגיל", "משקל (ק\"ג)"])
    st.dataframe(df_wl[df_wl["משקל (ק\"ג)"] > 0], hide_index=True, use_container_width=True)

with col2:
    st.markdown("**Gymnastics**")
    df_gym = pd.DataFrame(list(gym_data.items()), columns=["תרגיל", "חזרות"])
    st.dataframe(df_gym[df_gym["חזרות"] > 0], hide_index=True, use_container_width=True)
