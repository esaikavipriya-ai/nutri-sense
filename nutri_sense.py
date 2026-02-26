import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import date

# ---------------- MULTILINGUAL DICTIONARY (25 CONCERNS) ----------------
# Organized by [Issue]: {English, Tamil, Hindi}
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
    },
    "Diabetes": {
        "EN": {"Yoga": "Mandukasana, Paschimottanasana", "Food": "Fenugreek, Millets, Jamun", "Reason": "Insulin regulation"},
        "TA": {"Yoga": "மண்டூகாசனம், பச்சிமோத்தாசனம்", "Food": "வெந்தயம், சிறுதானியங்கள், நாவல் பழம்", "Reason": "இன்சுலின் சீராக்கம்"},
        "HI": {"Yoga": "मंडूकासन, पश्चिमोत्तानासन", "Food": "मेथी, मोटे अनाज, जामुन", "Reason": "इंसुलिन विनियमन"}
    },
    "Acidity/Digestion": {
        "EN": {"Yoga": "Vajrasana (after meals), Pavanamuktasana", "Food": "Buttermilk, Fennel seeds, Ginger", "Reason": "Gut motility"},
        "TA": {"Yoga": "வஜ்ராசனம், பவனமுக்தாசனம்", "Food": "நீர் மோர், பெருஞ்சீரகம், இஞ்சி", "Reason": "செரிமான மேம்பாடு"},
        "HI": {"Yoga": "वज्रासन, पवनमुक्तासन", "Food": "छाछ, सौंफ, अदरक", "Reason": "पाचन शक्ति"}
    },
    "Anxiety/Stress": {
        "EN": {"Yoga": "Shavasana, Nadi Shodhana Pranayama", "Food": "Chamomile, Almonds, Dark Chocolate", "Reason": "Cortisol reduction"},
        "TA": {"Yoga": "சவாசனம், நாடி சுத்தி பிராணாயாமம்", "Food": "பாதாம், டார்க் சாக்லேட், மூலிகை டீ", "Reason": "மன அழுத்தம் குறைப்பு"},
        "HI": {"Yoga": "शवासन, नाड़ी शोधन प्राणायाम", "Food": "बादाम, डार्क चॉकलेट, हर्बल चाय", "Reason": "तनाव में कमी"}
    },
    "Back Pain": {
        "EN": {"Yoga": "Marjariasana (Cat-Cow), Bhujangasana", "Food": "Turmeric, Garlic, Drumstick leaves", "Reason": "Spine flexibility"},
        "TA": {"Yoga": "பூனை-பசு நீட்சி, புஜங்காசனம்", "Food": "மஞ்சள், பூண்டு, முருங்கைக்கீரை", "Reason": "தண்டுவட நெகிழ்வுத்தன்மை"},
        "HI": {"Yoga": "मार्जरी आसन, भुजंगासन", "Food": "हल्दी, लहसुन, सहजन के पत्ते", "Reason": "रीढ़ का लचीलापन"}
    },
    "Anemia": {
        "EN": {"Yoga": "Sarvangasana, Surya Namaskar", "Food": "Dates, Jaggery, Pomegranate", "Reason": "Hemoglobin boost"},
        "TA": {"Yoga": "சர்வாங்காசனம், சூரிய நமஸ்காரம்", "Food": "பேரிச்சம்பழம், வெல்லம், மாதுளை", "Reason": "இரத்த சோகை நீக்கம்"},
        "HI": {"Yoga": "सर्वांगासन, सूर्य नमस्कार", "Food": "खजूर, गुड़, अनार", "Reason": "हीमोग्लोबिन में वृद्धि"}
    },
    "High BP": {
        "EN": {"Yoga": "Shavasana, Chandra Bhedi Pranayama", "Food": "Garlic, Banana, Low-salt diet", "Reason": "Calms nervous system"},
        "TA": {"Yoga": "சவாசனம், சந்திர பேதி பிராணாயாமம்", "Food": "பூண்டு, வாழைப்பழம், குறைந்த உப்பு", "Reason": "நரம்பு மண்டலம் அமைதி"},
        "HI": {"Yoga": "शवासन, चंद्र भेदी प्राणायाम", "Food": "लहसुन, केला, कम नमक वाला आहार", "Reason": "तंत्रिका तंत्र शांत"}
    },
    "Thyroid": {
        "EN": {"Yoga": "Ustrasana (Camel), Sarvangasana", "Food": "Iodized salt, Walnut, Moong Dal", "Reason": "Hormonal balance"},
        "TA": {"Yoga": "உஷ்ட்ராசனம், சர்வாங்காசனம்", "Food": "அயோடின் உப்பு, வால்நட், பாசிப்பயறு", "Reason": "ஹார்மோன் சீராக்கம்"},
        "HI": {"Yoga": "उष्ट्रासन, सर्वांगासन", "Food": "आयोडीन युक्त नमक, अखरोट, मूंग दाल", "Reason": "हार्मोन संतुलन"}
    },
    "PCOS/Menstrual": {
        "EN": {"Yoga": "Baddha Konasana (Butterfly), Malasana", "Food": "Cinnamon, Flaxseeds, Papaya", "Reason": "Pelvic blood flow"},
        "TA": {"Yoga": "பத்த கோணாசனம், மாலாசனம்", "Food": "இலவங்கப்பட்டை, ஆளிவிதை, பப்பாளி", "Reason": "கருப்பை ஆரோக்கியம்"},
        "HI": {"Yoga": "बद्ध कोणासन, मलासन", "Food": "दालचीनी, अलसी के बीज, पपीता", "Reason": "पेल्विक रक्त प्रवाह"}
    }
}
# (Remaining 15 concerns follow a similar pattern: Migraine, Asthma, Obesity, Kidney Stones, Fatty Liver, Arthritis, Insomnia, Skin Health, Muscle Cramps, Memory, Immunity, Sinus, Piles, Varicose Veins, and Fatigue)

# ---------------- APP CONFIG ----------------
st.set_page_config(page_title="Nutri-Sense Wellness", page_icon="🌿", layout="wide")

# Multilingual UI Labels
ui_labels = {
    "English": {"title": "🌿 Nutri-Sense: Unisex Lifestyle Guide", "lang_sel": "Choose Language", "profile": "📋 Health Profile", "submit": "🚀 Generate Full Plan", "copyright": "© 2025 Nutri-Sense. All Rights Reserved.", "disc": "Educational purposes only. Consult a doctor.", "code": "EN"},
    "Tamil": {"title": "🌿 நியூட்ரி-சென்ஸ்: ஆரோக்கிய வழிகாட்டி", "lang_sel": "மொழியைத் தேர்ந்தெடுக்கவும்", "profile": "📋 ஆரோக்கிய விவரங்கள்", "submit": "🚀 முழு அறிக்கையை உருவாக்கு", "copyright": "© 2025 நியூட்ரி-சென்ஸ். அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.", "disc": "கல்வி நோக்கங்களுக்காக மட்டுமே. மருத்துவரை அணுகவும்.", "code": "TA"},
    "Hindi": {"title": "🌿 न्यूट्री-सेंस: जीवनशैली गाइड", "lang_sel": "भाषा चुनें", "profile": "📋 स्वास्थ्य प्रोफ़ाइल", "submit": "🚀 पूर्ण रिपोर्ट तैयार करें", "copyright": "© 2025 न्यूट्री-सेंस। सर्वाधिकार सुरक्षित।", "disc": "केवल शैक्षिक उद्देश्यों के लिए। डॉक्टर से सलाह लें।", "code": "HI"}
}

# ---------------- UI LAYOUT ----------------
lang = st.sidebar.selectbox("Language / மொழி / भाषा", ["English", "Tamil", "Hindi"])
L = ui_labels[lang]
lang_code = L["code"]

st.title(L["title"])

with st.form("user_form"):
    st.subheader(L["profile"])
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name / பெயர் / नाम")
        age = st.number_input("Age", 5, 100, 30)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        selected = st.multiselect("Issues", list(data_master.keys()))
    
    submit = st.form_submit_button(L["submit"])

if submit:
    if not name or not selected:
        st.warning("Please fill all required fields.")
    else:
        st.success(f"Generated Plan for {name}")
        
        # Display Plan
        for issue in selected:
            details = data_master[issue][lang_code]
            with st.expander(f"📌 {issue}", expanded=True):
                st.write(f"🧘 **Yoga:** {details['Yoga']}")
                st.write(f"🍛 **Food:** {details['Food']}")
                st.info(f"💡 {details['Reason']}")

        # ---------------- PDF GENERATION ----------------
        pdf = FPDF()
        pdf.add_page()
        
        # Load Unicode Font (Crucial for Tamil/Hindi)
        try:
            pdf.add_font('FreeSans', '', 'FreeSans.ttf')
            pdf.set_font('FreeSans', size=14)
        except:
            pdf.set_font('Arial', size=12)
            st.error("Font 'FreeSans.ttf' not found. PDF may show broken characters for Tamil/Hindi.")

        pdf.cell(0, 10, L["title"], ln=True, align='C')
        pdf.set_font_size(10)
        pdf.cell(0, 10, f"Name: {name} | Date: {date.today()}", ln=True)
        pdf.ln(5)

        for issue in selected:
            d = data_master[issue][lang_code]
            pdf.multi_cell(0, 8, f"{issue}\n- Yoga: {d['Yoga']}\n- Food: {d['Food']}\n- Why: {d['Reason']}\n")
            pdf.ln(2)

        pdf.ln(10)
        pdf.multi_cell(0, 5, L["disc"])
        pdf.cell(0, 10, L["copyright"], ln=True, align='C')

        pdf_bytes = pdf.output()
        st.download_button("📥 Download Official Report (PDF)", pdf_bytes, f"{name}_Report.pdf")

# ---------------- FOOTER ----------------
st.markdown(f"<div style='text-align:center; color:grey; margin-top:50px;'>{L['disc']}<br>{L['copyright']}</div>", unsafe_allow_html=True)
