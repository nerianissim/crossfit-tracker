import streamlit as st
import pandas as pd

st.set_page_config(page_title="CrossFit PR Tracker", page_icon="🏋️‍♂️", layout="centered")

st.title("🏋️‍♂️ מעקב שיאי קרוספיט")

# קישור ישיר ל-Google Sheets (מותנה בכך שהגיליון שותף לציבור: Anyone with the link can view)
# שים לב: החלף את הקישור למטה בקישור האמיתי של הגיליון שלך
SHEET_ID = "1oKK8oJ2N_z0I3oGKYJPhG-AUNf4hR9VGNNWpg6wUayc"

# דרך פשוטה ומהירה לקרוא את הנתונים ישירות ללא תלות בספריות חיצוניות
@st.cache_data(ttl=60)
def load_data():
    # כתובת ייצוא ל-CSV מתוך גוגל שיטס
    url_wl = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Weightlifting"
    url_gym = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Gymnastics"
    
    df_wl = pd.read_csv(url_wl)
    df_gym = pd.read_csv(url_gym)
    return df_wl, df_gym

try:
    df_wl, df_gym = load_data()
except Exception as e:
    st.warning("נא להזין את ה-ID של הגיליון שלך בקוד כדי לטעון את הנתונים.")
    st.stop()

tab1, tab2 = st.tabs(["🏋️ Weightlifting & Powerlifting", "🤸 Gymnastics & Calisthenics"])

with tab1:
    st.subheader("משקלי עבודה (ק\"ג)")
    st.dataframe(df_wl, hide_index=True, use_container_width=True)

with tab2:
    st.subheader("תרגילי גמישות וממשקל גוף (חזרות)")
    st.dataframe(df_gym, hide_index=True, use_container_width=True)
