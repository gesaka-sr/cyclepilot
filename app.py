import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE SETUP ---
st.set_page_config(page_title="CyclePilot", layout="centered")
st.title("🩸 CyclePilot - Period & Symptom Tracker")

# --- LAST PERIOD DATE INPUT ---
st.header("📅 Cycle Start Info")
last_period = st.date_input("Select your last period start date:", value=datetime.today())
cycle_length = st.slider("Average cycle length (days):", 21, 35, 28)

# Predict next period, ovulation, fertile window
next_period = last_period + timedelta(days=cycle_length)
ovulation = next_period - timedelta(days=14)
fertile_start = ovulation - timedelta(days=2)
fertile_end = ovulation + timedelta(days=2)

st.success(f"🩸 **Next Period** is estimated on: `{next_period.strftime('%B %d, %Y')}`")
st.info(f"🌸 **Fertile Window**: `{fertile_start.strftime('%B %d')}` → `{fertile_end.strftime('%B %d')}`")
st.warning(f"📍 **Ovulation Day**: `{ovulation.strftime('%B %d')}`")

# --- SYMPTOM TRACKER ---
st.header("📖 Daily Symptom Tracker")

today = datetime.today().strftime("%B %d, %Y")
st.subheader(f"🗓️ Entry for {today}")

flow = st.radio("Flow level:", ["None", "Light", "Medium", "Heavy", "Very Heavy"])
discharge_color = st.selectbox("Discharge color", ["None", "Clear", "White", "Yellow", "Brown", "Bloody"])
discharge_texture = st.selectbox("Discharge texture", ["None", "Watery", "Sticky", "Creamy", "Egg white", "Clumpy"])
mood = st.selectbox("Mood today:", ["Happy", "Neutral", "Irritable", "Sad", "]()
