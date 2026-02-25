import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import date
from io import BytesIO

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="Nutri-Sense Health", layout="wide", page_icon="🌿")
st.markdown("""
    <style>
    .main { background-color: #f9fbf9; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1b5e20; color: white; height: 3.5em; font-weight: bold; }
    div[data-testid="stExpander"] { border: 1px solid #e0e0e0; border-radius: 12px; background-color: #ffffff; }
    h1 { color: #2e7d32; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Nutri-Sense: Lifestyle & Yoga Guide")
st.info("Public Access: No sign-in required. Please complete all fields to generate your 7-day wellness plan.")

# --- 2. 7-DAY WELLNESS DATASET ---
weekly_data = {
    "Monday": {"Yoga": "Tree Pose" , "Food": "Oats & Berries", "Benefit": "Improves balance and focus."},
    "Tuesday": {"Yoga": "Cobra Pose", "Food": "Quinoa Salad", "Benefit": "Strengthens the spine and relieves tension."},
    "Wednesday": {"Yoga": "Warrior II", "Food": "Lentil Soup", "Benefit": "Increases muscular endurance."},
    "Thursday": {"Yoga": "Triangle Pose",  "Food": "Grilled Tofu", "Benefit": "Relieves back stiffness and stretches hips."},
    "Friday": {"Yoga": "Child's Pose",  "Food": "Sweet Potato", "Benefit": "Calms the nervous system and neck."},
    "Saturday": {"Yoga": "Plank Pose", "Food": "Greek Yogurt", "Benefit": "Builds core strength and improves posture."},
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

    submit = st.form_submit_button("🚀 Generate Weekly Plan")

# --- 4. VALIDATION & DISPLAY ---
if submit:
    if not name or gender == "Select" or mood == "Select" or not selected_concerns:
        st.error("⚠️ All fields marked with * are required.")
    else:
        st.success(f"Wellness Plan successfully generated for {name}!")
        
        # Insight Logic
        insight_title = "Standard Lifestyle Guidance"
        insight_desc = "Prioritize a balanced diet, consistent hydration, and mindful movement."
        
        if "Hair fall" in selected_concerns or "PCOS" in selected_concerns:
            insight_title = "Nutritional Focus: Hormonal Support"
            insight_desc = "Integrate iron-rich foods (Spinach, Beets) and lean proteins. Limit refined sugars to stabilize energy."
        elif "Eye issue" in selected_concerns:
            insight_title = "Nutritional Focus: Ocular Health"
            insight_desc = "Enhance intake of Vitamin A (Carrots, Sweet Potatoes). Practice distance-viewing exercises to reduce strain."
        elif "Heart discomfort" in selected_concerns:
            insight_title = "Nutritional Focus: Cardiovascular Support"
            insight_desc = "Prioritize healthy fats (Omega-3) and reduce processed sodium. Focus on gentle, rhythmic breathing."
        
        st.subheader("📊 Wellness Analysis")
        st.info(f"💡 **{insight_title}:** {insight_desc}")

        st.subheader("📅 Step 2: Your 7-Day Plan")
        tabs = st.tabs(list(weekly_data.keys()))
        for i, day in enumerate(weekly_data.keys()):
            with tabs[i]:
                st.markdown(f"#### 🧘 Yoga Practice: {weekly_data[day]['Yoga']}")
                st.write(f"**🥗 Nutrition Goal:** {weekly_data[day]['Food']}")
                st.write(f"**💪 Intended Benefit:** {weekly_data[day]['Benefit']}")

        # --- 5. PDF GENERATION ---
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 18)
        pdf.set_text_color(27, 94, 32)
        pdf.cell(0, 15, "Nutri-Sense Wellness & Lifestyle Report", ln=True, align='C')
        
        # User Info
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Name: {name} | Age: {age} | Date: {date.today()}", ln=True)
        pdf.cell(0, 10, f"Primary Concerns: {', '.join(selected_concerns)}", ln=True)
        pdf.ln(5)
        
        # Insight Section
        pdf.set_fill_color(245, 245, 245)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"Recommendation: {insight_title}", ln=True, fill=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, f"Based on the lifestyle profile provided: {insight_desc}. Consistent rest of {sleep} hours is highly recommended for recovery.")
        pdf.ln(5)
        
        # Weekly Table
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Personalized 7-Day Schedule", ln=True)
        pdf.set_font("Arial", 'B', 10)
        pdf.set_fill_color(230, 235, 230)
        pdf.cell(30, 10, "Day", 1, 0, 'C', True)
        pdf.cell(60, 10, "Yoga Practice", 1, 0, 'C', True)
        pdf.cell(100, 10, "Nutrition Goal", 1, 1, 'C', True)
        
        pdf.set_font("Arial", '', 10)
        for day, details in weekly_data.items():
            pdf.cell(30, 10, day, 1)
            pdf.cell(60, 10, details['Yoga'], 1)
            pdf.cell(100, 10, details['Food'], 1, 1)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 5, "Official Disclaimer:", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.multi_cell(0, 5, "The information provided in this report is for general educational and wellness purposes only. It is not intended to serve as medical advice, diagnosis, or treatment. Users should consult with a qualified healthcare professional before implementing any dietary changes or starting a new exercise regimen. Nutri-Sense and its creators are not responsible for any health outcomes or adverse effects resulting from the use of this information.")
        
        # Download
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download Official Report (PDF)", data=pdf_bytes, file_name=f"{name}_Report.pdf")

st.divider()
st.caption("**Legal Notice:** This tool provides wellness suggestions based on user-reported data. It is not a clinical assessment tool. All content is for educational use only.")

