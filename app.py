import streamlit as st
from shared.ui import add_brand_style, render_footer

st.set_page_config(page_title="Gestão & Custos RH – Suite", layout="wide")
add_brand_style()

st.title("Gestão & Custos RH")
st.caption("Use o menu (à esquerda) para acessar as calculadoras.")

st.markdown("""
- 📊 **Calculadora de PLR** — Antecipação 2025 - Diretrizes da CCT 2025.
- 💸 **Calculadora de Custos** — Custo mensal/anual por colaborador.
""")

render_footer("Gestão & Custos RH", "v2.0")
