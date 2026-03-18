import streamlit as st
from fpdf import FPDF
import datetime
import pandas as pd
import os
import pytz
import plotly.express as px

# 1. ---------------- DATA MASTER (SCHEDULE & MEDICINAL RECIPES) ----------------
base_schedule = {
    "06:00 AM - 07:00 AM": {"Activity": "Early Morning Detox", "Standard": "Warm Jeera (Cumin) Water"},
    "08:30 AM - 09:30 AM": {"Activity": "Traditional Breakfast", "Standard": "Millet Idli or Ragi Dosai"},
    "11:00 AM - 11:30 AM": {"Activity": "Mid-Morning Refresh", "Standard": "Elaneer (Tender Coconut) or Neer Mor"},
    "01:00 PM - 02:00 PM": {"Activity": "Nutritious Lunch", "Standard": "Red Rice, Keerai Poriyal, and Rasam"},
    "04:30 PM - 05:30 PM": {"Activity": "Evening Protein", "Standard": "Sundal (Chickpea/Green Gram)"},
    "07:30 PM - 08:30 PM": {"Activity": "Light Dinner", "Standard": "Idiyappam or Millet Kanji"}
}

# Added 'Recipe' key for each concern
concern_data = {
    "Hair Fall": {
        "Morning": "Karisalanganni Tea", "Yoga": "Sarvangasana",
        "Recipe": "Boil 5-6 fresh Karisalanganni leaves in 1 cup water until it reduces to half. Strain and drink warm."
    },
    "Diabetes": {
        "Morning": "Vendhayam Water", "Yoga": "Mandukasana",
        "Recipe": "Soak 1 tsp Fenugreek seeds (Vendhayam) in a glass of water overnight. Drink the water and chew the seeds in the morning."
    },
    "Eye Strain": {
        "Morning": "Ponnanganni Juice", "Yoga": "Trataka",
        "Recipe": "Blend a handful of Ponnanganni leaves with 1/2 cup water. Strain, add a pinch of salt/pepper, and consume immediately."
    },
    "Acidity": {
        "Morning": "Inji Honey Water", "Yoga": "Vajrasana",
        "Recipe": "Crush 1 inch of fresh ginger (Inji). Boil in water for 5 mins. Add 1 tsp honey after it cools slightly."
    },
    "Thyroid": {
        "Morning": "Kothamalli Water", "Yoga": "Ustrasana",
        "Recipe": "Crush 1 tbsp dry Coriander seeds. Boil in 2 cups water until reduced to 1 cup. Drink daily on an empty stomach."
    },
    "PCOD/PCOS": {
        "Morning": "Ulunthu Kanji", "Yoga": "Baddha Konasana",
        "Recipe": "Boil broken Black Gram (Ulunthu) and rice in water until soft. Add garlic, cumin, and dry ginger powder. Serve warm with jaggery."
    },
    "Joint Pain": {
        "Morning": "Mudakathan Soup", "Yoga": "Tadasana",
        "Recipe": "Sauté Mudakathan leaves with small onions, tomato, cumin, and pepper. Add water and boil for 10 mins. Strain and serve as soup."
    },
    "High BP": {
        "Morning": "Poondu (Garlic) Water", "Yoga": "Shavasana",
        "Recipe": "Boil 2 cloves of crushed garlic in 1/2 cup water for 3 mins. Drink the warm water and consume the cooked garlic."
    }
}

# 2. ---------------- LOGGING FUNCTION (SILENT SAVING) ----------------
def log_download(name, age, gender, bmi, issues):
    ist = pytz.timezone('Asia/Kolkata')
    ts = datetime.datetime.now(ist).strftime("%Y-%m-%d %I:%M:%S %p")
    target_path = r"C:\Users\LENOVO\Documents\qwings\Science Expo"
    if not os.path.exists(target_path): os.makedirs(target_path)
    log_file = os.path.join(target_path, "nutrisense_logs.csv")
    
    log_entry = pd.DataFrame([{"Timestamp": ts, "Name": name, "Age": age, "Gender": gender, "BMI": bmi, "Concerns": ", ".join(issues)}])
    if not os.path.isfile(log_file): log_entry.to_csv(log_file, index=False)
    else: log_entry.to_csv(log_file, mode='a', header=False, index=False)

# 3. ---------------- APP UI ----------------
st.set_page_config(page_title="NutriSense Tamil Nadu", layout="wide")
if 'submitted' not in st.session_state: st.session_state.submitted = False

st.title("🌿 NutriSense: Personalized Tamil Wellness")

with st.sidebar:
    st.header("👤 Profile")
    with st.form("user_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 5, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", 30.0, 150.0, 70.0)
        height = st.number_input("Height (cm)", 100.0, 220.0, 170.0)
        selected_issues = st.multiselect("Select Concerns", list(concern_data.keys()))
        submit = st.form_submit_button("Generate Plan")

# 4. ---------------- DASHBOARD LOGIC ----------------
if submit and name and selected_issues:
    st.session_state.submitted = True
    bmi = round(weight / ((height/100)**2), 1)
    st.session_state.user_info = {"name": name, "age": age, "gender": gender, "bmi": bmi, "issues": selected_issues}

if st.session_state.submitted:
    u = st.session_state.user_info
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Daily Plan", "🍲 Traditional Recipes", "📊 Health Analytics", "📥 Download Report"])

    with tab1:
        st.subheader(f"Customized Plan for {u['name']}")
        for slot, info in base_schedule.items():
            extra = ""
            if "06:00 AM" in slot:
                yogas = [concern_data[iss]["Yoga"] for iss in u["issues"]]
                foods = [concern_data[iss]["Morning"] for iss in u["issues"]]
                extra = f"\n\n🧘 Yoga Focus: {', '.join(yogas)}\n\n🥗 Morning Intake: {', '.join(foods)}"
            st.info(f"**{slot}** | {info['Activity']}: {info['Standard']}{extra}")

    with tab2:
        st.subheader("How to Prepare Your Medicinal Foods")
        for issue in u['issues']:
            with st.expander(f"📖 Recipe for {issue} ({concern_data[issue]['Morning']})", expanded=True):
                st.write(concern_data[issue]['Recipe'])
                st.caption(f"Traditional benefit: {issue} management")

    with tab3:
        log_path = r"C:\Users\LENOVO\Documents\qwings\Science Expo\nutrisense_logs.csv"
        if os.path.exists(log_path):
            df_logs = pd.read_csv(log_path)
            c1, c2 = st.columns(2)
            with c1:
                all_c = df_logs["Concerns"].str.split(", ").explode().value_counts().reset_index()
                all_c.columns = ["Issue", "Count"]
                st.plotly_chart(px.pie(all_c, values="Count", names="Issue", title="Health Concerns Distribution"), use_container_width=True)
            with c2:
                st.plotly_chart(px.histogram(df_logs, x="BMI", title="Community BMI Spread"), use_container_width=True)
        else: st.warning("Download a report first to see analytics.")

    with tab4:
        # --- PDF GENERATOR (STABLE VERSION) ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "NUTRISENSE WELLNESS REPORT", ln=True, align='C')
        
        ist = pytz.timezone('Asia/Kolkata')
        pdf.set_font("Helvetica", 'I', 9)
        pdf.cell(0, 10, f"Generated: {datetime.datetime.now(ist).strftime('%I:%M %p')}", ln=True, align='R')
        
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 10, f"Name: {u['name']} | Age: {u['age']} | Gender: {u['gender']} | BMI: {u['bmi']}", ln=True)
        pdf.ln(5)

        col_w = 63 
        pdf.set_fill_color(220, 240, 220)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(col_w, 10, "Time", 1, 0, 'C', 1)
        pdf.cell(col_w, 10, "Yoga/Activity", 1, 0, 'C', 1)
        pdf.cell(col_w, 10, "Tamil Food", 1, 1, 'C', 1)

        pdf.set_font("Helvetica", size=9)
        for slot, info in base_schedule.items():
            y_txt, f_txt = info['Activity'], info['Standard']
            if "06:00 AM" in slot:
                y_txt += "\nYoga: " + ", ".join([concern_data[i]['Yoga'] for i in u['issues']])
                f_txt += "\nDetox: " + ", ".join([concern_data[i]['Morning'] for i in u['issues']])

            s_y = pdf.get_y()
            lines_y = len(pdf.multi_cell(col_w, 6, y_txt, split_only=True))
            lines_f = len(pdf.multi_cell(col_w, 6, f_txt, split_only=True))
            max_h = max(lines_y, lines_f, 1) * 6 + 4

            pdf.multi_cell(col_w, max_h, slot, border=1, align='C')
            pdf.set_xy(pdf.l_margin + col_w, s_y)
            pdf.multi_cell(col_w, max_h / (lines_y if lines_y > 0 else 1), y_txt, border=1)
            pdf.set_xy(pdf.l_margin + (col_w * 2), s_y)
            pdf.multi_cell(col_w, max_h / (lines_f if lines_f > 0 else 1), f_txt, border=1)
            pdf.set_y(s_y + max_h)

        pdf.ln(10)
        pdf.set_font("Helvetica", 'I', 8)
        pdf.multi_cell(0, 5, "Disclaimer: Based on Tamil traditional practices. Consult a doctor before starting.")

        try:
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            if st.download_button("📥 Download PDF Report", pdf_bytes, f"{u['name']}_Report.pdf", "application/pdf"):
                log_download(u['name'], u['age'], u['gender'], u['bmi'], u['issues'])
                st.success("Report Downloaded!")
        except Exception as e:
            st.error("Error generating PDF. Please ensure all details are correct.")
