import pandas as pd
from sqlalchemy import create_engine,text
import streamlit as st

# Conexión a la base de datos
@st.cache_resource
def get_db_connection():
    connection_string = 'postgresql://airflow:airflow@postgres:5432/airflow'
    return create_engine(connection_string)

# Obtener datos de precios
@st.cache_data(ttl=3600)
def get_prices():
    engine = get_db_connection()
    query = """
    SELECT 
        fecha, 
        hora, 
        precio_kwh, 
        unidad 
    FROM 
        energia.precios_diarios 
    ORDER BY 
        fecha, hora
    """
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn)

# Obtener estadísticas
@st.cache_data(ttl=3600)
def get_stats():
    engine = get_db_connection()
    query = """
    SELECT 
        fecha, 
        precio_medio, 
        precio_maximo, 
        precio_minimo, 
        hora_pico, 
        hora_valle 
    FROM 
        energia.estadisticas_diarias 
    ORDER BY 
        fecha
    """
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn)