import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Nutri-Sense Health", layout="wide", page_icon="🌿")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #f1f8e9 0%, #ffffff 50%, #e8f5e9 100%); }
.stButton>button { width: 100%; border-radius: 10px; background-color: #1b5e20; color: white; height: 3.5em; font-weight: bold; }
h1 { color: #1b5e20; text-align: center; }
.footer-text { text-align: center; color: #666; font-size: 12px; margin-top: 50px; border-top: 1px solid #ddd; padding-top: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🌿 Nutri-Sense: Tamil Traditional Wellness (Unisex)")

# ---------------- UNISEX CONCERN DATA (Tamil Traditional) ----------------
concern_plan = {
    "Hair Fall": {"Yoga": "Downward Dog, Camel Pose", "Food": "Murungai Keerai (Moringa), Karupatti (Palm Jaggery)", "Reason": "Iron & Antioxidants for scalp health"},
    "Eye Strain": {"Yoga": "Palming, Trataka", "Food": "Carrot Poriyal, Agathi Keerai, Papaya", "Reason": "High Vitamin A & Lutein"},
    "Stress/Headache": {"Yoga": "Child Pose, Nadi Shodhana", "Food": "Sukku Coffee (Dry Ginger), Coconut Water", "Reason": "Natural electrolytes and anti-inflammatory"},
    "Hormonal Balance (F)": {"Yoga": "Butterfly Pose", "Food": "Ellu Urundai (Sesame), Fenugreek Kali", "Reason": "Regulates endocrine function"},
    "Prostate & Vitality (M)": {"Yoga": "Virasana (Hero Pose), Baddha Konasana", "Food": "Pumpkin Seeds, Watermelon, Gooseberry (Amla)", "Reason": "Zinc and Lycopene support"},
    "Muscle Recovery": {"Yoga": "Pigeon Pose, Legs up wall", "Food": "Sundal (Chickpeas), Black Urad Dal Kali", "Reason": "High protein for tissue repair"},
    "Digestive Issues": {"Yoga": "Vajrasana, Pawanmuktasana", "Food": "Buttermilk (Neer Mor), Jeera Water, Ginger", "Reason": "Probiotics and digestive enzymes"},
    "Joint/Body Pain": {"Yoga": "Cat-Cow Stretch", "Food": "Mudakathan Keerai, Turmeric Milk", "Reason": "Anti-inflammatory and joint lubrication"}
}

# ---------------- TAMIL WEEKLY ROUTINE TABLE ----------------
# Updated to include Tamil traditional breakfast/lunch concepts
weekly_routine = [
    ["Day", "Yoga Practice", "Tamil Traditional Nutrition"],
    ["Monday", "Tree Pose (Vrikshasana)", "Kambu Koozh (Pearl Millet) & Small Onions"],
    ["Tuesday", "Cobra Pose (Bhujangasana)", "Ragi Dosa with Groundnut Chutney"],
    ["Wednesday", "Warrior II (Virabhadrasana)", "Rice with Kollu Rasam (Horsegram)"],
    ["Thursday", "Triangle Pose (Trikonasana)", "Varagu Rice (Kodo Millet) & Sambhar"],
    ["Friday", "Child Pose (Balasana)", "Vegetable Upma & Pomegranate"],
    ["Saturday", "Plank Pose (Phalakasana)", "Sprouted Moong Dal Sundal & Buttermilk"],
    ["Sunday", "Corpse Pose (Shavasana)", "Traditional Brown Rice & Keerai Kootu"]
]

# ---------------- USER INPUT FORM ----------------
with st.form("health_form"):
    st.subheader("📋 Wellness Profile")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name*")
        age = st.number_input("Age*", 10, 100, 30)
    with col2:
        gender = st.selectbox("Gender*", ["Select", "Male", "Female", "Other"])
        concerns = st.multiselect("Health Concerns*", list(concern_plan.keys()))
    
    submit = st.form_submit_button("🚀 Generate Unisex Wellness Report")

# ---------------- REPORT GENERATION ----------------
if submit:
    if not name or gender == "Select" or not concerns:
        st.error("⚠️ Please provide your name, gender, and at least one health concern.")
    else:
        st.success(f"✅ Report successfully generated for {name}")
        
        # Display Personalized Plan
        st.subheader("🎯 Personalized Recommendations")
        for c in concerns:
            with st.expander(f"Plan for: {c}", expanded=True):
                st.write(f"🧘 **Yoga:** {concern_plan[c]['Yoga']}")
                st.write(f"🍛 **Tamil Food:** {concern_plan[c]['Food']}")
                st.caption(f"💡 Why: {concern_plan[c]['Reason']}")

        # Display Weekly Table
        st.subheader("📅 Tamil Traditional Weekly Nutrition Table")
        df_week = pd.DataFrame(weekly_routine[1:], columns=weekly_routine[0])
        st.table(df_week)

        # ---------------- PDF LOGIC ----------------
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Nutri-Sense: Personalized Wellness Report", ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 10, f"Issued to: {name} | Gender: {gender} | Date: {date.today()}", ln=True, align='C')
        pdf.ln(5)

        # Personalized Concerns
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "1. Targeted Health Solutions", ln=True)
        pdf.set_font("Arial", '', 10)
        for c in concerns:
            pdf.multi_cell(0, 7, f"Concern: {c}\nYoga: {concern_plan[c]['Yoga']}\nFood: {concern_plan[c]['Food']}\n")
            pdf.ln(2)

        # Weekly Table in PDF
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "2. Tamil Traditional Weekly Plan", ln=True)
        pdf.set_font("Arial", 'B', 9)
        
        # Table Header
        pdf.cell(25, 10, "Day", 1)
        pdf.cell(65, 10, "Yoga Practice", 1)
        pdf.cell(90, 10, "Nutrition Focus", 1)
        pdf.ln()
        
        # Table Rows
        pdf.set_font("Arial", '', 8)
        for row in weekly_routine[1:]:
            pdf.cell(25, 10, row[0], 1)
            pdf.cell(65, 10, row[1], 1)
            pdf.cell(90, 10, row[2], 1)
            pdf.ln()

        # Legal Section
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 8)
        pdf.multi_cell(0, 5, "DISCLAIMER: This report is for educational and lifestyle guidance only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with a physician or qualified healthcare provider regarding a medical condition.")
        pdf.ln(2)
        pdf.cell(0, 10, f"Copyright (c) {date.today().year} Nutri-Sense Wellness. All Rights Reserved.", ln=True, align='C')

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download Official PDF Report", pdf_output, file_name=f"NutriSense_{name}.pdf")

# ---------------- FOOTER ----------------
st.markdown(f"""
<div class="footer-text">
    <p><b>Disclaimer:</b> Educational wellness guidance only. Consult a doctor for medical issues.</p>
    <p>© {date.today().year} Nutri-Sense Health. All Rights Reserved. Protected by Copyright Law.</p>
</div>
""", unsafe_allow_html=True)
