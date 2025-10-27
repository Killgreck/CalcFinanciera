import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.components.input_form import render_input_form
from src.components.display import render_summary, render_amortization_table, render_charts
from src.components.payments import render_payment_manager, get_registered_payments
from src.utils.interest_rates import effective_rate_for_period, calculate_payment
from src.utils.amortization import generate_amortization_table, recalculate_with_extra_payment
from src.utils.export import export_to_csv, export_to_excel
from datetime import datetime


st.set_page_config(
    page_title="Calculadora Financiera",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💰 Calculadora Financiera - Amortización de Créditos")
st.markdown("---")

params = render_input_form()

frequency_map = {
    "Mensual": 12,
    "Bimestral": 6,
    "Trimestral": 4,
    "Cuatrimestral": 3,
    "Semestral": 2,
    "Anual": 1
}

annual_freq_tasa = frequency_map[params['frecuencia_tasa']]
annual_freq_pago = frequency_map[params['frecuencia_pago']]

tasa_efectiva = effective_rate_for_period(
    params['tasa'],
    params['tipo_tasa'],
    params['modalidad_tasa'],
    annual_freq_tasa,
    annual_freq_pago
)

cuota = calculate_payment(params['monto'], tasa_efectiva, params['periodos'])

render_summary(params, tasa_efectiva, cuota)

df_amortization = generate_amortization_table(
    params['monto'],
    tasa_efectiva,
    params['periodos'],
    params['fecha_inicio'],
    params['frecuencia_pago']
)

render_payment_manager()

abonos = get_registered_payments()

if abonos:
    st.info(f"ℹ️ Se aplicarán {len(abonos)} abono(s) extraordinario(s) a la tabla de amortización")
    
    abonos_sorted = sorted(abonos, key=lambda x: x['periodo'])
    
    for abono in abonos_sorted:
        df_amortization = recalculate_with_extra_payment(
            df_amortization,
            abono['periodo'],
            abono['monto'],
            abono['estrategia']
        )

st.markdown("---")

render_amortization_table(df_amortization)

st.markdown("---")

render_charts(df_amortization)

st.markdown("---")

st.header("📥 Exportar Resultados")

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Exportar a CSV", use_container_width=True):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"amortizacion_{timestamp}.csv"
        filepath = export_to_csv(df_amortization, filename)
        st.success(f"✅ Archivo exportado: {filepath}")
        
        with open(filepath, 'rb') as f:
            st.download_button(
                label="⬇️ Descargar CSV",
                data=f,
                file_name=filename,
                mime="text/csv",
                use_container_width=True
            )

with col2:
    if st.button("📊 Exportar a Excel", use_container_width=True):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"amortizacion_{timestamp}.xlsx"
        
        summary_data = {
            "Monto": params['monto'],
            "Tasa Nominal": params['tasa'] * 100,
            "Tipo Tasa": params['tipo_tasa'],
            "Modalidad": params['modalidad_tasa'],
            "Tasa Efectiva Periodo": tasa_efectiva * 100,
            "Plazo": f"{params['plazo']} {params['unidad_plazo']}",
            "Frecuencia Pago": params['frecuencia_pago'],
            "Cuota": cuota,
            "Total Intereses": df_amortization["Interés"].sum(),
            "Total Pagado": df_amortization["Cuota"].sum()
        }
        
        filepath = export_to_excel(df_amortization, summary_data, filename)
        st.success(f"✅ Archivo exportado: {filepath}")
        
        with open(filepath, 'rb') as f:
            st.download_button(
                label="⬇️ Descargar Excel",
                data=f,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

st.markdown("---")
st.caption("💡 Calculadora Financiera - Desarrollada con Streamlit | Basada en fórmulas de Ingeniería Financiera")
