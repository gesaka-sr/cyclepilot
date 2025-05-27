import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- Load config.yaml ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- Authenticator setup ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

name, authentication_status, username = authenticator.login("Login")

if authentication_status:
    # Logged-in UI
    st.set_page_config(page_title="CyclePilot", layout="centered")
    st.title("🩸 CyclePilot - Period & Symptom Tracker")

    authenticator.logout("Logout", "sidebar")

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
    mood = st.selectbox("Mood today:", ["Happy", "Neutral", "Irritable", "Sad", "Anxious"])
    cramps = st.radio("Cramps level:", ["None", "Mild", "Moderate", "Severe"])
    headache = st.radio("Headache?", ["No", "Yes"])
    temperature = st.number_input("Body Temperature (°C)", min_value=35.0, max_value=42.0, step=0.1)

    if st.button("💾 Save Entry"):
        new_entry = {
            "User": username,
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

    if st.checkbox("📊 Show Symptom Log"):
        try:
            df = pd.read_csv("cycle_log.csv")
            df_user = df[df["User"] == username]
            st.dataframe(df_user)
        except FileNotFoundError:
            st.warning("No entries saved yet.")

elif authentication_status == False:
    st.error("🚫 Incorrect username or password.")
elif authentication_status == None:
    st.warning("👤 Please enter your username and password.")
