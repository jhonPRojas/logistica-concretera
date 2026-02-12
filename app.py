import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard Logístico Concretera", layout="wide")

st.title("🚛 Dashboard Ejecutivo - Logística Concretera")

# -------------------------
# CONFIGURACIÓN
# -------------------------
st.sidebar.header("⚙️ Configuración")

costo_minuto = st.sidebar.number_input(
    "Costo por minuto de espera (S/)",
    min_value=0.0,
    value=5.0,
    step=0.5
)

uploaded_file = st.file_uploader("📂 Subir Excel exportado del sistema", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Convertir columnas de tiempo a minutos
    if "Espera" in df.columns:
        df["Espera_min"] = df["Espera"] * 1440
    else:
        st.error("No se encontró la columna 'Espera'")
        st.stop()

    # KPIs principales
    total_viajes = len(df)
    espera_promedio = df["Espera_min"].mean()
    costo_total = df["Espera_min"].sum() * costo_minuto

    col1, col2, col3 = st.columns(3)

    col1.metric("📦 Total Viajes", total_viajes)
    col2.metric("⏱ Espera Promedio (min)", round(espera_promedio,1))
    col3.metric("💰 Costo Total Espera (S/)", f"{round(costo_total,2):,}")

    st.divider()

    # -------------------------
    # ANÁLISIS POR CLIENTE
    # -------------------------
    st.subheader("📊 Ranking de Clientes")

    resumen_cliente = df.groupby("Cliente").agg(
        Viajes=("Cliente","count"),
        Espera_Promedio=("Espera_min","mean"),
        Espera_Total=("Espera_min","sum")
    ).reset_index()

    resumen_cliente["Costo_Estimado"] = resumen_cliente["Espera_Total"] * costo_minuto

    resumen_cliente["Clasificación"] = np.where(
        resumen_cliente["Espera_Promedio"] > 20, "🔴 CRÍTICO",
        np.where(resumen_cliente["Espera_Promedio"] > 15, "🟡 LENTO", "🟢 EFICIENTE")
    )

    resumen_cliente = resumen_cliente.sort_values(by="Espera_Promedio", ascending=False)

    st.dataframe(resumen_cliente)

    st.bar_chart(resumen_cliente.set_index("Cliente")["Espera_Promedio"])

    st.divider()

    # -------------------------
    # ALERTAS
    # -------------------------
    st.subheader("🚨 Alertas Automáticas")

    clientes_criticos = resumen_cliente[resumen_cliente["Espera_Promedio"] > 20]

    if len(clientes_criticos) > 0:
        for _, row in clientes_criticos.iterrows():
            st.error(
                f"""
                🔴 CLIENTE CRÍTICO: {row['Cliente']}

                Espera promedio: {round(row['Espera_Promedio'],1)} min  
                Viajes: {row['Viajes']}  
                Impacto estimado: S/ {round(row['Costo_Estimado'],2):,}

                Recomendación: Programar llegada +15 min.
                """
            )
    else:
        st.success("No hay clientes críticos detectados.")

else:
    st.info("Sube el archivo Excel exportado del sistema para comenzar.")
