import streamlit as st
import pandas as pd
import csv
from fpdf import FPDF
from datetime import date
import matplotlib.pyplot as plt
import qrcode
from PIL import Image
import io

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Nutri_Sense", layout="wide")

# ---------- LANGUAGE ----------
lang = st.sidebar.selectbox("🌐 Language", ["English", "Tamil", "Hindi"])
title_text = {
    "English": "🌸 Nutri_Sense",
    "Tamil": "🌸 Nutri_Sense — புத்திசாலி ஊட்டச்சத்து உதவி",
    "Hindi": "🌸 Nutri_Sense — स्मार्ट पोषण सहायक"
}
st.title(title_text.get(lang, "Nutri_Sense"))

# ---------- USER DETAILS ----------
with st.expander("👤 Enter Details"):
    name = st.text_input("Name")
    age = st.number_input("Age", 10, 60)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    sleep = st.slider("Sleeping Hours", 3, 12, 7)
    mood = st.selectbox("Daily Mood", ["Happy", "Normal", "Stress", "Sad"])
    review = st.text_area("Review")

# ---------- SCORE ----------
score_map = {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3}
st.header("🩺 Select Symptoms")
col1, col2, col3 = st.columns(3)
with col1:
    hair = st.selectbox("Hair fall", list(score_map.keys()))
    eye = st.selectbox("Eye issue", list(score_map.keys()))
    head = st.selectbox("Headache", list(score_map.keys()))
    pigmentation = st.selectbox("Pigmentation", list(score_map.keys()))
with col2:
    heart = st.selectbox("Heart discomfort", list(score_map.keys()))
    leg = st.selectbox("Leg pain", list(score_map.keys()))
    infection = st.selectbox("Infection", list(score_map.keys()))
    kidney = st.selectbox("Kidney issue", list(score_map.keys()))
with col3:
    gall = st.selectbox("Gall bladder", list(score_map.keys()))
    bodypain = st.selectbox("Body pain", list(score_map.keys()))
    periods = st.selectbox("Irregular periods", list(score_map.keys())) if gender=="Female" else "None"
    pcos = st.selectbox("PCOS Symptoms", list(score_map.keys())) if gender=="Female" else "None"

# ---------- RISK CALCULATION ----------
scores = [hair, eye, head, pigmentation, heart, leg, infection, kidney, gall, bodypain, periods, pcos]
total = sum(score_map[i] for i in scores)
risk_percent = int((total/39)*100)

st.header("🎯 Health Risk Score")
st.progress(risk_percent/100)

# ---------- AI INSIGHT ----------
st.subheader("🤖 AI Health Insight")
if risk_percent < 30:
    st.success("Low Risk — Maintain balanced diet and hydration.")
elif risk_percent < 60:
    st.warning("Moderate Risk — Improve nutrition, sleep and stress management.")
else:
    st.error("High Risk — Preventive medical consultation recommended.")

# ---------- COLOR RISK METER ----------
st.subheader("📊 Risk Level")
if risk_percent < 30:
    st.success(f"Low Risk: {risk_percent}%")
elif risk_percent < 60:
    st.warning(f"Moderate Risk: {risk_percent}%")
else:
    st.error(f"High Risk: {risk_percent}%")

# ---------- DOCTOR ALERT ----------
if risk_percent > 65:
    st.error("👩‍⚕ Doctor consultation recommended")

# ---------- MOTIVATION MESSAGE ----------
st.subheader("💡 Daily Suggestion")
if mood == "Stress":
    st.info("Practice meditation and consume magnesium-rich foods.")
elif mood == "Sad":
    st.info("Include Omega-3 foods and sunlight exposure.")
elif mood == "Happy":
    st.success("Great! Maintain your lifestyle.")

# ---------- PIE CHART ----------
iron = 25 if hair!="None" or periods!="None" or pcos!="None" else 10
vitA = 25 if eye!="None" else 10
protein = 20 if bodypain!="None" or leg!="None" else 15
omega = 20 if heart!="None" else 10
hydration = 20 if kidney!="None" or infection!="None" else 15

labels = ["Iron","Vitamin A","Protein","Omega-3","Hydration"]
values = [iron, vitA, protein, omega, hydration]
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%")
st.pyplot(fig)

# ---------- FOOD RECOMMENDATIONS ----------
foods = []
if hair!="None" or periods!="None" or pcos!="None":
    foods += ["Spinach","Dates","Beetroot","Pomegranate"]
if eye!="None":
    foods += ["Carrot","Pumpkin","Almonds"]
if heart!="None":
    foods += ["Oats","Walnuts","Flax seeds"]
if kidney!="None":
    foods += ["Cucumber","Watermelon","Coconut water"]

st.write("🍎 Recommended Foods: " + ", ".join(foods))

# ---------- WEEKLY PLAN WITH MEALS, DRINKS, YOGA & BENEFITS ----------
st.subheader("📅 Weekly Smart Health Plan")

weekly_plan = {
    "Monday": {
        "Breakfast": "Oats with Spinach",
        "Lunch": "Grilled Chicken with Veggies",
        "Dinner": "Cucumber Salad with Quinoa",
        "Drink": "Green Tea",
        "Yoga": "Surya Namaskar",
        "Yoga_Image": "images/surya_namaskar.jpg",
        "Benefit": "Improves metabolism, reduces bloating"
    },
    "Tuesday": {
        "Breakfast": "Beetroot smoothie",
        "Lunch": "Pumpkin soup with nuts",
        "Dinner": "Grilled Fish with Watermelon",
        "Drink": "Herbal Infusion",
        "Yoga": "Bhujangasana (Cobra Pose)",
        "Yoga_Image": "images/bhujangasana.jpg",
        "Benefit": "Strengthens core, supports hormonal balance"
    },
    # Add other days similarly...
}

for day, info in weekly_plan.items():
    st.markdown(f"### {day}")
    st.write(f"**Breakfast:** {info['Breakfast']}")
    st.write(f"**Lunch:** {info['Lunch']}")
    st.write(f"**Dinner:** {info['Dinner']}")
    st.write(f"**Drink:** {info['Drink']}")
    st.write(f"**Yoga Pose:** {info['Yoga']}")
    st.write(f"**Health Benefit:** {info['Benefit']}")
    
    yoga_img = Image.open(info['Yoga_Image'])
    st.image(yoga_img, width=250)
    st.markdown("---")

# ---------- SAVE USER DATA ----------
if st.button("Save Record"):
    with open("health.csv","a",newline="") as f:
        csv.writer(f).writerow([name, age, gender, sleep, mood, total, risk_percent, date.today()])
    st.success("Record saved successfully!")

# ---------- PDF REPORT ----------
if st.button("Download PDF"):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"Nutri_Sense Health Report", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(0,8,f"Name: {name}", ln=True)
    pdf.cell(0,8,f"Risk Score: {risk_percent}%", ln=True)
    pdf.multi_cell(0,7,"Recommended Foods: "+", ".join(foods))

    # Add weekly plan table with yoga images
    for day, info in weekly_plan.items():
        pdf.ln(5)
        pdf.set_font("Arial","B",12)
        pdf.cell(0,6,f"{day}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0,5,
            f"Breakfast: {info['Breakfast']}\n"
            f"Lunch: {info['Lunch']}\n"
            f"Dinner: {info['Dinner']}\n"
            f"Drink: {info['Drink']}\n"
            f"Yoga: {info['Yoga']}\n"
            f"Benefit: {info['Benefit']}\n"
        )
        pdf.image(info['Yoga_Image'], x=25, w=150)

    pdf.image(buf, x=25, w=150, type='PNG')
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0,6,
        "Disclaimer: Insights are based on user-reported symptoms. "
        "Not a substitute for professional medical advice. "
        "Recommendations are lifestyle-supportive and follow privacy standards."
    )
    pdf_file = "Nutri_Sense_Report.pdf"
    pdf.output(pdf_file)

    with open(pdf_file,"rb") as f:
        st.download_button("📥 Download Report", f, file_name=pdf_file)

# ---------- QR CODE FOR MOBILE ----------
st.subheader("📱 Open App on Mobile")
app_url = "https://nutri-sense.streamlit.app"  # replace with your deployed Streamlit URL
qr = qrcode.make(app_url)
st.image(qr, width=220)
st.write("Scan the QR code to open Nutri_Sense on mobile")
