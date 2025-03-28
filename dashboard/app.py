import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import get_prices, get_stats

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Precios de Energía",
    page_icon="⚡",
    layout="wide"
)

# Título principal
st.title("Dashboard de Precios de Energía en España")

# Cargar datos
prices = get_prices()
stats = get_stats()

# Sidebar con filtros
st.sidebar.header("Filtros")

# Filtro de fechas
min_date = prices['fecha'].min()
max_date = prices['fecha'].max()
start_date, end_date = st.sidebar.date_input(
    "Selecciona un rango de fechas",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filtrar datos según selección
filtered_prices = prices[(prices['fecha'] >= start_date) & (prices['fecha'] <= end_date)]
st.subheader("Tabla de precios")
st.table(filtered_prices.head())

filtered_stats = stats[(stats['fecha'] >= start_date) & (stats['fecha'] <= end_date)]

# Métricas principales
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Precio Medio", f"{filtered_stats['precio_medio'].mean():.2f} €/MWh")
with col2:
    st.metric("Precio Máximo", f"{filtered_stats['precio_maximo'].max():.2f} €/MWh")
with col3:
    st.metric("Precio Mínimo", f"{filtered_stats['precio_minimo'].min():.2f} €/MWh")

# Sacamos una copia para no modificar el original
filtered_prices_streamlit = filtered_prices.copy()
# Gráfico de evolución de precios
st.subheader("Evolución de precios")
# Convertir 'fecha' a datetime y combinar con 'hora'

# Supongamos que 'hora' son enteros de 0 a 23
filtered_prices_streamlit['hora'] = filtered_prices_streamlit['hora'].apply(lambda x: f"{x:02d}:00")

filtered_prices_streamlit['fecha_hora'] = pd.to_datetime(filtered_prices_streamlit['fecha'].astype(str) + ' ' + filtered_prices_streamlit['hora'])

# Crear la gráfica
fig = px.line(
    filtered_prices_streamlit, 
    x='fecha_hora',  
    y='precio_kwh', 
    color='fecha',  # Diferenciar cada día por color
    title='Precio por hora a lo largo del tiempo'
)

# Mostrar en Streamlit
st.title("Visualización de precios por hora")
st.plotly_chart(fig,use_container_width=True)
# fig = px.line(
#     filtered_prices, 
#     x='fecha', 
#     y='precio_kwh', 
#     color='hora',
#     title='Precio por hora a lo largo del tiempo'
# )
# st.plotly_chart(fig, use_container_width=True)

# Mapa de calor de precios por hora y día
st.subheader("Mapa de calor de precios")
pivot = filtered_prices.pivot_table(index='fecha', columns='hora', values='precio_kwh')
fig_heatmap = px.imshow(
    pivot, 
    labels=dict(x="Hora del día", y="Fecha", color="Precio (€/MWh)"),
    x=pivot.columns, 
    y=pivot.index,
    color_continuous_scale='Viridis'
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Tabla de estadísticas
st.subheader("Estadísticas diarias")
st.dataframe(filtered_stats)