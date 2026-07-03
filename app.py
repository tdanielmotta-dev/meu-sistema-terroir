import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WineIndex", page_icon="🍷", layout="wide")


def bootstrap():
    init_db()
    seed_if_empty()


def main():
    bootstrap()

    st.title("🍷 WineIndex")
    st.write("Digite um rótulo, produtor, safra, denominação ou região para pesquisar no banco local.")

    query = st.text_input(
        "Pesquisar vinho / rótulo / denominação",
        placeholder="Ex.: Château Margaux 2015, Barolo DOCG, Bordeaux AOC..."
    )

    if st.button("Pesquisar"):
        if not query.strip():
            st.warning("Digite algo para pesquisar.")
            return

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


if __name__ == "__main__":
    main()
