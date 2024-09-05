import streamlit as st
import pandas as pd
import plotly.express as px

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

# Cargar los datos
@st.cache_data
def load_data():
    df = pd.read_csv('data/ventas.csv')
    df['State'] = df['State'].str.title()
    # Convertir nombres de estados a códigos
    df['State_Code'] = df['State'].map(state_codes)
    return df

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
sales_by_state = df.groupby(['State', 'State_Code'])['Sales'].sum().reset_index()

# Verificar los estados únicos
unique_states = sales_by_state['State'].unique()
st.write(f"Estados únicos en los datos: {', '.join(unique_states)}")

fig_map = px.choropleth(sales_by_state, 
                        locations='State_Code', 
                        locationmode="USA-states", 
                        color='Sales', 
                        scope="usa", 
                        color_continuous_scale="Viridis",
                        hover_name='State')

# Ajustar la configuración del mapa
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

st.plotly_chart(fig_map)

# Tabla de datos
st.subheader('Datos Detallados')
st.dataframe(df)
