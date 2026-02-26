import streamlit as st
from fpdf import FPDF

# ---------------- MULTILINGUAL DATA (10 SAMPLE CONCERNS) ----------------
data_master = {
    "Hair Fall": {
        "EN": {"Yoga": "Adho Mukha Svanasana, Sarvangasana", "Food": "Moringa leaves, Amla, Curry leaves", "Reason": "Scalp circulation"},
        "TA": {"Yoga": "அதோ முக ஸ்வனாசனம், சர்வாங்காசனம்", "Food": "முருங்கைக்கீரை, நெல்லிக்காய், கறிவேப்பிலை", "Reason": "தலைப்பகுதிக்கு இரத்த ஓட்டம்"},
        "HI": {"Yoga": "अधो मुख श्वानासन, सर्वांगासन", "Food": "सहजन की पत्तियां, आंवला, करी पत्ता", "Reason": "स्कैल्प में रक्त संचार"}
    },
    "Eye Strain": {
        "EN": {"Yoga": "Trataka (Candle Gazing), Palming", "Food": "Carrots, Papaya, Agathi Keerai", "Reason": "Vitamin A support"},
        "TA": {"Yoga": "திராடகம், பாமிங் பயிற்சி", "Food": "கேரட், பப்பாளி, அகத்திக்கீரை", "Reason": "வைட்டமின் ஏ சத்து"},
        "HI": {"Yoga": "त्राटक, पाल्मिंग", "Food": "गाजर, पपीता, अगथी के पत्ते", "Reason": "विटामिन ए का सहारा"}
    }
}

# ---------------- ALERTS & MOTIVATION ----------------
doctor_alert_text = {
    "EN": "⚠️ Doctor Alert: Consult your doctor before making any lifestyle changes or if you have medical conditions.",
    "TA": "⚠️ மருத்துவர் அறிவிப்பு: எந்த மருத்துவ நிலை இருந்தாலும் வாழ்க்கை முறையை மாற்றுவதற்கு முன் மருத்துவரை அணுகவும்.",
    "HI": "⚠️ डॉक्टर चेतावनी: किसी भी जीवनशैली परिवर्तन से पहले या किसी भी चिकित्सीय स्थिति में डॉक्टर से सलाह लें।"
}

hydration_text = {
    "EN": "💧 Hydration Reminder: Drink at least 8 glasses of water daily.",
    "TA": "💧 நீர்சத்து அறிவிப்பு: தினமும் குறைந்தது 8 கண்ணாடி தண்ணீர் குடிக்கவும்.",
    "HI": "💧 हाइड्रेशन अनुस्मारक: रोजाना कम से कम 8 गिलास पानी पिएं।"
}

disclaimer_text = {
    "EN": "📌 Disclaimer: This report is for educational purposes only. It does not replace professional medical advice.",
    "TA": "📌 பிரதி அறிவிப்பு: இந்த அறிக்கை கல்வி நோக்கங்களுக்காக மட்டுமே. இது மருத்துவ ஆலோசனையை மாற்றாது.",
    "HI": "📌 अस्वीकरण: यह रिपोर्ट केवल शैक्षिक उद्देश्यों के लिए है। यह पेशेवर चिकित्सा सलाह का विकल्प नहीं है।"
}

motivation_text = {
    "EN": "🌟 Stay consistent! Small daily efforts lead to big results in your health journey.",
    "TA": "🌟 தொடருங்கள்! தினசரி சிறிய முயற்சிகள் உங்கள் ஆரோக்கிய பயணத்தில் பெரிய மாற்றத்தை உருவாக்கும்.",
    "HI": "🌟 लगातार बने रहें! रोजाना के छोटे प्रयास आपके स्वास्थ्य में बड़े परिणाम लाते हैं।"
}

# ---------------- APP CONFIG ----------------
st.set_page_config(page_title="Nutri-Sense Wellness", page_icon="🌿", layout="wide")
ui_labels = {
    "English": {"title": "🌿 Nutri-Sense: Unisex Lifestyle Guide", "code":"EN", "copyright":"© 2025 Nutri-Sense"},
    "Tamil": {"title": "🌿 நியூட்ரி-சென்ஸ்: ஆரோக்கிய வழிகாட்டி", "code":"TA", "copyright":"© 2025 நியூட்ரி-சென்ஸ்"},
    "Hindi": {"title": "🌿 न्यूट्री-सेंस: जीवनशैली गाइड", "code":"HI", "copyright":"© 2025 न्यूट्री-सेंस"}
}

lang = st.sidebar.selectbox("Language / மொழி / भाषा", ["English", "Tamil", "Hindi"])
L = ui_labels[lang]
lang_code = L["code"]

st.title(L["title"])

# ---------------- USER FORM ----------------
with st.form("user_form"):
    st.subheader("📋 Health Profile")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name / பெயர் / नाम")
        age = st.number_input("Age", 5, 100, 30)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        selected = st.multiselect("Issues", list(data_master.keys()))
    
    submit = st.form_submit_button("🚀 Generate Full Plan")

# ---------------- DISPLAY PLAN ----------------
if submit:
    if not name or not selected:
        st.warning("Please fill all required fields.")
    else:
        st.success(f"Generated Plan for {name}")

        # Display each issue in app
        for issue in selected:
            d = data_master[issue][lang_code]
            with st.expander(f"📌 {issue}", expanded=True):
                st.write(f"🧘 **Yoga:** {d['Yoga']}")
                st.write(f"🍛 **Food:** {d['Food']}")
                st.info(f"💡 {d['Reason']}")

        # Alerts + Motivation
        st.warning(doctor_alert_text[lang_code])
        st.info(hydration_text[lang_code])
        st.caption(disclaimer_text[lang_code])
        st.success(motivation_text[lang_code])

        # ---------------- PDF GENERATION ----------------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Helvetica', size=12)

        # Title
        pdf.cell(0, 10, f"🌿 Wellness Report: {name}", ln=True, align='C')
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
            d = data_master[issue][lang_code]
            pdf.cell(50,8,issue,1)
            pdf.cell(70,8,d['Yoga'],1)
            pdf.cell(70,8,d['Food'],1)
            pdf.cell(0,8,d['Reason'],1,1)

        pdf.ln(5)
        pdf.multi_cell(0,8,doctor_alert_text[lang_code])
        pdf.ln(2)
        pdf.multi_cell(0,8,hydration_text[lang_code])
        pdf.ln(2)
        pdf.multi_cell(0,8,disclaimer_text[lang_code])
        pdf.ln(2)
        pdf.multi_cell(0,8,motivation_text[lang_code])
        pdf.ln(10)
        pdf.cell(0,10,L['copyright'],ln=True,align='C')

        # Download button
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        st.download_button("📥 Download Wellness Report (PDF)", pdf_bytes, f"{name}_Wellness_Report.pdf")

        # ---------------- ASK RATING AFTER DOWNLOAD ----------------
        st.subheader("⭐ How would you rate this app after downloading your report?")
        user_rating = st.radio(
            "Choose your rating",
            ["★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★"],
            index=2
        )
        if user_rating:
            st.success(f"Thank you for rating: {user_rating}")
