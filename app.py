import folium
import streamlit as st
from streamlit_folium import st_folium
import requests
import os

# Some constants
pickup_longitude_mean = -73.975777
pickup_latitude_mean = 40.750939
dropoff_longitude_mean = -73.974643
dropoff_latitude_mean = 40.751211
pickup_longitude_min = -74.244137
pickup_latitude_min = 40.502598
dropoff_longitude_min = -74.24945
dropoff_latitude_min = 40.501408
pickup_longitude_max = -73.70258
pickup_latitude_max = 40.89347
dropoff_longitude_max = -73.700838
dropoff_latitude_max = 40.898937

# User input
pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude = (
    None,
    None,
    None,
    None,
)

st.set_page_config(page_title="Taxi Fare Predictor", page_icon="🚕", layout="centered")
st.title("🚕 Taxi Fare Predictor")
pickup_datetime = st.datetime_input("Pickup datetime", value="2013-07-06 17:18:00")
passenger_count = st.slider("Passenger count", value=1, min_value=1, max_value=6)

left_col, right_col = st.columns(2)

with left_col:
    with st.container(horizontal_alignment="center"):
        map_data_pickup = None
        st.title("Pickup location", text_alignment="right")

        m_pickup = folium.Map(
            location=[pickup_latitude_mean, pickup_longitude_mean],
            zoom_start=11,
        )
        m_pickup.add_child(folium.LatLngPopup())
        map_data_pickup = st_folium(m_pickup, height=300, use_container_width=True)

        if map_data_pickup and map_data_pickup.get("last_clicked"):
            pickup_latitude = map_data_pickup["last_clicked"]["lat"]
            pickup_longitude = map_data_pickup["last_clicked"]["lng"]
            st.success(
                f"Selected: lat = {pickup_latitude:.6f}, lon = {pickup_longitude:.6f}"
            )

with right_col:
    with st.container(horizontal_alignment="center"):
        st.title("Dropoff location")

        m_dropoff = folium.Map(
            location=[dropoff_latitude_mean, dropoff_longitude_mean], zoom_start=11
        )
        m_dropoff.add_child(folium.LatLngPopup())
        map_data_dropoff = st_folium(m_dropoff, height=300, use_container_width=True)

        if map_data_dropoff and map_data_dropoff.get("last_clicked"):
            dropoff_latitude = map_data_dropoff["last_clicked"]["lat"]
            dropoff_longitude = map_data_dropoff["last_clicked"]["lng"]
            st.success(
                f"Selected: lat = {dropoff_latitude:.6f}, lon = {dropoff_longitude:.6f}"
            )

if pickup_latitude and dropoff_latitude:
    url = f"{os.environ["HOSTNAME"]}/predict"

    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count,
    }

    response = requests.get(url, params=params)

    result = response.json()

    st.success(f"Predicted fare: ${result['fare']:.2f}")
