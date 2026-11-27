import streamlit as st
import requests

st.title("🚕 Taxi Fare Predictor")

pickup_datetime = st.text_input(
    "Pickup datetime",
    value="2013-07-06 17:18:00"
)

pickup_longitude = st.number_input(
    "Pickup longitude",
    value=-73.95
)

pickup_latitude = st.number_input(
    "Pickup latitude",
    value=40.78
)

dropoff_longitude = st.number_input(
    "Dropoff longitude",
    value=-73.98
)

dropoff_latitude = st.number_input(
    "Dropoff latitude",
    value=40.76
)

passenger_count = st.number_input(
    "Passenger count",
    min_value=1,
    max_value=8,
    value=1
)

if st.button("Predict fare"):

    url = "http://127.0.0.1:8000/predict"

    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    response = requests.get(url, params=params)

    result = response.json()

    st.success(
        f"Predicted fare: ${result['fare']:.2f}"
    )
