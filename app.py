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

# הזרקת עיצוב CSS מותאם אישית (Dark Mode יוקרתי, כרטיסיות מוקפדות ויישור לימין)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap');
    
    /* רקע כללי שחור-אפור עמוק */
    .stApp {
        background-color: #0E1117;
        color: #F8FAFC;
        font-family: 'Heebo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* כותרת ראשית ענקית באמצע */
    .hero-container {
        text-align: center;
        padding: 2rem 0 1rem 0;
        border-bottom: 2px solid #1F2937;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 3rem;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 2px;
        margin: 0;
        text-transform: uppercase;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #9CA3AF;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* עיצוב לשוניות (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 10px;
        background-color: #161B22;
        padding: 10px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #21262D;
        color: #9CA3AF;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
    }

    /* כרטיסיות קטנות לתרגילים */
    div.stNumberInput {
        background-color: #161B22;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #30363D;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    div.stNumberInput label {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* כפתור שמירה מקצועי ובולט */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.2rem;
        padding: 0.8rem;
        border: none;
        box-
