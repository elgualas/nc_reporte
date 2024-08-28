import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def display_kpi():
    st.header("Indicadores Clave de Desempeño (KPI)")

    # Cargar datos de feed.csv
    feed_df = pd.read_csv('data/feed.csv')

    # Procesar la columna call_date
    feed_df['call_date'] = pd.to_datetime(feed_df['call_date'], format='%Y-%m-%d %H:%M:%S')
    feed_df['day'] = feed_df['call_date'].dt.day

    # Llamadas por día
    calls_per_day = feed_df['day'].value_counts().sort_index()

    # Ventas por día (VENTA CON TITULAR)
    ventas_df = feed_df[feed_df['DESCRIPCION'] == 'VENTA CON TITULAR']
    ventas_por_dia = ventas_df['day'].value_counts().sort_index()

    # Ventas por día (CONTACTO EFECTIVO)
    contacto_df = feed_df[feed_df['TIPO'] == 'CONTACTO EFECTIVO']
    contacto_por_dia = contacto_df['day'].value_counts().sort_index()

    # Calcular Efectividad por día
    efectividad_por_dia = (contacto_por_dia / calls_per_day * 100).fillna(0)

    # Crear las gráficas

    # Gráfica 1: Llamadas por día
    fig_calls = px.bar(
        x=calls_per_day.index,
        y=calls_per_day.values,
        labels={'x': 'Día de Agosto', 'y': 'Cantidad de Llamadas'},
        title='Llamadas por Día',
        template='plotly_white'
    )
    fig_calls.update_traces(marker_color='skyblue', hovertemplate='Día: %{x}<br>Cantidad de Llamadas: %{y}')

    # Gráfica 2: Ventas por día (VENTA CON TITULAR)
    fig_ventas = px.bar(
        x=ventas_por_dia.index,
        y=ventas_por_dia.values,
        labels={'x': 'Día de Agosto', 'y': 'Cantidad de Ventas'},
        title='Ventas por Día (VENTA CON TITULAR)',
        template='plotly_white'
    )
    fig_ventas.update_traces(marker_color='orange', hovertemplate='Día: %{x}<br>Cantidad de Ventas: %{y}')

    # Gráfica 3: Contactos Efectivos por día
    fig_contacto = px.bar(
        x=contacto_por_dia.index,
        y=contacto_por_dia.values,
        labels={'x': 'Día de Agosto', 'y': 'Cantidad de Contactos Efectivos'},
        title='Contactos Efectivos por Día',
        template='plotly_white'
    )
    fig_contacto.update_traces(marker_color='green', hovertemplate='Día: %{x}<br>Cantidad de Contactos Efectivos: %{y}')

    # Gráfica 4: Efectividad por día
    fig_efectividad = go.Figure()

    fig_efectividad.add_trace(go.Scatter(
        x=efectividad_por_dia.index,
        y=efectividad_por_dia.values,
        mode='lines+markers',
        name='Efectividad',
        line=dict(dash='dot'),  # Línea punteada
        marker=dict(symbol='square', size=10, color='purple'),  # Cuadrados
        hovertemplate='Día: %{x}<br>Efectividad: %{y:.2f}%'
    ))

    fig_efectividad.update_layout(
        title='Efectividad por Día',
        xaxis_title='Día de Agosto',
        yaxis_title='Porcentaje de Efectividad (%)',
        template='plotly_white'
    )

    # Organizar las gráficas en un layout 2x2
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_calls, use_container_width=True)
        st.plotly_chart(fig_ventas, use_container_width=True)
    with col2:
        st.plotly_chart(fig_contacto, use_container_width=True)
        st.plotly_chart(fig_efectividad, use_container_width=True)

   
    # Crear la tabla con llamadas por día
    st.subheader("Tabla de Gestion")
    llamadas_table = pd.DataFrame({
        'Día': calls_per_day.index,
        'Llamadas': calls_per_day.values
    }).transpose()

    llamadas_table.columns = llamadas_table.iloc[0]
    llamadas_table = llamadas_table.drop('Día')

    # Agregar la fila de contactos efectivos
    llamadas_table.loc['Contactos'] = contacto_por_dia.reindex(calls_per_day.index, fill_value=0).values

    # Agregar la fila de ventas (VENTA CON TITULAR)
    llamadas_table.loc['Ventas'] = ventas_por_dia.reindex(calls_per_day.index, fill_value=0).values

    # Calcular la sumatoria de tiempo en horas
    tiempo_en_segundos = feed_df.groupby(feed_df['day'])['length_in_sec'].sum()
    tiempo_en_horas = (tiempo_en_segundos / 3600).reindex(calls_per_day.index, fill_value=0).round(2)

    # Agregar la fila de tiempo
    llamadas_table.loc['Tmo(Horas)'] = tiempo_en_horas.values

    # Calcular la sumatoria de tiempo de ventas en horas
    tiempo_venta_en_segundos = ventas_df.groupby(ventas_df['day'])['length_in_sec'].sum()
    tiempo_venta_en_horas = (tiempo_venta_en_segundos / 3600).reindex(calls_per_day.index, fill_value=0).round(2)

    # Agregar la fila de tiempo de ventas
    llamadas_table.loc['TmoV(Horas)'] = tiempo_venta_en_horas.values

    # Calcular la sumatoria de tiempo de no ventas en horas
    no_ventas_df = feed_df[feed_df['DESCRIPCION'] != 'VENTA CON TITULAR']
    tiempo_no_venta_en_segundos = no_ventas_df.groupby(no_ventas_df['day'])['length_in_sec'].sum()
    tiempo_no_venta_en_horas = (tiempo_no_venta_en_segundos / 3600).reindex(calls_per_day.index, fill_value=0).round(2)

    # Agregar la fila de tiempo de no ventas
    llamadas_table.loc['TmoNV(Horas)'] = tiempo_no_venta_en_horas.values

    # Agregar la columna Total
    llamadas_table['Total'] = llamadas_table.iloc[0:6, :].sum(axis=1)

    # Calcular el porcentaje de distribución
    llamadas_distribucion = (llamadas_table.loc['Llamadas'] / llamadas_table.loc['Llamadas'].sum()) * 100
    llamadas_table.loc['% Distribución'] = llamadas_distribucion.round(2).astype(str) + '%'
    llamadas_table.loc['% Distribución', 'Total'] = '100.00%'

    # Calcular el porcentaje de Contactabilidad
    contactabilidad_porcentaje = (llamadas_table.loc['Contactos'] / llamadas_table.loc['Llamadas']) * 100
    contactabilidad_porcentaje = contactabilidad_porcentaje.fillna(0).round(2)
    llamadas_table.loc['% Contactabilidad'] = contactabilidad_porcentaje.astype(str) + '%'
    llamadas_table.loc['% Contactabilidad', 'Total'] = '100.00%'

    # Calcular el porcentaje de Efectividad (Ventas entre Contactos)
    efectividad_porcentaje = (llamadas_table.loc['Ventas'] / llamadas_table.loc['Contactos']) * 100
    efectividad_porcentaje = efectividad_porcentaje.fillna(0).round(2)
    llamadas_table.loc['% Efectividad'] = efectividad_porcentaje.astype(str) + '%'
    llamadas_table.loc['% Efectividad', 'Total'] = '100.00%'

    # Mostrar la tabla en Streamlit
    st.dataframe(llamadas_table)








