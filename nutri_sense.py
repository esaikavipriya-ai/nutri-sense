import streamlit as st
from fpdf import FPDF

# ---------------- DATA (10 SAMPLE CONCERNS) ----------------
data_master = {
    "Hair Fall": {"Yoga": "Adho Mukha Svanasana, Sarvangasana",
                  "Food": "Moringa leaves, Amla, Curry leaves",
                  "Reason": "Scalp circulation"},
    "Eye Strain": {"Yoga": "Trataka (Candle Gazing), Palming",
                   "Food": "Carrots, Papaya, Agathi Keerai",
                   "Reason": "Vitamin A support"},
    "Diabetes": {"Yoga": "Mandukasana, Paschimottanasana",
                 "Food": "Fenugreek, Millets, Jamun",
                 "Reason": "Insulin regulation"},
    "Acidity/Digestion": {"Yoga": "Vajrasana, Pavanamuktasana",
                           "Food": "Buttermilk, Fennel seeds, Ginger",
                           "Reason": "Gut motility"},
    "Anxiety/Stress": {"Yoga": "Shavasana, Nadi Shodhana",
                       "Food": "Chamomile, Almonds, Dark Chocolate",
                       "Reason": "Cortisol reduction"},
    "Back Pain": {"Yoga": "Marjariasana, Bhujangasana",
                  "Food": "Turmeric, Garlic, Drumstick leaves",
                  "Reason": "Spine flexibility"},
    "Anemia": {"Yoga": "Sarvangasana, Surya Namaskar",
               "Food": "Dates, Jaggery, Pomegranate",
               "Reason": "Hemoglobin boost"},
    "High BP": {"Yoga": "Shavasana, Chandra Bhedi",
                "Food": "Garlic, Banana, Low-salt diet",
                "Reason": "Calms nervous system"},
    "Thyroid": {"Yoga": "Ustrasana, Sarvangasana",
                "Food": "Iodized salt, Walnut, Moong Dal",
                "Reason": "Hormonal balance"}
}

# ---------------- ALERTS & MOTIVATION ----------------
doctor_alert_text = "Doctor Alert: Consult your doctor before making any lifestyle changes or if you have medical conditions."
hydration_text = "Hydration Reminder: Drink at least 8 glasses of water daily."
disclaimer_text = "Disclaimer: This report is for educational purposes only. It does not replace professional medical advice."
motivation_text = "Stay consistent! Small daily efforts lead to big results in your health journey."

# ---------------- APP CONFIG ----------------
st.set_page_config(page_title="Nutri-Sense Wellness", page_icon="🌿", layout="wide")
st.title("Nutri-Sense: Lifestyle & Health Guide")

# ---------------- USER FORM ----------------
with st.form("user_form"):
    st.subheader("Health Profile")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", 5, 100, 30)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        selected = st.multiselect("Select Health Issues", list(data_master.keys()))
    submit = st.form_submit_button("Generate Full Plan")

# ---------------- DISPLAY PLAN ----------------
if submit:
    if not name or not selected:
        st.warning("Please fill all required fields.")
    else:
        st.success(f"Generated Plan for {name}")

        # Display each issue
        for issue in selected:
            d = data_master[issue]
            with st.expander(f"{issue}", expanded=True):
                st.write(f"🧘 Yoga: {d['Yoga']}")
                st.write(f"🍛 Food: {d['Food']}")
                st.info(f"💡 Reason: {d['Reason']}")

        # Alerts + Motivation
        st.warning(doctor_alert_text)
        st.info(hydration_text)
        st.caption(disclaimer_text)
        st.success(motivation_text)

        # ---------------- PDF GENERATION ----------------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=12)  # regular font

        # Title
        pdf.cell(0, 10, f"Wellness Report: {name}", ln=True, align='C')
        pdf.ln(5)

        # Table header
        pdf.set_font('', 'B')
        pdf.cell(50,8,"Issue",1,0,'C')
        pdf.cell(70,8,"Yoga",1,0,'C')
        pdf.cell(70,8,"Food",1,0,'C')
        pdf.cell(0,8,"Reason",1,1,'C')
        pdf.set_font('', '')

        # Table rows
        for issue in selected:
            d = data_master[issue]
            pdf.cell(50,8,issue,1)
            pdf.cell(70,8,d['Yoga'],1)
            pdf.cell(70,8,d['Food'],1)
            pdf.cell(0,8,d['Reason'],1,1)

        pdf.ln(5)
        pdf.multi_cell(0,8,doctor_alert_text)
        pdf.ln(2)
        pdf.multi_cell(0,8,hydration_text)
        pdf.ln(2)
        pdf.multi_cell(0,8,disclaimer_text)
        pdf.ln(2)
        pdf.multi_cell(0,8,motivation_text)

        pdf.ln(10)
        pdf.cell(0,10,"© 2025 Nutri-Sense",ln=True,align='C')

        # Download button
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        st.download_button("Download Wellness Report (PDF)", pdf_bytes, f"{name}_Wellness_Report.pdf")

        # ---------- Rating AFTER download ----------
        st.subheader("Rate Your Health")
        rating = st.radio(
            "Choose your rating",
            ["★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★"],
            index=2
        )
        st.success(f"Thanks for your rating: {rating}")
