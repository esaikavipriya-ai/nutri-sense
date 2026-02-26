import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import date

# ---------------- MULTILINGUAL DATA ----------------
translations = {
    "English": {
        "title": "🌿 Nutri-Sense: Global Wellness Guide",
        "labels": {"Yoga": "Yoga", "Food": "Traditional Food", "Benefit": "Benefit", "Morning": "Morning", "Breakfast": "Breakfast", "Lunch": "Lunch", "Dinner": "Dinner"},
        "ui": {"lang": "Select Language", "name": "Name*", "age": "Age*", "gender": "Gender*", "concerns": "Health Concerns*", "submit": "🚀 Generate Full Plan", "download": "📥 Download PDF Report"},
        "disclaimer": "DISCLAIMER: Educational purposes only. Consult a doctor. © 2025 Nutri-Sense.",
        "gender_opts": ["Select", "Male", "Female", "Other"]
    },
    "Tamil": {
        "title": "🌿 நியூட்ரி-சென்ஸ்: ஆரோக்கிய வழிகாட்டி",
        "labels": {"Yoga": "யோகா", "Food": "பாரம்பரிய உணவு", "Benefit": "நன்மை", "Morning": "காலை (வெறும் வயிறு)", "Breakfast": "காலை உணவு", "Lunch": "மதிய உணவு", "Dinner": "இரவு உணவு"},
        "ui": {"lang": "மொழியைத் தேர்ந்தெடுக்கவும்", "name": "பெயர்*", "age": "வயது*", "gender": "பாலினம்*", "concerns": "ஆரோக்கிய பிரச்சனைகள்*", "submit": "🚀 முழு அறிக்கையை உருவாக்கு", "download": "📥 அறிக்கையைப் பதிவிறக்கவும் (PDF)"},
        "disclaimer": "பொறுப்புத் துறப்பு: கல்வி நோக்கங்களுக்காக மட்டுமே. மருத்துவ ஆலோசனைக்கு மருத்துவரை அணுகவும். © 2025 நியூட்ரி-சென்ஸ்.",
        "gender_opts": ["தேர்ந்தெடு", "ஆண்", "பெண்", "மற்றவை"]
    },
    "Hindi": {
        "title": "🌿 न्यूट्री-सेंस: समग्र स्वास्थ्य मार्गदर्शिका",
        "labels": {"Yoga": "योग", "Food": "पारंपरिक आहार", "Benefit": "लाभ", "Morning": "सुबह (खाली पेट)", "Breakfast": "नाश्ता", "Lunch": "दोपहर का भोजन", "Dinner": "रात का खाना"},
        "ui": {"lang": "भाषा चुनें", "name": "नाम*", "age": "आयु*", "gender": "लिंग*", "concerns": "स्वास्थ्य संबंधी चिंताएं*", "submit": "🚀 पूर्ण रिपोर्ट तैयार करें", "download": "📥 पीडीएफ रिपोर्ट डाउनलोड करें"},
        "disclaimer": "अस्वीकरण: केवल शैक्षिक उद्देश्यों के लिए। चिकित्सा सलाह के लिए डॉक्टर से परामर्श करें। © 2025 न्यूट्री-सेंस।",
        "gender_opts": ["चुनें", "पुरुष", "महिला", "अन्य"]
    }
}

# ---------------- EXPANDED CONCERN DATA (Unisex) ----------------
concern_data = {
    "English": {
        "Kidney Stones": {"Yoga": "Ustrasana (Camel Pose), Pawanmuktasana", "Food": "Coconut Water, Barley Water, Bottle Gourd sabzi", "Reason": "Helps flush toxins and prevents crystal formation."},
        "Fatty Liver": {"Yoga": "Bhujangasana (Cobra), Mandukasana", "Food": "Turmeric, Cruciferous Veg (Broccoli), Green Tea", "Reason": "Stimulates liver enzymes and reduces fat accumulation."},
        "Heart Health/Cholesterol": {"Yoga": "Surya Namaskar, Ardha Matsyendrasana", "Food": "Oats, Walnuts, Garlic, Flax seeds", "Reason": "Improves circulation and lowers LDL levels."},
        "Arthritis/Joint Pain": {"Yoga": "Vajrasana, Marjariasana (Cat-Cow)", "Food": "Ginger, Turmeric Milk, Whole Grains", "Reason": "Reduces inflammation and keeps joints flexible."},
        "Anemia": {"Yoga": "Sarvangasana, Anulom Vilom", "Food": "Dates, Moringa, Pomegranate", "Reason": "Increases iron absorption and blood oxygenation."}
    },
    "Tamil": {
        "சிறுநீரகக் கல் (Kidney Stones)": {"Yoga": "உஷ்ட்ராசனம், பவனமுக்தாசனம்", "Food": "இளநீர், பார்லி கஞ்சி, சுரைக்காய் கூட்டு", "Reason": "நச்சுகளை வெளியேற்றி கல் உருவாவதைத் தடுக்கிறது."},
        "கல்லீரல் ஆரோக்கியம் (Fatty Liver)": {"Yoga": "புஜங்காசனம், மண்டூகாசனம்", "Food": "மஞ்சள், காலிஃபிளவர், பச்சைத் தேயிலை (Green Tea)", "Reason": "கல்லீரல் கொழுப்பைக் குறைத்து என்சைம்களைத் தூண்டுகிறது."},
        "இதய ஆரோக்கியம்/கொலஸ்ட்ரால்": {"Yoga": "சூரிய நமஸ்காரம், அர்த்த மத்ஸ்யேந்திராசனம்", "Food": "ஓட்ஸ், வால்நட்ஸ், பூண்டு, ஆளிவிதை", "Reason": "இரத்த ஓட்டத்தை சீராக்கி கெட்ட கொழுப்பைக் குறைக்கிறது."},
        "மூட்டு வலி (Arthritis)": {"Yoga": "வஜ்ராசனம், பூனை-பசு நீட்சி", "Food": "இஞ்சி, மஞ்சள் பால், முழு தானியங்கள்", "Reason": "வீக்கத்தைக் குறைத்து மூட்டுகளை வலுவாக்குகிறது."}
    },
    "Hindi": {
        "पथरी (Kidney Stones)": {"Yoga": "उष्ट्रासन, पवनमुक्तासन", "Food": "नारियल पानी, जौ का पानी, लौकी की सब्जी", "Reason": "विषाक्त पदार्थों को बाहर निकालने में मदद करता है."},
        "फैटी लिवर (Fatty Liver)": {"Yoga": "भुजंगासन, मंडूकासन", "Food": "हल्दी, ब्रोकोली, ग्रीन टी", "Reason": "लिवर एंजाइम को सक्रिय करता है और वसा कम करता है."},
        "हृदय स्वास्थ्य/कोलेस्ट्रॉल": {"Yoga": "सूर्य नमस्कार, अर्ध मत्स्येंद्रासन", "Food": "ओट्स, अखरोट, लहसुन, अलसी", "Reason": "रक्त संचार में सुधार और कोलेस्ट्रॉल कम करता है."},
        "गठिया/जोड़ों का दर्द (Arthritis)": {"Yoga": "वज्रासन, मार्जरी आसन", "Food": "अदरक, हल्दी वाला दूध, साबुत अनाज", "Reason": "सूजन कम करता है और जोड़ों को लचीला बनाता है."}
    }
}

# ---------------- APP INTERFACE ----------------
st.set_page_config(page_title="Nutri-Sense", page_icon="🌿", layout="wide")
lang = st.sidebar.selectbox(translations["English"]["ui"]["lang"], ["English", "Tamil", "Hindi"])
t = translations[lang]
cd = concern_data[lang]

st.title(t["title"])

with st.form("wellness_form"):
    st.subheader(t["ui"]["name"])
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(t["ui"]["name"])
        age = st.number_input(t["ui"]["age"], 10, 100, 30)
    with col2:
        gender = st.selectbox(t["ui"]["gender"], t["gender_opts"])
        selected = st.multiselect(t["ui"]["concerns"], list(cd.keys()))
    submit = st.form_submit_button(t["ui"]["submit"])

if submit:
    if not name or not selected:
        st.error("⚠️ Please fill all fields.")
    else:
        st.success(f"Plan for {name}")
        for c in selected:
            with st.expander(c, expanded=True):
                st.write(f"🧘 **{t['labels']['Yoga']}:** {cd[c]['Yoga']}")
                st.write(f"🍛 **{t['labels']['Food']}:** {cd[c]['Food']}")
                st.info(f"💡 {cd[c]['Reason']}")

        # --- PDF Export (Requires FreeSans.ttf for Hindi/Tamil characters) ---
        pdf = FPDF()
        pdf.add_page()
        try:
            pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)
            pdf.set_font('FreeSans', '', 12)
        except:
            pdf.set_font('Arial', '', 12)

        pdf.cell(0, 10, t["title"], ln=True, align='C')
        pdf.cell(0, 10, f"Name: {name} | Age: {age} | Date: {date.today()}", ln=True)
        for c in selected:
            pdf.multi_cell(0, 10, f"\n{c}\nYoga: {cd[c]['Yoga']}\nFood: {cd[c]['Food']}")
        
        pdf.ln(10)
        pdf.set_font_size(8)
        pdf.multi_cell(0, 5, t["disclaimer"])
        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
        st.download_button(t["ui"]["download"], pdf_bytes, f"Report_{name}.pdf")

st.markdown(f"--- \n {t['disclaimer']}")
