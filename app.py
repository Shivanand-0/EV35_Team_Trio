
import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Accident Severity Predictor", page_icon="🚗", layout="wide")

# Ensure you have uploaded 'model.pkl' to your Colab session!
try:
    model = pickle.load(open('EV35_Team_Trio_Model (1).pkl', 'rb'))
except FileNotFoundError:
    st.error("Please upload EV35_Team_Trio_Model (1).pkl to the Colab files section on the left!")
    st.stop()

st.title("🚦 Road Accident Severity Predictor")
st.markdown("This application predicts the severity of a road accident based on various conditions.")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        longitude = st.number_input("Longitude", value=-1.5)
        day_of_week = st.number_input("Day of Week (1-7)", min_value=1, max_value=7, value=6)
        number_of_vehicles = st.number_input("Number of Vehicles", min_value=1, value=2)
        did_police_officer_attend = st.number_input("Police Attended? (1=Yes, 2=No)", value=1)
        sex_of_driver = st.number_input("Sex of Driver (1=Male, 2=Female)", value=1)
        pedestrian_road_maintenance = st.number_input("Pedestrian/Maintenance Worker", value=0)
        
    with col2:
        first_road_class = st.number_input("First Road Class", value=3)
        second_road_class = st.number_input("Second Road Class", value=-1)
        second_road_number = st.number_input("Second Road Number", value=0)
        junction_detail = st.number_input("Junction Detail", value=0)
        junction_control = st.number_input("Junction Control", value=-1)
        junction_location = st.number_input("Junction Location", value=0)
        pedestrian_crossing = st.number_input("Pedestrian Crossing", value=0)

    with col3:
        weather_conditions = st.number_input("Weather Conditions (e.g. 1=Fine, 2=Rain)", value=1)
        road_surface_conditions = st.number_input("Road Surface Conditions", value=1)
        special_conditions_at_site = st.number_input("Special Conditions at Site", value=0)
        carriageway_hazards = st.number_input("Carriageway Hazards", value=0)
        vehicle_location_restricted_lane = st.number_input("Restricted Lane", value=0)
        first_point_of_impact = st.number_input("First Point of Impact", value=1)
        vehicle_left_hand_drive = st.number_input("Left Hand Drive (1=No, 2=Yes)", value=1)

    submit_button = st.form_submit_button(label="Predict Severity")

if submit_button:
    input_data = pd.DataFrame([[
        longitude, number_of_vehicles, first_road_class, junction_detail, junction_control,
        second_road_class, second_road_number, pedestrian_crossing, weather_conditions,
        road_surface_conditions, special_conditions_at_site, carriageway_hazards,
        did_police_officer_attend, pedestrian_road_maintenance, vehicle_location_restricted_lane,
        junction_location, first_point_of_impact, vehicle_left_hand_drive, sex_of_driver, day_of_week
    ]], columns=[
        'longitude', 'number_of_vehicles', 'first_road_class', 'junction_detail', 'junction_control',
        'second_road_class', 'second_road_number', 'pedestrian_crossing', 'weather_conditions',
        'road_surface_conditions', 'special_conditions_at_site', 'carriageway_hazards',
        'did_police_officer_attend_scene_of_accident', 'pedestrian_road_maintenance_worker',
        'vehicle_location_restricted_lane', 'junction_location', 'first_point_of_impact',
        'vehicle_left_hand_drive', 'sex_of_driver', 'day_of_week'
    ])

    prediction = model.predict(input_data)[0]
    
    st.divider()
    if prediction == 1:
        st.error("🚨 Predicted Severity: Fatal (Class 1)")
    elif prediction == 2:
        st.warning("⚠️ Predicted Severity: Serious (Class 2)")
    else:
        st.success("🚗 Predicted Severity: Slight (Class 3)")