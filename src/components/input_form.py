import streamlit as st
from datetime import datetime


def render_input_form():
    st.sidebar.header("⚙️ Parámetros del Crédito")
    
    monto = st.sidebar.number_input(
        "Monto del Crédito",
        min_value=0.0,
        value=100000.0,
        step=1000.0,
        format="%.2f"
    )
    
    st.sidebar.subheader("Configuración de Tasa")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        tipo_tasa = st.selectbox(
            "Tipo de Tasa",
            ["Nominal", "Efectiva"]
        )
    
    with col2:
        modalidad_tasa = st.selectbox(
            "Modalidad",
            ["Vencida", "Anticipada"]
        )
    
    tasa = st.sidebar.number_input(
        "Tasa de Interés (%)",
        min_value=0.0,
        max_value=100.0,
        value=12.0,
        step=0.1,
        format="%.2f"
    )
    
    frecuencia_tasa = st.sidebar.selectbox(
        "Frecuencia de la Tasa",
        ["Mensual", "Bimestral", "Trimestral", "Cuatrimestral", "Semestral", "Anual"]
    )
    
    st.sidebar.subheader("Configuración de Pagos")
    
    col3, col4 = st.sidebar.columns(2)
    
    with col3:
        plazo = st.number_input(
            "Plazo",
            min_value=1,
            value=12,
            step=1
        )
    
    with col4:
        unidad_plazo = st.selectbox(
            "Unidad",
            ["Meses", "Años"]
        )
    
    frecuencia_pago = st.sidebar.selectbox(
        "Frecuencia de Pago",
        ["Mensual", "Bimestral", "Trimestral", "Cuatrimestral", "Semestral", "Anual"]
    )
    
    fecha_inicio = st.sidebar.date_input(
        "Fecha de Inicio",
        value=datetime.now()
    )
    
    if unidad_plazo == "Años":
        plazo_meses = plazo * 12
    else:
        plazo_meses = plazo
    
    frequency_map = {
        "Mensual": 1,
        "Bimestral": 2,
        "Trimestral": 3,
        "Cuatrimestral": 4,
        "Semestral": 6,
        "Anual": 12
    }
    
    periodos = plazo_meses // frequency_map[frecuencia_pago]
    
    return {
        "monto": monto,
        "tasa": tasa / 100,
        "tipo_tasa": tipo_tasa,
        "modalidad_tasa": modalidad_tasa,
        "frecuencia_tasa": frecuencia_tasa,
        "plazo": plazo,
        "unidad_plazo": unidad_plazo,
        "frecuencia_pago": frecuencia_pago,
        "fecha_inicio": fecha_inicio,
        "periodos": periodos
    }
