import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Cargar los datos desde un archivo CSV
@st.cache_data
def load_data():
    csv_path = os.path.join('data', 'ventas.csv')
    df = pd.read_csv(csv_path)
    # Convertir la columna 'Order Date' a datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

# Cargar los datos
try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: No se pudo encontrar el archivo 'ventas.csv' en la carpeta 'data'.")
    st.stop()

# Título de la aplicación
st.title('Dashboard de Ventas')

# Sidebar para filtros
st.sidebar.header('Filtros')
category = st.sidebar.multiselect('Selecciona Categoría', options=df['Category'].unique(), default=df['Category'].unique())
date_range = st.sidebar.date_input('Rango de Fechas', [df['Order Date'].min(), df['Order Date'].max()])

# Filtrar datos
df_filtered = df[df['Category'].isin(category) & 
                 (df['Order Date'].dt.date >= date_range[0]) & 
                 (df['Order Date'].dt.date <= date_range[1])]

# Gráfico de barras: Ventas por Categoría
st.subheader('Ventas por Categoría')
fig_sales = px.bar(df_filtered.groupby('Category')['Sales'].sum().reset_index(), 
                   x='Category', y='Sales', color='Category')
st.plotly_chart(fig_sales)

# Gráfico de dispersión: Ventas vs Beneficio
st.subheader('Ventas vs Beneficio')
fig_scatter = px.scatter(df_filtered, x='Sales', y='Profit', color='Category', 
                         hover_data=['Customer Name'])
st.plotly_chart(fig_scatter)

# Mapa de ventas por estado
st.subheader('Mapa de Ventas por Estado')
sales_by_state = df_filtered.groupby('State')['Sales'].sum().reset_index()
fig_map = px.choropleth(sales_by_state, locations='State', locationmode="USA-states", 
                        color='Sales', scope="usa", color_continuous_scale="Viridis")
st.plotly_chart(fig_map)

# Tabla de datos
st.subheader('Datos Detallados')
st.dataframe(df_filtered)
