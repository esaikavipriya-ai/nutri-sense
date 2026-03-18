import streamlit as st
from fpdf import FPDF
import datetime

# 1. ---------------- DATA MASTER ----------------
base_schedule = {
    "06:00 - 07:00": {"Activity": "Early Morning Detox", "Standard": "1 Glass Warm Water"},
    "08:30 - 09:30": {"Activity": "Healthy Breakfast", "Standard": "Oats / Poha / Whole Wheat Toast"},
    "11:00 - 11:30": {"Activity": "Mid-Morning Snack", "Standard": "Fruit (Apple/Papaya) or Coconut Water"},
    "13:00 - 14:00": {"Activity": "Nutritious Lunch", "Standard": "Brown Rice/Roti, Dal, Sabzi & Salad"},
    "16:30 - 17:30": {"Activity": "Evening Refresher", "Standard": "Roasted Makhana or Green Tea"},
    "19:30 - 20:30": {"Activity": "Light Dinner", "Standard": "Vegetable Soup or Moong Dal Khichdi"}
}

concern_data = {
    "Hair Fall": {"Morning": "Soaked Almonds & Amla", "Yoga": "Adho Mukha Svanasana"},
    "Diabetes": {"Morning": "Fenugreek Water", "Yoga": "Mandukasana"},
    "Eye Strain": {"Morning": "Carrot Juice", "Yoga": "Eye Palming"},
    "Acidity": {"Morning": "Fennel Seed Water", "Yoga": "Vajrasana"},
    "Thyroid": {"Morning": "Coriander Seed Water", "Yoga": "Ustrasana"}
}

# 2. ---------------- APP CONFIG ----------------
st.set_page_config(page_title="NutriSense Pro", page_icon="🌿", layout="wide")
if 'submitted' not in st.session_state: st.session_state.submitted = False

st.title("🌿 NutriSense: Personalized Health Intelligence")

# 3. ---------------- SIDEBAR INPUTS ----------------
with st.sidebar:
    st.header("👤 Profile")
    with st.form("user_form"):
        name = st.text_input("Full Name")
        weight = st.number_input("Weight (kg)", 30, 150, 70)
        height = st.number_input("Height (cm)", 100, 220, 170)
        selected_issues = st.multiselect("Select Concerns", list(concern_data.keys()))
        submit = st.form_submit_button("Generate Report")

if submit and name and selected_issues:
    st.session_state.submitted = True
    bmi = round(weight / ((height/100)**2), 1)
    st.session_state.user_info = {"name": name, "bmi": bmi}

# 4. ---------------- MAIN DISPLAY & PDF ----------------
if st.session_state.submitted:
    u = st.session_state.user_info
    tab1, tab2 = st.tabs(["📅 Your Timeline", "📥 Download PDF"])
    
    with tab1:
        st.subheader(f"24-Hour Plan for {u['name']}")
        for slot, info in base_schedule.items():
            extra = f" + {', '.join([concern_data[iss]['Morning'] for iss in selected_issues])}" if slot == "06:00 - 07:00" else ""
            st.info(f"**{slot}** | {info['Activity']}: {info['Standard']}{extra}")

    with tab2:
        # --- PDF GENERATOR WITH ALIGNMENT FIX ---
        pdf = FPDF()
        pdf.add_page()
        
        # Header & Timestamp
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "NUTRISENSE WELLNESS REPORT", ln=True, align='C')
        pdf.set_font("Helvetica", 'I', 9)
        download_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(0, 10, f"Generated on: {download_time}", ln=True, align='R')
        
        # User Info
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 8, f"Name: {u['name']} | BMI: {u['bmi']}", ln=True)
        pdf.ln(5)

        # Table Setup
        col_time, col_details = 45, 145
        line_h = 8
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(col_time, line_h, "Time Slot", 1, 0, 'C', 1)
        pdf.cell(col_details, line_h, "Activity Details", 1, 1, 'C', 1)

        pdf.set_font("Helvetica", size=10)
        for slot, info in base_schedule.items():
            content = f"{info['Activity']}: {info['Standard']}"
            if slot == "06:00 - 07:00":
                content += f" (Take: {', '.join([concern_data[iss]['Morning'] for iss in selected_issues])})"
            
            # --- ROW ALIGNMENT LOGIC ---
            # 1. Calculate how many lines 'content' will take
            # get_string_width helps estimate wrapping
            str_w = pdf.get_string_width(content)
            num_lines = int(str_w / (col_details - 5)) + 1
            if "\n" in content: num_lines += content.count("\n")
            row_h = max(line_h, num_lines * (line_h - 2)) # Dynamic height

            curr_x, curr_y = pdf.get_x(), pdf.get_y()
            
            # 2. Draw Time Slot (fixed height to match details)
            pdf.cell(col_time, row_h, slot, border=1, align='C')
            
            # 3. Draw Details (using multi_cell for wrapping)
            pdf.set_xy(curr_x + col_time, curr_y)
            pdf.multi_cell(col_details, row_h/num_lines if num_lines > 1 else row_h, content, border=1)

        # --- DISCLAIMER ---
        pdf.ln(10)
        pdf.set_font("Helvetica", 'B', 9)
        pdf.cell(0, 5, "LEGAL DISCLAIMER:", ln=True)
        pdf.set_font("Helvetica", '', 8)
        disclaimer = ("This report is for educational purposes only and does not constitute medical advice. "
                      "Always consult with a healthcare professional before changing your diet or lifestyle.")
        pdf.multi_cell(0, 4, disclaimer)

        # Download Button
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download Official Report", pdf_bytes, f"NutriSense_{u['name']}.pdf", "application/pdf")
