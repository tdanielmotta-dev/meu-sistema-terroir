import streamlit as st
from database import init_db, seed_if_empty
from report_builder import build_wine_report


def render_wine_block(wine):
    st.subheader("🍷 Vinho encontrado no banco local")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Produtor:** {wine.get('producer', '-')}")
        st.write(f"**Vinho:** {wine.get('wine_name', '-')}")
        st.write(f"**Safra:** {wine.get('vintage', '-')}")
        st.write(f"**Uva principal:** {wine.get('grape', '-')}")
        st.write(f"**Tipo:** {wine.get('wine_type', '-')}")

    with col2:
        st.write(f"**Região:** {wine.get('region', '-')}")
        st.write(f"**País:** {wine.get('country', '-')}")
        st.write(f"**Denominação:** {wine.get('denomination', '-')}")
        st.write(f"**Álcool:** {wine.get('alcohol', '-')}")
        st.write(f"**Score local:** {wine.get('_score', '-')}")

    notes = wine.get("notes")
    if notes:
        st.write("**Observações:**")
        st.write(notes)


def render_denomination_block(den):
    st.subheader("🛡️ Denominação encontrada no banco local")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**País:** {den.get('country', '-')}")
        st.write(f"**Região:** {den.get('region', '-')}")
        st.write(f"**Denominação:** {den.get('denomination', '-')}")
        st.write(f"**Classificação:** {den.get('classification', '-')}")

    with col2:
        st.write(f"**Álcool mínimo:** {den.get('min_alcohol', '-')}")
        st.write(f"**Castas permitidas:** {den.get('allowed_grapes', '-')}")
        st.write(f"**Regras de envelhecimento:** {den.get('aging_rules', '-')}")
        st.write(f"**Score local:** {den.get('_score', '-')}")

    notes = den.get
