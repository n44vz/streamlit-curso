import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
@st.cache_data
def load_data():
    return pd.read_csv('.data/ventas.csv')

# Cargar los datos
df = load_data()

# Título de la aplicación
st.title('Dashboard de Ventas')

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

# Verificar los estados únicos
unique_states = sales_by_state['State'].unique()
st.write(f"Estados únicos en los datos: {', '.join(unique_states)}")

fig_map = px.choropleth(sales_by_state, 
                        locations='State', 
                        locationmode="USA-states", 
                        color='Sales', 
                        scope="usa", 
                        color_continuous_scale="Viridis")

# Ajustar la configuración del mapa
fig_map.update_layout(geo_scope='usa')  # Enfocar en USA
fig_map.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white", showstates=True, statecolor="Black")

st.plotly_chart(fig_map)

# Tabla de datos
st.subheader('Datos Detallados')
st.dataframe(df)
