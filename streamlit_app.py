import pandas as pd
import streamlit as st
import folium
import joblib

data = pd.read_csv("world_Port_Index.csv")

model = joblib.load('trained_model.pkl')

st.title("World Port Index Visualization")

st.sidebar.title("Options")

unique_countries = data['COUNTRY'].unique()
selected_country = st.sidebar.selectbox("Select a Country", unique_countries)

filtered_data = data[data['COUNTRY'] == selected_country]

st.sidebar.header("Country Information")
st.sidebar.write(f"Country: {selected_country}")
st.sidebar.write(f"Number of Ports: {len(filtered_data)}")

m = folium.Map(location=[filtered_data['LATITUDE'].mean(), filtered_data['LONGITUDE'].mean()], zoom_start=6)

for idx, row in filtered_data.iterrows():
    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        popup=row['PORT_NAME']
    ).add_to(m)

st.write(f"Ports in {selected_country}:")
st.components.v1.html(m._repr_html_(), width=700, height=700, scrolling=True)
