import pandas as pd
import streamlit as st
import folium

# Load the data
data = pd.read_csv("world_Port_Index.csv")

# Create a Streamlit app
st.title("World Port Index Visualization")

# Sidebar
st.sidebar.title("Options")

# Display unique countries
unique_countries = data['COUNTRY'].unique()
selected_country = st.sidebar.selectbox("Select a Country", unique_countries)

# Filter the data for the selected country
filtered_data = data[data['COUNTRY'] == selected_country]

# Display basic information about the selected country
st.sidebar.header("Country Information")
st.sidebar.write(f"Country: {selected_country}")
st.sidebar.write(f"Number of Ports: {len(filtered_data)}")

# Create a map centered at the mean latitude and longitude of the filtered data
m = folium.Map(location=[filtered_data['LATITUDE'].mean(), filtered_data['LONGITUDE'].mean()], zoom_start=6)

# Add markers for each port using a loop
for idx, row in filtered_data.iterrows():
    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        popup=row['PORT_NAME']
    ).add_to(m)

# Display the map
st.write(f"Ports in {selected_country}:")
st.write(m._repr_html_(), unsafe_allow_html=True)
