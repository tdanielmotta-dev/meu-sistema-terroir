import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WineIndex", page_icon="🍷", layout="wide")

init_db()
seed_if_empty()

st.title("🍷 WineIndex")
st.write("Pesquisa local de rótulos, vinhos e denominações.")

query = st.text_input(
    "Digite o rótulo / produtor / denominação / região",
    placeholder="Ex.: Barolo DOCG, Château Margaux 2015, Bordeaux AOC"
)

if st.button("Pesquisar"):
    if not query.strip():
        st.warning("Digite algo para pesquisar.")
    else:
        report = build_wine_report(query)

        st.subheader("Resultado")
        for line in report["summary"]:
            st.write(f"- {line}")

        if report["wine_found"]:
            st.markdown("## Vinho encontrado")
            st.json(report["wine_found"])

        if report["denomination_found"]:
            st.markdown("## Denominação encontrada")
            st.json(report["denomination_found"])
