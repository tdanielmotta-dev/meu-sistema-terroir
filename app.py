import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WineIndex OMEGA V2", page_icon="🍷", layout="wide")


def bootstrap_database():
    init_db()
    seed_if_empty()


def render_parser(parsed: dict):
    conf = parsed.get("confidence", {})

    st.subheader("🧠 Parser inteligente")
    st.write(f"**Consulta bruta:** {parsed.get('raw_query', '-')}")
    st.write(f"**Produtor provável:** {parsed.get('producer_guess', '-')}")
    st.write(f"**Nome provável do vinho:** {parsed.get('wine_name_guess', '-')}")
    st.write(f"**Safra detectada:** {parsed.get('year', '-')}")
    st.write(f"**País provável:** {parsed.get('country_guess', '-')}")
    st.write(f"**Regiões detectadas:** {', '.join(parsed.get('regions_detected', [])) or '-'}")
    st.write(f"**Classificações detectadas:** {', '.join(parsed.get('classifications', [])) or '-'}")
    st.write(f"**Termos de qualidade:** {', '.join(parsed.get('quality_terms', [])) or '-'}")
    st.write(f"**Uvas detectadas:** {', '.join(parsed.get('grapes_detected', [])) or '-'}")
    st.write(f"**Estilos prováveis:** {', '.join(parsed.get('styles_detected', [])) or '-'}")

    st.markdown("### 🎯 Confiança por campo")
    st.write(f"- **Produtor:** {conf.get('producer', 0.0):.2f}")
    st.write(f"- **Nome do vinho:** {conf.get('wine_name', 0.0):.2f}")
    st.write(f"- **Safra:** {conf.get('year', 0.0):.2f}")
    st.write(f"- **País:** {conf.get('country', 0.0):.2f}")
    st.write(f"- **Regiões:** {conf.get('regions', 0.0):.2f}")
    st.write(f"- **Classificações:** {conf.get('classifications', 0.0):.2f}")
    st.write(f"- **Termos de qualidade:** {conf.get('quality_terms', 0.0):.2f}")
    st.write(f"- **Uvas:** {conf.get('grapes', 0.0):.2f}")
    st.write(f"- **Estilos:** {conf.get('styles', 0.0):.2f}")


def render_consolidated_card(card: dict):
    st.subheader("📌 Ficha consolidada")
    st.write(f"**Produtor:** {card.get('producer') or '-'}")
    st.write(f"**Vinho / Cuvée:** {card.get('wine_name') or '-'}")
    st.write(f"**Safra:** {card.get('vintage') or '-'}")
    st.write(f"**País:** {card.get('country') or '-'}")
    st.write(f"**Região:** {card.get('region') or '-'}")
    st.write(f"**Denominação:** {card.get('denomination') or '-'}")
    st.write(f"**Classificação:** {card.get('classification') or '-'}")
    st.write(f"**Tipo / estilo consolidado:** {card.get('wine_type') or ', '.join(card.get('styles_detected', [])) or '-'}")

    grapes = card.get("grapes", [])
    if grapes:
        st.write(f"**Uvas relacionadas:** {', '.join(grapes)}")
    else:
        st.write("**Uvas relacionadas:** -")

    q = card.get("quality_terms", [])
    if q:
        st.write(f"**Termos de qualidade detectados:** {', '.join(q)}")
    else:
        st.write("**Termos de qualidade detectados:** -")


def render_local_wine(wine: dict):
    st.subheader("🍷 Banco local — vinho")
    st.write(f"**Produtor:** {wine.get('producer', '-')}")
    st.write(f"**Rótulo:** {wine.get('wine_name', '-')}")
    st.write(f"**Safra:** {wine.get('vintage', '-')}")
    st.write(f"**Uva(s):** {wine.get('grape', '-')}")
    st.write(f"**Região:** {wine.get('region', '-')}")
    st.write(f"**País:** {wine.get('country', '-')}")
    st.write(f"**Denominação:** {wine.get('denomination', '-')}")
    st.write(f"**Classificação:** {wine.get('classification', '-')}")
    st.write(f"**Tipo:** {wine.get('wine_type', '-')}")
    st.write(f"**Álcool:** {wine.get('alcohol', '-')}")
    st.write(f"**Notas:** {wine.get('notes', '-')}")
    st.write(f"**Score local:** {wine.get('_score', '-')}")


def render_local_denomination(den: dict):
    st.subheader("🏛️ Banco local — denominação")
    st.write(f"**País:** {den.get('country', '-')}")
    st.write(f"**Região:** {den.get('region', '-')}")
    st.write(f"**Denominação:** {den.get('denomination', '-')}")
    st.write(f"**Classificação:** {den.get('classification', '-')}")
    st.write(f"**Uvas permitidas:** {den.get('allowed_grapes', '-')}")
    st.write(f"**Álcool mínimo:** {den.get('min_alcohol', '-')}")
    st.write(f"**Regras de amadurecimento:** {den.get('aging_rules', '-')}")
    st.write(f"**Notas:** {den.get('notes', '-')}")
    st.write(f"**Score local:** {den.get('_score', '-')}")


def render_online_results(title: str, items: list):
    st.subheader(title)
    if not items:
        st.info("Nenhum resultado online.")
        return

    for idx, item in enumerate(items, start=1):
        st.markdown(f"### {idx}. {item.get('title', 'Sem título')}")
        if item.get("url"):
            st.write(item["url"])
        if item.get("snippet"):
            st.write(f"**Snippet:** {item['snippet']}")
        if item.get("page_summary"):
            st.write(f"**Resumo da página:** {item['page_summary']}")
        st.markdown("---")


def main():
    bootstrap_database()

    st.title("🍷 WineIndex OMEGA V2")
    st.write("Pesquisa híbrida de vinhos, rótulos, produtores, denominações e terroirs.")

    query = st.text_input(
        "Digite o rótulo / produtor / safra / denominação / região",
        placeholder="Ex.: Château Margaux 2015 Bordeaux | Barolo DOCG Vietti Castiglione 2019 | Miolo Lote 43 Vale dos Vinhedos"
    )

    if st.button("Pesquisar"):
        if not query.strip():
            st.warning("Digite uma consulta.")
            return

        with st.spinner("Executando parser inteligente, busca local e busca online..."):
            report = build_wine_report(query)

        st.header("📋 Resumo geral")
        for line in report.get("summary", []):
            st.write(f"- {line}")

        st.markdown("---")
        col_a, col_b = st.columns([1, 1])

        with col_a:
            render_parser(report.get("parsed", {}))

        with col_b:
            render_consolidated_card(report.get("consolidated", {}))

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            wine_local = report.get("wine", {}).get("local")
            if wine_local:
                render_local_wine(wine_local)
            else:
                st.info("Nenhum vinho encontrado no banco local.")

        with col2:
            den_local = report.get("denomination", {}).get("local")
            if den_local:
                render_local_denomination(den_local)
            else:
                st.info("Nenhuma denominação encontrada no banco local.")

        st.markdown("---")
        col3, col4 = st.columns(2)

        with col3:
            render_online_results(
                "🌐 Online — vinho / produtor / rótulo",
                report.get("wine", {}).get("online", [])
            )

        with col4:
            render_online_results(
                "🌍 Online — denominação / terroir / legislação",
                report.get("denomination", {}).get("online", [])
            )


if __name__ == "__main__":
    main()
