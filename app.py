# app.py

import streamlit as st
from datetime import datetime
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from modules.role_utils import get_user_role
from modules.sexual_health import sexual_health_ui
from modules.teleconsult import teleconsult_ui
from modules.symptom_correlation import plus_features_ui

# --- Load config ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- TEMP AUTH SKIPPED FOR TESTING ---
username = "test_user"  # Simulated user
user_role = get_user_role(username)  # free, lite, plus, admin

# --- PAGE SETUP ---
st.set_page_config(page_title="CyclePilot", layout="centered")
st.title("🩸 CyclePilot - Every Woman, Every Stage")

# --- NAVIGATION ---
pages = {
    "🩸 Period Tracker": "period",
    "🛏️ Sexual Health Log": "sexual",
    "🧬 Symptom Insights": "insights",
    "🩺 Teleconsultation": "consult"
}
selection = st.sidebar.radio("📂 Navigate", list(pages.keys()))
st.sidebar.success(f"Logged in as: `{username}` ({user_role})")

# --- PAGE ROUTING ---
if pages[selection] == "period":
    st.subheader("📅 Period Tracker")
    from datetime import timedelta

    last_period = st.date_input("Last period start date:", value=datetime.today())
    cycle_length = st.slider("Cycle length (days):", 21, 35, 28)

    next_period = last_period + timedelta(days=cycle_length)
    ovulation = next_period - timedelta(days=14)
    fertile_start = ovulation - timedelta(days=2)
    fertile_end = ovulation + timedelta(days=2)

    st.success(f"🩸 Next period: `{next_period.strftime('%B %d, %Y')}`")
    st.warning(f"📍 Ovulation: `{ovulation.strftime('%B %d')}`")
    st.info(f"🌸 Fertile Window: `{fertile_start.strftime('%b %d')}` – `{fertile_end.strftime('%b %d')}`")

elif pages[selection] == "sexual":
    sexual_health_ui(username)

elif pages[selection] == "insights":
    if user_role in ["plus", "admin"]:
        plus_features_ui(username)
    else:
        st.error("🔒 Upgrade to Plus to unlock Symptom Insights.")

elif pages[selection] == "consult":
    if user_role in ["lite", "plus", "admin"]:
        teleconsult_ui(username)
    else:
        st.warning("🔒 Available in Lite and Plus plans. Upgrade to access teleconsultation.")

