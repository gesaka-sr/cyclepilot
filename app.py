# Save this as app.py

import streamlit as st
import pandas as pd
import numpy as np

# --- Access Control ---
PASSWORD = "cyclefriends"  # Change this password and share privately

def check_password():
    st.title("🔒 CyclePilot Access")
    password = st.text_input("Enter access password:", type="password")
    if password != PASSWORD:
        st.warning("Incorrect password or not entered yet.")
        st.stop()

check_password()

# --- App Starts ---
st.title("🩸 CyclePilot Period Tracker (LCP v0.1 & v0.2)")
st.markdown("Welcome! This is a wellness-focused cycle predictor demo. Input your last two cycle lengths to estimate your next one.")

# Input form
st.header("📥 Input Your Recent Cycle Data")
cycle_1 = st.number_input("Cycle Length 1 (most recent)", min_value=15, max_value=45)
cycle_2 = st.number_input("Cycle Length 2 (prior to that)", min_value=15, max_value=45)

if st.button("Predict Next Cycle"):
    st.subheader("📊 Predictions")

    # LCP v0.1: Last cycle predictor
    prediction_v1 = cycle_1
    st.write(f"**LCP v0.1** (Last Cycle): `{prediction_v1} days`")

    # LCP v0.2: Rolling average of last 2
    prediction_v2 = round((cycle_1 + cycle_2) / 2, 2)
    st.write(f"**LCP v0.2** (2-Cycle Avg): `{prediction_v2} days`")

st.markdown("---")
st.info("🚨 This app is for personal wellness use only — not for diagnosis or clinical decision-making.")
