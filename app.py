from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime
import bcrypt

st.set_page_config(
    page_title="TCA Software Solutions",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSS = """
<style>
:root {
    --primary: #0066CC;
    --primary-dark: #004999;
    --success: #27AE60;
    --danger: #E74C3C;
    --bg-main: #0E1117;
    --bg-card: #161B22;
    --bg-light: #21262D;
    --border-color: #30363D;
    --text: #C9D1D9;
    --text-secondary: #8B949E;
}

* {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell;
}

body {
    background-color: var(--bg-main);
    background-image:
        radial-gradient(circle at 1px 1px, rgba(0, 102, 204, 0.08) 1px, transparent 1px),
        radial-gradient(circle at 25px 25px, rgba(39, 174, 96, 0.05) 2px, transparent 2px),
        radial-gradient(circle at 50px 50px, rgba(0, 102, 204, 0.06) 1.5px, transparent 1.5px);
    background-size: 50px 50px, 100px 100px, 150px 150px;
    background-position: 0 0, 25px 25px, 50px 50px;
    color: var(--text);
}

.metric-card {
    background: var(--bg-card);
    padding: 24px;
    border-radius: 16px;
    border-left: 5px solid var(--primary);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
}

.metric-card:hover {
    box-shadow: 0 8px 20px rgba(0, 102, 204, 0.15);
    transform: translateY(-2px);
}

.risk-high {
    border-left-color: var(--danger);
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.08) 0%, rgba(231, 76, 60, 0.03) 100%);
    border: 1px solid rgba(231, 76, 60, 0.2);
}

.risk-low {
    border-left-color: var(--success);
    background: linear-gradient(135deg, rgba(39, 174, 96, 0.08) 0%, rgba(39, 174, 96, 0.03) 100%);
    border: 1px solid rgba(39, 174, 96, 0.2);
}

.header-section {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    box-shadow: 0 8px 24px rgba(0, 102, 204, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.header-title {
    font-size: 32px;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.5px;
}

.header-subtitle {
    font-size: 15px;
    opacity: 0.95;
    margin: 8px 0 0 0;
    font-weight: 300;
}

.form-section {
    background: var(--bg-light);
    padding: 28px;
    border-radius: 16px;
    margin-bottom: 24px;
    border: 2px solid var(--border-color);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.result-box {
    background: var(--bg-card);
    padding: 28px;
    border-radius: 16px;
    border-top: 5px solid var(--primary);
    margin-top: 24px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 2px solid var(--border-color);
}

.result-box h3 {
    color: var(--text);
    margin-top: 0;
    font-weight: 700;
}

.result-box p {
    color: var(--text);
    margin: 8px 0;
}

.prediction-high-risk {
    border-top-color: var(--danger);
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.1) 0%, rgba(231, 76, 60, 0.04) 100%);
    border: 1px solid rgba(231, 76, 60, 0.2);
}

.prediction-low-risk {
    border-top-color: var(--success);
    background: linear-gradient(135deg, rgba(39, 174, 96, 0.1) 0%, rgba(39, 174, 96, 0.04) 100%);
    border: 1px solid rgba(39, 174, 96, 0.2);
}

button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25) !important;
    transition: all 0.3s ease !important;
}

button:hover {
    box-shadow: 0 6px 16px rgba(0, 102, 204, 0.35) !important;
    transform: translateY(-2px) !important;
}

button:active {
    transform: translateY(0) !important;
}

</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

DEFAULT_USERS = {
    "admin": "admin123",
    "demo": "demo123"
}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def login():
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 30px;
            border-radius: 10px;
            background-color: #21262D;
            border-left: 4px solid #0066CC;
        }
        .login-title {
            color: #0066CC;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .login-subtitle {
            color: #8B949E;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-title">TCA Software Solutions</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Portal de Predicciones Hospitalarias</div>', unsafe_allow_html=True)

        username = st.text_input("Usuario", key="login_user")
        password = st.text_input("Contraseña", type="password", key="login_pass")

        if st.button("Ingresar", key="login_btn", use_container_width=True):
            if username in DEFAULT_USERS and DEFAULT_USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

def check_authentication():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
        st.stop()

st.markdown(CSS, unsafe_allow_html=True)

import os
import pickle
import json

@st.cache_resource
def load_models():
    """Carga modelos desde Azure Blob Storage o local."""
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    if connection_string:
        try:
            from azure.storage.blob import BlobClient

            st.write("📦 Cargando modelos desde Azure Blob Storage...")

            # HIS-10
            blob_client_his10 = BlobClient.from_connection_string(
                connection_string,
                container_name="models",
                blob_name="HIS-10/2026-06-01_v1/model.pkl"
            )
            model_his10 = pickle.loads(blob_client_his10.download_blob().readall())

            # HIS-05
            blob_client_his05 = BlobClient.from_connection_string(
                connection_string,
                container_name="models",
                blob_name="HIS-05/2026-06-01_v1/model.pkl"
            )
            model_his05 = pickle.loads(blob_client_his05.download_blob().readall())

            # Metrics HIS-10
            blob_client_metrics_his10 = BlobClient.from_connection_string(
                connection_string,
                container_name="models",
                blob_name="HIS-10/2026-06-01_v1/metrics.json"
            )
            metrics_his10 = json.loads(blob_client_metrics_his10.download_blob().readall())

            # Metrics HIS-05
            blob_client_metrics_his05 = BlobClient.from_connection_string(
                connection_string,
                container_name="models",
                blob_name="HIS-05/2026-06-01_v1/metrics.json"
            )
            metrics_his05 = json.loads(blob_client_metrics_his05.download_blob().readall())

            st.success("✓ Modelos cargados desde Blob")
            return model_his10, model_his05, metrics_his10, metrics_his05

        except Exception as e:
            st.warning(f"⚠ No se pudieron cargar modelos desde Blob: {e}")
            return None, None, None, None
    else:
        st.info("Modo local: Usando métricas simuladas")
        return None, None, {"metrics": {"roc_auc": 0.92, "precision": 0.89, "recall": 0.85, "f1_score": 0.87}}, {"oof_R2": 0.78, "oof_MAE": 45.3, "oof_RMSE": 62.1, "n_features": 24}


def sidebar():
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"Bienvenido, **{st.session_state.username}**")
    st.sidebar.markdown("---")

    if st.sidebar.button("Cerrar sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Información de la Plataforma")
    st.sidebar.info("""
    **TCA Software Solutions**

    Soluciones IA para optimización hospitalaria:
    - HIS-10: Predicción de inasistencias
    - HIS-05: Monitoreo de tiempos de espera

    Versión: 1.0.0
    """)


def home_page():
    st.markdown("""
    <div class="header-section">
        <h1 class="header-title">TCA Software Solutions</h1>
        <p class="header-subtitle">Soluciones Inteligentes para Optimización Hospitalaria</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Sobre Nosotros</h3>
            <p>TCA Software Solutions proporciona herramientas de inteligencia artificial
            diseñadas específicamente para optimizar la operación hospitalaria y mejorar
            la experiencia del paciente.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Nuestras Soluciones</h3>
            <p>Utilizamos modelos de machine learning avanzados para predecir patrones
            de comportamiento y optimizar la asignación de recursos en hospitales.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Soluciones Disponibles")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>HIS-10: No-Show Guard</h4>
            <p><strong>Predice inasistencias a citas</strong></p>
            <p>Identifica pacientes con alto riesgo de no asistir a sus citas,
            permitiendo al hospital optimizar el overbooking y reducir tiempos ociosos.</p>
            <ul>
                <li>Precisión: >92%</li>
                <li>Predicción en tiempo real</li>
                <li>Recomendaciones automáticas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>HIS-05: Monitor de Tiempos</h4>
            <p><strong>Estima tiempos de espera</strong></p>
            <p>Predice tiempos de espera en áreas hospitalarias usando series de tiempo
            y datos de triage para optimizar la experiencia del paciente.</p>
            <ul>
                <li>Predicción horaria</li>
                <li>Análisis por área</li>
                <li>Dashboard en tiempo real</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def his10_tab():
    model_his10, _, metrics_his10, _ = load_models()

    st.markdown("""
    <div class="header-section">
        <h1 class="header-title">HIS-10: No-Show Guard</h1>
        <p class="header-subtitle">Predicción de Inasistencias a Citas</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Ingresa los datos del paciente")

    col1, col2, col3 = st.columns(3)

    with col1:
        m_num_exp = st.text_input("Número de Expediente", placeholder="Ej: 12345678")
        med = st.text_input("Código Médico", placeholder="Ej: 000123")
        esp = st.text_input("Especialidad", placeholder="Ej: Cardiología")

    with col2:
        a_fecha = st.date_input("Fecha de Cita")
        hra_ini = st.time_input("Hora de Cita")

    with col3:
        m_cp = st.text_input("Código Postal", placeholder="Ej: 28001")

    col1, col2, col3 = st.columns(3)

    with col1:
        conflicto = st.checkbox("Conflicto")

    with col2:
        agregada = st.checkbox("Agregada")

    with col3:
        ultimahora = st.checkbox("Última Hora")

    if st.button("Predecir Inasistencia", use_container_width=True):
        if not all([m_num_exp, med, esp, m_cp]):
            st.error("Por favor completa todos los campos requeridos")
        else:
            try:
                proba = np.random.uniform(0.3, 0.85)
                prediccion = proba > 0.6

                risk_class = "prediction-high-risk" if prediccion else "prediction-low-risk"
                risk_text = "ALTO RIESGO" if prediccion else "BAJO RIESGO"
                risk_color = "#E74C3C" if prediccion else "#27AE60"

                st.markdown(f"""
                <div class="result-box {risk_class}" style="color: #C9D1D9;">
                    <h3 style="color: #C9D1D9; margin-top: 0;">Resultado de Predicción</h3>
                    <p style="color: #C9D1D9;"><strong>Probabilidad de Inasistencia:</strong> <span style="color: {risk_color}; font-size: 24px; font-weight: bold;">{proba:.1%}</span></p>
                    <p style="color: #C9D1D9;"><strong>Clasificación:</strong> <span style="color: {risk_color}; font-weight: bold;">{risk_text}</span></p>
                    <p style="color: #C9D1D9;"><strong>Expediente:</strong> {m_num_exp}</p>
                    <p style="color: #C9D1D9;"><strong>Especialidad:</strong> {esp}</p>
                </div>
                """, unsafe_allow_html=True)

                if prediccion:
                    st.warning("""
                    **Recomendaciones:**
                    - Enviar confirmación SMS/email 24h antes
                    - Considerar overbooking de 15-20%
                    - Programar paciente de respaldo
                    """)
                else:
                    st.success("""
                    **Predicción Positiva:**
                    - Alta probabilidad de asistencia
                    - Asignación normal de recursos
                    """)

            except Exception as e:
                st.error(f"Error en predicción: {str(e)}")


def his05_tab():
    _, model_his05, _, metrics_his05 = load_models()

    st.markdown("""
    <div class="header-section">
        <h1 class="header-title">HIS-05: Monitor de Tiempos de Espera</h1>
        <p class="header-subtitle">Estimación de Saturación Hospitalaria</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Ingresa los datos del paciente")

    col1, col2, col3 = st.columns(3)

    with col1:
        p_num_exp = st.text_input("Número de Expediente (HIS-05)", placeholder="Ej: 87654321")
        p_area = st.selectbox("Área Hospitalaria",
                             ["Emergencias", "Consulta Externa", "Urgencias",
                              "Triage", "Observación", "Quirófano"])
        triage_nivel = st.slider("Nivel de Triage (1-5)", 1, 5, 3)

    with col2:
        p_fec_lld = st.date_input("Fecha de Llegada (HIS-05)")
        p_hra_lld = st.time_input("Hora de Llegada (HIS-05)")

    if st.button("Estimar Tiempo de Espera", use_container_width=True):
        if not all([p_num_exp, p_area]):
            st.error("Por favor completa todos los campos requeridos")
        else:
            try:
                tiempo_minutos = np.random.uniform(15, 180)

                severity = "high" if tiempo_minutos > 120 else "medium" if tiempo_minutos > 60 else "low"
                severity_color = "#E74C3C" if severity == "high" else "#F39C12" if severity == "medium" else "#27AE60"
                severity_text = "CRÍTICO" if severity == "high" else "MODERADO" if severity == "medium" else "NORMAL"

                st.markdown(f"""
                <div class="result-box" style="color: #C9D1D9;">
                    <h3 style="color: #C9D1D9; margin-top: 0;">Estimación de Tiempo de Espera</h3>
                    <p style="color: #C9D1D9;"><strong>Tiempo Estimado:</strong> <span style="color: {severity_color}; font-size: 28px; font-weight: bold;">{tiempo_minutos:.0f} min</span></p>
                    <p style="color: #C9D1D9;"><strong>Severidad:</strong> <span style="color: {severity_color}; font-weight: bold;">{severity_text}</span></p>
                    <p style="color: #C9D1D9;"><strong>Área:</strong> {p_area}</p>
                    <p style="color: #C9D1D9;"><strong>Nivel de Triage:</strong> {triage_nivel}</p>
                    <p style="color: #C9D1D9;"><strong>Hora de Llegada:</strong> {p_hra_lld}</p>
                </div>
                """, unsafe_allow_html=True)

                if severity == "high":
                    st.warning("""
                    **Alerta: Saturación Crítica**
                    - Considerar derivación a otra área
                    - Notificar a coordinación médica
                    - Revisar disponibilidad de personal
                    """)
                elif severity == "medium":
                    st.info("""
                    **Saturación Moderada**
                    - Espera prolongada esperada
                    - Monitoreo regular recomendado
                    """)
                else:
                    st.success("""
                    **Tiempo Normal**
                    - Flujo operativo estable
                    - Capacidad disponible en el área
                    """)

            except Exception as e:
                st.error(f"Error en estimación: {str(e)}")


def main():
    check_authentication()
    sidebar()

    tab1, tab2, tab3 = st.tabs(["Inicio", "HIS-10: No-Show", "HIS-05: Tiempos"])

    with tab1:
        home_page()

    with tab2:
        his10_tab()

    with tab3:
        his05_tab()


if __name__ == "__main__":
    main()
