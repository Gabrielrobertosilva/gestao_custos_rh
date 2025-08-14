import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from shared.ui import fmt_brl, format_money_cols_for_display, add_brand_style, render_footer

def render_plr():
    st.set_page_config(page_title="Gestão & Custos RH – Calculadora de PLR", layout="wide")
    add_brand_style()

    REQUIRED_COLS = [
        "Matricula", "Nome", "Cargo",
        "Salario",
        "Data_Admissao", "Data_Desligamento",
        "Diretoria", "Centro_Custo",
        "Valor_Pago_2025", "Motivo_Afastamento", "Conta_Ativa"
    ]
    DERIVED_COLS = ["Salario_Base", "Verbas_Fixas_Salariais"]
    DEFAULTS = {
        "Salario": 0.0,
        "Data_Desligamento": None,
        "Diretoria": "",
        "Centro_Custo": "",
        "Valor_Pago_2025": 0.0,
        "Motivo_Afastamento": "nenhum",
        "Conta_Ativa": "sim",
    }

    if "manual_df_plr" not in st.session_state:
        st.session_state.manual_df_plr = pd.DataFrame(columns=REQUIRED_COLS + DERIVED_COLS)
    if "data_assinatura_cct_plr" not in st.session_state:
        st.session_state.data_assinatura_cct_plr = pd.to_datetime("2025-09-01").date()

    def ensure_required_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = df.columns.str.strip()
        if "Salario" not in df.columns:
            if ("Salario_Base" in df.columns) and ("Verbas_Fixas_Salariais" in df.columns):
                df["Salario"] = pd.to_numeric(df["Salario_Base"], errors="coerce").fillna(0.0) + \
                                pd.to_numeric(df["Verbas_Fixas_Salariais"], errors="coerce").fillna(0.0)
            else:
                df["Salario"] = 0.0
        for col in REQUIRED_COLS:
            if col not in df.columns:
                df[col] = DEFAULTS.get(col, np.nan)
        df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce").fillna(0.0)
        df["Valor_Pago_2025"] = pd.to_numeric(df.get("Valor_Pago_2025", 0.0), errors="coerce").fillna(0.0)
        for c in ["Data_Admissao", "Data_Desligamento"]:
            df[c] = pd.to_datetime(df[c], errors="coerce")
        df["Salario_Base"] = df["Salario"] / 1.55
        df["Verbas_Fixas_Salariais"] = df["Salario_Base"] * 0.55
        return df

    st.sidebar.title("PLR – Parâmetros Globais")
    ano_ref = st.sidebar.selectbox("Ano de referência", options=list(range(2023, 2031)), index=2)
    data_assinatura_cct = st.sidebar.date_input(
        "Data de assinatura da CCT",
        value=st.session_state.data_assinatura_cct_plr,
        help="Usada nas regras de elegibilidade do caput e dos parágrafos."
    )
    st.session_state.data_assinatura_cct_plr = data_assinatura_cct

    st.sidebar.subheader("Antecipação PLR 2025")
    lucro_liquido_1s2025 = st.sidebar.number_input(
        "Lucro líquido 1º semestre/2025 (BRL)",
        min_value=0.0, value=0.0, step=100000.0,
        help="Base do teto global (12,8%) e da parcela adicional (2,2%)."
    )
    compensar_planos_proprios = st.sidebar.checkbox(
        "Compensar valores já pagos em 2025 (Regra Básica)", value=False
    )

    st.title("📊 Calculadora de PLR – Antecipação 2025")
    st.caption("Regra de antecipação (caput + §1º–§4º) com adicional e seu teto individual proporcionais aos meses/12.")

    aba_base, aba_calc, aba_export = st.tabs(["Base (Manual/Upload)", "Apuração", "Exportação"])

    with aba_base:
        st.subheader("Cadastro da Base: Manual ou Upload")

        dedup_toggle = st.checkbox("Remover duplicatas por Matrícula (manter a última)", value=True)
        modo = st.radio("Como deseja informar os dados?", ["Cadastro manual", "Upload (CSV/Excel)"])

        if modo == "Cadastro manual":
            with st.form("form_manual_plr"):
                colA, colB, colC = st.columns(3)
                with colA:
                    matricula = st.text_input("Matrícula")
                    nome = st.text_input("Nome")
                    cargo = st.text_input("Cargo")
                    diretoria = st.text_input("Diretoria")
                with colB:
                    salario = st.number_input("Salário (total)", min_value=0.0, step=100.0, key="sal_plr")
                    cc = st.text_input("Centro de Custo")
                    valor_pago = st.number_input("Valor já pago em 2025 (compensação)", min_value=0.0, step=50.0)
                with colC:
                    dt_adm = st.date_input("Data de admissão")
                    dt_desl = st.date_input("Data de desligamento (se houver)", value=None)
                    motivo = st.selectbox("Motivo de afastamento", ["nenhum", "doença", "acidente", "licença-maternidade"])
                    conta_ativa = st.selectbox("Conta corrente ativa no banco?", ["sim", "não"])
                substituir = st.checkbox("Substituir se Matrícula já existir", value=True)
                add = st.form_submit_button("Adicionar à base")

            if add:
                if not matricula:
                    st.error("Informe a Matrícula antes de adicionar.")
                else:
                    nova = {
                        "Matricula": matricula,
                        "Nome": nome,
                        "Cargo": cargo,
                        "Salario": salario,
                        "Data_Admissao": pd.to_datetime(dt_adm),
                        "Data_Desligamento": pd.to_datetime(dt_desl) if dt_desl else None,
                        "Diretoria": diretoria,
                        "Centro_Custo": cc,
                        "Valor_Pago_2025": valor_pago,
                        "Motivo_Afastamento": motivo,
                        "Conta_Ativa": conta_ativa,
                    }
                    df = st.session_state.manual_df_plr.copy()
                    if substituir and "Matricula" in df.columns:
                        df = df[df["Matricula"] != matricula]
                    st.session_state.manual_df_plr = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)

            st.markdown("### Base (Cadastro manual)")
            st.session_state.manual_df_plr = ensure_required_columns(st.session_state.manual_df_plr)
            st.session_state.manual_df_plr = st.data_editor(
                st.session_state.manual_df_plr,
                num_rows="dynamic",
                use_container_width=True,
                key="editor_manual_plr"
            )

            tmpl = pd.DataFrame(columns=REQUIRED_COLS)
            csv_bytes = tmpl.to_csv(index=False).encode("utf-8")
            st.download_button("Baixar template CSV", data=csv_bytes, file_name="template_plr.csv", mime="text/csv")

            base = st.session_state.manual_df_plr.copy()

        else:
            st.markdown("Faça upload do arquivo com as colunas mínimas exigidas (use o template, se possível).")
            up = st.file_uploader("CSV ou Excel (UTF-8)", type=["csv", "xlsx"], key="up_plr")

            if up is None:
                base = pd.DataFrame(columns=REQUIRED_COLS)
                st.info("Nenhum arquivo carregado. A base está vazia (você pode usar o cadastro manual).")
            else:
                if up.name.endswith(".csv"):
                    base = pd.read_csv(up)
                else:
                    base = pd.read_excel(up)

            base = ensure_required_columns(base)
            st.dataframe(base, use_container_width=True)

        if dedup_toggle and "Matricula" in base.columns:
            base = base.drop_duplicates(subset=["Matricula"], keep="last").reset_index(drop=True)

        must_have = ["Matricula", "Nome", "Salario", "Data_Admissao"]
        faltantes = [c for c in must_have if base[c].isna().all()]
        if faltantes:
            st.warning(f"Estas colunas estão vazias na base: {faltantes}. Preencha/edite antes de apurar.")

    # ======= ELEGIBILIDADE =======
    def calcular_proporcionalidade_especial(row, data_assinatura):
        admissao = pd.to_datetime(row.get("Data_Admissao"), errors="coerce")
        desligamento_raw = row.get("Data_Desligamento")
        if pd.isna(admissao):
            return 0.0, "Dados insuficientes (sem Data_Admissao)", 0.0
        if pd.isna(desligamento_raw) or desligamento_raw in (None, "", "nan"):
            desligamento = None
        else:
            desligamento = pd.to_datetime(desligamento_raw, errors="coerce")
            if pd.isna(desligamento):
                desligamento = None
        motivo = str(row.get("Motivo_Afastamento", "")).lower().strip()
        if motivo == "licenca-maternidade":
            motivo = "licença-maternidade"
        assinatura = pd.to_datetime(data_assinatura)

        def meses_12avos(inicio, fim):
            """
            Conta 1/12 por mês com fração >= 15 dias,
            MAS o mês de admissão só conta se o dia da admissão for <= 15.
            """
            if pd.isna(inicio) or pd.isna(fim) or inicio > fim:
                return 0.0
            total = 0
            cur = pd.Timestamp(year=inicio.year, month=inicio.month, day=1)
            end = pd.Timestamp(year=fim.year, month=fim.month, day=1)
            while cur <= end:
                mes_ini = cur
                mes_fim = (cur + pd.offsets.MonthEnd(0))
                seg_ini = max(inicio, mes_ini)
                seg_fim = min(fim, mes_fim)
                dias = (seg_fim - seg_ini).days + 1
                conta_mes = False
                if (cur.year == inicio.year) and (cur.month == inicio.month):
                    if inicio.day <= 15 and dias >= 15:
                        conta_mes = True
                else:
                    if dias >= 15:
                        conta_mes = True
                if conta_mes:
                    total += 1
                cur = cur + pd.offsets.MonthBegin(1)
            return min(12.0, float(total))

        # §1º
        if (admissao <= pd.Timestamp("2024-12-31")) and (motivo in ["doença", "acidente", "licença-maternidade"]) and (desligamento is None or desligamento > assinatura):
            return 1.0, "§1º – Admitido até 31/12/2024 com afastamento coberto; ativo na assinatura (integral).", 12.0
        # §2º
        if (admissao >= pd.Timestamp("2025-01-01")) and (desligamento is None or desligamento > assinatura):
            meses = meses_12avos(admissao, pd.Timestamp("2025-12-31"))
            prop = float(meses / 12.0)
            return prop, f"§2º – Admitido em 2025; proporcional {meses:.0f}/12 até 31/12/2025.", meses
        # §3º
        if (desligamento is not None) and (pd.Timestamp("2025-08-02") <= desligamento <= assinatura):
            meses = meses_12avos(admissao, desligamento)
            prop = float(meses / 12.0)
            return prop, f"§3º – Dispensado sem justa causa entre 02/08/2025 e assinatura; proporcional {meses:.0f}/12.", meses
        # CAPUT
        if (desligamento is None) or (desligamento > assinatura):
            return 1.0, "Caput – Empregado ativo na data da assinatura (integral).", 12.0
        # §4º
        return 0.0, "§4º – Não elegível.", 0.0

    with aba_calc:
        st.subheader("Apuração – Antecipação 2025")
        calcular = st.button("Calcular Antecipação", type="primary", key="calc_plr")
        if not calcular:
            st.info("Preencha o sidebar e a base, depois clique em **Calcular Antecipação**.")
        else:
            if base.empty:
                st.warning("Nenhuma base carregada ou cadastrada. Use a aba 'Base (Manual/Upload)'.")
            else:
                FIXO_BASICA = 2005.82
                LIMITE_BASICA_INDIV = 10760.26
                PCT_LUCRO_BASICA = 0.128
                PCT_LUCRO_ADIC   = 0.022
                LIMITE_ADIC_INDIV = 3471.13

                base_calc = ensure_required_columns(base)
                trip = base_calc.apply(lambda r: calcular_proporcionalidade_especial(r, data_assinatura_cct), axis=1)
                base_calc["Proporcionalidade"] = trip.apply(lambda x: x[0])
                base_calc["Motivo_Elegibilidade"] = trip.apply(lambda x: x[1])
                base_calc["Meses_Contabilizados"] = trip.apply(lambda x: x[2])
                base_calc["Elegivel"] = np.where(base_calc["Proporcionalidade"] > 0, "Sim", "Não")

                elegiveis = base_calc[base_calc["Proporcionalidade"] > 0].copy()
                if "Matricula" in elegiveis.columns:
                    elegiveis = elegiveis.drop_duplicates(subset=["Matricula"], keep="last")
                n_elegiveis = int(elegiveis.shape[0])

                if n_elegiveis == 0:
                    st.warning("Nenhum colaborador elegível pelas regras (caput/§§). Confira datas e motivos de afastamento.")
                else:
                    elegiveis["Base_PLR_Basica"] = (0.54 * elegiveis["Salario"].astype(float) + FIXO_BASICA) * elegiveis["Proporcionalidade"]
                    elegiveis["Basica_Indiv_Cap"] = elegiveis["Base_PLR_Basica"].clip(upper=LIMITE_BASICA_INDIV)

                    total_basica_pre_cap = float(elegiveis["Basica_Indiv_Cap"].sum())
                    limite_global_basica = PCT_LUCRO_BASICA * float(lucro_liquido_1s2025)
                    fator_cap = 1.0
                    if limite_global_basica == 0:
                        st.warning("O lucro 1S/2025 está 0. O teto global (12,8%) zera a Regra Básica.")
                    if limite_global_basica > 0 and total_basica_pre_cap > limite_global_basica:
                        fator_cap = limite_global_basica / total_basica_pre_cap
                    elegiveis["Basica_Pos_Global"] = elegiveis["Basica_Indiv_Cap"] * fator_cap

                    if st.sidebar.checkbox("Compensar valores já pagos em 2025 (Regra Básica)", value=compensar_planos_proprios, key="cmp_plr"):
                        pagos = elegiveis["Valor_Pago_2025"].astype(float).fillna(0.0)
                        elegiveis["Basica_Final"] = (elegiveis["Basica_Pos_Global"] - pagos).clip(lower=0.0)
                    else:
                        elegiveis["Basica_Final"] = elegiveis["Basica_Pos_Global"]

                    pool_adic = PCT_LUCRO_ADIC * float(lucro_liquido_1s2025)
                    if pool_adic == 0:
                        st.warning("O lucro 1S/2025 está 0. A Parcela Adicional (2,2%) será 0.")
                    soma_props = float(elegiveis["Proporcionalidade"].sum())
                    if soma_props > 0:
                        elegiveis["Adicional_Base"] = pool_adic * (elegiveis["Proporcionalidade"] / soma_props)
                    else:
                        elegiveis["Adicional_Base"] = 0.0
                    elegiveis["Teto_Adic_Proporcional"] = LIMITE_ADIC_INDIV * elegiveis["Proporcionalidade"].clip(lower=0.0, upper=1.0)
                    elegiveis["Adicional_Final"] = np.minimum(elegiveis["Adicional_Base"], elegiveis["Teto_Adic_Proporcional"])

                    base_calc = base_calc.drop_duplicates(subset=["Matricula"], keep="last")
                    base_calc = base_calc.merge(
                        elegiveis[[
                            "Matricula", "Basica_Final",
                            "Adicional_Base", "Teto_Adic_Proporcional", "Adicional_Final",
                            "Basica_Pos_Global", "Basica_Indiv_Cap", "Base_PLR_Basica"
                        ]],
                        on="Matricula", how="left"
                    )
                    for col in ["Basica_Final", "Adicional_Final", "Adicional_Base", "Teto_Adic_Proporcional",
                                "Basica_Pos_Global", "Basica_Indiv_Cap", "Base_PLR_Basica"]:
                        base_calc[col] = base_calc[col].fillna(0.0)
                    base_calc["PLR_Antecipacao_Total"] = base_calc["Basica_Final"] + base_calc["Adicional_Final"]

                    total_basica_final = base_calc["Basica_Final"].sum()
                    total_adicional_final = base_calc["Adicional_Final"].sum()
                    total_antecipacao = base_calc["PLR_Antecipacao_Total"].sum()

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Elegíveis", f"{n_elegiveis}")
                    c2.metric("Total Regra Básica (após cap)", fmt_brl(total_basica_final))
                    c3.metric("Total Parcela Adicional (pós cap indiv.)", fmt_brl(total_adicional_final))
                    c4.metric("Antecipação Total", fmt_brl(total_antecipacao))

                    st.markdown("### Resultado por Colaborador")
                    money_cols = [
                        "Salario", "Base_PLR_Basica", "Basica_Indiv_Cap", "Basica_Pos_Global", "Basica_Final",
                        "Adicional_Base", "Teto_Adic_Proporcional", "Adicional_Final", "PLR_Antecipacao_Total"
                    ]
                    desired_cols = [
                        "Matricula", "Nome", "Cargo", "Diretoria", "Centro_Custo",
                        "Salario", "Elegivel", "Motivo_Elegibilidade", "Meses_Contabilizados", "Proporcionalidade",
                        "Base_PLR_Basica", "Basica_Indiv_Cap", "Basica_Pos_Global", "Basica_Final",
                        "Adicional_Base", "Teto_Adic_Proporcional", "Adicional_Final", "PLR_Antecipacao_Total"
                    ]
                    display_df = format_money_cols_for_display(base_calc, money_cols)
                    display_cols = [c for c in desired_cols if c in display_df.columns]
                    st.dataframe(display_df[display_cols], use_container_width=True)

                    st.markdown("### Totais por Diretoria")
                    if "Diretoria" in base_calc.columns and not base_calc["Diretoria"].isna().all():
                        tot_dir = base_calc.groupby("Diretoria", as_index=False)["PLR_Antecipacao_Total"].sum()
                        tot_dir_display = tot_dir.copy()
                        tot_dir_display["PLR_Antecipacao_Total"] = tot_dir_display["PLR_Antecipacao_Total"].apply(fmt_brl)
                        st.dataframe(tot_dir_display.rename(columns={"PLR_Antecipacao_Total": "Total_Antecipacao"}), use_container_width=True)

                    st.markdown("### Verificações e Limites")
                    debug_data = {
                        "Teto Global Regra Básica (12,8% do lucro)": fmt_brl(PCT_LUCRO_BASICA * float(lucro_liquido_1s2025)),
                        "Soma Individuais antes do cap (Básica)": fmt_brl(total_basica_pre_cap),
                        "Fator de Redução Aplicado (Básica)": f"{fator_cap:0.6f}",
                        "Pool Parcela Adicional (2,2% do lucro)": fmt_brl(pool_adic),
                        "Soma Proporcionalidades (para Adicional)": f"{soma_props:0.6f}",
                    }
                    st.write(debug_data)

    with aba_export:
        st.subheader("Exportar Resultado (números puros)")
        def to_excel_bytes(df_dict):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for name, df in df_dict.items():
                    df.to_excel(writer, index=False, sheet_name=name)
            return output.getvalue()

        if "base_calc" in locals() and 'PLR_Antecipacao_Total' in base_calc.columns and not base.empty:
            sheets = {"Resultado_Antecipacao": base_calc.round(2)}
            if "Diretoria" in base_calc.columns and not base_calc["Diretoria"].isna().all():
                sheets["Totais_Diretoria"] = base_calc.groupby("Diretoria", as_index=False)["PLR_Antecipacao_Total"].sum().round(2)
            bytes_file = to_excel_bytes(sheets)
            st.download_button(
                label="Baixar Excel com Antecipação 2025",
                data=bytes_file,
                file_name=f"PLR_Antecipacao_{ano_ref}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Calcule na aba 'Apuração' para habilitar a exportação.")

    render_footer("Gestão & Custos RH", "v2.0")

if __name__ == "__main__":
    render_plr()
