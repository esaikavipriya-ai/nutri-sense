import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import date
from io import BytesIO

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="Nutri-Sense AI", layout="wide", page_icon="🧘")
st.markdown("""
    <style>
    .main { background-color: #f9fbf9; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1b5e20; color: white; height: 3.5em; font-weight: bold; }
    div[data-testid="stExpander"] { border: 1px solid #e0e0e0; border-radius: 12px; background-color: #ffffff; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    h1 { color: #2e7d32; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧘 Nutri-Sense: AI Health & Yoga Guide")
st.write("### Personalized 7-Day Wellness & Nutrition Plan")

# --- 2. 7-DAY WELLNESS DATASET ---
# Images sourced from Unsplash (Royalty-free)
weekly_data = {
    "Monday": {
        "Yoga": "Tree Pose (Vrikshasana)",
        "Img": "https://images.unsplash.com",
        "Food": "Steel-cut oats with almonds & flax seeds",
        "Benefit": "Enhances physical balance and mental focus."
    },
    "Tuesday": {
        "Yoga": "Cobra Pose (Bhujangasana)",
        "Img": "https://images.unsplash.com",
        "Food": "Quinoa bowl with leafy greens and lemon",
        "Benefit": "Strengthens the spine and stimulates abdominal organs."
    },
    "Wednesday": {
        "Yoga": "Warrior II (Virabhadrasana II)",
        "Img": "https://images.unsplash.com",
        "Food": "Lentil dal with brown rice and turmeric",
        "Benefit": "Improves circulation and increases muscular endurance."
    },
    "Thursday": {
        "Yoga": "Triangle Pose (Trikonasana)",
        "Img": "https://images.unsplash.com",
        "Food": "Grilled tofu/chickpea salad with avocado",
        "Benefit": "Stretches the hips and helps relieve back pain."
    },
    "Friday": {
        "Yoga": "Child's Pose (Balasana)",
        "Img": "https://images.unsplash.com",
        "Food": "Steamed broccoli and sweet potato mash",
        "Benefit": "Calms the nervous system and relieves neck tension."
    },
    "Saturday": {
        "Yoga": "Plank Pose (Phalakasana)",
        "Img": "https://images.unsplash.com",
        "Food": "Greek yogurt/Plant-based yogurt with berries",
        "Benefit": "Builds core strength and improves overall posture."
    },
    "Sunday": {
        "Yoga": "Corpse Pose (Savasana)",
        "Img": "https://images.unsplash.com",
        "Food": "Light vegetable stir-fry with ginger",
        "Benefit": "Allows the body to recover and reduces fatigue."
    }
}

# --- 3. THE REQUIRED USER FORM ---
with st.form("health_profile"):
    st.subheader("📋 Step 1: Complete Your Profile (All Fields Required)")
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name*", placeholder="Enter your name")
        age = st.number_input("Age*", 10, 100, value=25)
        gender = st.selectbox("Gender*", ["--Select--", "Male", "Female", "Other"])
    with c2:
        mood = st.selectbox("Current Mood*", ["--Select--", "Happy", "Stressed", "Tired", "Calm"])
        sleep = st.slider("Sleep Hours*", 0, 12, 7)
        symptoms = st.multiselect("Health Concerns*", ["None", "Headache", "Body Pain", "Fatigue", "Digestion Issues"])

    submit_button = st.form_submit_button("🚀 Generate Wellness Report")

# --- 4. VALIDATION & DASHBOARD ---
if submit_button:
    # Strict validation check
    if not name or gender == "--Select--" or mood == "--Select--" or not symptoms:
        st.error("⚠️ Error: All fields marked with * are required to generate your plan.")
    else:
        st.success(f"Form Submitted! Generating plan for {name}...")
        
        # Risk Metric
        risk_level = "Low" if "None" in symptoms else "Moderate"
        st.divider()
        st.subheader("📊 Your AI Health Analysis")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Health Risk Score", risk_level)
        with col_m2:
            st.info(f"💡 AI Insight: Given your {mood} mood, we recommend focusing on 'Pranayama' (breathing) alongside your yoga poses.")

        # 7-Day Plan Display
        st.subheader("📅 Step 2: Your 7-Day Yoga & Food Plan")
        day_tabs = st.tabs(list(weekly_data.keys()))
        for idx, day in enumerate(weekly_data.keys()):
            with day_tabs[idx]:
                col_img, col_txt = st.columns([1, 1.5])
                with col_img:
                    st.image(weekly_data[day]["Img"], caption=weekly_data[day]["Yoga"], use_container_width=True)
                with col_txt:
                    st.markdown(f"#### 🧘 Yoga: {weekly_data[day]['Yoga']}")
                    st.write(f"**💪 Benefit:** {weekly_data[day]['Benefit']}")
                    st.markdown(f"#### 🥗 Recommended Food: {weekly_data[day]['Food']}")
                    st.caption("Tip: Ensure you stay hydrated throughout the day.")

        # --- 5. PDF GENERATION ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Nutri-Sense Personal Report: {name}", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Date: {date.today()} | Risk Level: {risk_level}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Based on your profile (Mood: {mood}, Sleep: {sleep} hrs), a consistent {weekly_data['Monday']['Yoga']} practice is recommended.")
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label="📥 Download Detailed PDF Report", data=pdf_output, file_name=f"Report_{name}.pdf", mime="application/pdf")
