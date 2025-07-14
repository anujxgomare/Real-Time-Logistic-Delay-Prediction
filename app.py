import streamlit as st
import pandas as pd
import joblib

# Load the trained pipeline
model = joblib.load("delay_classifier_pipeline.pkl")

# UI config
st.set_page_config(page_title="Delivery Delay Predictor", layout="centered")
st.title("🚚 Delivery Delay Prediction")
st.markdown("Enter delivery details below to predict if it will be delayed.")

# Form input
with st.form("prediction_form"):
    order_id = st.text_input("Order ID", "ORD001")
    vendor = st.text_input("Vendor", "VendorA")
    vehicle_type = st.selectbox("Vehicle Type", ["Truck", "Van", "Bike"])
    origin_city = st.text_input("Origin City", "CityA")
    destination_city = st.text_input("Destination City", "CityB")
    shipment_date = st.date_input("Shipment Date")
    planned_delivery = st.text_input("Planned Delivery (YYYY-MM-DD HH:MM:SS)")
    actual_delivery = st.text_input("Actual Delivery (YYYY-MM-DD HH:MM:SS)")
    distance_km = st.number_input("Distance (in km)", min_value=0.0, step=0.1)
    weather_condition = st.selectbox("Weather Condition", ["Clear", "Rain", "Storm", "Fog"])
    traffic_condition = st.selectbox("Traffic Condition", ["Light", "Moderate", "Heavy"])
    vendor_delay_score = st.number_input("Vendor Delay Score", 0.0, 1.0, 0.5, step=0.01)
    hour_of_day = st.slider("Hour of Day", 0, 23, 12)
    day_of_week = st.selectbox("Day of Week", list(range(0, 7)))
    holiday_flag = st.selectbox("Is Holiday?", [0, 1])
    pickup_delay_minutes = st.number_input("Pickup Delay (minutes)", min_value=0, step=1)
    driver_rating = st.slider("Driver Rating", 1.0, 5.0, 4.5, step=0.1)
    vehicle_age_years = st.slider("Vehicle Age (years)", 0, 20, 3)
    order_weight_kg = st.number_input("Order Weight (kg)", min_value=0.0, step=0.1)
    num_packages = st.number_input("Number of Packages", min_value=1, step=1)
    order_priority = st.selectbox("Order Priority", ["Standard", "High"])
    road_type = st.selectbox("Road Type", ["Urban", "Rural"])

    submitted = st.form_submit_button("Predict")


# Prediction
if submitted:
    input_data = pd.DataFrame([{
        "order_id": "ORD001",
        "vendor": "VendorA",
        "vehicle_type": "Truck",
        "origin_city": "CityA",
        "destination_city": "CityB",
        "shipment_date": "2025-07-01",
        "planned_delivery": "2025-07-01 12:00:00",
        "actual_delivery": "2025-07-01 12:00:00",
        "distance_km": distance_km,
        "weather_condition": weather_condition,
        "traffic_condition": traffic_condition,
        "vendor_delay_score": 0.5,
        "hour_of_day": 12,
        "day_of_week": 1,
        "holiday_flag": 0,
        "pickup_delay_minutes": pickup_delay_minutes,
        "driver_rating": driver_rating,
        "vehicle_age_years": 3,
        "order_weight_kg": 20.0,
        "num_packages": 3,
        "order_priority": "Standard",
        "road_type": "Urban"
    }])

    # Prediction
    prediction = model.predict(input_data)[0]
    result = "🟢 On-Time Delivery" if prediction == 0 else "🔴 Delayed Delivery"

    st.success(f"### Prediction: {result}")
