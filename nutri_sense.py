import streamlit as st
from fpdf import FPDF
import datetime
import pandas as pd
import os
import pytz
import plotly.express as px

# 1. ---------------- RESTRUCTURED DATA ----------------
# Each concern now has its own unique 'Menu' items
concern_data = {
    "Hair Fall": {"Morning": "Karisalanganni Tea", "Breakfast": "Millet Porridge", "Yoga": "Sarvangasana"},
    "Diabetes": {"Morning": "Vendhayam Water", "Breakfast": "Samba Wheat Upma", "Yoga": "Mandukasana"},
    "Eye Strain": {"Morning": "Ponnanganni Juice", "Breakfast": "Carrot Idli", "Yoga": "Trataka"},
    "Acidity": {"Morning": "Inji Honey Water", "Breakfast": "Pazhaya Sadham (Fermented Rice)", "Yoga": "Vajrasana"},
    "Thyroid": {"Morning": "Kothamalli Water", "Breakfast": "Barley Upma", "Yoga": "Ustrasana"},
    "PCOD/PCOS": {"Morning": "Ulunthu Kanji", "Breakfast": "Ragi Dosai", "Yoga": "Baddha Konasana"},
    "Joint Pain": {"Morning": "Mudakathan Soup", "Breakfast": "Garlic Rice", "Yoga": "Tadasana"},
    "High BP": {"Morning": "Poondu Water", "Breakfast": "Banana Flower Stir-fry", "Yoga": "Shavasana"}
}

# 2. ---------------- LOGGING FUNCTION ----------------
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
        selected_issues = st.multiselect("Select Primary Concerns", list(concern_data.keys()))
        submit = st.form_submit_button("Generate Menu & Analytics")

# 4. ---------------- DASHBOARD ----------------
if submit and name and selected_issues:
    st.session_state.submitted = True
    bmi = round(weight / ((height/100)**2), 1)
    st.session_state.user_info = {"name": name, "age": age, "gender": gender, "bmi": bmi, "issues": selected_issues}

if st.session_state.submitted:
    u = st.session_state.user_info
    tab1, tab2, tab3 = st.tabs(["🍽️ Personalized Menu", "📊 Health Analytics", "📥 Download Report"])

    with tab1:
        st.subheader(f"Customized Menu for {u['name']}")
        # Each concern now gets a separate line in the menu
        for issue in u['issues']:
            with st.expander(f"📌 Menu for {issue}", expanded=True):
                st.write(f"🍵 **Early Morning (6-7 AM):** {concern_data[issue]['Morning']}")
                st.write(f"🍛 **Breakfast (8-9 AM):** {concern_data[issue]['Breakfast']}")
                st.write(f"🧘 **Yoga Practice:** {concern_data[issue]['Yoga']}")

    with tab2:
        log_path = r"C:\Users\LENOVO\Documents\qwings\Science Expo\health.csv"
        if os.path.exists(log_path):
            df_logs = pd.read_csv(log_path)
            # Logic for Pie Chart
            all_c = df_logs["Concerns"].str.split(", ").explode().value_counts().reset_index()
            all_c.columns = ["Issue", "Frequency"]
            fig = px.pie(all_c, values="Frequency", names="Issue", title="Popular Health Concerns")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data found. Please download a report first to see analytics.")

    with tab3:
        # Standard PDF download button logic
        if st.download_button("📥 Download PDF Report", "dummy data", file_name="Report.pdf"):
            log_download(u['name'], u['age'], u['gender'], u['bmi'], u['issues'])
            st.success("Downloaded and Logged!")
