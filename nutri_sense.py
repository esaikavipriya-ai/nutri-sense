import streamlit as st
from fpdf import FPDF
import datetime

# 1. ---------------- DATA MASTER (TIMELINE & CONCERNS) ----------------
# Standard Daily Schedule
base_schedule = {
    "06:00 - 07:00": {"Activity": "Early Morning Detox", "Standard": "1 Glass Warm Water"},
    "08:30 - 09:30": {"Activity": "Healthy Breakfast", "Standard": "Oats / Poha / Whole Wheat Toast"},
    "11:00 - 11:30": {"Activity": "Mid-Morning Snack", "Standard": "Fruit (Apple/Papaya) or Coconut Water"},
    "13:00 - 14:00": {"Activity": "Nutritious Lunch", "Standard": "Brown Rice/Roti, Dal, Sabzi & Salad"},
    "16:30 - 17:30": {"Activity": "Evening Refresher", "Standard": "Roasted Makhana or Green Tea"},
    "19:30 - 20:30": {"Activity": "Light Dinner", "Standard": "Vegetable Soup or Moong Dal Khichdi"}
}

# Concern-Specific Add-ons
concern_data = {
    "Hair Fall": {"Morning": "Soaked Almonds & Amla", "Yoga": "Adho Mukha Svanasana", "Reason": "Scalp Health"},
    "Diabetes": {"Morning": "Fenugreek Water", "Yoga": "Mandukasana", "Reason": "Sugar Control"},
    "Eye Strain": {"Morning": "Carrot Juice", "Yoga": "Eye Palming", "Reason": "Vision Support"},
    "Acidity": {"Morning": "Fennel Seed Water", "Yoga": "Vajrasana", "Reason": "Digestion"},
    "Anxiety": {"Morning": "Chamomile Tea", "Yoga": "Shavasana", "Reason": "Stress Relief"},
    "Back Pain": {"Morning": "Turmeric Milk", "Yoga": "Bhujangasana", "Reason": "Spine Health"},
    "Thyroid": {"Morning": "Coriander Seed Water", "Yoga": "Ustrasana", "Reason": "Hormone Balance"}
}

# 2. ---------------- APP CONFIG & SESSION STATE ----------------
st.set_page_config(page_title="NutriSense Pro", page_icon="🌿", layout="wide")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

st.title("🌿 NutriSense: Smart Health Planner")

# 3. ---------------- SIDEBAR INPUT FORM ----------------
with st.sidebar:
    st.header("👤 Your Profile")
    with st.form("user_form"):
        name = st.text_input("Full Name", placeholder="e.g. John Doe")
        age = st.number_input("Age", 5, 100, 25)
        weight = st.number_input("Weight (kg)", 30.0, 150.0, 70.0)
        height = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
        selected_issues = st.multiselect("Health Concerns", list(concern_data.keys()))
        submit_btn = st.form_submit_button("Generate 24h Plan")

# 4. ---------------- CALCULATION LOGIC ----------------
if submit_btn:
    if not name or not selected_issues:
        st.error("Please provide your name and select at least one concern.")
    else:
        st.session_state.submitted = True
        # BMI Calculation
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
        
        if bmi < 18.5: cat = "Underweight"
        elif 18.5 <= bmi < 25: cat = "Healthy"
        elif 25 <= bmi < 30: cat = "Overweight"
        else: cat = "Obese"
        
        st.session_state.report_data = {
            "name": name, "bmi": bmi, "cat": cat, "issues": selected_issues
        }

# 5. ---------------- MAIN DISPLAY ----------------
if st.session_state.submitted:
    rd = st.session_state.report_data
    
    # Dashboard Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("BMI Score", rd["bmi"])
    m2.metric("Weight Status", rd["cat"])
    m3.metric("Concerns", len(rd["issues"]))

    tab1, tab2, tab3 = st.tabs(["🕒 Daily Timeline", "🧘 Yoga Guide", "📥 Download Report"])

    with tab1:
        st.subheader("Your Personalized 24-Hour Schedule")
        for slot, info in base_schedule.items():
            # Inject concern-specific food into early morning slot
            morning_add = ""
            if slot == "06:00 - 07:00":
                foods = [concern_data[iss]["Morning"] for iss in rd["issues"]]
                morning_add = f" + **{', '.join(foods)}**"
            
            with st.container():
                c1, c2 = st.columns([1, 4])
                c1.write(f"**{slot}**")
                c2.info(f"**{info['Activity']}**: {info['Standard']}{morning_add}")

    with tab2:
        st.subheader("Targeted Yoga Routine")
        for issue in rd["issues"]:
            with st.expander(f"Yoga for {issue}", expanded=True):
                st.write(f"🧘 **Posture**: {concern_data[issue]['Yoga']}")
                st.write(f"💡 **Benefit**: {concern_data[issue]['Reason']}")

    with tab3:
        st.subheader("Export Report")
        
        # --- PDF GENERATOR ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "NUTRISENSE PERSONALIZED WELLNESS LOG", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Helvetica", size=11)
        pdf.cell(0, 8, f"Patient: {rd['name']} | Date: {datetime.date.today()}", ln=True)
        pdf.cell(0, 8, f"BMI Status: {rd['bmi']} ({rd['cat']})", ln=True)
        pdf.ln(5)

        # Header Table
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(45, 10, "Time Slot", 1, 0, 'C', 1)
        pdf.cell(145, 10, "Activity & Nutrition Details", 1, 1, 'C', 1)

        # Body Table
        pdf.set_font("Helvetica", size=10)
        for slot, info in base_schedule.items():
            details = f"{info['Activity']}: {info['Standard']}"
            if slot == "06:00 - 07:00":
                extra = ", ".join([concern_data[iss]["Morning"] for iss in rd["issues"]])
                details += f" (Take: {extra})"
            
            # Using multi_cell to handle wrapping and prevent errors
            x, y = pdf.get_x(), pdf.get_y()
            pdf.multi_cell(45, 10, slot, border=1)
            pdf.set_xy(x + 45, y)
            pdf.multi_cell(145, 10, details, border=1)

        # Download Fix
        try:
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="📥 Download My NutriSense PDF",
                data=pdf_bytes,
                file_name=f"{rd['name']}_WellnessReport.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error("Failed to generate PDF. Please ensure all inputs are correct.")

    # Feedback
    st.divider()
    st.caption("NutriSense v1.0 | Educational purposes only.")
    st.feedback("stars")
