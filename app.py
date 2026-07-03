import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report

st.set_page_config(page_title="WINEINDEX OMEGA V12", page_icon="🍷", layout="wide")

def show_match_block(report):
    wine = report.get("local_wine_match")
    do = report.get("local_denomination_match")

    st.subheader("1) Interpretação inicial do rótulo")
    st.json(report["parsed"])

    st.subheader("2) Melhor correspondência local — vinho")
    if wine and wine["score"] >= 45:
        st.success(f"Match local encontrado: {wine['wine_name']} ({wine['score']} pontos)")
        st.write(f"**Produtor:** {wine['producer']}")
        st.write(f"**País:** {wine['country']}")
        st.write(f"**Região:** {wine['macro_region']}")
        st.write(f"**Sub-região:** {wine['sub_region']}")
        st.write(f"**Denominação:** {wine['appellation_name']}")
        st.write(f"**Safra cadastrada:** {wine['vintage']}")
        st.write(f"**Uvas:** {wine['grapes']}")
        st.write(f"**Estilo:** {wine['style']}")
        st.write(f"**Notas:** {wine['notes']}")
    else:
        st.warning("Nenhum vinho local suficientemente forte encontrado.")

    st.subheader("3) Melhor correspondência local — denominação")
    if do and do["score"] >= 40:
        st.success(f"Denominação local encontrada: {do['appellation_name']} ({do['score']} pontos)")
        st.write(f"**ID:** {do['universal_id']}")
        st.write(f"**País:** {do['country']}")
        st.write(f"**Macro-região:** {do['macro_region']}")
        st.write(f"**Sub-região:** {do['sub_region']}")
        st.write(f"**Nível legal:** {do['legal_level']}")
        st.write(f"**Escopo:** {do['wine_color_scope']}")
        st.write(f"**Álcool mínimo:** {do['alcohol_min']}")
        st.write(f"**Castas permitidas:** {do['allowed_grapes']}")
        st.write(f"**Notas:** {do['notes']}")
    else:
        st.warning("Nenhuma denominação local suficientemente forte encontrada.")

    st.subheader("4) Pesquisa complementar na internet")
    web = report["web_results"]

    if web.get("error"):
        st.error(f"Erro na busca web: {web['error']}")
    else:
        if not web["results"]:
            st.warning("Nenhum resultado web retornado.")
        else:
            for idx, item in enumerate(web["results"], start=1):
                st.markdown(f"**{idx}. {item['title']}**")
                st.write(item["url"])

def main():
    init_db()
    seed_if_empty()

    st.title("🍷 WINEINDEX OMEGA V12 — Motor de Pesquisa de Vinhos")
    st.caption("Pesquisa híbrida: banco local + internet")

    label = st.text_input(
        "Digite o rótulo / nome do vinho / produtor / safra",
        placeholder="Ex.: Chateau d'Yquem 2015"
    )

    if st.button("Pesquisar"):
        if not label.strip():
            st.warning("Digite algum rótulo ou nome de vinho.")
            return

        with st.spinner("Pesquisando no banco e na internet..."):
            report = build_wine_report(label)

        show_match_block(report)

if __name__ == "__main__":
    main()
