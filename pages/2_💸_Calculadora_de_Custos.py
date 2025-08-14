import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from shared.ui import fmt_brl, format_money_cols_for_display, add_brand_style, render_footer

def calcular_detalhado(salario, ajuste_percentual):
    salario_ajustado = salario * (1 + (ajuste_percentual or 0) / 100)
    plr = min(salario_ajustado * 2.2, 37000)
    ferias_12 = salario_ajustado / 12
    um_terco_ferias = ferias_12 / 3
    decimo_terceiro = salario_ajustado / 12
    plr_12 = plr / 12
    va_vr = 2057.92
    assist_medica = 978.00

    base_encargos = salario_ajustado + ferias_12 + um_terco_ferias + decimo_terceiro
    inss = base_encargos * 0.282
    fgts = base_encargos * 0.08

    custo_mensal = salario_ajustado + ferias_12 + um_terco_ferias + decimo_terceiro + plr_12 + va_vr + assist_medica + inss + fgts
    custo_anual = custo_mensal * 12

    return {
        "Salário Ajustado": salario_ajustado,
        "Férias": ferias_12,
        "1/3 Férias": um_terco_ferias,
        "13º": decimo_terceiro,
        "PLR (mensalizada)": plr_12,
        "PLR Anual": plr,
        "VA/VR": va_vr,
        "Assist. Médica": assist_medica,
        "INSS": inss,
        "FGTS": fgts,
        "Total Mensal": custo_mensal,
        "Total Anual": custo_anual
    }

def render_custos():
    st.set_page_config(page_title="Gestão & Custos RH – Calculadora de Custos", layout="wide")
    add_brand_style()
    st.title("💸 Calculadora de Custo do Colaborador")

    if "colaboradores" not in st.session_state:
        st.session_state.colaboradores = []

    # Sidebar – inclusão manual
    st.sidebar.subheader("➕ Adicionar colaborador manualmente")

    # Carrega nomes sugeridos do Excel externo (opcional)
    try:
        nomes_df = pd.read_excel("lista_nomes.xlsx")
        nomes_sugeridos = nomes_df["Nome da Pessoa"].dropna().astype(str).tolist()
    except Exception:
        nomes_sugeridos = []

    if nomes_sugeridos:
        nome_sel = st.sidebar.selectbox("Nome do colaborador", options=nomes_sugeridos + ["Outro"])
        if nome_sel == "Outro":
            nome = st.sidebar.text_input("Digite o nome completo")
        else:
            nome = nome_sel
    else:
        nome = st.sidebar.text_input("Digite o nome do colaborador")

    salario = st.sidebar.number_input("Salário (R$)", min_value=0.0, step=1000.0, format="%.2f")
    ajuste = st.sidebar.number_input("Ajuste de salário (%)", min_value=0.0, step=1.0, format="%.1f")

    if st.sidebar.button("Adicionar colaborador"):
        if nome:
            novo_colab = {"Nome": nome, "Salário Base": salario, "Ajuste (%)": ajuste}
            if novo_colab not in st.session_state.colaboradores:
                st.session_state.colaboradores.append(novo_colab)
            else:
                st.sidebar.warning("Esse colaborador já foi adicionado.")
        else:
            st.sidebar.warning("Por favor, insira o nome do colaborador.")

    # Upload
    st.subheader("📄 Ou envie uma planilha Excel com os dados")
    st.markdown("Exemplo de colunas esperadas na planilha:")
    st.dataframe(pd.DataFrame({
        "Nome": ["João Silva", "Maria Souza"],
        "Salário Base": [12000, 9500],
        "Ajuste (%)": [5, 0]
    }))

    arquivo = st.file_uploader("Importar colaboradores (xlsx)", type=["xlsx"])
    if arquivo:
        df_upload = pd.read_excel(arquivo)
        obrigatorias = {"Nome", "Salário Base", "Ajuste (%)"}
        if obrigatorias.issubset(set(df_upload.columns)):
            novos = df_upload[["Nome", "Salário Base", "Ajuste (%)"]].to_dict(orient="records")
            for novo in novos:
                if novo not in st.session_state.colaboradores:
                    st.session_state.colaboradores.append(novo)
            st.success("Colaboradores importados com sucesso!")
        else:
            st.error(f"A planilha deve conter as colunas: {obrigatorias}")

    # Detalhamento por colaborador
    st.subheader("📋 Detalhamento do custo por colaborador")
    colaboradores_processados = []
    i = 0
    while i < len(st.session_state.colaboradores):
        colab = st.session_state.colaboradores[i]
        resultado = calcular_detalhado(colab["Salário Base"], colab["Ajuste (%)"])
        colab_resultado = {**colab, **resultado}
        colaboradores_processados.append(colab_resultado)

        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(
                f"**{colab['Nome']}** – Total Mensal: **{fmt_brl(resultado['Total Mensal'])}** "
                f"| Total Anual: **{fmt_brl(resultado['Total Anual'])}**"
            )
        with col2:
            if st.button("➖", key=f"excluir_{i}"):
                del st.session_state.colaboradores[i]
                st.experimental_rerun()
                return
        i += 1

    # Tabela com totais
    if colaboradores_processados:
        df_final = pd.DataFrame(colaboradores_processados)

        # Linha de totalização
        total_row = {}
        for col in df_final.columns:
            if pd.api.types.is_numeric_dtype(df_final[col]):
                total_row[col] = df_final[col].sum()
            else:
                total_row[col] = "Total Geral"
        df_tabela = pd.concat([df_final, pd.DataFrame([total_row])], ignore_index=True)

        # Formatação BRL só na UI
        money_cols = [
            "Salário Base", "Salário Ajustado", "Férias", "1/3 Férias", "13º",
            "PLR (mensalizada)", "PLR Anual", "VA/VR", "Assist. Médica",
            "INSS", "FGTS", "Total Mensal", "Total Anual"
        ]
        df_formatado = format_money_cols_for_display(df_tabela, money_cols)

        def highlight_total(s):
            return ['font-weight: bold' if s.name == len(df_formatado) - 1 else '' for _ in s]

        st.dataframe(df_formatado.style.apply(highlight_total, axis=1), use_container_width=True)

        # Gráfico
        st.subheader("📊 Distribuição do custo total da equipe")
        resumo = df_final[[
            "Salário Ajustado", "Férias", "1/3 Férias", "13º",
            "PLR (mensalizada)", "VA/VR", "Assist. Médica", "INSS", "FGTS"
        ]].sum()

        fig, ax = plt.subplots(figsize=(8, 4))
        resumo.sort_values().plot(kind="barh", ax=ax)
        ax.set_title("Distribuição do custo total por componente")
        ax.set_xlabel("Custo (R$)")
        ax.set_ylabel("Componente")
        ax.grid(axis="x", linestyle="--", alpha=0.7)
        st.pyplot(fig)

        # Exportação (números puros)
        st.subheader("⬇️ Exportar resultado")
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df_final.to_excel(writer, index=False, sheet_name="Custo por Colaborador")
        st.download_button("📥 Baixar Excel", data=buffer.getvalue(), file_name="custo_colaboradores.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("Adicione colaboradores manualmente ou importe uma planilha para começar.")

    render_footer("Gestão & Custos RH", "v2.0")

if __name__ == "__main__":
    render_custos()
