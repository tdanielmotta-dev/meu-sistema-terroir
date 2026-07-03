import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report


def render_wine_block(wine):
    st.subheader("🍷 Vinho encontrado no banco local")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Produtor:** {wine.get('producer', '-')}")
        st.write(f"**Vinho:** {wine.get('wine_name', '-')}")
        st.write(f"**Safra:** {wine.get('vintage', '-')}")
        st.write(f"**Uva principal:** {wine.get('grape', '-')}")
        st.write(f"**Tipo:** {wine.get('wine_type', '-')}")

    with col2:
        st.write(f"**Região:** {wine.get('region', '-')}")
        st.write(f"**País:** {wine.get('country', '-')}")
        st.write(f"**Denominação:** {wine.get('denomination', '-')}")
        st.write(f"**Álcool:** {wine.get('alcohol', '-')}")
        st.write(f"**Score local:** {wine.get('_score', '-')}")

    notes = wine.get("notes")
    if notes:
        st.write("**Observações:**")
        st.write(notes)


def render_denomination_block(den):
    st.subheader("🛡️ Denominação encontrada no banco local")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**País:** {den.get('country', '-')}")
        st.write(f"**Região:** {den.get('region', '-')}")
        st.write(f"**Denominação:** {den.get('denomination', '-')}")
        st.write(f"**Classificação:** {den.get('classification', '-')}")

    with col2:
        st.write(f"**Álcool mínimo:** {den.get('min_alcohol', '-')}")
        st.write(f"**Castas permitidas:** {den.get('allowed_grapes', '-')}")
        st.write(f"**Regras de envelhecimento:** {den.get('aging_rules', '-')}")
        st.write(f"**Score local:** {den.get('_score', '-')}")

    notes = den.get("notes")
    if notes:
        st.write("**Observações:**")
        st.write(notes)


def render_parsed_query(parsed):
    st.subheader("🧠 Parser do rótulo / consulta")

    if not parsed:
        st.info("Nenhuma estrutura extraída da consulta.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Consulta normalizada:** {parsed.get('normalized_query', '-')}")
        st.write(f"**Safra detectada:** {parsed.get('vintage', '-')}")
        st.write(f"**Possível uva detectada:** {parsed.get('grape', '-')}")

    with col2:
        st.write(f"**Possível país detectado:** {parsed.get('country', '-')}")
        st.write(f"**Possível região detectada:** {parsed.get('region', '-')}")
        st.write(f"**Possível denominação detectada:** {parsed.get('denomination', '-')}")

    tokens = parsed.get("tokens", [])
    if tokens:
        st.write("**Tokens reconhecidos:**")
        st.write(", ".join(tokens))


def render_knowledge_matches(matches):
    st.subheader("📚 Base técnica local / conhecimento estruturado")

    if not matches:
        st.info("Nenhuma correspondência específica na base técnica local.")
        return

    for item in matches:
        data = item.get("data", {})
        st.markdown(f"### Match: {item.get('key', '-')}")
        st.write(f"**Tipo de match:** {item.get('match_type', '-')}")
        st.write(f"**País:** {data.get('country', '-')}")
        st.write(f"**Classificação:** {data.get('classification', '-')}")
        st.write(f"**Estilo:** {data.get('style', '-')}")

        grapes = data.get("grapes", [])
        if grapes:
            st.write(f"**Castas associadas:** {', '.join(grapes)}")

        notes = data.get("notes")
        if notes:
            st.write(f"**Notas técnicas:** {notes}")

        st.divider()


def render_web_results(title, results):
    st.subheader(title)

    if not results:
        st.info("Nenhum resultado online útil encontrado.")
        return

    for idx, item in enumerate(results, start=1):
        st.markdown(f"### {idx}. {item.get('title', 'Sem título')}")

        url = item.get("url", "")
        if url:
            st.write(url)

        snippet = item.get("snippet", "")
        if snippet:
            st.write(f"**Snippet:** {snippet}")

        summary = item.get("page_summary", "")
        if summary:
            st.write("**Resumo bruto da página:**")
            st.write(summary)

        st.divider()


def main():
    st.set_page_config(
        page_title="WineIndex OMEGA",
        page_icon="🍷",
        layout="wide"
    )

    init_db()
    seed_if_empty()

    st.title("🍷 WineIndex OMEGA")
    st.write(
        "Ferramenta de pesquisa de rótulos, vinhos, produtores, regiões, "
        "denominações de origem, terroir e regras técnicas."
    )

    query = st.text_input(
        "Digite o rótulo, vinho, produtor, safra, denominação ou região:",
        placeholder="Ex.: Château d’Yquem 2018 / Barolo DOCG / Sassicaia / Rioja Alta / Merlot Reserva"
    )

    pesquisar = st.button("Pesquisar")

    if pesquisar:
        if not query.strip():
            st.warning("Digite algo para pesquisar.")
            return

        with st.spinner("Consultando banco local + busca online..."):
            report = build_wine_report(query)

        if not isinstance(report, dict):
            st.error("O relatório retornado não está em formato válido.")
            st.write(report)
            return

        wine_found = report.get("wine_found")
        denomination_found = report.get("denomination_found")
        summary = report.get("summary", [])
        parsed = report.get("parsed_query", {})
        knowledge_matches = report.get("knowledge_matches", [])
        web = report.get("web", {})

        wine_web = web.get("wine_results", []) if isinstance(web, dict) else []
        denom_web = web.get("denomination_results", []) if isinstance(web, dict) else []

        st.subheader("📌 Resumo da análise")
        if summary:
            for line in summary:
                st.write(f"- {line}")
        else:
            st.info("Nenhum resumo disponível.")

        render_parsed_query(parsed)

        if wine_found:
            render_wine_block(wine_found)
        else:
            st.subheader("🍷 Vinho encontrado no banco local")
            st.warning("Nenhum vinho correspondente foi localizado no banco local.")

        if denomination_found:
            render_denomination_block(denomination_found)
        else:
            st.subheader("🛡️ Denominação encontrada no banco local")
            st.warning("Nenhuma denominação correspondente foi localizada no banco local.")

        render_knowledge_matches(knowledge_matches)
        render_web_results("🌐 Busca online — vinho / produtor / rótulo", wine_web)
        render_web_results("🌐 Busca online — denominação / legislação / terroir", denom_web)


if __name__ == "__main__":
    main()
