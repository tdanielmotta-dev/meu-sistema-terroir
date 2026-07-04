import json
import streamlit as st

from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WINEINDEX OMEGA X", page_icon="🍷", layout="wide")


DISPLAY_FIELDS = [
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


def show_sources(source_map, field):
    srcs = source_map.get(field, [])
    if srcs:
        st.caption("Fonte(s): " + " | ".join(srcs))
    else:
        st.caption("Fonte(s): sem fonte atribuída")


def main():
    init_db()
    seed_if_empty()

    st.title("🍷 WINEINDEX OMEGA X — REAL FETCH ENGINE")
    st.write(
        "Digite somente o nome do rótulo do vinho. "
        "O sistema tenta consolidar dados de banco local + knowledge base + internet."
    )

    query = st.text_input(
        "🔎 Digite o rótulo / nome do vinho",
        value="Dom Perignon"
    )

    if st.button("Pesquisar") and query.strip():
        with st.spinner("Pesquisando banco local, knowledge base e web..."):
            report = build_wine_report(query.strip())

        st.subheader("📌 Resumo consolidado")
        st.write(f"• Knowledge base encontrou **{len(report['knowledge_matches'])}** correspondência(s).")
        st.write(f"• Campos preenchidos na ficha: **{report['filled_fields']}/{report['total_fields']}**.")
        st.write(f"• Total de atribuições de fonte: **{report['total_source_attributions']}**.")

        st.subheader("🍷 Ficha consolidada do vinho")
        st.write(f"**Nome consultado:** {report['query']}")

        final_data = report["final_data"]
        source_map = report["source_map"]

        for key, label in DISPLAY_FIELDS:
            value = final_data.get(key, "")
            st.markdown(f"**{label}**")
            st.write(value if str(value).strip() else "—")
            show_sources(source_map, key)

        st.subheader("🧠 Parser da consulta")
        st.code(json.dumps(report["parsed_query"], ensure_ascii=False, indent=2), language="json")

        st.subheader("🗄️ Resultado do banco local")
        if report["local_wine"]:
            st.write("**Vinho encontrado no banco local:**")
            st.json(report["local_wine"])
        else:
            st.write("Nenhum vinho correspondente encontrado no banco local.")

        if report["local_denomination"]:
            st.write("**Denominação encontrada no banco local:**")
            st.json(report["local_denomination"])
        else:
            st.write("Nenhuma denominação correspondente encontrada no banco local.")

        st.subheader("🧠 Knowledge base")
        if report["knowledge_matches"]:
            for i, item in enumerate(report["knowledge_matches"], start=1):
                st.write(f"**Match {i}**")
                st.json(item)
        else:
            st.write("Nenhum match de knowledge base.")

        st.subheader("🌐 Fontes online encontradas")
        if report["online_sources"]:
            for i, src in enumerate(report["online_sources"], start=1):
                st.markdown(f"**Fonte {i}**")
                st.write(f"**Título:** {src.get('title', '')}")
                st.write(f"**URL:** {src.get('url', '')}")
                st.write(f"**Snippet:** {src.get('snippet', '')}")
                if src.get("page_text"):
                    st.text_area(
                        f"Trecho bruto da fonte {i}",
                        src["page_text"],
                        height=180,
                        key=f"page_text_{i}"
                    )
        else:
            st.write("Nenhuma fonte online relevante foi consolidada.")

        st.subheader("🧪 Extração por fonte")
        if report["parsed_online_sources"]:
            for i, item in enumerate(report["parsed_online_sources"], start=1):
                st.write(f"**Parser da fonte {i}**")
                st.json(item)
        else:
            st.write("Nenhum parser online gerou dados estruturados.")


if __name__ == "__main__":
    main()
