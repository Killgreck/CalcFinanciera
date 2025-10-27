import streamlit as st


def render_payment_manager():
    st.header("💰 Gestión de Abonos Extraordinarios")
    
    with st.expander("➕ Agregar Abono Extraordinario", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            periodo_abono = st.number_input(
                "Periodo del Abono",
                min_value=1,
                value=1,
                step=1,
                key="periodo_abono"
            )
        
        with col2:
            monto_abono = st.number_input(
                "Monto del Abono",
                min_value=0.0,
                value=0.0,
                step=100.0,
                format="%.2f",
                key="monto_abono"
            )
        
        estrategia = st.radio(
            "Estrategia de Recálculo",
            ["Reducir Plazo", "Reducir Cuota"],
            horizontal=True,
            key="estrategia_abono"
        )
        
        col3, col4 = st.columns([1, 3])
        
        with col3:
            agregar_abono = st.button("Agregar Abono", type="primary", use_container_width=True)
        
        with col4:
            descripcion = st.text_input(
                "Descripción (opcional)",
                value="Abono extraordinario",
                key="descripcion_abono"
            )
        
        if agregar_abono:
            if monto_abono > 0:
                if 'abonos' not in st.session_state:
                    st.session_state.abonos = []
                
                st.session_state.abonos.append({
                    'periodo': periodo_abono,
                    'monto': monto_abono,
                    'estrategia': estrategia.lower().replace(" ", "_"),
                    'descripcion': descripcion
                })
                st.success(f"✅ Abono de ${monto_abono:,.2f} agregado al periodo {periodo_abono}")
                st.rerun()
            else:
                st.error("⚠️ El monto del abono debe ser mayor a 0")
    
    if 'abonos' in st.session_state and len(st.session_state.abonos) > 0:
        st.subheader("📝 Abonos Registrados")
        
        for idx, abono in enumerate(st.session_state.abonos):
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
            
            with col1:
                st.write(f"**#{idx+1}**")
            
            with col2:
                st.write(f"Periodo: **{abono['periodo']}**")
            
            with col3:
                st.write(f"Monto: **${abono['monto']:,.2f}**")
            
            with col4:
                estrategia_display = abono['estrategia'].replace("_", " ").title()
                st.write(f"Estrategia: **{estrategia_display}**")
            
            with col5:
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state.abonos.pop(idx)
                    st.rerun()
        
        if st.button("🗑️ Limpiar Todos los Abonos", type="secondary"):
            st.session_state.abonos = []
            st.rerun()
    else:
        st.info("ℹ️ No hay abonos extraordinarios registrados")


def get_registered_payments():
    if 'abonos' in st.session_state:
        return st.session_state.abonos
    return []
