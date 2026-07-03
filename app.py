import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WINEINDEX OMEGA V7", page_icon="🍷", layout="wide")


def render_dict_block(title, data):
    st.subheader(title)
    if not data:
        st.write("Nenhum dado.")
        return
    st.json(data)


def render_profile(profile: dict, field_sources: dict):
    st.subheader("🍷 Ficha consolidada do vinho")

    st.markdown(f"**Nome consultado:** {profile.get('query', '')}")

    fields_order = [
        ("producer", "Produtor"),
        ("wine_name", "Nome do vinho"),
        ("vintage", "Safra"),
        ("grape", "Uva"),
        ("country", "País"),
        ("region", "Região"),
        ("subregion", "Sub-região"),
        ("denomination", "Denominação"),
        ("classification", "Classificação"),
        ("wine_type", "Tipo"),
        ("alcohol", "Teor alcoólico"),
        ("aromas", "Aromas"),
        ("palate", "Paladar"),
        ("acidity", "Acidez"),
        ("body", "Corpo"),
        ("soil", "Solo"),
        ("climate", "Clima"),
        ("terroir", "Terroir"),
        ("aging", "Amadurecimento"),
        ("pairing", "Harmonização"),
        ("notes", "Observações"),
    ]

    for key, label in fields_order:
        value = str(profile.get(key, "")).strip()
        if not value:
            value = "—"

        sources = field_sources.get(key, [])
        source_text = " | ".join(sources) if sources else "sem fonte atribuída"

        st.markdown(f"**{label}:** {value}")
        st.caption(f"Fonte(s): {source_text}")


def main():
    init_db()
    seed_if_empty()

    st.title("🍷 WINEINDEX OMEGA V7")
    st.write("**Pesquisa definitiva de rótulos de vinho:** banco local + internet + consolidação automática")
    st.write("""
Digite somente o nome do rótulo ou o título do vinho, por exemplo:

- Gato Negro Merlot 2020
- Barolo DOCG 2018
- Catena Malbec
- Chablis Premier Cru

O sistema tenta levantar:
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
""")

    query = st.text_input("🔎 Digite o rótulo / nome do vinho", value="Gato Negro Malbec 2019")

    if st.button("Pesquisar"):
        with st.spinner("Pesquisando banco local, knowledge base e internet..."):
            report = build_wine_report(query)

        st.subheader("📌 Resumo consolidado")
        for item in report["summary"]:
            st.write(f"• {item}")

        render_profile(report["profile"], report["field_sources"])

        st.divider()
        render_dict_block("🧠 Parser da consulta", report["parser"])

        st.divider()
        st.subheader("🗄️ Resultado do banco local")
        if report["wine_found"]:
            st.write("**Vinho encontrado no banco local:**")
            st.json(report["wine_found"])
        else:
            st.write("Nenhum vinho correspondente encontrado no banco local.")

        if report["denomination_found"]:
            st.write("**Denominação encontrada no banco local:**")
            st.json(report["denomination_found"])
        else:
            st.write("Nenhuma denominação correspondente encontrada no banco local.")

        st.divider()
        st.subheader("🧠 Knowledge base")
        if report["knowledge_matches"]:
            for idx, kb in enumerate(report["knowledge_matches"], start=1):
                st.markdown(f"**Match {idx}**")
                st.json(kb)
        else:
            st.write("Nenhuma correspondência encontrada na knowledge base.")

        st.divider()
        st.subheader("🌐 Fontes online encontradas")
        if report["online_sources"]:
            for idx, src in enumerate(report["online_sources"], start=1):
                st.markdown(f"### Fonte {idx}")
                st.write(f"**Título:** {src.get('title', '')}")
                st.write(f"**URL:** {src.get('url', '')}")
                if src.get("snippet"):
                    st.write(f"**Snippet:** {src.get('snippet')}")
        else:
            st.write("Nenhuma fonte online relevante foi consolidada.")

        st.divider()
        st.subheader("🧪 Extração por fonte")
        if report["parsed_sources"]:
            for idx, ps in enumerate(report["parsed_sources"], start=1):
                st.markdown(f"### Parser da fonte {idx}")
                st.write(f"**Título:** {ps.get('source_title', '')}")
                st.write(f"**URL:** {ps.get('source_url', '')}")
                st.json(ps.get("extracted", {}))
        else:
            st.write("Nenhuma fonte foi parseada.")


if __name__ == "__main__":
    main()
