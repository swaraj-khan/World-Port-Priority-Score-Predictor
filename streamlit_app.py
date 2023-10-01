import streamlit as st
import pandas as pd
import joblib
import geopandas as gpd

loaded_model = joblib.load('priority_score_model.joblib')
st.image('banner.jpg', width=700)
@st.cache_data
def load_data():
    return pd.read_csv("Port.csv")

data = load_data()

st.title("World Port Index Analysis")

selected_country = st.selectbox("Select a Country", data['COUNTRY'].unique())

update_button = st.button("Update Map")

if update_button:
    filtered_data = data[data['COUNTRY'] == selected_country]

    filtered_gdf = gpd.GeoDataFrame(
        filtered_data,
        geometry=gpd.points_from_xy(filtered_data.LONGITUDE, filtered_data.LATITUDE),
    )

    st.header(f"Ports in {selected_country}")
    st.map(filtered_gdf)

ports_per_country = data['COUNTRY'].value_counts()

N = 10
top_countries = ports_per_country.head(N)

st.header("Raw Data")
st.write(data)
    
def calculate_priority_score(overhd_lim, tide_range):
    overhd_lim_threshold = 1.0
    tide_range_threshold = 3  
    overhd_lim_score = 5 if overhd_lim >= overhd_lim_threshold else (3 if 10 <= overhd_lim < overhd_lim_threshold else 1)
    tide_range_score = 5 if tide_range >= tide_range_threshold else (3 if 5 <= tide_range < tide_range_threshold else 1)

    priority_score = overhd_lim_score + tide_range_score

    return priority_score

st.title("Priority Score Calculator")
overhd_lim = st.number_input("What is the Overhead limit of the cruises on your port?:(0-20)", min_value=0.0, max_value=20.0)
tide_range = st.number_input("What is the Tide Range limit of the cruises on your port?:(0-10)", min_value=0.0, max_value=10.0)

priority_score = calculate_priority_score(overhd_lim, tide_range)

st.write(f"Priority Score: {priority_score}")
