import streamlit as st

st.set_page_config(page_title="Rastreamento de Rótulos", page_icon="🍷")
st.title("🍷 Fiscalizador de Rótulos de Vinho")
st.write("Verifique se as informações do rótulo da garrafa cumprem as regras da região.")

# Regras Oficiais baseadas no que vem no rótulo
REGRAS_DO = {
    "alcool_minimo": 12.0,
    "uvas_permitidas": ["Merlot", "Chardonnay", "Pinot Noir", "Cabernet Sauvignon", "Malbec"],
    "safra_maxima": 2026
}

st.sidebar.header("📝 Digite os Dados do Rótulo")
nome = st.sidebar.text_input("Nome do Vinho", "Meu Vinho Favorito")
uva = st.sidebar.selectbox("Uva Principal (Casta)", ["Merlot", "Cabernet Sauvignon", "Chardonnay", "Pinot Noir", "Malbec", "Tannat"])
alcool = st.sidebar.number_input("Teor Alcoólico (% vol) indicado no rótulo", min_value=5.0, max_value=20.0, value=13.0, step=0.1)
safra = st.sidebar.number_input("Ano da Safra", min_value=1900, max_value=2030, value=2024)

# Execução da análise do Rótulo
erros = []

if alcool < REGRAS_DO["alcool_minimo"]:
    erros.append(f"Álcool abaixo do exigido para esta D.O. (O rótulo indica {alcool}%, mas o mínimo é {REGRAS_DO['alcool_minimo']}%).")

if uva not in REGRAS_DO["uvas_permitidas"]:
    erros.append(f"A uva '{uva}' não é autorizada nesta região protegida.")

if safra > REGRAS_DO["safra_maxima"]:
    erros.append(f"Ano de safra inválido ou futuro ({safra}).")

st.subheader("🔍 Resultado da Auditoria do Rótulo")

if erros:
    st.error(f"❌ **{nome}** possui inconformidades no rótulo:")
    for e in erros:
        st.write(f" ↳ {e}")
else:
    st.success(f"✅ **{nome}** cumpre todas as exigências visíveis do rótulo! Selo D.O. Confirmado.")
