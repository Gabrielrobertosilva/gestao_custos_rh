# app.py — Home estilizada (People Analytics - Gestão & Custos)
import streamlit as st
from shared.ui import add_brand_style, render_footer, PALETTE

st.set_page_config(page_title="People Analytics - Gestão & Custos", layout="wide")

# ========= CONFIG VISUAL =========
add_brand_style()

# Imagem de fundo (use uma URL https pública ou troque por outra de sua preferência)
BG_URL = "https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=1920&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
      /* Fundo com overlay na cor #15252D (ink) – corrigido e com altura total */
      .stApp {{
        min-height: 100vh;
        background:
          linear-gradient(rgba(21,37,45,0.80), rgba(21,37,45,0.80)),
          url('{BG_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
      }}
      /* container central (hero) */
      .hero {{
        max-width: 1100px;
        margin: 4rem auto 2rem auto;
        padding: 2rem 2.5rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(150,223,229,0.25);
        border-radius: 18px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.25);
      }}
      .hero h1, .hero p {{ color: #FFFFFF; }}
      .hero h1 {{ font-size: 2.2rem; margin-bottom: 0.5rem; }}
      .hero p {{ font-size: 1.05rem; opacity: 0.95; margin: 0.25rem 0 0; }}

      /* grid de cards visuais */
      .cards {{
        max-width: 1100px;
        margin: 0 auto 0.5rem auto;
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
      }}
      .card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 28px rgba(0,0,0,0.12); }}
      .card h3 {{ margin: 6px 0 6px 0; color: {PALETTE["ink"]}; font-size: 1.15rem; }}
      .card p {{ margin: 0; color: #42545B; font-size: 0.98rem; }}
      .pill {{
        display: inline-block; background: {PALETTE["bg2"]}; color: {PALETTE["ink"]};
        border: 1px solid {PALETTE["accent"]}; border-radius: 999px; padding: 4px 10px; font-size: 0.85rem;
      }}
    </style>
    """,
    unsafe_allow_html=True
)

# ========= CONTEÚDO =========
st.markdown(
    """
    <div class="hero">
      <span class="pill">People Analytics - Gestão & Custos</span>
      <h1>Insights e cálculos para decisões de pessoas</h1>
      <p>Consolide custos de colaboradores e calcule a antecipação de PLR com regras atualizadas.
         Tudo alinhado à política interna e pronto para exportar.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Cards visuais (apenas apresentação)
st.markdown(
    """
    <div class="cards">
      <div class="card">
        <div class="pill">PLR</div>
        <h3>Calculadora de PLR</h3>
        <p>Antecipação 2025 (caput e parágrafos), teto global/individual e adicional proporcional. Importação e exportação em Excel.</p>
      </div>
      <div class="card">
        <div class="pill">Custos</div>
        <h3>Calculadora de Custos</h3>
        <p>Detalhamento mensal e anual por colaborador (salário, férias, 13º, PLR mensalizada, benefícios e encargos), com gráfico e export.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Navegação confiável por botões → switch_page
c1, c2 = st.columns([1, 1], gap="large")
with c1:
    if st.button("📊 Ir para Calculadora de PLR", type="primary", use_container_width=True):
        st.switch_page("pages/1_📊_Calculadora_de_PLR.py")
with c2:
    if st.button("💸 Ir para Calculadora de Custos", type="primary", use_container_width=True):
        st.switch_page("pages/2_💸_Calculadora_de_Custos.py")

# (Opcional) Links extras no rodapé usando page_link (se preferir)
# st.page_link("pages/1_📊_Calculadora_de_PLR.py", label="Ir para PLR")
# st.page_link("pages/2_💸_Calculadora_de_Custos.py", label="Ir para Custos")

render_footer("People Analytics - Gestão & Custos", "v2.2")
