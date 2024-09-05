import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página (debe ser la primera llamada a Streamlit)
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# Diccionario de mapeo de nombres de estados a códigos
state_codes = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District of Columbia': 'DC'
}

@st.cache_data
def load_data():
    df = pd.read_csv('data/ventas.csv')
    df['State'] = df['State'].str.title()
    df['State_Code'] = df['State'].map(state_codes)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

# Cargar los datos
df = load_data()

# Título de la aplicación
st.title('Dashboard de Ventas')

# Barra lateral para filtros
st.sidebar.header('Filtros')

# Filtro de categoría
categories = ['Todas'] + list(df['Category'].unique())
category = st.sidebar.selectbox('Selecciona una categoría:', categories)

# Filtro de fecha
date_range = st.sidebar.date_input(
    "Rango de fechas",
    [df['Order Date'].min(), df['Order Date'].max()],
    min_value=df['Order Date'].min().to_pydatetime(),
    max_value=df['Order Date'].max().to_pydatetime()
)

# Filtro de estado
states = ['Todos'] + list(df['State'].unique())
state = st.sidebar.selectbox('Selecciona un estado:', states)

# Aplicar filtros
if category != 'Todas':
    df_filtered = df[df['Category'] == category]
else:
    df_filtered = df

df_filtered = df_filtered[
    (df_filtered['Order Date'].dt.date >= date_range[0]) &
    (df_filtered['Order Date'].dt.date <= date_range[1])
]

if state != 'Todos':
    df_filtered = df_filtered[df_filtered['State'] == state]

# Métricas principales
col1, col2, col3 = st.columns(3)
col1.metric("Total de Ventas", f"${df_filtered['Sales'].sum():,.2f}")
col2.metric("Beneficio Total", f"${df_filtered['Profit'].sum():,.2f}")
col3.metric("Número de Pedidos", len(df_filtered))

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader('Ventas por Categoría')
    fig_sales = px.bar(df_filtered.groupby('Category')['Sales'].sum().reset_index(), 
                       x='Category', y='Sales', color='Category')
    st.plotly_chart(fig_sales, use_container_width=True)

with col2:
    st.subheader('Ventas vs Beneficio')
    fig_scatter = px.scatter(df_filtered, x='Sales', y='Profit', color='Category', 
                             hover_data=['Customer Name'])
    st.plotly_chart(fig_scatter, use_container_width=True)

# Mapa de ventas por estado
st.subheader('Mapa de Ventas por Estado')
sales_by_state = df_filtered.groupby(['State', 'State_Code'])['Sales'].sum().reset_index()

fig_map = px.choropleth(sales_by_state, 
                        locations='State_Code', 
                        locationmode="USA-states", 
                        color='Sales', 
                        scope="usa", 
                        color_continuous_scale="Viridis",
                        hover_name='State')

fig_map.update_layout(
    geo_scope='usa',
    geo=dict(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="white",
        showsubunits=True,
        subunitcolor="Black"
    )
)

st.plotly_chart(fig_map, use_container_width=True)

# Tabla de datos
st.subheader('Datos Detallados')
st.dataframe(df_filtered)
