import streamlit as st
from fpdf import FPDF
import datetime

# ---------------- 1. ENHANCED DATA MODEL ----------------
data_master = {
    "Hair Fall": {"Yoga": "Adho Mukha Svanasana, Sarvangasana", "Food": "Moringa, Amla", "Timing": "Morning empty stomach", "Reason": "Scalp circulation"},
    "Eye Strain": {"Yoga": "Trataka (Candle Gazing), Palming", "Food": "Carrots, Papaya", "Timing": "During work breaks", "Reason": "Vitamin A support"},
    "Diabetes": {"Yoga": "Mandukasana, Paschimottanasana", "Food": "Fenugreek, Jamun", "Timing": "Pre-meal", "Reason": "Insulin regulation"},
    "Acidity": {"Yoga": "Vajrasana (Post-meal)", "Food": "Buttermilk, Ginger", "Timing": "After lunch", "Reason": "Gut motility"},
    "Anxiety": {"Yoga": "Shavasana, Nadi Shodhana", "Food": "Almonds, Chamomile", "Timing": "Before sleep", "Reason": "Cortisol reduction"},
    "Thyroid": {"Yoga": "Ustrasana, Sarvangasana", "Food": "Walnuts, Moong Dal", "Timing": "Daily consistent", "Reason": "Hormonal balance"}
}

# ---------------- 2. APP CONFIG & SESSION STATE ----------------
st.set_page_config(page_title="NutriSense Wellness", page_icon="🌿", layout="wide")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

st.title("🌿 NutriSense: Personalized Health Intelligence")

# ---------------- 3. USER INPUT FORM ----------------
with st.sidebar:
    st.header("👤 User Profile")
    with st.form("user_form"):
        name = st.text_input("Full Name", placeholder="Enter your name")
        age = st.number_input("Age", 5, 100, 30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        st.divider()
        st.subheader("Physical Metrics")
        weight = st.number_input("Weight (kg)", 20.0, 200.0, 70.0)
        height_cm = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
        
        st.divider()
        selected_issues = st.multiselect("Select Concerns", list(data_master.keys()))
        
        submit_btn = st.form_submit_button("Generate Health Plan")

# ---------------- 4. LOGIC & CALCULATION ----------------
if submit_btn:
    if not name or not selected_issues:
        st.error("Please provide your name and select at least one health concern.")
    else:
        st.session_state.submitted = True
        # BMI Calculation
        height_m = height_cm / 100
        bmi = round(weight / (height_m ** 2), 1)
        
        if bmi < 18.5: bmi_cat = "Underweight"
        elif 18.5 <= bmi < 25: bmi_cat = "Healthy Weight"
        elif 25 <= bmi < 30: bmi_cat = "Overweight"
        else: bmi_cat = "Obese"
        
        st.session_state.bmi_data = {"score": bmi, "category": bmi_cat}

# ---------------- 5. DISPLAY CONTENT ----------------
if st.session_state.submitted:
    # Top Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("BMI Score", st.session_state.bmi_data["score"])
    c2.metric("Status", st.session_state.bmi_data["category"])
    c3.metric("Concerns Tracked", len(selected_issues))

    # Organized Tabs
    tab_yoga, tab_diet, tab_report = st.tabs(["🧘 Yoga Studio", "🥗 Nutrition Lab", "📥 Export Report"])

    with tab_yoga:
        for issue in selected_issues:
            with st.expander(f"Yoga for {issue}", expanded=True):
                st.write(f"**Recommended:** {data_master[issue]['Yoga']}")
                st.info(f"**Focus:** {data_master[issue]['Reason']}")

    with tab_diet:
        for issue in selected_issues:
            with st.expander(f"Diet for {issue}", expanded=True):
                st.write(f"**Superfoods:** {data_master[issue]['Food']}")
                st.write(f"**Best Time:** {data_master[issue]['Timing']}")

    with tab_report:
        st.subheader("Generate Official PDF")
        
        # PDF Generation Logic
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "NUTRISENSE PERSONALIZED WELLNESS REPORT", ln=True, align='C')
        pdf.set_font("helvetica", "", 10)
        pdf.cell(0, 10, f"Date: {datetime.date.today()}", ln=True, align='R')
        
        # Profile Section
        pdf.ln(5)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, f" Name: {name} | BMI: {st.session_state.bmi_data['score']} ({st.session_state.bmi_data['category']})", fill=True, ln=True)
        
        # Table with Multi-line support
        pdf.ln(5)
        pdf.set_font("helvetica", "B", 11)
        pdf.set_fill_color(100, 150, 255) # Header Blue
        pdf.set_text_color(255, 255, 255)
        pdf.cell(40, 10, "Concern", 1, 0, 'C', fill=True)
        pdf.cell(70, 10, "Yoga & Exercise", 1, 0, 'C', fill=True)
        pdf.cell(80, 10, "Dietary Recommendations", 1, 1, 'C', fill=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("helvetica", "", 9)
        for issue in selected_issues:
            row = data_master[issue]
            # Multi-cell handles text wrapping
            x_start = pdf.get_x()
            y_start = pdf.get_y()
            pdf.multi_cell(40, 10, issue, border=1)
            pdf.set_xy(x_start + 40, y_start)
            pdf.multi_cell(70, 10, row['Yoga'], border=1)
            pdf.set_xy(x_start + 110, y_start)
            pdf.multi_cell(80, 10, f"{row['Food']} ({row['Timing']})", border=1)

        pdf_bytes = pdf.output()
        st.download_button("Download My NutriSense Report", data=pdf_bytes, file_name=f"{name}_report.pdf", mime="application/pdf")

    # Persistent Rating System
    st.divider()
    st.subheader("Help us improve NutriSense")
    rating = st.feedback("stars")
    if rating is not None:
        st.toast(f"Thank you for the {rating+1} star rating!")
