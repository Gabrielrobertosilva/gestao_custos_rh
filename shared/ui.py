import streamlit as st
import pandas as pd
from datetime import date

PALETTE = {
    "ink": "#15252D",
    "accent": "#96DFE5",
    "bg": "#FFFFFF",
    "bg2": "#F3FBFC",
}

def fmt_brl(x) -> str:
    """Formata valor numérico como BRL pt-BR: R$ 6.485,86."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "R$ 0,00"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_money_cols_for_display(df: pd.DataFrame, cols):
    df2 = df.copy()
    for c in cols:
        if c in df2.columns:
            df2[c] = df2[c].apply(fmt_brl)
    return df2

def add_brand_style():
    """CSS leve para refinar elementos com a paleta."""
    st.markdown(f"""
    <style>
      h1, h2, h3, h4, h5, h6 {{ color: {PALETTE["ink"]}; }}
      div[data-testid="stMetricValue"] {{ color: {PALETTE["ink"]}; }}
      .stButton>button {{
        border-radius: 10px;
        border: 1px solid {PALETTE["accent"]};
      }}
      .stDataFrame thead tr th {{ background: {PALETTE["bg2"]} !important; color: {PALETTE["ink"]} !important; }}
      .stTextInput>div>div>input, .stNumberInput input {{ border-radius: 8px !important; }}
    </style>
    """, unsafe_allow_html=True)

def render_footer(app_name: str, version: str = "v1.0"):
    st.markdown(
        f'<div style="text-align:center;color:{PALETTE["ink"]};opacity:0.7; margin-top:24px;">'
        f'{app_name} • {version} • {date.today().strftime("%d/%m/%Y")}'
        f'</div>',
        unsafe_allow_html=True
    )
