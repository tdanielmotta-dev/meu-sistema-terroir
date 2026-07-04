import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WINEINDEX OMEGA V8", page_icon="🍷", layout="wide")


def show_field(label, value, sources):
    if value:
        st.markdown(f"**{label}:** {value}")
    else:
        st.markdown(f"**{label}:** —")

    if sources:
        st.caption("Fonte(s): " + " | ".join(sources))
    else:
        st.caption("Fonte(s): sem fonte atribuída")


def main():
    init_db()
    seed_if_empty()

    st.title("🍷 WINEINDEX OMEGA V8")
    st.write("**Pesquisa definitiva de rótulos de vinho: banco local + internet + consolidação automática**")
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

    query = st.text_input("🔎 Digite o rótulo / nome do vinho")

    if st.button("Pesquisar") and query.strip():
        with st.spinner("Pesquisando banco local + internet + consolidando ficha..."):
            report = build_wine_report(query)

        st.subheader("📌 Resumo consolidado")
        for item in report["summary"]:
            st.write(f"• {item}")

        card = report["card"]

        st.subheader("🍷 Ficha consolidada do vinho")
        st.write(f"**Nome consultado:** {report['query']}")

        show_field("Produtor", card["producer"], card["_sources"]["producer"])
        show_field("Nome do vinho", card["wine_name"], card["_sources"]["wine_name"])
        show_field("Safra", card["vintage"], card["_sources"]["vintage"])
        show_field("Uva", card["grape"], card["_sources"]["grape"])
        show_field("País", card["country"], card["_sources"]["country"])
        show_field("Região", card["region"], card["_sources"]["region"])
        show_field("Sub-região", card["subregion"], card["_sources"]["subregion"])
        show_field("Denominação", card["denomination"], card["_sources"]["denomination"])
        show_field("Classificação", card["classification"], card["_sources"]["classification"])
        show_field("Tipo", card["wine_type"], card["_sources"]["wine_type"])
        show_field("Teor alcoólico", card["alcohol"], card["_sources"]["alcohol"])
        show_field("Aromas", card["aromas"], card["_sources"]["aromas"])
        show_field("Paladar", card["palate"], card["_sources"]["palate"])
        show_field("Acidez", card["acidity"], card["_sources"]["acidity"])
        show_field("Corpo", card["body"], card["_sources"]["body"])
        show_field("Solo", card["soil"], card["_sources"]["soil"])
        show_field("Clima", card["climate"], card["_sources"]["climate"])
        show_field("Terroir", card["terroir"], card["_sources"]["terroir"])
        show_field("Amadurecimento", card["aging"], card["_sources"]["aging"])
        show_field("Harmonização", card["pairing"], card["_sources"]["pairing"])
        show_field("Observações", card["notes"], card["_sources"]["notes"])

        st.subheader("🧠 Parser da consulta")
        st.json(report["parser"])

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

        st.subheader("🧠 Knowledge base")
        if report["knowledge_matches"]:
            for i, item in enumerate(report["knowledge_matches"], start=1):
                st.write(f"**Match {i}**")
                st.json(item)
        else:
            st.write("Nenhuma correspondência encontrada na knowledge base.")

        st.subheader("🌐 Fontes online encontradas")
        if report["online_sources"]:
            for i, src in enumerate(report["online_sources"], start=1):
                st.write(f"**Fonte {i}**")
                st.write(f"**Título:** {src.get('title', '')}")
                st.write(f"**URL:** {src.get('url', '')}")
                if src.get("snippet"):
                    st.write(f"**Snippet:** {src.get('snippet', '')}")
                if src.get("page_summary"):
                    st.write("**Resumo bruto da página:**")
                    st.write(src.get("page_summary"))
                if src.get("parsed_data"):
                    st.write("**Extração estruturada:**")
                    st.json(src.get("parsed_data"))
                st.markdown("---")
        else:
            st.write("Nenhuma fonte online relevante foi consolidada.")


if __name__ == "__main__":
    main()
