import streamlit as st
import pandas as pd
import csv
from fpdf import FPDF
from datetime import date
import matplotlib.pyplot as plt
import qrcode
from PIL import Image
import requests
from io import BytesIO
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Nutri_Sense | AI Health", layout="wide", page_icon="🥗")

# ---------- PROFESSIONAL THEME (CSS) ----------
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stExpander { border: 1px solid #e0e0e0; border-radius: 10px; background-color: white; }
    h1 { color: #1e3d59; font-family: 'Helvetica Neue', sans-serif; }
    h2, h3 { color: #2e5266; }
    </style>
    """, unsafe_allow_html=True)

# ---------- LANGUAGE ----------
lang = st.sidebar.selectbox("🌐 Language", ["English", "Tamil", "Hindi"])
title_text = {
    "English": "Nutri_Sense AI",
    "Tamil": "Nutri_Sense — ஊட்டச்சத்து உதவி",
    "Hindi": "Nutri_Sense — स्मार्ट पोषण सहायक"
}
st.title(title_text.get(lang, "Nutri_Sense"))

# ---------- USER DETAILS ----------
with st.expander("👤 Step 1: User Profile Details", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name", placeholder="John Doe")
        age = st.number_input("Age", 10, 100, 25)
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    with c2:
        sleep = st.slider("Average Sleep (Hours)", 3, 12, 7)
        mood = st.selectbox("Current Mood", ["Happy", "Normal", "Stress", "Sad"])
        review = st.text_area("Medical History / Notes")

# ---------- SYMPTOMS & SPECIFIC ISSUES ----------
score_map = {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3}
st.header("🩺 Step 2: Health Symptom Analysis")

col1, col2, col3 = st.columns(3)
with col1:
    hair = st.selectbox("Hair fall", list(score_map.keys()))
    eye = st.selectbox("Eye issue", list(score_map.keys()))
    head = st.selectbox("Headache", list(score_map.keys()))
    pigmentation = st.selectbox("Skin Pigmentation", list(score_map.keys()))
with col2:
    heart = st.selectbox("Heart discomfort", list(score_map.keys()))
    leg = st.selectbox("Leg/Joint pain", list(score_map.keys()))
    infection = st.selectbox("Frequent Infection", list(score_map.keys()))
    kidney = st.selectbox("Kidney issue", list(score_map.keys()))
with col3:
    gall = st.selectbox("Gall bladder", list(score_map.keys()))
    bodypain = st.selectbox("General Body pain", list(score_map.keys()))
    periods = st.selectbox("Irregular periods", list(score_map.keys())) if gender=="Female" else "None"
    pcos = st.selectbox("PCOS Symptoms", list(score_map.keys())) if gender=="Female" else "None"

# ---------- CALCULATE RISK ----------
scores = [hair, eye, head, pigmentation, heart, leg, infection, kidney, gall, bodypain, periods, pcos]
total = sum(score_map[i] for i in scores)
risk_percent = int((total / (len(scores) * 3)) * 100)

# ---------- DASHBOARD LAYOUT ----------
st.divider()
res1, res2 = st.columns([1, 1])

with res1:
    st.subheader("📊 Health Risk Status")
    if risk_percent < 30:
        st.success(f"LOW RISK: {risk_percent}%")
        insight = "Maintain current balanced diet and hydration."
    elif risk_percent < 60:
        st.warning(f"MODERATE RISK: {risk_percent}%")
        insight = "Improve nutrition, sleep, and stress management."
    else:
        st.error(f"HIGH RISK: {risk_percent}%")
        insight = "Preventive medical consultation highly recommended."
    
    st.info(f"**AI Insight:** {insight}")
    if mood == "Stress":
        st.write("💡 *Tip: Practice meditation and consume magnesium-rich foods.*")

with res2:
    # Nutrition Pie Chart
    iron = 25 if hair!="None" or periods!="None" or pcos!="None" else 10
    vitA = 25 if eye!="None" else 10
    protein = 20 if bodypain!="None" or leg!="None" else 15
    omega = 20 if heart!="None" else 10
    hydration = 20 if kidney!="None" or infection!="None" else 15

    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie([iron, vitA, protein, omega, hydration], 
           labels=["Iron","Vit A","Protein","Omega-3","Water"], 
           autopct="%1.1f%%", colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
    st.pyplot(fig)

# ---------- WEEKLY PLAN ----------
st.header("📅 Step 3: Personalized Wellness Plan")

# Using URLs to ensure the app works anywhere; replace with local paths if using locally only.
weekly_plan = {
    "Monday": {
        "Breakfast": ["Oats porridge", "Almond milk"],
        "Lunch": ["Grilled chicken salad", "Cucumber juice"],
        "Dinner": ["Steamed fish", "Vegetable soup"],
        "Yoga": "Surya Namaskar",
        "Yoga_Image": "https://images.unsplash.com",
        "Benefits": "Improves digestion and regulates metabolism."
    },
    "Tuesday": {
        "Breakfast": ["Spinach smoothie", "Green tea"],
        "Lunch": ["Quinoa salad", "Coconut water"],
        "Dinner": ["Grilled tofu", "Vegetable soup"],
        "Yoga": "Bhujangasana",
        "Yoga_Image": "https://images.unsplash.com",
        "Benefits": "Strengthens spine and improves flexibility."
    }
}

for day, info in weekly_plan.items():
    with st.expander(f"📌 View Schedule for {day}"):
        tab1, tab2 = st.columns([2, 1])
        with tab1:
            st.write(f"**🍱 Meals:** {', '.join(info['Breakfast'])} (AM) | {', '.join(info['Lunch'])} (Day)")
            st.write(f"**🧘 Yoga:** {info['Yoga']}")
            st.caption(f"**Benefit:** {info['Benefits']}")
        with tab2:
            st.image(info["Yoga_Image"], caption=info["Yoga"], use_container_width=True)

# ---------- REPORT GENERATION ----------
st.divider()
if st.button("🚀 Finalize & Download Medical Report"):
    with st.spinner("Generating Report..."):
        # Save to CSV
        with open("health_logs.csv", "a", newline="") as f:
            csv.writer(f).writerow([name, age, gender, risk_percent, date.today()])
        
        # PDF logic
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial","B",16)
        pdf.cell(0,10, f"Health Report: {name}", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.cell(0,10, f"Date: {date.today()} | Risk Score: {risk_percent}%", ln=True)
        pdf.ln(10)
        pdf.multi_cell(0,10, f"AI Recommendation: {insight}")
        
        pdf_file = "NutriSense_Report.pdf"
        pdf.output(pdf_file)
        
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Click Here to Download PDF", f, file_name=pdf_file)

# ---------- MOBILE QR ----------
st.sidebar.markdown("---")
st.sidebar.subheader("📱 Mobile Access")
qr_img = qrcode.make("https://your-app-link.streamlit.app")
st.sidebar.image(qr_img.get_image(), caption="Scan to sync with phone")
