import streamlit as st
from fpdf import FPDF
import datetime

# 1. ---------------- TAMIL NADU TRADITIONAL DATA ----------------
# Standard Tamil Daily Schedule
base_schedule = {
    "06:00 - 07:00": {"Activity": "Early Morning Detox (Detox Neer)", "Standard": "Warm Jeera (Cumin) Water"},
    "08:30 - 09:30": {"Activity": "Traditional Breakfast (Kaalai Unavu)", "Standard": "Millet Idli or Ragi Dosai with Onion Chutney"},
    "11:00 - 11:30": {"Activity": "Mid-Morning Refreshment", "Standard": "Elaneer (Tender Coconut) or Neer Mor (Buttermilk)"},
    "13:00 - 14:00": {"Activity": "Nutritious Lunch (Madhiya Unavu)", "Standard": "Hand-pounded Red Rice, Keerai Poriyal, and Rasam"},
    "16:30 - 17:30": {"Activity": "Evening Protein Snack", "Standard": "Sundal (Chickpea/Green Gram) with Grated Coconut"},
    "19:30 - 20:30": {"Activity": "Light Dinner (Iravu Unavu)", "Standard": "Vegetable Idiyappam or Kuthiraivali (Barnyard Millet) Kanji"}
}

# Concern-Specific Tamil Medicinal Foods & Yoga
concern_data = {
    "Hair Fall": {"Morning": "Karisalanganni (False Daisy) Tea & Soaked Almonds", "Yoga": "Sarvangasana", "Reason": "Improves scalp circulation"},
    "Diabetes": {"Morning": "Vendhayam (Fenugreek) Water & Sirukurinjan Tea", "Yoga": "Mandukasana", "Reason": "Regulates blood sugar naturally"},
    "Eye Strain": {"Morning": "Ponnanganni Keerai Juice or Carrot Juice", "Yoga": "Trataka (Candle Gazing)", "Reason": "Rich in Vitamin A for vision"},
    "Acidity": {"Morning": "Inji (Ginger) & Honey or Fennel Water", "Yoga": "Vajrasana (Post-meal)", "Reason": "Relieves gut inflammation"},
    "Thyroid": {"Morning": "Kothamalli (Coriander) Seed Water", "Yoga": "Ustrasana", "Reason": "Supports hormonal balance"},
    "Anemia": {"Morning": "Karupatti (Jaggery) with Dates & Pomegranate", "Yoga": "Surya Namaskar", "Reason": "Boosts Hemoglobin levels"}
}

# 2. ---------------- APP CONFIG & UI ----------------
st.set_page_config(page_title="NutriSense Tamil Nadu", page_icon="🌿", layout="wide")
if 'submitted' not in st.session_state: st.session_state.submitted = False

st.title("🌿 NutriSense: Tamil Traditional Wellness Guide")
st.markdown("*\"Unave Marundhu, Marunthe Unavu\" (Food is Medicine)*")

# 3. ---------------- SIDEBAR PROFILE ----------------
with st.sidebar:
    st.header("👤 User Profile")
    with st.form("user_form"):
        name = st.text_input("Name")
        weight = st.number_input("Weight (kg)", 30, 150, 70)
        height = st.number_input("Height (cm)", 100, 220, 170)
        selected_issues = st.multiselect("Select Concerns", list(concern_data.keys()))
        submit = st.form_submit_button("Generate Tamil Health Plan")

# 4. ---------------- REPORT LOGIC ----------------
if submit and name and selected_issues:
    st.session_state.submitted = True
    bmi = round(weight / ((height/100)**2), 1)
    st.session_state.user_info = {"name": name, "bmi": bmi, "issues": selected_issues}

# 5. ---------------- DASHBOARD & PDF ----------------
if st.session_state.submitted:
    u = st.session_state.user_info
    tab1, tab2 = st.tabs(["📅 Daily Tamil Plan", "📥 Download Report"])
    
    with tab1:
        st.subheader(f"Customized Tamil Lifestyle Plan for {u['name']}")
        for slot, info in base_schedule.items():
            extra = ""
            if slot == "06:00 - 07:00":
                yogas = [concern_data[iss]["Yoga"] for iss in u["issues"]]
                foods = [concern_data[iss]["Morning"] for iss in u["issues"]]
                extra = f"\n\n🧘 **Yoga:** {', '.join(yogas)}\n\n🥗 **Medicinal Intake:** {', '.join(foods)}"
            
            st.info(f"**{slot}** | **{info['Activity']}**\n\n{info['Standard']}{extra}")

    with tab2:
        # --- PDF GENERATOR ---
        pdf = FPDF()
        pdf.add_page()
        
        # Header & Metadata
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "NUTRISENSE: TAMIL TRADITIONAL REPORT", ln=True, align='C')
        pdf.set_font("Helvetica", 'I', 8)
        pdf.cell(0, 5, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='R')
        pdf.ln(5)

        # Profile Section
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, f"Name: {u['name']} | BMI: {u['bmi']}", ln=True)
        pdf.ln(5)

        # Table Alignment Logic
        col_time, col_yoga, col_diet = 35, 75, 80
        pdf.set_fill_color(230, 240, 230)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(col_time, 10, "Time Slot", 1, 0, 'C', 1)
        pdf.cell(col_yoga, 10, "Yoga & Activity", 1, 0, 'C', 1)
        pdf.cell(col_diet, 10, "Tamil Traditional Food", 1, 1, 'C', 1)

        pdf.set_font("Helvetica", size=9)
        for slot, info in base_schedule.items():
            yoga_text = info['Activity']
            diet_text = info['Standard']
            if slot == "06:00 - 07:00":
                yoga_text += f"\nYoga: {', '.join([concern_data[iss]['Yoga'] for iss in u['issues']])}"
                diet_text += f"\nDetox: {', '.join([concern_data[iss]['Morning'] for iss in u['issues']])}"

            # Calculate height for row alignment
            curr_x, curr_y = pdf.get_x(), pdf.get_y()
            pdf.multi_cell(col_time, 10, slot, border=1, align='C')
            new_y = pdf.get_y()
            
            pdf.set_xy(curr_x + col_time, curr_y)
            pdf.multi_cell(col_yoga, 5, yoga_text, border=1)
            new_y = max(new_y, pdf.get_y())
            
            pdf.set_xy(curr_x + col_time + col_yoga, curr_y)
            pdf.multi_cell(col_diet, 5, diet_text, border=1)
            new_y = max(new_y, pdf.get_y())
            pdf.set_y(new_y)

        # Footer Disclaimer
        pdf.ln(10)
        pdf.set_font("Helvetica", 'B', 8)
        pdf.cell(0, 5, "MARUTHUVA ARIKKAI (MEDICAL DISCLAIMER):", ln=True)
        pdf.set_font("Helvetica", '', 7)
        pdf.multi_cell(0, 4, "This report follows traditional Tamil dietary patterns. It is for educational purposes only. "
                             "Please consult a Siddha or Allopathic doctor before starting these regimens.")

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download NutriSense Tamil Report", pdf_bytes, f"Tamil_Report_{u['name']}.pdf", "application/pdf")
