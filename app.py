import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="CyclePilot", layout="centered")
st.title("🩸 CyclePilot - Period & Symptom Tracker")

# --- LAST PERIOD DATE INPUT ---
st.header("📅 Cycle Start Info")
last_period = st.date_input("Select your last period start date:", value=datetime.today())
cycle_length = st.slider("Average cycle length (days):", 21, 35, 28)

# Calculate predictions
next_period = last_period + timedelta(days=cycle_length)
ovulation = next_period - timedelta(days=14)
fertile_start = ovulation - timedelta(days=2)
fertile_end = ovulation + timedelta(days=2)

st.success(f"🩸 **Next Period** is estimated on: `{next_period.strftime('%B %d, %Y')}`")
st.info(f"🌸 **Fertile Window**: `{fertile_start.strftime('%B %d')}` → `{fertile_end.strftime('%B %d')}`")
st.warning(f"📍 **Ovulation Day**: `{ovulation.strftime('%B %d')}`")

# --- DAILY SYMPTOM TRACKER ---
st.header("📖 Daily Symptom Tracker")

today = datetime.today().strftime("%Y-%m-%d")
st.subheader(f"🗓️ Entry for {today}")

# Flow & discharge
flow = st.radio("How would you describe your flow today?", ["None", "Light", "Medium", "Heavy", "Very Heavy"])
discharge_color = st.selectbox("Discharge color", ["None", "Clear", "White", "Yellow", "Brown", "Bloody"])
discharge_texture = st.selectbox("Discharge texture", ["None", "Watery", "Sticky", "Creamy", "Egg white", "Clumpy"])

# Mood, symptoms, temperature
mood = st.selectbox("Your mood today", ["Happy", "Neutral", "Irritable", "Sad", "Anxious"])
cramps = st.radio("Cramps?", ["None", "Mild", "Moderate", "Severe"])
headache = st.radio("Headache?", ["No", "Yes"])
temperature = st.number_input("Body Temperature (°C)", min_value=35.0, max_value=42.0, step=0.1)

# Save log
if st.button("💾 Save Entry"):
    new_entry = {
        "Date": today,
        "Flow": flow,
        "Discharge_Color": discharge_color,
        "Discharge_Texture": discharge_texture,
        "Mood": mood,
        "Cramps": cramps,
        "Headache": headache,
        "Temperature": temperature,
    }
    try:
        df = pd.read_csv("cycle_log.csv")
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([new_entry])
    df.to_csv("cycle_log.csv", index=False)
    st.success("✅ Entry saved!")

# View logs and charts
if st.checkbox("📊 Show Symptom Log & Trends"):
    try:
        df = pd.read_csv("cycle_log.csv")
        st.subheader("📈 Logged Entries")
        st.dataframe(df)

        # Prepare data
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values("Date", inplace=True)

        # --- Mood trend ---
        mood_map = {"Happy": 2, "Neutral": 1, "Irritable": -1, "Sad": -2, "Anxious": -3}
        df["Mood_Score"] = df["Mood"].map(mood_map)
        st.write("📉 Mood Trend")
        st.line_chart(df.set_index("Date")["Mood_Score"])

        # --- Flow level ---
        flow_map = {"None": 0, "Light": 1, "Medium": 2, "Heavy": 3, "Very Heavy": 4}
        df["Flow_Score"] = df["Flow"].map(flow_map)
        st.write("💧 Flow Intensity")
        st.bar_chart(df.set_index("Date")["Flow_Score"])

        # --- Temperature trend ---
        st.write("🌡️ Temperature Trend")
        st.line_chart(df.set_index("Date")["Temperature"])

        # --- Cramps trend ---
        cramps_map = {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3}
        df["Cramps_Score"] = df["Cramps"].map(cramps_map)
        st.write("💥 Cramps Intensity")
        st.area_chart(df.set_index("Date")["Cramps_Score"])

    except FileNotFoundError:
        st.warning("⚠️ No data yet. Save your first entry above!")

