# app.py — Home refinada com botões estilizados
import streamlit as st
from shared.ui import add_brand_style, render_footer, PALETTE

st.set_page_config(page_title="People Analytics - Gestão & Custos", layout="wide")
add_brand_style()

# ======== FUNDO ========
BG_URL = "https://cdn.prod.website-files.com/65172cb208ef8ecb7765b47f/657071ee0f5e2868cd0c9228_Ouribank-credito-e-garantias-open-graph-p-800.webp"

st.markdown(
    f"""
    <style>
      .stApp {{
        min-height: 100vh;
        background:
          linear-gradient(rgba(21,37,45,0.80), rgba(21,37,45,0.80)),
          url('{BG_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
      }}
      .hero {{
        max-width: 1100px;
        margin: 4rem auto 2rem auto;
        padding: 2rem 2.5rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(150,223,229,0.25);
        border-radius: 18px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.25);
      }}
      .hero h1 {{ color: #FFFFFF; font-size: 2.6rem; margin-bottom: 0.3rem; }}
      .hero p {{ color: #FFFFFF; font-size: 1.05rem; opacity: 0.85; margin: 0; }}

      /* Cartão */
      .card {{
        background: #FFFFFF;
        border-radius: 16px;
        padding: 18px;
        border: 1px solid rgba(150,223,229,0.45);
        transition: transform .15s ease, box-shadow .15s ease;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        min-height: 170px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
      }}
      .card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 28px rgba(0,0,0,0.12); }}
      .card h3 {{ margin: 6px 0 6px 0; color: {PALETTE["ink"]}; font-size: 1.2rem; }}
      .card p {{ margin: 0; color: #42545B; font-size: 1.0rem; }}
      .pill {{
        display: inline-block;
        background: {PALETTE["bg2"]};
        color: {PALETTE["ink"]};
        border: 1px solid {PALETTE["accent"]};
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.9rem;
      }}

      /* Botão customizado */
      .custom-btn {{
        display: block;
        width: 100%;
        padding: 0.6rem;
        text-align: center;
        background-color: #96DFE5;
        color: #15252D;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: background-color 0.2s ease;
        text-decoration: none;
      }}
      .custom-btn:hover {{
        background-color: #7CD2D9;
      }}
    </style>
    """,
    unsafe_allow_html=True
)

# ======== HERO ========
st.markdown(
    """
    <div class="hero">
      <span class="pill">People Analytics - Gestão & Custos</span>
      <h1>People Analytics — Gestão & Custos</h1>
      <p>Insights e cálculos para decisões estratégicas em RH.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======== CARDS + BOTÕES ========
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        """
        <div class="card">
          <div class="pill">PLR</div>
          <h3>Calculadora de PLR</h3>
          <p>Antecipação 2025 com caput e parágrafos, teto global/individual e adicional proporcional. Importação de base e export em Excel.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)  # espaço
    st.markdown(
        "<a class='custom-btn' href='pages/1_📊_Calculadora_de_PLR.py'>📊 Abrir Calculadora de PLR</a>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="card">
          <div class="pill">Custos</div>
          <h3>Calculadora de Custos</h3>
          <p>Custo mensal e anual por colaborador: salário, 13º, férias, PLR mensalizada, benefícios e encargos. Inclui gráfico e exportação.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)  # espaço
    st.markdown(
        "<a class='custom-btn' href='pages/2_💸_Calculadora_de_Custos.py'>💸 Abrir Calculadora de Custos</a>",
        unsafe_allow_html=True
    )

# ======== RODAPÉ ========
render_footer("People Analytics - Gestão & Custos", "v2.4")
