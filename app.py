import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

st.set_page_config(
    page_title="TCA Software Solutions",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("TCA Software Solutions")
st.write("Aplicación funcionando correctamente")

st.info("La app está lista para usar")
