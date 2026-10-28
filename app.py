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
