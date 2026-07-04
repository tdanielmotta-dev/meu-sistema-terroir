import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WINEINDEX OMEGA FINAL", page_icon="🍷", layout="wide")

FIELDS_ORDER = [
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

def show_field(label, value, source_map, field_key):
    source = source_map.get(field_key, {}).get("source", "sem fonte atribuída")
    val = value if str(value or "").strip() else "—"

    st.markdown(f"**{label}**")
    st.write(val)
    st.caption(f"Fonte(s): {source}")

def main():
    init_db()
    seed_if_empty()

    st.title("🍷 WINEINDEX OMEGA FINAL")
    st.write("Pesquisa definitiva de rótulos de vinho: banco local + internet + consolidação automática + auto-aprendizado do knowledge base.")
    st.write("Digite somente o nome do rótulo ou o título do vinho, por exemplo:")
    st.code("Dom Perignon\nGato Negro Malbec 2019\nBarolo DOCG 2018\nCatena Malbec\nChablis Premier Cru")

    query = st.text_input("🔎 Digite o rótulo / nome do vinho")

    if not query:
        return

    with st.spinner("Pesquisando banco local, knowledge base e internet..."):
        report = build_wine_report(query)

    consolidated = report["consolidated"]
    source_map = report["source_map"]

    st.subheader("📌 Resumo consolidado")
    st.write(f"• Knowledge base encontrou **{len(report['kb_matches'])}** correspondência(s).")
    st.write(f"• Campos preenchidos na ficha: **{report['filled_fields']}/{report['total_fields']}**.")
    st.write(f"• Total de atribuições de fonte: **{len(source_map)}**.")

    st.subheader("🍷 Ficha consolidada do vinho")
    st.markdown("**Nome consultado**")
    st.write(report["query"])
    st.caption("Fonte(s): USER_QUERY")

    for key, label in FIELDS_ORDER:
        show_field(label, consolidated.get(key, ""), source_map, key)

    with st.expander("🧠 Parser da consulta"):
        st.json(report["parsed_query"])

    with st.expander("🗄️ Resultado do banco local"):
        if report["local_wine"]:
            st.write("Vinho encontrado no banco local:")
            st.json(report["local_wine"])
        else:
            st.write("Nenhum vinho correspondente encontrado no banco local.")

    with st.expander("🧠 Knowledge base"):
        if report["kb_matches"]:
            for idx, item in enumerate(report["kb_matches"], start=1):
                st.write(f"Match {idx}")
                st.json(item)
        else:
            st.write("Nenhum match de knowledge base.")

    with st.expander("🌐 Fontes online encontradas"):
        if report["online_sources"]:
            for idx, src in enumerate(report["online_sources"], start=1):
                st.write(f"Fonte {idx}")
                st.write(f"**Título:** {src.get('title', '')}")
                st.write(f"**URL:** {src.get('url', '')}")
                st.write(f"**Snippet:** {src.get('snippet', '')}")
                st.write("---")
        else:
            st.write("Nenhuma fonte online relevante foi consolidada.")

    with st.expander("🧪 Extração por fonte"):
        if report["parsed_sources"]:
            for idx, item in enumerate(report["parsed_sources"], start=1):
                st.write(f"Parser da fonte {idx}")
                st.write(f"**Título:** {item.get('_source_title', '')}")
                st.write(f"**URL:** {item.get('_source_url', '')}")
                st.json(item)
        else:
            st.write("Nenhum parser online gerou dados estruturados.")

if __name__ == "__main__":
    main()
