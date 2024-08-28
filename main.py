import streamlit as st
import kpi
import ranking  # Importar el nuevo módulo

def main():
    st.title("Aplicación de Gestión de Ventas")

    # Barra lateral con opciones
    option = st.sidebar.selectbox(
        'Seleccione una opción',
        ['KPI', 'Ranking']  # Añadir la opción Ranking
    )

    # Navegar a la opción seleccionada
    if option == 'KPI':
        kpi.display_kpi()
    elif option == 'Ranking':
        ranking.display_ranking()  # Llamar a la función display_ranking en ranking.py

if __name__ == "__main__":
    main()
