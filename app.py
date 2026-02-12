import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------- CONFIGURACIÓN ----------
USUARIO_CORRECTO = "admin"
CLAVE_CORRECTA = "1234"

st.set_page_config(page_title="Logística Concretera", layout="wide")

# ---------- LOGIN ----------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def login():
    st.title("🔐 Acceso Privado - Logística Concretera")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario == USUARIO_CORRECTO and clave == CLAVE_CORRECTA:
            st.session_state.autenticado = True
            st.success("Acceso concedido")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

if not st.session_state.autenticado:
    login()
    st.stop()

# ---------- APP PRINCIPAL ----------
st.title("🚛 Sistema de Logística – Concretera")

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

st.subheader("📋 Registro de despachos")
st.dataframe(st.session_state.data, use_container_width=True)

if not st.session_state.data.empty:
    df = st.session_state.data.copy()

    total_m3 = df["m3"].sum()
    total_ingresos = df["Total"].sum()
    promedio_precio = df["Precio x m3"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total m3 vendidos", f"{total_m3:.2f}")
    col2.metric("Ingresos totales (S/)", f"{total_ingresos:.2f}")
    col3.metric("Precio promedio (S/)", f"{promedio_precio:.2f}")

    st.subheader("📈 Evolución de ingresos")
    df_group = df.groupby("Fecha")["Total"].sum()

    fig, ax = plt.subplots()
    df_group.plot(kind="line", marker="o", ax=ax)
    ax.set_ylabel("Ingresos (S/)")
    ax.set_xlabel("Fecha")
    st.pyplot(fig)

    archivo = "reporte_logistica.xlsx"
    df.to_excel(archivo, index=False)

    with open(archivo, "rb") as f:
        st.download_button("Descargar Excel", f, file_name=archivo)

# ---------- BOTÓN CERRAR SESIÓN ----------
if st.sidebar.button("Cerrar sesión"):
    st.session_state.autenticado = False
    st.rerun()

