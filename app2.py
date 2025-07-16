# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 16:44:46 2025

@author: Shruti
"""


import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# Set Streamlit page config
st.set_page_config(page_title="Solar Power Dashboard ☀️", layout="wide")

# Load model
model = joblib.load("Gradient_Boosting_Regressor_best_model.pkl")  

# Dark mode toggle
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=True)
if dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
        .stSlider > div > div {
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# Sidebar - Input section
st.sidebar.title("🛠 Adjust Inputs")

def user_inputs():
    Temperature = st.sidebar.slider("Temperature (°C)", 0.0, 50.0, 25.0)
    Humidity = st.sidebar.slider("Humidity (%)", 0, 100, 50)
    Wind_Speed = st.sidebar.slider("Wind Speed (m/s)", 0.0, 30.0, 5.0)
    Solar_Radiation = st.sidebar.slider("Solar Radiation (W/m²)", 0.0, 1500.0, 800.0)
    Cloud_Cover = st.sidebar.slider("Cloud Cover (%)", 0.0, 100.0, 20.0)

    data = {
        'Temperature': Temperature,
        'Humidity': Humidity,
        'Wind_Speed': Wind_Speed,
        'Solar_Radiation': Solar_Radiation,
        'Cloud_Cover': Cloud_Cover
    }
    return pd.DataFrame([data])

input_df = user_inputs()

# Main content
st.markdown("## 🌞 Solar Power Prediction Dashboard")
st.markdown("Enter current environmental conditions to predict solar power output.")

# Predict button
if st.button("⚡ Predict Now"):
    prediction = model.predict(input_df)[0]

    # Result Banner
    st.markdown(f"""
        <div style="background-color:#ff4b4b;padding:10px;border-radius:10px;text-align:center;font-size:22px;color:white;">
            🔋 Predicted Solar Power Output: <strong>{prediction:.2f} kWh</strong>
        </div>
    """, unsafe_allow_html=True)

    # Animated Gauge Meter
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prediction,
        title={'text': "Solar Output (kWh)"},
        gauge={
            'axis': {'range': [0, 1000]},
            'bar': {'color': "#ff4b4b"},
            'steps': [
                {'range': [0, 300], 'color': "lightgreen"},
                {'range': [300, 700], 'color': "yellow"},
                {'range': [700, 1000], 'color': "red"},
            ]
        }
    ))
    st.plotly_chart(gauge_fig, use_container_width=True)

    # Info Cards
    st.subheader("📋 Current Conditions Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡 Temperature", f"{input_df['Temperature'][0]} °C")
    col2.metric("💧 Humidity", f"{input_df['Humidity'][0]} %")
    col3.metric("💨 Wind Speed", f"{input_df['Wind_Speed'][0]} m/s")

    col4, col5 = st.columns(2)
    col4.metric("☀️ Solar Radiation", f"{input_df['Solar_Radiation'][0]} W/m²")
    col5.metric("☁️ Cloud Cover", f"{input_df['Cloud_Cover'][0]} %")

    # Recommendation Section
    st.markdown("---")
    st.markdown("### 🔎 Solar Output Insight")
    if prediction < 300:
        st.warning("⚠️ Low solar generation. Consider reducing load or using backup.")
    elif prediction < 700:
        st.info("☀️ Moderate generation. Ideal for partial daytime use.")
    else:
        st.success("✅ High solar generation! Great time to operate high-energy appliances.")
