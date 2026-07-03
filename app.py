import streamlit as st
from seed_data import bootstrap_database
from report_builder import build_wine_report

st.set_page_config(
    page_title="WineIndex",
    page_icon="🍷",
    layout="wide"
)

bootstrap_database()


def render_local_wine(wine: dict):
    st.subheader("🍷 Vinho encontrado no banco local")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Produtor:** {wine.get('producer', '-')}")
        st.write(f"**Rótulo:** {wine.get('wine_name', '-')}")
        st.write(f"**Safra:** {wine.get('vintage', '-')}")
        st.write(f"**Uva(s):** {wine.get('grape', '-')}")
        st.write(f"**Tipo:** {wine.get('wine_type', '-')}")
        st.write(f"**Álcool:** {wine.get('alcohol', '-')}")
    with col2:
        st.write(f"**Região:** {wine.get('region', '-')}")
        st.write(f"**País:** {wine.get('country', '-')}")
        st.write(f"**Denominação:** {wine.get('denomination', '-')}")
        st.write(f"**Notas locais:** {wine.get('notes', '-')}")
        st.write(f"**Score local:** {wine.get('_score', '-')}")


def render_local_denomination(den: dict):
    st.subheader("🏛️ Denominação encontrada no banco local")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Denominação:** {den.get('denomination', '-')}")
        st.write(f"**Classificação:** {den.get('classification', '-')}")
        st.write(f"**Região:** {den.get('region', '-')}")
        st.write(f"**País:** {den.get('country', '-')}")
    with col2:
        st.write(f"**Uvas permitidas:** {den.get('allowed_grapes', '-')}")
        st.write(f"**Álcool mínimo:** {den.get('min_alcohol', '-')}")
        st.write(f"**Regras de envelhecimento:** {den.get('aging_rules', '-')}")
        st.write(f"**Notas:** {den.get('notes', '-')}")
        st.write(f"**Score local:** {den.get('_score', '-')}")


def render_local_producer(prod: dict):
    st.subheader("🏰 Produtor encontrado no banco local")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Produtor:** {prod.get('producer_name', '-')}")
        st.write(f"**País:** {prod.get('country', '-')}")
        st.write(f"**Região:** {prod.get('region', '-')}")
    with col2:
        st.write(f"**Sub-região:** {prod.get('subregion', '-')}")
        st.write(f"**Website:** {prod.get('website', '-')}")
        st.write(f"**Notas:** {prod.get('notes', '-')}")
        st.write(f"**Score local:** {prod.get('_score', '-')}")


def render_web_results(results: list, title: str):
    st.subheader(title)

    if not results:
        st.info("Nenhum resultado online relevante encontrado.")
        return

    for idx, item in enumerate(results, start=1):
        with st.expander(f"{idx}. {item.get('title', 'Sem título')}"):
            url = item.get("url", "")
            snippet = item.get("snippet", "")
            page_summary = item.get("page_summary", "")

            if url:
                st.markdown(f"**Fonte:** [{url}]({url})")
            if snippet:
                st.write(f"**Resumo do buscador:** {snippet}")
            if page_summary:
                st.write("**Trecho extraído da página:**")
                st.write(page_summary)


def render_parsed(parsed: dict):
    st.subheader("🧠 Leitura da consulta")
    st.write(f"**Consulta bruta:** {parsed.get('raw_query', '-')}")
    st.write(f"**Safra detectada:** {parsed.get('vintage', '-')}")
    st.write(f"**Denominação sugerida:** {parsed.get('denomination_hint', '-')}")
    st.write(f"**Região sugerida:** {parsed.get('region_hint', '-')}")
    st.write(f"**País sugerido:** {parsed.get('country_hint', '-')}")


def main():
    st.title("🍷 WineIndex")
    st.caption("Pesquisa híbrida de rótulos, vinhos, produtores, denominações e regiões — banco local + internet.")

    st.markdown("""
Digite o máximo que você souber do rótulo:
- **produtor**
- **nome do vinho**
- **safra**
- **denominação**
- **região**
- **uvas**
    """)

    query = st.text_input(
        "Consulta",
        placeholder="Ex.: Château d'Yquem 2015, Barolo DOCG, Château Margaux 2018, Rioja Alta Gran Reserva"
    )

    if st.button("Pesquisar", use_container_width=True):
        if not query.strip():
            st.warning("Digite uma consulta.")
            return

        with st.spinner("Pesquisando no banco local e na internet..."):
            report = build_wine_report(query)

        st.success("Pesquisa concluída.")

        with st.expander("📌 Resumo executivo", expanded=True):
            for line in report["summary"]:
                st.write(f"- {line}")

        render_parsed(report["parsed"])

        wine = report.get("wine_found")
        if wine:
            render_local_wine(wine)

        denom = report.get("denomination_found")
        if denom:
            render_local_denomination(denom)

        prod = report.get("producer_found")
        if prod:
            render_local_producer(prod)

        st.divider()
        render_web_results(report.get("web_wine_results", []), "🌐 Resultados online — vinho / rótulo")
        st.divider()
        render_web_results(report.get("web_denom_results", []), "🌍 Resultados online — denominação / região")


if __name__ == "__main__":
    main()
