import pandas as pd
import streamlit as st

def display_ranking():
    st.header("Ranking de Ventas por Vendedor")

    # Cargar datos de feed.csv
    feed_df = pd.read_csv('data/feed.csv')

    # Filtrar las ventas (DESCRIPCION = 'VENTA CON TITULAR')
    ventas_df = feed_df[feed_df['DESCRIPCION'] == 'VENTA CON TITULAR']

    # Extraer día del mes de la columna call_date
    ventas_df['day'] = pd.to_datetime(ventas_df['call_date'], format='%Y-%m-%d %H:%M:%S').dt.day

    # Crear una tabla pivot para contar ventas por vendedor y por día
    ranking_table = ventas_df.pivot_table(
        index='full_name',
        columns='day',
        values='DESCRIPCION',
        aggfunc='count',
        fill_value=0
    )

    # Agregar una columna Total para el total de ventas por vendedor
    ranking_table['Total'] = ranking_table.sum(axis=1)

    # Mostrar la tabla en Streamlit
    st.dataframe(ranking_table)

