import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import streamlit_folium as sf

# Cargar el DataFrame una sola vez al inicio
@st.cache_data
def load_data():
    return {
        'pop': pd.read_csv('./data/world_pop.csv', skiprows=4).rename(columns={'Country Code': 'code'}),
        'cpi': pd.read_csv('./data/world_cpi.csv', skiprows=4).rename(columns={'Country Code': 'code'}),
        'income': pd.read_csv('./data/world_income.csv', skiprows=4).rename(columns={'Country Code': 'code'}),
        'pib': pd.read_csv('./data/world_pib.csv', skiprows=4).rename(columns={'Country Code': 'code'})
    }

# Cargar los datos geoespaciales
@st.cache_data
def load_shapefile():
    return gpd.read_file('./data/ne_110m_admin_0_countries.shp')

# Cargar los datos
data = load_data()
shapefile = load_shapefile()

def page1():
    st.title("Datos utilizados:")
    

    # Mostrar el gráfico en Streamlit
    with st.expander("Población", expanded=True):
        world_population = data['pop'][data['pop']['code'] == 'WLD']
        world_population.set_index('code', inplace=True)
        world_population = world_population.loc[:, '1960':'2023'].T

        st.header("Tabla de datos de la población mundial")
        st.write(data['pop'])
        st.header("Evolución de la población mundial")
        st.line_chart(world_population)

    
    with st.expander("Índice de Precios al Consumidor (CPI)"):
        world_cpi = data['cpi']
        world_cpi.set_index('code', inplace=True)
        world_cpi = world_cpi.loc[:, '1960':'2023'].T
        world_cpi = world_cpi.mean(axis=1)

        st.header("Tabla de datos del Índice de Precios al Consumidor (CPI)")
        st.write(data['cpi'])
        st.header("Evolución del Índice de Precios al Consumidor (CPI)")
        st.line_chart(world_cpi)
    
    with st.expander("Ingreso per cápita"):
        world_income = data['income'][data['income']['code'] == 'WLD']
        world_income.set_index('code', inplace=True)
        world_income = world_income.loc[:, '1960':'2023'].T

        st.header("Tabla de datos del Ingreso Nacional Bruto per cápita")
        st.write(data['income'])
        st.header("Evolución del Ingreso Nacional Bruto per cápita")
        st.line_chart(world_income)
    
    with st.expander("Producto Interno Bruto (PIB)"):
        world_pib = data['pib'][data['pib']['code'] == 'WLD']
        world_pib.set_index('code', inplace=True)
        world_pib = world_pib.loc[:, '1960':'2023'].T / 1e12

        st.header("Tabla de datos del Producto Interno Bruto (PIB)")
        st.write(data['pib'])
        st.header("Evolución del Producto Interno Bruto (PIB) en billones de dólares")
        st.line_chart(world_pib)

def page2():
    st.title("Gráficos")

    st.header("Mapa con Folium")

    # Seleccionar la información deseada
    variable = st.selectbox("Selecciona el tipo de dato", options=["pop", "cpi", "income", "pib"], format_func=lambda x: {
        "pop": "Población",
        "cpi": "Índice de Precios al Consumidor (CPI)",
        "income": "Ingreso per cápita",
        "pib": "Producto Interno Bruto (PIB)"
    }[x])


    # Seleccionar el año
    year = str(st.slider("Selecciona el año", min_value=1960, max_value=2022, value=2022))

    if variable == 'income':
        st.header(f"Mapa de Coropletas del Ingreso Nacional Bruto per cápita en {year}")
        label = "Ingreso Nacional Bruto per cápita"
    elif variable == 'pop':
        st.header(f"Mapa de Coropletas de la Población Mundial en {year}")
        label = "Población"
    elif variable == 'cpi':
        st.header(f"Mapa de Coropletas del Índice de Precios al Consumidor (CPI) en {year}")
        label = "Índice de Precios al Consumidor (CPI)"
    elif variable == 'pib':
        st.header(f"Mapa de Coropletas del Producto Interno Bruto (PIB) en {year}")
        label = "Producto Interno Bruto (PIB)"


    df = data[variable]

    # Unir los datos del CSV con el shapefile
    merged = shapefile.set_index('ADM0_A3').join(df.set_index('code'), how='inner')
    merged = merged.dropna(subset=[year])
    merged[year].fillna('', inplace=True)

    m = folium.Map(location=[0, 0], zoom_start=2)

    folium.Choropleth(
        geo_data=merged,
        name="data",
        data=merged,
        columns=[merged.index, year],
        key_on="feature.id",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=label,
    ).add_to(m)

    # Agregar los tooltips
    folium.GeoJson(
        merged,
        tooltip=folium.features.GeoJsonTooltip(fields=[year], aliases=[label]),
        style_function=lambda x: {'color': 'black', 'weight': 0.5}
    ).add_to(m)

    sf.folium_static(m)

    n_countries = st.number_input("Número de países a mostrar", min_value=1, max_value=merged.shape[0], value=5)
    
    left, right = st.columns(2)
    merged.set_index('Country Name', inplace=True)
    with left:
        st.subheader(f"Los {n_countries} países con mayor valor")
        # Mostrar los N países con mayor valor con un grafico de barras
        top = merged.nlargest(n_countries, year)
        st.bar_chart(top[year])
    with right:
        st.subheader(f"Los {n_countries} países con menor valor")
        # Mostrar los N países con menor valor con un grafico de barras
        bottom = merged.nsmallest(n_countries, year)
        st.bar_chart(bottom[year])
    
    
    st.header("Evolución en el tiempo")
    st.line_chart(merged.loc[:, '1960':'2023'].T)



def page3():
    st.title("Video de la web")
    st.video("https://www.youtube.com/watch?v=IR1b00jtMBk")

# Diccionario para la navegación entre páginas 
pages = {
    "Tablas de datos": page1,
    "Gráficos": page2,
    "Video": page3,
}



# Barra lateral para la selección de la página
st.sidebar.title("Navegación")
selection = st.sidebar.radio("Selecciona la página", list(pages.keys()), label_visibility="collapsed")

# Llamar a la función de la página seleccionada
page = pages[selection]
page()
