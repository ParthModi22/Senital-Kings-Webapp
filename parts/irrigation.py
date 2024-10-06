import streamlit as st
import requests
import json
import math
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import leafmap.foliumap as leafmap
import requests
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
from folium.plugins import Draw
import folium
import google.generativeai as genai
import os


def AI(crop,lat,long,stage,language):
    genai.configure(api_key="AIzaSyDcukeocIFxr-sYS3x2uJgfszJ6el77Hqo")

# Load the generative model and generate content
    model = genai.GenerativeModel("gemini-1.5-flash")
    # crop = 'tomato'
    # lat = 39
    # long = -107
    # stage = "initial"

    response = model.generate_content(f"explain about {crop} and its water needs in following latitude and longitude: {lat:.2f} and {long:.2f} at {stage} growth stage and give output in a single para in {language} ")  
    # response = model.generate_content(f"quantum computer ")  

    # Print the generated content
    # print()
    s = response.text

    return s


# Function to create an interactive map for selecting location
def interactive_location_selection_map():
    #st.subheader("Irrigation Managaement")
    st.write("""Efficient irrigation is critical for optimizing water use in agriculture. By using Evapotranspiration (ET) values, farmers can determine the precise amount of water required by their crops based on the actual rate of water loss from the soil and plants. This is a data-driven approach.  Helps in managing irrigation schedules more effectively, reducing water wastage, and ensuring crops receive just the right amount of moisture, which leads to healthier growth and improved yields.

How to use 
1)	Select current location or any location on map
2)	Select – crop type and growth stage of the crop
3)	Water required for the desired crop will be displayed on the screen (by calculating ET value)
""")
    # Default location (center of the map)
    # initial_lat, initial_lon = 38.7946, -106.5348;;

    # Create a folium map centered on the default location
   
    m_draw = leafmap.Map(center=[38.7946, -106.5348], zoom=15, draw_control = False)




    m_draw.add_basemap("SATELLITE")
    # m_draw.add_basemap("GOOGLE_HYBRID")
    # m_draw.add_basemap("GOOGLE_SATELLITE_HYBRID'")
    m_draw.add_child(folium.LatLngPopup()) # shows that lat and long in folium
    # Draw(export=True).add_to(m_draw)




    # map_data = st_folium(m_draw, height="400px", width="800px", key="draw_map")
    map_data = st_folium(m_draw, height=400, width=1000,key="draw_map")


    # st.markdown(
    #     """
    #     <style>
    #     .main .block-container {
    #         padding: 0;
    #         margin: 0;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    #     )



    # If the user clicked on the map, retrieve the coordinates
    if map_data and map_data['last_clicked']:
        latitude = map_data['last_clicked']['lat']
        longitude = map_data['last_clicked']['lng']
        st.write(f"**Selected Location**: Latitude = {latitude:.4f}, Longitude = {longitude:.4f}")

        # Store selected coordinates in session state
        st.session_state['latitude'] = latitude
        st.session_state['longitude'] = longitude
def maps_visualization():
    st.title("Irrigation Management")

    # Unified Map Selector: Radio button to switch between different map views
    # map_type = st.radio(
    #     "Select Map View",
    #     ("Interactive Map for Location Selection")
    # )

    # Render the appropriate map view based on user selection
    # if map_type == "Interactive Map for Location Selection":
    interactive_location_selection_map()


def irrigation_monitoring():
    st.subheader("Irrigation Requirement Monitoring")
    st.write("This section provides insights on the irrigation requirements for different crops based on their growth stage and location.")

    # Check if coordinates are already selected in session state from the map section
    if 'latitude' in st.session_state and 'longitude' in st.session_state and st.session_state['latitude'] is not None:
        latitude = st.session_state['latitude']
        longitude = st.session_state['longitude']
        # if latitude:
        st.write(f"**Selected Location**: Latitude = {latitude:.4f}, Longitude = {longitude:.4f}")
    else:
        st.warning("Please select your farm location from the 'Farm Maps' section.")
        return
    # Load Kc values from the uploaded JSON file
    with open('utlis/kc_values.json', 'r') as f:
        kc_values = json.load(f)

# NASA POWER API fetch function
    def fetch_nasa_power_data(latitude, longitude, date):
        base_url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PS,ALLSKY_SFC_SW_DWN,T2M_MAX,T2M_MIN,WS2M,RH2M&community=AG&longitude={longitude}&latitude={latitude}&start={date}&end={date}&format=JSON"
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()['properties']['parameter']
            return data
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            return None

# Function to calculate ET₀ (Reference Evapotranspiration)
    def calculate_et0(data, date):
        gamma = 0.665e-3 * data['PS'][date]  # Psychrometric constant (kPa/°C)
        Rn = data['ALLSKY_SFC_SW_DWN'][date] * 0.0864  # Convert W/m² to MJ/m²/day

        T_max = data['T2M_MAX'][date]  # Max temperature (°C)
        T_min = data['T2M_MIN'][date]  # Min temperature (°C)
        T_mean = (T_max + T_min) / 2  # Mean temperature

        U2 = data['WS2M'][date]  # Wind speed at 2m (m/s)
        RH_mean = data['RH2M'][date]  # Mean relative humidity (%)

    # Calculate saturation vapor pressure (kPa)
        e_s = 0.6108 * (math.exp((17.27 * T_max) / (T_max + 237.3)) + math.exp((17.27 * T_min) / (T_min + 237.3))) / 2

    # Actual vapor pressure (kPa)
        e_a = e_s * (RH_mean / 100)

    # Slope of vapor pressure curve (kPa/°C)
        delta = (4098 * (0.6108 * math.exp((17.27 * T_mean) / (T_mean + 237.3)))) / ((T_mean + 237.3) ** 2)

    # Penman-Monteith equation for ET₀
        ET0 = (0.408 * delta * (Rn - 0) + gamma * (900 / (T_mean + 273)) * U2 * (e_s - e_a)) / (delta + gamma * (1 + 0.34 * U2))
        return ET0

# Function to calculate water needed based on ET₀ and crop coefficient
    def calculate_water_needed(et0, kc):
        return max(0, kc * et0)
    # Fetch current date and format it for NASA POWER API
    current_date = datetime.now()
    five_days_before = current_date - timedelta(days=5)
    date = five_days_before.strftime("%Y%m%d")  # Format for NASA POWER API

# Fetch NASA POWER weather data
    data = fetch_nasa_power_data(latitude, longitude, date)

    # Crop selection dropdown based on kc_values.json
    if data:

        crop = st.selectbox("Select Crop Type", list(kc_values.keys()))
    # Growth stage selection dropdown based on the selected crop

        languages_list = ['English','Hindi','Urdu','Marathi','Tamil','Telugu']

        growth_stage = st.selectbox("Select Growth Stage", kc_values[crop].keys())
        language = st.selectbox("Select any language for Insight", languages_list)
    # Get the Kc value for the selected crop and growth stage

        kc = kc_values[crop][growth_stage]
    # Calculate ET₀ using the fetched weather data

        et0 = calculate_et0(data, date)
    # Calculate water needed based on ET₀ and Kc

        water_needed = calculate_water_needed(et0, kc)
    # Display results
        st.write(f"Growth Stage: {growth_stage}")
        st.write(f"Crop: {crop}")
        st.write(f"Crop Coefficient (Kc): {kc}")
        st.write(f"Reference Evapotranspiration (ET₀): {et0:.2f} mm/day")
        if water_needed <= 0:
            st.success("The crop is sufficiently irrigated. No need for additional water.")
        else:
            st.warning(f"Amount of water needed: {water_needed:.2f} mm/day")

        if 'latitude' in st.session_state:
            s = AI(crop,st.session_state['latitude'],st.session_state['longitude'],growth_stage,language)
            # st.write(s)

        with st.container():
                st.markdown("### **Insight**")
                st.write(s)
                st.markdown("<hr>", unsafe_allow_html=True)
        
    else:
        st.warning("Unable to fetch weather data. Please try again.")
    





# Retrieve the API key from the environment variable "GOOGLE_API_KEY"

# export GOOGLE_API_KEY="AIzaSyDcukeocIFxr-sYS3x2uJgfszJ6el77Hqo"
# write above in terminal


