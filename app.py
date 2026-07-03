import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WineIndex", page_icon="🍷", layout="centered")


def bootstrap_database():
    """
    Garante que o banco exista e tenha ao menos dados seed
    antes de qualquer pesquisa.
    """
    init_db()
    seed_if_empty()


def render_wine_block(wine: dict):
    st.subheader("🍷 Vinho encontrado")
    st.write(f"**Produtor:** {wine.get('producer', '-')}")
    st.write(f"**Rótulo:** {wine.get('wine_name', '-')}")
    st.write(f"**Safra:** {wine.get('vintage', '-')}")
    st.write(f"**Uva:** {wine.get('grape', '-')}")
    st.write(f"**Região:** {wine.get('region', '-')}")
    st.write(f"**País:** {wine.get('country', '-')}")
    st.write(f"**Denominação:** {wine.get('denomination', '-')}")
    st.write(f"**Tipo:** {wine.get('wine_type', '-')}")
    st.write(f"**Álcool:** {wine.get('alcohol', '-')}")
    st.write(f"**Notas:** {wine.get('notes', '-')}")
    st.write(f"**Score local:** {wine.get('_score', '-')}")


def render_denomination_block(den: dict):
    st.subheader("🏛️ Denominação encontrada")
    st.write(f"**País:** {den.get('country', '-')}")
    st.write(f"**Região:** {den.get('region', '-')}")
    st.write(f"**Denominação:** {den.get('denomination', '-')}")
    st.write(f"**Classificação:** {den.get('classification', '-')}")
    st.write(f"**Uvas permitidas:** {den.get('allowed_grapes', '-')}")
    st.write(f"**Álcool mínimo:** {den.get('min_alcohol', '-')}")
    st.write(f"**Regras de amadurecimento:** {den.get('aging_rules', '-')}")
    st.write(f"**Notas:** {den.get('notes', '-')}")
    st.write(f"**Score local:** {den.get('_score', '-')}")


def main():
    # MUITO IMPORTANTE: inicializa o banco antes de qualquer consulta
    bootstrap_database()

    st.title("🍷 WineIndex")
    st.write("Pesquisa local de rótulos, vinhos e denominações.")

    query = st.text_input(
        "Digite o rótulo / produtor / denominação / região",
        placeholder="Ex.: Barolo DOCG, Château Margaux 2015, Bordeaux AOC"
    )

    if st.button("Pesquisar"):
        if not query.strip():
            st.warning("Digite alguma busca.")
            return

        report = build_wine_report(query)

        st.subheader("📋 Resumo")
        for line in report.get("summary", []):
            st.write(f"- {line}")

        wine = report.get("wine_found")
        denomination = report.get("denomination_found")

        if wine:
            render_wine_block(wine)

        if denomination:
            render_denomination_block(denomination)

        if not wine and not denomination:
            st.info("Nada encontrado no banco local para essa consulta.")


if __name__ == "__main__":
    main()
