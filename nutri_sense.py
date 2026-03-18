import streamlit as st
from fpdf import FPDF
import datetime
import pandas as pd
import os
import pytz  # Required for IST timezone support

# 1. ---------------- DATA MASTER (TAMIL NADU 12-HR) ----------------
base_schedule = {
    "06:00 AM - 07:00 AM": {"Activity": "Early Morning Detox", "Standard": "Warm Jeera (Cumin) Water"},
    "08:30 AM - 09:30 AM": {"Activity": "Traditional Breakfast", "Standard": "Millet Idli or Ragi Dosai with Chutney"},
    "11:00 AM - 11:30 AM": {"Activity": "Mid-Morning Refresh", "Standard": "Elaneer (Tender Coconut) or Neer Mor"},
    "01:00 PM - 02:00 PM": {"Activity": "Nutritious Lunch", "Standard": "Red Rice, Keerai Poriyal, and Rasam"},
    "04:30 PM - 05:30 PM": {"Activity": "Evening Protein Snack", "Standard": "Sundal (Chickpea/Green Gram)"},
    "07:30 PM - 08:30 PM": {"Activity": "Light Dinner", "Standard": "Idiyappam or Millet Kanji"}
}

concern_data = {
    "Hair Fall": {"Morning": "Karisalanganni Tea", "Yoga": "Sarvangasana"},
    "Diabetes": {"Morning": "Vendhayam Water", "Yoga": "Mandukasana"},
    "Eye Strain": {"Morning": "Ponnanganni Juice", "Yoga": "Trataka"},
    "Acidity": {"Morning": "Inji Honey Water", "Yoga": "Vajrasana"},
    "Thyroid": {"Morning": "Kothamalli Water", "Yoga": "Ustrasana"},
    "PCOD/PCOS": {"Morning": "Ulunthu Kanji", "Yoga": "Baddha Konasana"},
    "Joint Pain": {"Morning": "Mudakathan Soup", "Yoga": "Tadasana"},
    "High BP": {"Morning": "Poondu (Garlic) Water", "Yoga": "Shavasana"}
}

# 2. ---------------- LOGGING FUNCTION (IST & ABSOLUTE PATH) ----------------
def log_download(name, age, gender, bmi, issues):
    # Set the timezone to IST (Asia/Kolkata)
    ist = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.datetime.now(ist).strftime("%Y-%m-%d %I:%M:%S %p")
    
    # Target Path for Science Expo
    target_path = r"C:\Users\LENOVO\Documents\qwings\Science Expo"
    
    # Create folder if it doesn't exist
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        
    log_file = os.path.join(target_path, "nutrisense_logs.csv")
    
    log_entry = pd.DataFrame([{
        "Timestamp": timestamp,
        "Name": name, 
        "Age": age,
        "Gender": gender,
        "BMI": bmi, 
        "Concerns": ", ".join(issues)
    }])
    
    if not os.path.isfile(log_file): 
        log_entry.to_csv(log_file, index=False)
    else: 
        log_entry.to_csv(log_file, mode='a', header=False, index=False)
    
    return log_file

# 3. ---------------- APP CONFIG & UI ----------------
st.set_page_config(page_title="NutriSense Tamil Nadu", layout="wide")
if 'submitted' not in st.session_state: st.session_state.submitted = False

st.title("🌿 NutriSense: Tamil Traditional Wellness")

with st.sidebar:
    st.header("👤 Your Profile")
    with st.form("user_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 5, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", 30.0, 150.0, 70.0)
        height = st.number_input("Height (cm)", 100.0, 220.0, 170.0)
        selected_issues = st.multiselect("Select Concerns", list(concern_data.keys()))
        submit = st.form_submit_button("Generate Plan")

# 4. ---------------- UI & PDF ----------------
if submit and name and selected_issues:
    st.session_state.submitted = True
    bmi = round(weight / ((height/100)**2), 1)
    st.session_state.user_info = {
        "name": name, "age": age, "gender": gender, "bmi": bmi, "issues": selected_issues
    }

if st.session_state.submitted:
    u = st.session_state.user_info
    tab1, tab2 = st.tabs(["📅 Daily Plan", "📥 Download PDF"])

    with tab1:
        st.subheader(f"Plan for {u['name']} (Age: {u['age']}, Gender: {u['gender']})")
        for slot, info in base_schedule.items():
            st.info(f"**{slot}** | {info['Activity']}: {info['Standard']}")

    with tab2:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "NUTRISENSE WELLNESS REPORT", ln=True, align='C')
        
        # Current time in IST for the report
        ist = pytz.timezone('Asia/Kolkata')
        report_time = datetime.datetime.now(ist).strftime('%I:%M %p')
        
        pdf.set_font("Helvetica", 'I', 9)
        pdf.cell(0, 10, f"Generated: {report_time}", ln=True, align='R')
        
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 10, f"Name: {u['name']} | Age: {u['age']} | Gender: {u['gender']} | BMI: {u['bmi']}", ln=True)
        pdf.ln(5)

        # Header Configuration
        col_w = 63 
        pdf.set_fill_color(220, 240, 220)
        pdf.cell(col_w, 10, "Time (12h)", 1, 0, 'C', True)
        pdf.cell(col_w, 10, "Activity & Yoga", 1, 0, 'C', True)
        pdf.cell(col_w, 10, "Tamil Traditional Food", 1, 1, 'C', True)

        pdf.set_font("Helvetica", '', 9)
        for slot, info in base_schedule.items():
            yoga_txt = info['Activity']
            food_txt = info['Standard']
            if "06:00 AM" in slot:
                yoga_txt += "\nYoga: " + ", ".join([concern_data[i]['Yoga'] for i in u['issues']])
                food_txt += "\nDetox: " + ", ".join([concern_data[i]['Morning'] for i in u['issues']])

            # Row Alignment Logic
            start_y = pdf.get_y()
            lines_y = len(pdf.multi_cell(col_w, 6, yoga_txt, split_only=True))
            lines_f = len(pdf.multi_cell(col_w, 6, food_txt, split_only=True))
            max_h = max(lines_y, lines_f, 1) * 6 + 4

            pdf.multi_cell(col_w, max_h, slot, border=1, align='C')
            pdf.set_xy(pdf.l_margin + col_w, start_y)
            pdf.multi_cell(col_w, max_h / (lines_y if lines_y > 0 else 1), yoga_txt, border=1)
            pdf.set_xy(pdf.l_margin + (col_w * 2), start_y)
            pdf.multi_cell(col_w, max_h / (lines_f if lines_f > 0 else 1), food_txt, border=1)
            pdf.set_y(start_y + max_h)

        pdf.ln(10)
        pdf.set_font("Helvetica", 'I', 8)
        pdf.multi_cell(0, 5, "Disclaimer: Based on Tamil traditional practices. Consult a doctor before starting.")

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        if st.download_button("📥 Download PDF Report", pdf_bytes, f"{u['name']}_WellnessReport.pdf", "application/pdf"):
            saved_to = log_download(u['name'], u['age'], u['gender'], u['bmi'], u['issues'])
            st.success(f"Report downloaded! CSV saved at: {saved_to}")
