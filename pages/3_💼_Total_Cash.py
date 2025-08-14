import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from shared.ui import add_brand_style, render_footer, fmt_brl

def anualizar_beneficios(va_vr_mensal=0.0, outros_benef_mensais=0.0, subsidio_saude_mensal=0.0):
    return 12 * (float(va_vr_mensal or 0) + float(outros_benef_mensais or 0) + float(subsidio_saude_mensal or 0))

def calcular_total_cash(
    salario_mensal,
    plr_valor=0.0,
    plr_pct_sobre_salario=0.0,
    usar_plr_valor=True,
    va_vr_mensal=0.0,
    outros_benef_mensais=0.0,
    subsidio_saude_mensal=0.0,
    premio_pontual=0.0,
    stock_anuais=0.0
):
    salario_mensal = float(salario_mensal or 0)
    fixo_anual = 12 * salario_mensal
    decimo_terceiro = salario_mensal
    um_terco_ferias = salario_mensal / 3.0

    if usar_plr_valor:
        plr_anual = float(plr_valor or 0)
    else:
        plr_anual = (float(plr_pct_sobre_salario or 0) / 100.0) * fixo_anual

    beneficios_anual = anualizar_beneficios(va_vr_mensal, outros_benef_mensais, subsidio_saude_mensal)

    total_cash = fixo_anual + decimo_terceiro + um_terco_ferias + plr_anual + beneficios_anual + float(premio_pontual or 0) + float(stock_anuais or 0)

    breakdown = {
        "Fixo (12×)": fixo_anual,
        "13º": decimo_terceiro,
        "1/3 Férias": um_terco_ferias,
        "PLR/Bonus": plr_anual,
        "Benefícios (anual)": beneficios_anual,
        "Premiação Pontual": float(premio_pontual or 0),
        "Ações/RSUs (ano)": float(stock_anuais or 0),
        "Total Cash Anual": total_cash
    }
    return breakdown

def bloco_inputs(titulo: str, key_prefix: str):
    st.markdown(f"### {titulo}")
    col1, col2, col3 = st.columns(3)
    with col1:
        sal = st.number_input("Salário mensal (R$)", min_value=0.0, step=100.0, key=f"{key_prefix}_sal")
        usar_valor = st.radio("PLR/Bonus", ["Informar valor anual", "Informar % do salário anual"], key=f"{key_prefix}_plrmodo")
        plr_valor = st.number_input("PLR/Bonus anual (R$)", min_value=0.0, step=500.0, key=f"{key_prefix}_plrvalor")
        plr_pct   = st.number_input("PLR/Bonus (% do salário anual)", min_value=0.0, step=5.0, key=f"{key_prefix}_plrpct")
    with col2:
        va_vr = st.number_input("VA/VR mensal (R$)", min_value=0.0, step=50.0, key=f"{key_prefix}_vavr")
        outros = st.number_input("Outros benefícios mensais (R$)", min_value=0.0, step=50.0, key=f"{key_prefix}_outros")
        saude = st.number_input("Subsídio saúde mensal (R$)", min_value=0.0, step=50.0, key=f"{key_prefix}_saude")
    with col3:
        signon = st.number_input("Premiação pontual / Sign-on (R$)", min_value=0.0, step=500.0, key=f"{key_prefix}_signon")
        stocks = st.number_input("Ações/RSUs anualizadas (R$)", min_value=0.0, step=1000.0, key=f"{key_prefix}_stocks")

    usar_plr_valor = (usar_valor == "Informar valor anual")
    return {
        "sal": sal, "usar_plr_valor": usar_plr_valor, "plr_valor": plr_valor, "plr_pct": plr_pct,
        "va_vr": va_vr, "outros": outros, "saude": saude, "signon": signon, "stocks": stocks
    }

def render_total_cash():
    st.set_page_config(page_title="People Analytics - Gestão & Custos – Total Cash", layout="wide")
    add_brand_style()
    st.title("💼 Total Cash do Colaborador")
    st.caption("Compare duas propostas (A vs B) somando fixo, 13º, 1/3 de férias, PLR/bonus, benefícios anualizados e prêmios pontuais.")

    tab_calc, tab_export = st.tabs(["Simulação e Comparativo", "Exportação"])

    with tab_calc:
        st.subheader("Parâmetros das propostas")
        colA, colB = st.columns(2, gap="large")
        with colA:
            inputsA = bloco_inputs("Oferta A", "A")
        with colB:
            inputsB = bloco_inputs("Oferta B", "B")

        if st.button("Calcular Comparativo", type="primary", use_container_width=True, key="btn_calc_tc"):
            A = calcular_total_cash(
                salario_mensal=inputsA["sal"],
                plr_valor=inputsA["plr_valor"],
                plr_pct_sobre_salario=inputsA["plr_pct"],
                usar_plr_valor=inputsA["usar_plr_valor"],
                va_vr_mensal=inputsA["va_vr"],
                outros_benef_mensais=inputsA["outros"],
                subsidio_saude_mensal=inputsA["saude"],
                premio_pontual=inputsA["signon"],
                stock_anuais=inputsA["stocks"]
            )
            B = calcular_total_cash(
                salario_mensal=inputsB["sal"],
                plr_valor=inputsB["plr_valor"],
                plr_pct_sobre_salario=inputsB["plr_pct"],
                usar_plr_valor=inputsB["usar_plr_valor"],
                va_vr_mensal=inputsB["va_vr"],
                outros_benef_mensais=inputsB["outros"],
                subsidio_saude_mensal=inputsB["saude"],
                premio_pontual=inputsB["signon"],
                stock_anuais=inputsB["stocks"]
            )

            # Métricas
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Cash A", fmt_brl(A["Total Cash Anual"]))
            c2.metric("Total Cash B", fmt_brl(B["Total Cash Anual"]))
            diff = B["Total Cash Anual"] - A["Total Cash Anual"]
            c3.metric("Diferença (B − A)", fmt_brl(diff), delta=None)

            # Tabela detalhada
            df = pd.DataFrame({
                "Componente": [k for k in A.keys() if k != "Total Cash Anual"] + ["Total Cash Anual"],
                "Oferta A":   [v for k, v in A.items()],
                "Oferta B":   [v for k, v in B.items()]
            })
            # garantir a ordem (Fixo... Total)
            ordem = ["Fixo (12×)", "13º", "1/3 Férias", "PLR/Bonus", "Benefícios (anual)", "Premiação Pontual", "Ações/RSUs (ano)", "Total Cash Anual"]
            df["ord"] = df["Componente"].apply(lambda x: ordem.index(x) if x in ordem else 999)
            df = df.sort_values("ord").drop(columns=["ord"]).reset_index(drop=True)

            df_fmt = df.copy()
            for col in ["Oferta A", "Oferta B"]:
                df_fmt[col] = df_fmt[col].apply(fmt_brl)
            st.dataframe(df_fmt, use_container_width=True)

            # Gráfico comparativo (matplotlib, sem escolher cores explicitamente)
            resumo = df[df["Componente"] != "Total Cash Anual"].set_index("Componente")
            fig, ax = plt.subplots(figsize=(8, 4))
            resumo.plot(kind="barh", ax=ax)
            ax.set_title("Comparativo por componente (A vs B)")
            ax.set_xlabel("R$ (anual)")
            ax.set_ylabel("")
            ax.grid(axis="x", linestyle="--", alpha=0.6)
            st.pyplot(fig)

            # Guardar em sessão para export
            st.session_state.tc_last_result = df

        else:
            st.info("Preencha os dados das duas ofertas e clique em **Calcular Comparativo**.")

    with tab_export:
        st.subheader("Exportação do comparativo")
        if "tc_last_result" in st.session_state:
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                st.session_state.tc_last_result.to_excel(writer, index=False, sheet_name="TotalCash_Comparativo")
            st.download_button(
                "📥 Baixar Excel (comparativo)",
                data=output.getvalue(),
                file_name="TotalCash_Comparativo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Faça um cálculo na aba anterior para habilitar a exportação.")

    render_footer("People Analytics - Gestão & Custos", "v3.0")

if __name__ == "__main__":
    render_total_cash()
