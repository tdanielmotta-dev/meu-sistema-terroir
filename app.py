import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report


def show_value(label, value):
    if value is None or value == "":
        st.write(f"**{label}:** —")
    else:
        st.write(f"**{label}:** {value}")


def render_profile(profile: dict):
    st.subheader("🍷 Ficha consolidada do vinho")

    c1, c2 = st.columns(2)

    with c1:
        show_value("Rótulo / vinho", profile.get("wine_title") or profile.get("query"))
        show_value("Produtor", profile.get("producer"))
        show_value("Safra", profile.get("vintage"))
        show_value("País", profile.get("country"))
        show_value("Região", profile.get("region"))
        show_value("Denominação", profile.get("denomination"))
        show_value("Classificação", profile.get("classification"))
        show_value("Tipo", profile.get("wine_type"))

    with c2:
        show_value("Uva principal", profile.get("grape"))
        show_value("Teor alcoólico", profile.get("alcohol"))
        show_value("Corpo", profile.get("body"))
        show_value("Acidez", profile.get("acidity"))
        show_value("Taninos", profile.get("tannin"))
        show_value("Madeira / barrica", profile.get("oak"))
        show_value("Castas permitidas na DO", profile.get("allowed_grapes"))
        show_value("Regras de envelhecimento", profile.get("aging_rules"))

    st.markdown("### Sensorial e terroir")
    show_value("Aroma", profile.get("aroma"))
    show_value("Sabor / boca", profile.get("flavor"))
    show_value("Solo", profile.get("soil"))
    show_value("Clima", profile.get("climate"))

    notes = profile.get("notes", [])
    if notes:
        st.markdown("### Observações / trilha de fontes")
        for n in notes:
            st.write(f"- {n}")

    sources_used = profile.get("sources_used", [])
    if sources_used:
        st.markdown("### Mapa de preenchimento dos campos")
        for s in sources_used:
            st.write(f"- {s}")


def render_summary(summary):
    st.subheader("📌 Resumo da pesquisa")
    for line in summary:
        st.write(f"- {line}")


def render_parser(parsed):
    st.subheader("🧠 Parser da consulta")
    show_value("Consulta normalizada", parsed.get("normalized_query"))
    show_value("Safra detectada", parsed.get("vintage"))
    show_value("Uva detectada", parsed.get("grape"))
    show_value("País detectado", parsed.get("country"))
    show_value("Região detectada", parsed.get("region"))
    show_value("Denominação detectada", parsed.get("denomination"))

    tokens = parsed.get("tokens", [])
    if tokens:
        st.write("**Tokens:** " + ", ".join(tokens))


def render_web_results(title, results):
    st.subheader(title)

    if not results:
        st.info("Nenhuma página online útil foi processada.")
        return

    for i, item in enumerate(results, start=1):
        st.markdown(f"### {i}. {item.get('title', 'Sem título')}")
        if item.get("url"):
            st.write(item["url"])
        if item.get("snippet"):
            st.write(f"**Snippet:** {item['snippet']}")

        extracted = item.get("extracted", {})
        if extracted:
            st.write("**Campos extraídos desta página:**")
            for k, v in extracted.items():
                st.write(f"- {k}: {v}")

        st.divider()


def main():
    st.set_page_config(page_title="WineIndex OMEGA V4", page_icon="🍷", layout="wide")

    init_db()
    seed_if_empty()

    st.title("🍷 WineIndex OMEGA V4 — Internet Parser Real")
    st.write(
        "Digite somente o nome do rótulo. O sistema tenta consolidar dados do banco local, "
        "knowledge base e páginas online processadas automaticamente."
    )

    query = st.text_input(
        "Digite o rótulo do vinho",
        placeholder="Ex.: Gato Negro Merlot 2020"
    )

    if st.button("Pesquisar"):
        if not query.strip():
            st.warning("Digite um rótulo.")
            return

        with st.spinner("Pesquisando banco + knowledge base + internet + extração de campos..."):
            report = build_wine_report(query)

        render_summary(report.get("summary", []))
        render_profile(report.get("profile", {}))
        render_parser(report.get("parsed_query", {}))

        web = report.get("web", {})
        render_web_results("🌐 Páginas processadas — rótulo / vinho / produtor", web.get("wine_results", []))
        render_web_results("🌐 Páginas processadas — região / denominação / terroir", web.get("denomination_results", []))


if __name__ == "__main__":
    main()
