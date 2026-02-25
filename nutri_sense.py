import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import date
from io import BytesIO

# --- 1. PAGE CONFIG & GRADIENT THEME ---
st.set_page_config(page_title="Nutri-Sense Health", layout="wide", page_icon="🌿")

# Custom CSS for Gradient Background and Professional Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 50%, #f1f8e9 100%);
        background-attachment: fixed;
    }
    .stButton>button { 
        width: 100%; border-radius: 10px; background-color: #2e7d32; 
        color: white; height: 3.5em; font-weight: bold; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1b5e20; border: none; }
    div[data-testid="stExpander"] { 
        border: none; border-radius: 15px; 
        background-color: rgba(255, 255, 255, 0.8); 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
    }
    h1 { color: #1b5e20; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Nutri-Sense: Lifestyle & Yoga Guide")
st.info("Public Access Enabled. Please complete all required fields to generate your 7-day wellness plan.")

# --- 2. 7-DAY WELLNESS DATASET ---
weekly_data = {
    "Monday": {"Yoga": "Tree Pose", "Food": "Oats & Berries", "Benefit": "Improves balance and focus."},
    "Tuesday": {"Yoga": "Cobra Pose", "Food": "Quinoa Salad", "Benefit": "Strengthens the spine and relieves tension."},
    "Wednesday": {"Yoga": "Warrior II", "Food": "Lentil Soup", "Benefit": "Increases muscular endurance."},
    "Thursday": {"Yoga": "Triangle Pose", "Food": "Grilled Tofu", "Benefit": "Relieves back stiffness."},
    "Friday": {"Yoga": "Child's Pose", "Food": "Sweet Potato", "Benefit": "Calms the nervous system."},
    "Saturday": {"Yoga": "Plank Pose", "Food": "Greek Yogurt", "Benefit": "Builds core strength."},
    "Sunday": {"Yoga": "Corpse Pose", "Food": "Veggie Stir-fry", "Benefit": "Allows for total body recovery."}
}

# --- 3. REQUIRED FORM ---
with st.form("health_form"):
    st.subheader("📋 Step 1: Wellness Profile")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name*")
        age = st.number_input("Age*", 10, 100, value=25)
        gender = st.selectbox("Gender*", ["Select", "Male", "Female", "Other"])
    with col2:
        mood = st.selectbox("Mood*", ["Select", "Happy", "Stressed", "Tired", "Sad"])
        sleep = st.slider("Sleep (Hours)*", 0, 12, 7)
    
    st.write("**Select Current Health Concerns* (Multiple allowed)**")
    all_concerns = [
        "None / General Wellness", "Hair fall", "Eye issue", "Headache", 
        "Pigmentation", "Heart discomfort", "Leg pain", "Infection", 
        "Kidney issue", "Gall bladder", "Body pain", "Irregular periods", "PCOS"
    ]
    selected_concerns = st.multiselect("Concerns*", all_concerns)

    submit = st.form_submit_button("🚀 Generate Wellness Plan")

# --- 4. VALIDATION & DISPLAY ---
if submit:
    if not name or gender == "Select" or mood == "Select" or not selected_concerns:
        st.error("⚠️ All fields marked with * are required.")
    else:
        st.success(f"Wellness Plan successfully generated for {name}!")
        
        # Expert Insight Logic
        insight_title = "Standard Lifestyle Guidance"
        insight_desc = "Prioritize a balanced diet, consistent hydration, and mindful movement."
        
        if any(x in selected_concerns for x in ["Hair fall", "PCOS", "Irregular periods"]):
            insight_title = "Nutritional Focus: Hormonal & Tissue Support"
            insight_desc = "Integrate iron-rich foods (Spinach, Beets) and lean proteins. Following a protein-rich breakfast helps stabilize energy."
        elif "Eye issue" in selected_concerns:
            insight_title = "Nutritional Focus: Ocular Health"
            insight_desc = "Enhance intake of Vitamin A (Carrots, Sweet Potatoes) and focus on distance-viewing exercises."
        
        st.subheader("📊 Wellness Analysis")
        st.info(f"💡 **{insight_title}:** {insight_desc}")

        st.subheader("📅 Step 2: Your 7-Day Plan")
        tabs = st.tabs(list(weekly_data.keys()))
        for i, day in enumerate(weekly_data.keys()):
            with tabs[i]:
                st.markdown(f"#### 🧘 Yoga: {weekly_data[day]['Yoga']}")
                st.write(f"**🥗 Food Goal:** {weekly_data[day]['Food']}")
                st.write(f"**💪 Benefit:** {weekly_data[day]['Benefit']}")

        # --- 5. PDF GENERATION WITH BRIEF EXPLANATIONS ---
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 18)
        pdf.set_text_color(27, 94, 32)
        pdf.cell(0, 15, "Nutri-Sense Wellness Report", ln=True, align='C')
        
        # User Info
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"User: {name} | Age: {age} | Date: {date.today()}", ln=True)
        pdf.cell(0, 10, f"Concerns: {', '.join(selected_concerns)}", ln=True)
        pdf.ln(5)
        
        # Brief Explanation Section
        pdf.set_fill_color(240, 245, 240)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"Recommendation: {insight_title}", ln=True, fill=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, f"Based on your profile, we recommend: {insight_desc}. Recovery requires at least {sleep} hours of rest.")
        pdf.ln(5)
        
        # Table
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(30, 10, "Day", 1, 0, 'C')
        pdf.cell(60, 10, "Yoga Practice", 1, 0, 'C')
        pdf.cell(100, 10, "Nutrition Goal", 1, 1, 'C')
        
        pdf.set_font("Arial", '', 10)
        for day, details in weekly_data.items():
            pdf.cell(30, 10, day, 1)
            pdf.cell(60, 10, details['Yoga'], 1)
            pdf.cell(100, 10, details['Food'], 1, 1)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 5, "Official Disclaimer:", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.multi_cell(0, 5, "This report is for educational purposes only. It is not medical advice or diagnosis. Consult a healthcare professional before making dietary or exercise changes.")
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download Official Report (PDF)", data=pdf_bytes, file_name=f"{name}_Wellness_Report.pdf")

st.divider()
st.caption("**Disclaimer:** Nutri-Sense provides lifestyle suggestions. All health-related decisions should be made in consultation with a medical professional.")
