import streamlit as st
import pandas as pd
import csv
from fpdf import FPDF
from datetime import date
import matplotlib.pyplot as plt
import threading


# ---------- PAGE ----------
st.set_page_config(page_title="Nutri_Sense", layout="wide")

# ---------- LANGUAGE ----------
lang = st.sidebar.selectbox("🌐 Language", ["English","Tamil","Hindi"])

title_text = {
    "English":"🌸 Nutri_Sense",
    "Tamil":"🌸 Nutri_Sense — புத்திசாலி ஊட்டச்சத்து உதவி",
    "Hindi":"🌸 Nutri_Sense — स्मार्ट पोषण सहायक"
}

st.title(title_text.get(lang,"Nutri_Sense"))
# ---------- USER DETAILS ----------
with st.expander("👤 Enter Details"):
    name = st.text_input("Name")
    age = st.number_input("Age",10,60)
    gender = st.selectbox("Gender",["Female","Male","Other"])
    sleep = st.slider("Sleeping Hours",3,12,7)
    mood = st.selectbox("Daily Mood",["Happy","Normal","Stress","Sad"])
    rating = st.slider("Rate this App",1,5)
    review = st.text_area("Review")

# ---------- SCORE ----------
score_map = {"None":0,"Mild":1,"Moderate":2,"Severe":3}
st.header("🩺 Select Symptoms")

col1,col2,col3 = st.columns(3)

with col1:
    hair = st.selectbox("Hair fall",list(score_map.keys()))
    eye = st.selectbox("Eye issue",list(score_map.keys()))
    head = st.selectbox("Headache",list(score_map.keys()))
    pigmentation = st.selectbox("Pigmentation",list(score_map.keys()))

with col2:
    heart = st.selectbox("Heart discomfort",list(score_map.keys()))
    leg = st.selectbox("Leg pain",list(score_map.keys()))
    infection = st.selectbox("Infection",list(score_map.keys()))
    kidney = st.selectbox("Kidney issue",list(score_map.keys()))

with col3:
    gall = st.selectbox("Gall bladder",list(score_map.keys()))
    bodypain = st.selectbox("Body pain",list(score_map.keys()))
    periods = st.selectbox("Irregular periods",list(score_map.keys())) if gender=="Female" else "None"

# ---------- RISK ----------
scores = [hair,eye,head,pigmentation,heart,leg,infection,kidney,gall,bodypain,periods]
total = sum(score_map[i] for i in scores)
risk_percent = int((total/33)*100)

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

# ---------- COLOR RISK ----------
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

# ---------- MOTIVATION ----------
st.subheader("💡 Daily Suggestion")

if mood == "Stress":
    st.info("Practice meditation and consume magnesium-rich foods.")
elif mood == "Sad":
    st.info("Include Omega-3 foods and sunlight exposure.")
elif mood == "Happy":
    st.success("Great! Maintain your lifestyle.")

# ---------- PIE CHART ----------
iron = 25 if hair!="None" or periods!="None" else 10
vitA = 25 if eye!="None" else 10
protein = 20 if bodypain!="None" or leg!="None" else 15
omega = 20 if heart!="None" else 10
hydration = 20 if kidney!="None" or infection!="None" else 15

labels = ["Iron","Vitamin A","Protein","Omega-3","Hydration"]
values = [iron,vitA,protein,omega,hydration]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%")
st.pyplot(fig)

# ---------- FOOD ----------
foods=[]
if hair!="None" or periods!="None":
    foods+=["Spinach","Dates","Beetroot","Pomegranate"]
if eye!="None":
    foods+=["Carrot","Pumpkin","Almonds"]
if heart!="None":
    foods+=["Oats","Walnuts","Flax seeds"]
if kidney!="None":
    foods+=["Cucumber","Watermelon","Coconut water"]

st.write(", ".join(foods))

# ---------- SAVE ----------
if st.button("Save Record"):
    with open("health.csv","a",newline="") as f:
        csv.writer(f).writerow([name,age,sleep,mood,total,rating,date.today()])
    st.success("Saved")

# ---------- PDF ----------
if st.button("Download PDF"):
    chart_file="chart.png"
    fig.savefig(chart_file)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"Nutri Sense Health Report",ln=True,align="C")
    pdf.set_font("Arial",size=12)
    pdf.cell(0,8,f"Name: {name or 'Unknown'}",ln=True)
    pdf.cell(0,8,f"Risk Score: {risk_percent}%",ln=True)
    pdf.multi_cell(0,7,"Foods: "+", ".join(foods))
    try:
        pdf.image(chart_file,x=25,w=150)
    except Exception:
        pass

    file_path = "report.pdf"
    pdf.output(file_path)

    with open(file_path, "rb") as f:
        pdf_bytes = f.read()


    st.download_button(label="Download Report", data=pdf_bytes, file_name=file_path, mime="application/pdf")

