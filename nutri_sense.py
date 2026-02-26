import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import date

# ---------------- MULTILINGUAL DICTIONARY ----------------
translations = {
    "English": {
        "title": "🌿 Nutri-Sense: Wellness Guide",
        "lang_select": "Choose Language / மொழியைத் தேர்ந்தெடுக்கவும் / भाषा चुनें",
        "name": "Full Name*",
        "age": "Age*",
        "gender": "Gender*",
        "concerns": "Health Concerns*",
        "submit": "🚀 Generate Wellness Report",
        "report_title": "Nutri-Sense Wellness Report",
        "disclaimer": "DISCLAIMER: This report is for educational purposes only and is not medical advice.",
        "copyright": "All Rights Reserved. ©",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    },
    "Tamil": {
        "title": "🌿 நியூட்ரி-சென்ஸ்: ஆரோக்கிய வழிகாட்டி",
        "lang_select": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "name": "முழு பெயர்*",
        "age": "வயது*",
        "gender": "பாலினம்*",
        "concerns": "ஆரோக்கிய பிரச்சனைகள்*",
        "submit": "🚀 அறிக்கையை உருவாக்கு",
        "report_title": "நியூட்ரி-சென்ஸ் ஆரோக்கிய அறிக்கை",
        "disclaimer": "பொறுப்புத் துறப்பு: இந்த அறிக்கை கல்வி நோக்கங்களுக்காக மட்டுமே, மருத்துவ ஆலோசனை அல்ல.",
        "copyright": "அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை. ©",
        "days": ["திங்கள்", "செவ்வாய்", "புதன்", "வியாழன்", "வெள்ளி", "சனி", "ஞாயிறு"]
    },
    "Hindi": {
        "title": "🌿 न्यूट्री-सेंस: जीवनशैली और योग मार्गदर्शिका",
        "lang_select": "भाषा चुनें",
        "name": "पूरा नाम*",
        "age": "आयु*",
        "gender": "लिंग*",
        "concerns": "स्वास्थ्य संबंधी चिंताएं*",
        "submit": "🚀 रिपोर्ट तैयार करें",
        "report_title": "न्यूट्री-सेंस स्वास्थ्य रिपोर्ट",
        "disclaimer": "अस्वीकरण: यह रिपोर्ट केवल शैक्षिक उद्देश्यों के लिए है और चिकित्सा सलाह नहीं है।",
        "copyright": "सर्वाधिकार सुरक्षित। ©",
        "days": ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
    }
}

# ---------------- DATA ----------------
concern_data = {
    "English": {"Hair Fall": "Murungai Keerai (Moringa)", "Eye Strain": "Carrot Poriyal", "PCOS": "Flax Seeds"},
    "Tamil": {"Hair Fall": "முருங்கைக்கீரை, கருப்பட்டி", "Eye Strain": "கேரட் பொரியல், அகத்திக்கீரை", "PCOS": "வெந்தயக்களி"},
    "Hindi": {"Hair Fall": "सहजन (मुरुंगई), गुड़", "Eye Strain": "गाजर की सब्जी", "PCOS": "अलसी के बीज"}
}

# ---------------- APP CONFIG ----------------
st.set_page_config(page_title="Nutri-Sense", page_icon="🌿")
lang = st.sidebar.selectbox(translations["English"]["lang_select"], ["English", "Tamil", "Hindi"])
t = translations[lang]

st.title(t["title"])

with st.form("wellness_form"):
    name = st.text_input(t["name"])
    age = st.number_input(t["age"], 10, 100, 30)
    selected_concerns = st.multiselect(t["concerns"], list(concern_data[lang].keys()))
    submit = st.form_submit_button(t["submit"])

if submit:
    st.subheader(t["report_title"])
    for c in selected_concerns:
        st.write(f"🎯 **{c}:** {concern_data[lang][c]}")

    # ---------------- PDF GENERATION ----------------
    # Note: To print Tamil/Hindi in PDF, you MUST download 'FreeSans.ttf' 
    # from GNU FreeFont and place it in your project folder.
    pdf = FPDF()
    pdf.add_page()
    
    # FPDF2 supports Unicode via .add_font()
    try:
        pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)
        pdf.set_font('FreeSans', '', 14)
    except:
        pdf.set_font('Arial', '', 12) # Fallback if font file missing

    pdf.cell(0, 10, t["report_title"], ln=True, align='C')
    pdf.cell(0, 10, f"{t['name']}: {name} | {t['age']}: {age}", ln=True)
    
    for c in selected_concerns:
        pdf.multi_cell(0, 10, f"{c}: {concern_data[lang][c]}")
    
    pdf.ln(10)
    pdf.set_font_size(8)
    pdf.multi_cell(0, 5, t["disclaimer"])
    pdf.cell(0, 10, f"{t['copyright']} {date.today().year} Nutri-Sense", ln=True, align='C')

    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button("📥 Download PDF", pdf_bytes, "Report.pdf")

st.markdown(f"--- \n {t['disclaimer']} \n\n {t['copyright']} {date.today().year} Nutri-Sense")
