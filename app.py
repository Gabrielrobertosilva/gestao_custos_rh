# app.py — Home estilizada (Gestão & Custos RH)
import streamlit as st
from shared.ui import add_brand_style, render_footer, PALETTE

st.set_page_config(page_title="People Analytics - Gestão & Custos", layout="wide")

# ========= CONFIG VISUAL =========
add_brand_style()

# 👉 Troque a URL abaixo por uma imagem corporativa (intranet/drive) se quiser
BG_URL = "https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=1920&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
      /* Fundo com overlay na cor principal (ink) */
      .stApp {{
        background: 
          linear-gradient(rgba(21,37,45,0.80), rgba(21,37,45,0.80))),
          url('{BG_URL}');
        background-size: cover;
        background-position: center;
      }}
      /* container central */
      .hero {{
        max-width: 1100px;
        margin: 4rem auto 2rem auto;
        padding: 2rem 2.5rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(150,223,229,0.25);
        border-radius: 18px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.25);
      }}
      .hero h1, .hero p {{
        color: #FFFFFF;
      }}
      .hero h1 {{
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
      }}
      .hero p {{
        font-size: 1.05rem;
        opacity: 0.95;
        margin: 0.25rem 0 0;
      }}

      /* grid de cards */
      .cards {{
        max-width: 1100px;
        margin: 0 auto 2rem auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 18px;
      }}
      .card {{
        background: #FFFFFF;
        border-radius: 16px;
        padding: 18px 18px;
        border: 1px solid rgba(150,223,229,0.45);
        transition: transform .15s ease, box-shadow .15s ease;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        cursor: pointer;
        text-decoration: none;
      }}
      .card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(0,0,0,0.12);
      }}
      .card h3 {{
        margin: 6px 0 6px 0;
        color: {PALETTE["ink"]};
        font-size: 1.15rem;
      }}
      .card p {{
        margin: 0;
        color: #42545B;
        font-size: 0.98rem;
      }}
      .pill {{
        display: inline-block;
        background: {PALETTE["bg2"]};
        color: {PALETTE["ink"]};
        border: 1px solid {PALETTE["accent"]};
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.85rem;
      }}
    </style>
    """,
    unsafe_allow_html=True
)

# ========= CONTEÚDO =========
st.markdown(
    """
    <div class="hero">
      <span class="pill">Gestão & Custos RH</span>
      <h1>Insights e cálculos para decisões de pessoas</h1>
      <p>Consolide custos de colaboradores e calcule a antecipação de PLR com regras atualizadas.
         Tudo alinhado à sua política e pronto para exportar.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Cards clicáveis – usando st.page_link (Streamlit ≥ 1.31) como call-to-action
col1, col2 = st.columns([1,1], gap="large")
with col1:
    st.page_link("pages/1_📊_Calculadora_de_PLR.py", label="📊 Ir para Calculadora de PLR", icon=":material/analytics:")
with col2:
    st.page_link("pages/2_💸_Calculadora_de_Custos.py", label="💸 Ir para Calculadora de Custos", icon=":material/paid:")

# Cards visuais (clicáveis) em HTML — linka para as mesmas páginas
st.markdown(
    """
    <div class="cards">
      <a class="card" href="/pages/1_%F0%9F%93%8A_Calculadora_de_PLR" target="_self">
        <div class="pill">PLR</div>
        <h3>Calculadora de PLR</h3>
        <p>Antecipação 2025 com caput e parágrafos, teto global/individual e adicional proporcional. Importação de base e export em Excel.</p>
      </a>
      <a class="card" href="/pages/2_%F0%9F%92%B8_Calculadora_de_Custos" target="_self">
        <div class="pill">Custos</div>
        <h3>Calculadora de Custos</h3>
        <p>Detalhamento mensal e anual por colaborador (salário, férias, 13º, PLR mensalizada, benefícios e encargos), com gráfico e export.</p>
      </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Rodapé
render_footer("Gestão & Custos RH", "v2.1")
