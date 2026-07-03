import streamlit as st
from database import init_db, seed_if_empty, get_all_denominations, get_appellation_by_name

st.set_page_config(page_title="WINEINDEX OMEGA V11", page_icon="🍷", layout="wide")


def audit_label(nome, uva, alcool, safra, appellation_name):
    row = get_appellation_by_name(appellation_name)
    if not row:
        return [f"Denominação '{appellation_name}' não encontrada no banco."]

    (
        universal_id,
        country,
        macro_region,
        sub_region,
        appellation_name,
        legal_level,
        wine_color_scope,
        alcohol_min,
        alcohol_max,
        vintage_max,
        allowed_grapes,
        notes,
    ) = row

    erros = []

    if alcohol_min is not None and alcool < alcohol_min:
        erros.append(f"Álcool abaixo do mínimo exigido ({alcool}% < {alcohol_min}%).")

    if alcohol_max is not None and alcool > alcohol_max:
        erros.append(f"Álcool acima do máximo permitido ({alcool}% > {alcohol_max}%).")

    if vintage_max is not None and safra > vintage_max:
        erros.append(f"Safra inválida/futura para a base atual ({safra} > {vintage_max}).")

    permitted = [x.strip().lower() for x in allowed_grapes.split(";")] if allowed_grapes else []
    if permitted and uva.strip().lower() not in permitted:
        erros.append(f"A uva '{uva}' não consta entre as castas permitidas para {appellation_name}.")

    return erros


def main():
    init_db()
    seed_if_empty()

    st.title("🍷 WINEINDEX OMEGA V11")
    st.caption("Auditoria de rótulos + banco inicial modular de denominações")

    tabs = st.tabs(["Auditoria", "Denominações", "Busca", "Diagnóstico"])

    # =====================================================
    # TAB 1 - AUDITORIA
    # =====================================================
    with tabs[0]:
        rows = get_all_denominations()
        appellations = [r[4] for r in rows]

        c1, c2 = st.columns(2)

        with c1:
            nome = st.text_input("Nome do vinho", "Meu Vinho Reserva")
            appellation = st.selectbox("Denominação", appellations)
            uva = st.text_input("Uva principal", "Merlot")

        with c2:
            alcool = st.number_input("Teor alcoólico (% vol)", 5.0, 20.0, 13.0, 0.1)
            safra = st.number_input("Safra", 1900, 2035, 2024)

        if st.button("Executar auditoria"):
            erros = audit_label(nome, uva, alcool, safra, appellation)

            if erros:
                st.error(f"❌ {nome} apresenta inconformidades:")
                for e in erros:
                    st.write(f"- {e}")
            else:
                st.success(f"✅ {nome} está conforme as regras visíveis parametrizadas para {appellation}.")

    # =====================================================
    # TAB 2 - DENOMINAÇÕES
    # =====================================================
    with tabs[1]:
        st.subheader("Base inicial")

        for r in get_all_denominations():
            (
                uid,
                country,
                macro_region,
                sub_region,
                appellation_name,
                legal_level,
                wine_color_scope,
                alcohol_min,
                alcohol_max,
                vintage_max,
                allowed_grapes,
                notes
            ) = r

            with st.expander(f"{appellation_name} — {country} / {macro_region} / {sub_region}"):
                st.markdown(f"**ID:** {uid}")
                st.markdown(f"**Nível legal:** {legal_level}")
                st.markdown(f"**Escopo:** {wine_color_scope}")
                st.markdown(f"**Álcool mínimo:** {alcohol_min if alcohol_min is not None else '-'}")
                st.markdown(f"**Álcool máximo:** {alcohol_max if alcohol_max is not None else '-'}")
                st.markdown(f"**Safra máxima:** {vintage_max if vintage_max is not None else '-'}")
                st.markdown(f"**Castas permitidas:** {allowed_grapes}")
                st.markdown(f"**Notas:** {notes}")

    # =====================================================
    # TAB 3 - BUSCA
    # =====================================================
    with tabs[2]:
        rows = get_all_denominations()
        termo = st.text_input("Buscar por denominação, país, região, sub-região ou ID")

        if termo:
            termo_l = termo.lower()
            filtrados = [
                r for r in rows
                if termo_l in (r[0] or "").lower()
                or termo_l in (r[1] or "").lower()
                or termo_l in (r[2] or "").lower()
                or termo_l in (r[3] or "").lower()
                or termo_l in (r[4] or "").lower()
            ]
        else:
            filtrados = rows

        st.write(f"Resultados: **{len(filtrados)}**")
        for r in filtrados:
            st.write(f"- {r[4]} | {r[1]} | {r[2]} | {r[3]} | {r[0]}")

    # =====================================================
    # TAB 4 - DIAGNÓSTICO
    # =====================================================
    with tabs[3]:
        rows = get_all_denominations()
        st.write(f"Total de denominações carregadas: **{len(rows)}**")
        st.code("Se esta aba abriu e mostrou registros, a estrutura principal está íntegra.")


if __name__ == "__main__":
    main()
