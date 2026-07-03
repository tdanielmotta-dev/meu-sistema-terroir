import streamlit as st
import pandas as pd

st.set_page_config(page_title="Minha Adega Virtual", page_icon="🍷")
st.title("🍷 Minha Adega Virtual com Memória")
st.write("Cadastre os vinhos que você tem em casa e guarde o seu histórico!")

# Criar a memória do site (se ela ainda não existir)
if "minha_adega" not in st.session_state:
    st.session_state["minha_adega"] = []

# Aba lateral para digitar os dados
st.sidebar.header("📝 Cadastrar Novo Vinho")
nome = st.sidebar.text_input("Nome do Vinho (Rótulo)", "Ex: Pera Manca")
uva = st.sidebar.selectbox("Uva Principal", ["Merlot", "Cabernet Sauvignon", "Chardonnay", "Malbec", "Tannat", "Outra"])
alcool = st.sidebar.slider("Teor Alcoólico (% vol)", 5.0, 20.0, 13.5)
safra = st.sidebar.number_input("Ano da Safra", min_value=1900, max_value=2026, value=2023)
nota = st.sidebar.slider("Sua Nota para o Vinho (⭐)", 1, 5, 5)

# Botão mágico de salvar na memória
bt_salvar = st.sidebar.button("💾 Salvar Vinho na Minha Adega")

if bt_salvar:
    # Cria a ficha do vinho
    novo_vinho = {
        "Nome": nome,
        "Uva": uva,
        "Álcool (%)": alcool,
        "Safra": int(safra),
        "Sua Nota": f"{'⭐' * nota}"
    }
    # Guarda na memória do site
    st.session_state["minha_adega"].append(novo_vinho)
    st.sidebar.success(f"Pronto! '{nome}' foi salvo na adega!")

# Mostrar os vinhos salvos na tela principal
st.subheader("📊 Meus Vinhos Cadastrados")

if len(st.session_state["minha_adega"]) == 0:
    st.info("Sua adega está vazia. Use o menu do lado esquerdo para salvar o seu primeiro vinho!")
else:
    # Transforma a lista de vinhos em uma tabela bonita na tela
    df = pd.DataFrame(st.session_state["minha_adega"])
    st.dataframe(df, use_container_width=True)
    
    # Mostra quantos vinhos você já tem cadastrados
    st.metric(label="Total de Garrafas na Adega", value=len(st.session_state["minha_adega"]))
