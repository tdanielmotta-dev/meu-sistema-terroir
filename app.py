import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WineIndex OMEGA V6", page_icon="🍷", layout="wide")


def render_kv(label, value):
    if value is None:
        return
    if isinstance(value, str) and not value.strip():
        return
    st.markdown(f"**{label}:** {value}")


def render_list(label, values):
    if not values:
        return
    cleaned = [str(v).strip() for v in values if str(v).strip()]
    if not cleaned:
        return
    st.markdown(f"**{label}:** " + " | ".join(cleaned))


def main():
    init_db()
    seed_if_empty()

    st.title("🍷 WINEINDEX OMEGA V6")
    st.caption("Pesquisa definitiva de rótulos de vinho: banco local + internet + consolidação automática")

    st.markdown(
        """
Digite **somente o nome do rótulo** ou o título do vinho, por exemplo:

- `Gato Negro Merlot 2020`
- `Barolo DOCG 2018`
- `Catena Malbec`
- `Chablis Premier Cru`

O sistema vai tentar levantar:
- produtor
- safra
- uva
- país / região / sub-região
- denominação
- teor alcoólico
- aromas / paladar / acidez / corpo
- solo / clima / terroir
- amadurecimento / harmonização
- e outras informações encontradas
"""
    )

    query = st.text_input("🔎 Digite o rótulo / nome do vinho", value="Gato Negro Merlot 2020")

    col1, col2 = st.columns([1, 4])
    with col1:
        run = st.button("Pesquisar", use_container_width=True)

    if run and query.strip():
        with st.spinner("Pesquisando banco local, internet e consolidando dados..."):
            report = build_wine_report(query)

        st.subheader("📌 Resumo consolidado")
        for line in report.get("summary", []):
            st.write("•", line)

        st.divider()

        final = report.get("final_profile", {})

        st.subheader("🍷 Ficha consolidada do vinho")
        c1, c2 = st.columns(2)

        with c1:
            render_kv("Nome consultado", report.get("query"))
            render_kv("Produtor", final.get("producer"))
            render_kv("Vinho / Rótulo", final.get("wine_name"))
            render_kv("Safra", final.get("vintage"))
            render_kv("País", final.get("country"))
            render_kv("Região", final.get("region"))
            render_kv("Sub-região", final.get("subregion"))
            render_kv("Denominação", final.get("denomination"))
            render_kv("Classificação", final.get("classification"))
            render_kv("Tipo", final.get("wine_type"))
            render_kv("Uva principal", final.get("grape"))
            render_list("Outras uvas", final.get("other_grapes"))
            render_kv("Teor alcoólico", final.get("alcohol"))

        with c2:
            render_kv("Clima", final.get("climate"))
            render_kv("Solo", final.get("soil"))
            render_kv("Terroir", final.get("terroir"))
            render_kv("Acidez", final.get("acidity"))
            render_kv("Corpo", final.get("body"))
            render_kv("Taninos", final.get("tannins"))
            render_kv("Amadurecimento / Barrica", final.get("aging"))
            render_kv("Aromas", final.get("aromas"))
            render_kv("Paladar / Sabor", final.get("palate"))
            render_kv("Harmonização", final.get("pairing"))
            render_kv("Observações", final.get("notes"))

        st.divider()

        st.subheader("🧠 Parser da consulta")
        st.json(report.get("parsed_query", {}), expanded=True)

        st.subheader("🗄️ Resultado do banco local")
        local_wine = report.get("wine_found")
        local_denom = report.get("denomination_found")

        if local_wine:
            st.markdown("### Vinho encontrado no banco")
            st.json(local_wine, expanded=False)
        else:
            st.info("Nenhum vinho correspondente encontrado no banco local.")

        if local_denom:
            st.markdown("### Denominação encontrada no banco")
            st.json(local_denom, expanded=False)
        else:
            st.info("Nenhuma denominação correspondente encontrada no banco local.")

        st.divider()

        st.subheader("🌐 Fontes online encontradas")
        online = report.get("online_sources", [])
        if not online:
            st.warning("Nenhuma fonte online relevante foi consolidada.")
        else:
            for idx, item in enumerate(online, start=1):
                title = item.get("title", f"Fonte {idx}")
                url = item.get("url", "")
                snippet = item.get("snippet", "")
                page_summary = item.get("page_summary", "")
                extracted = item.get("extracted", {})

                with st.expander(f"{idx}. {title}", expanded=False):
                    if url:
                        st.write(url)
                    if snippet:
                        st.markdown("**Snippet**")
                        st.write(snippet)
                    if page_summary:
                        st.markdown("**Resumo bruto da página**")
                        st.write(page_summary)

                    if extracted:
                        st.markdown("**Campos extraídos desta fonte**")
                        st.json(extracted, expanded=False)

        st.divider()

        st.subheader("🧩 Consolidação técnica bruta")
        st.json(report, expanded=False)


if __name__ == "__main__":
    main()
