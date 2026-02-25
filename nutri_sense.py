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
weekly_data = {
    "Monday": {"Yoga": "Tree Pose" , "Food": "Oats & Berries", "Benefit": "Improves balance."},
    "Tuesday": {"Yoga": "Cobra Pose", "Food": "Quinoa Salad", "Benefit": "Strengthens spine."},
    "Wednesday": {"Yoga": "Warrior II", "Food": "Lentil Soup", "Benefit": "Increases stamina."},
    "Thursday": {"Yoga": "Triangle Pose",  "Food": "Grilled Tofu", "Benefit": "Relieves back pain."},
    "Friday": {"Yoga": "Child's Pose",  "Food": "Sweet Potato", "Benefit": "Calms the mind."},
    "Saturday": {"Yoga": "Plank Pose", "Food": "Greek Yogurt", "Benefit": "Builds core strength."},
    "Sunday": {"Yoga": "Corpse Pose", "Food": "Veggie Stir-fry", "Benefit": "Total relaxation."}
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
        mood = st.selectbox("Mood*", ["Select", "Happy", "Stressed", "Tired", "Sad"])
        sleep = st.slider("Sleep (Hours)*", 0, 12, 7)
    
    st.write("**Select All Current Health Concerns* (Multiple allowed)**")
    all_concerns = [
        "None / General Wellness", "Hair fall", "Eye issue", "Headache", 
        "Pigmentation", "Heart discomfort", "Leg pain", "Infection", 
        "Kidney issue", "Gall bladder", "Body pain", "Irregular periods", "PCOS"
    ]
    selected_concerns = st.multiselect("Concerns*", all_concerns)

    submit = st.form_submit_button("🚀 Generate Weekly Plan")

# --- 4. VALIDATION & DISPLAY ---
if submit:
    if not name or gender == "Select" or mood == "Select" or not selected_concerns:
        st.error("⚠️ All fields marked with * are required.")
    else:
        st.success(f"Plan generated for {name}!")
        
        # AI Insight Logic
        insight_title = "General Wellness"
        insight_desc = "Maintain a balanced diet and stay hydrated."
        
        if "Hair fall" in selected_concerns or "PCOS" in selected_concerns:
            insight_title = "Hormonal & Nutritional Support"
            insight_desc = "Focus on Iron-rich foods (Spinach, Beets) and high-quality Protein. Avoid processed sugars."
        elif "Eye issue" in selected_concerns:
            insight_title = "Ocular Health"
            insight_desc = "Increase Vitamin A intake (Carrots, Sweet Potatoes). Practice eye-rolling yoga exercises."
        elif "Heart discomfort" in selected_concerns:
            insight_title = "Cardiovascular Care"
            insight_desc = "Prioritize Omega-3 fatty acids and low-sodium meals. Focus on deep breathing."
        
        st.subheader("📊 Your AI Health Analysis")
        st.info(f"💡 **{insight_title}:** {insight_desc}")

        st.subheader("📅 Step 2: Your 7-Day Plan")
        tabs = st.tabs(list(weekly_data.keys()))
        for i, day in enumerate(weekly_data.keys()):
            with tabs[i]:
                st.markdown(f"#### 🧘 {weekly_data[day]['Yoga']}")
                st.write(f"**🥗 Diet:** {weekly_data[day]['Food']}")
                st.write(f"**💪 Why:** {weekly_data[day]['Benefit']}")

        # --- 5. ENHANCED PDF GENERATION ---
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 18)
        pdf.set_text_color(30, 70, 30)
        pdf.cell(0, 15, "Nutri-Sense AI Wellness Report", ln=True, align='C')
        
        # User Info Section
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Name: {name} | Age: {age} | Date: {date.today()}", ln=True)
        pdf.cell(0, 10, f"Primary Concerns: {', '.join(selected_concerns)}", ln=True)
        pdf.ln(5)
        
        # AI Explanation Section
        pdf.set_fill_color(240, 245, 240)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"AI Analysis: {insight_title}", ln=True, fill=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, f"Based on your profile, our AI suggests: {insight_desc}. Following a structured sleep cycle of {sleep} hours is vital for recovery.")
        pdf.ln(5)
        
        # Weekly Schedule Table
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Your 7-Day Yoga & Nutrition Schedule", ln=True)
        pdf.set_font("Arial", 'B', 10)
        
        # Table Header
        pdf.set_fill_color(200, 220, 200)
        pdf.cell(30, 10, "Day", 1, 0, 'C', True)
        pdf.cell(60, 10, "Yoga Pose", 1, 0, 'C', True)
        pdf.cell(100, 10, "Recommended Nutrition", 1, 1, 'C', True)
        
        # Table Content
        pdf.set_font("Arial", '', 10)
        for day, details in weekly_data.items():
            pdf.cell(30, 10, day, 1)
            pdf.cell(60, 10, details['Yoga'], 1)
            pdf.cell(100, 10, details['Food'], 1, 1)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 10)
        pdf.multi_cell(0, 5, "Disclaimer: This report is generated by AI for educational purposes. Consult a doctor before starting new health regimes.")
        
        # Download
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download Detailed Report (PDF)", data=pdf_bytes, file_name=f"{name}_Report.pdf")

st.divider()
st.caption("Nutri-Sense AI 2026 | No Personal Data is stored permanently on this server.")
