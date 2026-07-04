import streamlit as st
from report_builder import build_wine_report

st.set_page_config(page_title="WINEINDEX OMEGA V9", page_icon="🍷", layout="wide")


def render_field(label, value, sources=None):
    st.markdown(f"### {label}")
    if value not in [None, "", [], {}]:
        st.write(value)
    else:
        st.write("—")
    if sources:
        st.caption("Fonte(s): " + " | ".join(sources))
    else:
        st.caption("Fonte(s): sem fonte atribuída")


def main():
    st.title("🍷 WINEINDEX OMEGA V9")
    st.write("Pesquisa definitiva de rótulos de vinho: banco local + internet + consolidação automática.")
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

    if st.button("Pesquisar") and query.strip():
        with st.spinner("Pesquisando banco local + internet + consolidando ficha..."):
            report = build_wine_report(query)

        st.subheader("📌 Resumo consolidado")
        for line in report.get("summary", []):
            st.write(f"• {line}")

        ficha = report.get("final_record", {})
        sources_map = report.get("field_sources", {})

        st.subheader("🍷 Ficha consolidada do vinho")

        ordered_fields = [
            ("query_name", "Nome consultado"),
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

        for field_key, label in ordered_fields:
            render_field(label, ficha.get(field_key), sources_map.get(field_key, []))

        st.subheader("🧠 Parser da consulta")
        st.json(report.get("parsed_query", {}))

        st.subheader("🗄️ Resultado do banco local")
        if report.get("wine_found"):
            st.write("Vinho encontrado no banco local:")
            st.json(report["wine_found"])
        else:
            st.write("Nenhum vinho correspondente encontrado no banco local.")

        if report.get("denomination_found"):
            st.write("Denominação encontrada no banco local:")
            st.json(report["denomination_found"])
        else:
            st.write("Nenhuma denominação correspondente encontrada no banco local.")

        st.subheader("🧠 Knowledge base")
        kb_hits = report.get("knowledge_hits", [])
        if kb_hits:
            for idx, hit in enumerate(kb_hits, start=1):
                st.markdown(f"**Match {idx}**")
                st.json(hit)
        else:
            st.write("Nenhum match de knowledge base.")

        st.subheader("🌐 Fontes online encontradas")
        web_results = report.get("web_results", [])
        if web_results:
            for idx, item in enumerate(web_results, start=1):
                st.markdown(f"**Fonte {idx}**")
                st.write(f"**Título:** {item.get('title', '')}")
                st.write(f"**URL:** {item.get('url', '')}")
                if item.get("snippet"):
                    st.write(f"**Snippet:** {item.get('snippet')}")
                if item.get("page_summary"):
                    st.write(f"**Resumo extraído:** {item.get('page_summary')}")
        else:
            st.write("Nenhuma fonte online relevante foi consolidada.")

        st.subheader("🧪 Extração por fonte")
        extracted = report.get("web_extracted", [])
        if extracted:
            for idx, item in enumerate(extracted, start=1):
                st.markdown(f"**Parser da fonte {idx}**")
                st.write(f"**Título:** {item.get('title', '')}")
                st.write(f"**URL:** {item.get('url', '')}")
                st.json(item.get("parsed_data", {}))
        else:
            st.write("Nenhum parser online gerou dados estruturados.")


if __name__ == "__main__":
    main()
