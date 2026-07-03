import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WineIndex OMEGA V3", page_icon="🍷", layout="wide")


def render_local_wine(wine):
    st.subheader("🍷 Vinho localizado no banco local")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Produtor:** {wine.get('producer', '-')}")
        st.write(f"**Vinho:** {wine.get('wine_name', '-')}")
        st.write(f"**Safra:** {wine.get('vintage', '-')}")
        st.write(f"**Uva:** {wine.get('grape', '-')}")
        st.write(f"**Tipo:** {wine.get('wine_type', '-')}")

    with col2:
        st.write(f"**Região:** {wine.get('region', '-')}")
        st.write(f"**País:** {wine.get('country', '-')}")
        st.write(f"**Denominação:** {wine.get('denomination', '-')}")
        st.write(f"**Álcool:** {wine.get('alcohol', '-')}")
        st.write(f"**Score de correspondência:** {wine.get('_score', '-')}")


def render_local_denomination(den):
    st.subheader("🏛️ Denominação localizada no banco local")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Denominação:** {den.get('denomination', '-')}")
        st.write(f"**Classificação:** {den.get('classification', '-')}")
        st.write(f"**Região:** {den.get('region', '-')}")
        st.write(f"**País:** {den.get('country', '-')}")

    with col2:
        st.write(f"**Uvas permitidas:** {den.get('allowed_grapes', '-')}")
        st.write(f"**Álcool mínimo:** {den.get('min_alcohol', '-')}")
        st.write(f"**Regras de maturação:** {den.get('aging_rules', '-')}")
        st.write(f"**Score de correspondência:** {den.get('_score', '-')}")


def render_kb_match(match):
    st.subheader(f"🧠 Knowledge Base — {match.get('denomination', match.get('key', 'Região'))}")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**País:** {match.get('country', '-')}")
        st.write(f"**Região:** {match.get('region', '-')}")
        st.write(f"**Denominação:** {match.get('denomination', '-')}")
        st.write(f"**Classificação:** {match.get('classification', '-')}")
        st.write(f"**Castas:** {', '.join(match.get('grapes', [])) if match.get('grapes') else '-'}")
        st.write(f"**Álcool mínimo:** {match.get('min_alcohol', '-')}")

    with col2:
        st.write(f"**Clima:** {match.get('climate', '-')}")
        st.write(f"**Terroir:** {match.get('terroir', '-')}")
        st.write(f"**Estilo:** {match.get('style', '-')}")
        st.write(f"**Aromas típicos:** {', '.join(match.get('aromas', [])) if match.get('aromas') else '-'}")
        st.write(f"**Regras de envelhecimento:** {match.get('aging_rules', '-')}")
        st.write(f"**Notas:** {match.get('notes', '-')}")


def render_online_results(results, title):
    st.subheader(title)
    if not results:
        st.info("Nenhum resultado encontrado.")
        return

    for i, item in enumerate(results, start=1):
        st.markdown(f"### {i}. {item.get('title', 'Sem título')}")
        st.write(f"**URL:** {item.get('url', '-')}")
        if item.get("snippet"):
            st.write(f"**Snippet:** {item['snippet']}")
        if item.get("page_summary"):
            st.write("**Resumo da página:**")
            st.write(item["page_summary"])
        st.divider()


def main():
    init_db()
    seed_if_empty()

    st.title("🍷 WineIndex OMEGA V3 — Pesquisador Definitivo de Rótulos")
    st.write(
        "Digite o texto do rótulo, nome do vinho, produtor, denominação ou uma combinação deles. "
        "O sistema cruza **banco local + parser inteligente + knowledge base + internet**."
    )

    query = st.text_area(
        "Digite o rótulo / nome do vinho / denominação",
        height=150,
        placeholder="Ex.: Barolo DOCG 2018 Poderi XYZ Nebbiolo Italia"
    )

    if st.button("🔍 Pesquisar rótulo", type="primary"):
        if not query.strip():
            st.warning("Digite alguma informação do rótulo.")
            st.stop()

        with st.spinner("Analisando rótulo, consultando banco local, knowledge base e internet..."):
            report = build_wine_report(query)

        st.success("Pesquisa concluída.")

        st.header("1) Resumo Executivo")
        for line in report["summary"]:
            st.write(f"- {line}")

        st.header("2) Parser do rótulo")
        parsed = report["parsed"]
        st.json(parsed)

        st.header("3) Banco local")
        if report["wine_found"]:
            render_local_wine(report["wine_found"])
        else:
            st.info("Nenhum vinho correspondente localizado no banco local.")

        if report["denomination_found"]:
            render_local_denomination(report["denomination_found"])
        else:
            st.info("Nenhuma denominação correspondente localizada no banco local.")

        st.header("4) Knowledge Base")
        if report["knowledge_matches"]:
            for match in report["knowledge_matches"]:
                render_kb_match(match)
        else:
            st.info("Nenhuma entrada relevante encontrada na knowledge base.")

        st.header("5) Pesquisa online do vinho / rótulo")
        render_online_results(report["online_wine_results"], "Resultados online do vinho")

        st.header("6) Pesquisa online da denominação / terroir / legislação")
        render_online_results(report["online_denomination_results"], "Resultados online da denominação")


if __name__ == "__main__":
    main()
