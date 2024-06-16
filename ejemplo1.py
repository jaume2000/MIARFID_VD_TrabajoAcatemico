import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Cargar los datos
shapefile_path = './mnt/data/ne_110m_admin_0_countries.shp'
csv_path = './mnt/data/world_pop.csv'

@st.cache_data
def load_data():
    gdf = gpd.read_file(shapefile_path)
    df = pd.read_csv(csv_path, skiprows=4)
    return gdf, df

gdf, df = load_data()

# Unir los datos del CSV con el shapefile
merged = gdf.set_index('ADM0_A3').join(df.set_index('Country Code'), how='inner')

# Crear el mapa de coropletas
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged.plot(column='2022', ax=ax, legend=True,
            legend_kwds={'label': "Población por país",
                         'orientation': "horizontal"})
plt.title('Mapa de Coropletas de la Población Mundial')
plt.axis('off')

# Mostrar el mapa en Streamlit
st.title("Mapa de Coropletas de la Población Mundial")
st.pyplot(fig)
