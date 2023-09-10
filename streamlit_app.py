import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    return pd.read_csv("world_Port_Index.csv")

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

st.header(f"Top {N} Countries with the Most Ports")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_countries.index, y=top_countries.values, ax=ax)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Number of Ports", fontsize=12)
plt.tight_layout()

for i, v in enumerate(top_countries.values):
    ax.text(i, v, str(v), ha="center", va="bottom", fontsize=10)

st.pyplot(fig)

st.header("Raw Data")
st.write(data)
