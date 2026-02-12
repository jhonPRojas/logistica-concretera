import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Logística Concretera", layout="wide")

st.title("🚛 Sistema de Logística – Concretera")

# Inicializar datos
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Fecha", "Obra", "m3", "Precio x m3", "Total"
    ])

st.sidebar.header("📌 Registrar despacho")

fecha = st.sidebar.date_input("Fecha", datetime.today())
obra = st.sidebar.text_input("Nombre de la Obra")
m3 = st.sidebar.number_input("Metros cúbicos (m3)", min_value=0.0)
precio = st.sidebar.number_input("Precio por m3 (S/)", min_value=0.0)

if st.sidebar.button("Agregar despacho"):
    total = m3 * precio
    nuevo = pd.DataFrame([[fecha, obra, m3, precio, total]],
                         columns=st.session_state.data.columns)
    st.session_state.data = pd.concat([st.session_state.data, nuevo], ignore_index=True)
    st.success("Despacho agregado correctamente")

# Mostrar tabla
st.subheader("📋 Registro de despachos")
st.dataframe(st.session_state.data, use_container_width=True)

if not st.session_state.data.empty:

    df = st.session_state.data.copy()

    # Métricas superiores
    total_m3 = df["m3"].sum()
    total_ingresos = df["Total"].sum()
    promedio_precio = df["Precio x m3"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total m3 vendidos", f"{total_m3:.2f}")
    col2.metric("Ingresos totales (S/)", f"{total_ingresos:.2f}")
    col3.metric("Precio promedio (S/)", f"{promedio_precio:.2f}")

    # Gráfico
    st.subheader("📈 Evolución de ingresos")
    df_group = df.groupby("Fecha")["Total"].sum()

    fig, ax = plt.subplots()
    df_group.plot(kind="line", marker="o", ax=ax)
    ax.set_ylabel("Ingresos (S/)")
    ax.set_xlabel("Fecha")
    st.pyplot(fig)

    # Descargar Excel
    st.subheader("⬇ Descargar reporte")
    archivo = "reporte_logistica.xlsx"
    df.to_excel(archivo, index=False)

    with open(archivo, "rb") as f:
        st.download_button("Descargar Excel", f, file_name=archivo)
