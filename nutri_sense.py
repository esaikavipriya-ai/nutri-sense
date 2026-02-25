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
    div[data-testid="stExpander"] { border: 1px solid #e0e0e0; border-radius: 12px; background-color: #ffffff; }
    h1 { color: #2e7d32; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧘 Nutri-Sense: AI Health & Yoga Guide")
st.info("Public Access: No sign-in required. Please complete all fields to generate your 7-day plan.")

# --- 2. 7-DAY WELLNESS DATASET ---
# Images are royalty-free from Unsplash/Pexels for legal commercial use.
weekly_data = {
    "Monday": {"Yoga": "Tree Pose", "Img": "https://images.unsplash.com", "Food": "Oats & Berries", "Benefit": "Improves balance."},
    "Tuesday": {"Yoga": "Cobra Pose", "Img": "https://images.unsplash.com", "Food": "Quinoa Salad", "Benefit": "Strengthens spine."},
    "Wednesday": {"Yoga": "Warrior II", "Img": "https://images.unsplash.com", "Food": "Lentil Soup", "Benefit": "Increases stamina."},
    "Thursday": {"Yoga": "Triangle Pose", "Img": "https://images.unsplash.com", "Food": "Grilled Tofu", "Benefit": "Relieves back pain."},
    "Friday": {"Yoga": "Child's Pose", "Img": "https://images.unsplash.com", "Food": "Sweet Potato", "Benefit": "Calms the mind."},
    "Saturday": {"Yoga": "Plank Pose", "Img": "https://images.unsplash.com", "Food": "Greek Yogurt", "Benefit": "Builds core strength."},
    "Sunday": {"Yoga": "Corpse Pose", "Img": "https://images.unsplash.com", "Food": "Veggie Stir-fry", "Benefit": "Total relaxation."}
}

# --- 3. REQUIRED FORM ---
with st.form("health_form"):
    st.subheader("📋 Step 1: Health Profile")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name*")
        age = st.number_input("Age*", 10, 100, value=25)
        gender = st.selectbox("Gender*", ["Select", "Male", "Female", "Other"])
    with col2:
        mood = st.selectbox("Mood*", ["Select", "Happy", "Stressed", "Tired"])
        sleep = st.slider("Sleep (Hours)*", 0, 12, 7)
        symptoms = st.multiselect("Concerns*", ["None", "Headache", "Fatigue", "Digestion"])

    submit = st.form_submit_button("🚀 Generate Weekly Plan")

# --- 4. VALIDATION & DISPLAY ---
if submit:
    # Ensuring no empty required fields
    if not name or gender == "Select" or mood == "Select" or not symptoms:
        st.error("⚠️ All fields marked with * are required to generate your wellness report.")
    else:
        st.success(f"Plan generated for {name}!")
        
        st.subheader("📅 Step 2: Your 7-Day Yoga & Nutrition Plan")
        tabs = st.tabs(list(weekly_data.keys()))
        for i, day in enumerate(weekly_data.keys()):
            with tabs[i]:
                c_img, c_txt = st.columns([1, 1.5])
                with c_img: 
                    st.image(weekly_data[day]["Img"], caption=weekly_data[day]["Yoga"], use_container_width=True)
                with c_txt:
                    st.write(f"**Yoga:** {weekly_data[day]['Yoga']}")
                    st.write(f"**Recommended Food:** {weekly_data[day]['Food']}")
                    st.write(f"**Primary Benefit:** {weekly_data[day]['Benefit']}")

        # --- PDF GENERATION ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Nutri-Sense Personal Report: {name}", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Date: {date.today()} | Risk Level: {'Low' if 'None' in symptoms else 'Moderate'}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Based on your profile (Mood: {mood}, Sleep: {sleep} hrs), a consistent {weekly_data['Monday']['Yoga']} practice is recommended to improve overall wellness.")
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download Detailed PDF Report", data=pdf_bytes, file_name=f"{name}_Report.pdf", mime="application/pdf")

# --- 5. LEGAL DISCLAIMER ---
st.divider()
st.caption("""
**Medical Disclaimer:** This application provides general wellness information only. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider before starting any new exercise or diet.
**Copyright Note:** Yoga poses themselves are public domain; associated images are used via royalty-free licenses from Unsplash/Pexels.
""")
