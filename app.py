import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
@st.cache_data
def load_data():
    return pd.read_csv('data/ventas.csv')

# Cargar los datos
df = load_data()

# Título de la aplicación
st.title('Dashboard de Ventas Simplificado')

# Gráfico de barras: Ventas por Categoría
st.subheader('Ventas por Categoría')
fig_sales = px.bar(df.groupby('Category')['Sales'].sum().reset_index(), 
                   x='Category', y='Sales', color='Category')
st.plotly_chart(fig_sales)

# Gráfico de dispersión: Ventas vs Beneficio
st.subheader('Ventas vs Beneficio')
fig_scatter = px.scatter(df, x='Sales', y='Profit', color='Category', 
                         hover_data=['Customer Name'])
st.plotly_chart(fig_scatter)

# Mapa de ventas por estado
st.subheader('Mapa de Ventas por Estado')
sales_by_state = df.groupby('State')['Sales'].sum().reset_index()
fig_map = px.choropleth(sales_by_state, 
                        locations='State', 
                        locationmode="USA-states", 
                        color='Sales', 
                        scope="usa", 
                        color_continuous_scale="Viridis")
st.plotly_chart(fig_map)

# Tabla de datos
st.subheader('Datos Detallados')
st.dataframe(df)
