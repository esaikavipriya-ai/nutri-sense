```python
import streamlit as st
from fpdf import FPDF
from datetime import date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Nutri-Sense Health", layout="wide", page_icon="🌿")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 50%, #f1f8e9 100%);
}
.stButton>button { 
    width: 100%; border-radius: 10px; background-color: #2e7d32; 
    color: white; height: 3.5em; font-weight: bold;
}
h1 { color: #1b5e20; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🌿 Nutri-Sense: Lifestyle & Yoga Guide")

# ---------------- GENERAL WEEKLY PLAN ----------------
weekly_data = {
    "Monday": {"Yoga": "Tree Pose", "Food": "Oats & Berries"},
    "Tuesday": {"Yoga": "Cobra Pose", "Food": "Quinoa Salad"},
    "Wednesday": {"Yoga": "Warrior II", "Food": "Lentil Soup"},
    "Thursday": {"Yoga": "Triangle Pose", "Food": "Grilled Tofu"},
    "Friday": {"Yoga": "Child Pose", "Food": "Sweet Potato"},
    "Saturday": {"Yoga": "Plank Pose", "Food": "Greek Yogurt"},
    "Sunday": {"Yoga": "Corpse Pose", "Food": "Veggie Stir-fry"}
}

# ---------------- CONCERN BASED PLAN ----------------
concern_plan = {
    "Hair fall": {"Yoga": "Downward Dog, Camel Pose", "Food": "Spinach, Nuts", "Reason": "Improves scalp circulation"},
    "Eye issue": {"Yoga": "Palming, Trataka", "Food": "Carrot, Papaya", "Reason": "Supports Vitamin A"},
    "Headache": {"Yoga": "Child Pose, Nadi Shodhana", "Food": "Banana, Almonds", "Reason": "Reduces stress"},
    "PCOS": {"Yoga": "Butterfly Pose", "Food": "Flax seeds, Protein diet", "Reason": "Hormonal balance"},
    "Irregular periods": {"Yoga": "Bridge Pose", "Food": "Papaya, Iron foods", "Reason": "Pelvic circulation"},
    "Body pain": {"Yoga": "Cat-Cow Stretch", "Food": "Turmeric milk", "Reason": "Anti-inflammatory"}
}

# ---------------- TAMIL FOOD CHART ----------------
tamil_food = {
    "Hair fall": "Murungai keerai, Karupatti, Ellu urundai",
    "Eye issue": "Carrot poriyal, Pumpkin kootu, Papaya",
    "PCOS": "Ragi kali, Kollu rasam, Sundal",
    "Irregular periods": "Sesame laddu, Beetroot poriyal, Dates",
    "Body pain": "Manathakkali keerai, Turmeric milk",
    "Headache": "Sukku coffee, Banana, Coconut water"
}

tamil_week = {
    "Monday": "Idli + Sambar + Keerai",
    "Tuesday": "Ragi dosa + Groundnut chutney",
    "Wednesday": "Rice + Kollu rasam + Beans poriyal",
    "Thursday": "Kambu koozh + Sundal",
    "Friday": "Vegetable upma + Buttermilk",
    "Saturday": "Dosa + Tomato chutney",
    "Sunday": "Sambar rice + Curd"
}

# ---------------- FORM ----------------
with st.form("health_form"):
    st.subheader("📋 Wellness Profile")

    name = st.text_input("Name*")
    age = st.number_input("Age*", 10, 100, 25)
    gender = st.selectbox("Gender*", ["Select","Male","Female","Other"])
    mood = st.selectbox("Mood*", ["Select","Happy","Stressed","Tired","Sad"])
    sleep = st.slider("Sleep Hours*",0,12,7)

    concerns = list(concern_plan.keys()) + ["General Wellness"]
    selected = st.multiselect("Health Concerns*", concerns)

    submit = st.form_submit_button("🚀 Generate Plan")

# ---------------- OUTPUT ----------------
if submit:
    if not name or gender=="Select" or mood=="Select" or not selected:
        st.error("⚠️ Please fill all required fields")
    else:
        st.success(f"✅ Wellness plan generated for {name}")

        # ---------------- Personalized Plan ----------------
        st.subheader("🎯 Personalized Yoga & Nutrition")
        for c in selected:
            if c in concern_plan:
                st.markdown(f"### 🔎 {c}")
                st.write("🧘 Yoga:", concern_plan[c]["Yoga"])
                st.write("🥗 Food:", concern_plan[c]["Food"])
                st.info(concern_plan[c]["Reason"])

        # ---------------- Tamil Food Guidance ----------------
        st.subheader("🍛 Tamil Traditional Food Guidance")
        for c in selected:
            if c in tamil_food:
                st.write(f"👉 **{c}:** {tamil_food[c]}")

        # ---------------- Tamil Weekly Routine ----------------
        st.subheader("📅 Tamil Weekly Meal Routine")
        for day, food in tamil_week.items():
            st.write(f"**{day}:** {food}")

        # ---------------- General Weekly Routine ----------------
        st.subheader("📅 General Weekly Routine")
        tabs = st.tabs(list(weekly_data.keys()))
        for i,day in enumerate(weekly_data):
            with tabs[i]:
                st.write("🧘 Yoga:", weekly_data[day]["Yoga"])
                st.write("🥗 Food:", weekly_data[day]["Food"])

        # ---------------- PDF REPORT ----------------
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial",'B',16)
        pdf.cell(0,10,"Nutri-Sense Wellness Report",ln=True,align="C")

        pdf.set_font("Arial",'',12)
        pdf.cell(0,10,f"Name: {name}  Age: {age}",ln=True)
        pdf.cell(0,10,f"Concerns: {', '.join(selected)}",ln=True)
        pdf.cell(0,10,f"Date: {date.today()}",ln=True)

        pdf.ln(5)
        pdf.set_font("Arial",'B',13)
        pdf.cell(0,10,"Tamil Food Suggestions",ln=True)

        pdf.set_font("Arial",'',11)
        for c in selected:
            if c in tamil_food:
                pdf.multi_cell(0,8,f"{c}: {tamil_food[c]}")

        pdf_bytes = pdf.output(dest='S').encode('latin-1')

        st.download_button(
            "📥 Download Wellness Report (PDF)",
            pdf_bytes,
            file_name=f"{name}_NutriSense_Report.pdf"
        )

st.caption("⚠️ Educational wellness guidance only. Consult professionals for medical advice.")
```
