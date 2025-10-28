import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def render_summary(params, tasa_efectiva, cuota):
    st.header("📊 Resumen del Crédito")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Monto del Crédito", f"${params['monto']:,.2f}")

    with col2:
        tipo_tasa = f"{params['tipo_tasa']} - {params['modalidad_tasa']} ({params['frecuencia_tasa']})"
        st.metric("Tasa Efectiva Periodo", f"{tasa_efectiva*100:.4f}%", delta=tipo_tasa, delta_color="off")

    with col3:
        st.metric("Cuota Periódica", f"${cuota:,.2f}")

    with col4:
        st.metric("Número de Pagos", params['periodos'])

    st.divider()


def render_amortization_table(df):
    st.header("📋 Tabla de Amortización")
    
    st.dataframe(
        df.style.format({
            "Saldo Inicial": "${:,.2f}",
            "Cuota": "${:,.2f}",
            "Interés": "${:,.2f}",
            "Abono a Capital": "${:,.2f}",
            "Saldo Final": "${:,.2f}"
        }),
        use_container_width=True,
        height=400
    )
    
    total_interes = df["Interés"].sum()
    total_capital = df["Abono a Capital"].sum()
    total_pagado = df["Cuota"].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Intereses", f"${total_interes:,.2f}")
    
    with col2:
        st.metric("Total Capital", f"${total_capital:,.2f}")
    
    with col3:
        st.metric("Total Pagado", f"${total_pagado:,.2f}")


def render_charts(df):
    st.header("📈 Visualizaciones")
    
    tab1, tab2, tab3 = st.tabs(["Evolución del Saldo", "Composición de Cuotas", "Distribución Total"])
    
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Periodo"],
            y=df["Saldo Final"],
            mode='lines+markers',
            name='Saldo',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))
        fig.update_layout(
            title="Evolución del Saldo del Crédito",
            xaxis_title="Periodo",
            yaxis_title="Saldo ($)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["Periodo"],
            y=df["Interés"],
            name='Interés',
            marker_color='#ff7f0e'
        ))
        fig.add_trace(go.Bar(
            x=df["Periodo"],
            y=df["Abono a Capital"],
            name='Abono a Capital',
            marker_color='#2ca02c'
        ))
        fig.update_layout(
            title="Composición de las Cuotas",
            xaxis_title="Periodo",
            yaxis_title="Monto ($)",
            barmode='stack',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        total_interes = df["Interés"].sum()
        total_capital = df["Abono a Capital"].sum()
        
        fig = go.Figure(data=[go.Pie(
            labels=['Intereses', 'Capital'],
            values=[total_interes, total_capital],
            hole=.3,
            marker_colors=['#ff7f0e', '#2ca02c']
        )])
        fig.update_layout(
            title="Distribución Total: Capital vs Intereses"
        )
        st.plotly_chart(fig, use_container_width=True)
