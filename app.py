import streamlit as st

st.set_page_config(page_title="Consultor de Fichas Técnicas", page_icon="🍷")
st.title("🍷 Consultor de Fichas Técnicas de Terroir")
st.write("Escolha um vinho pelo rótulo para revelar as suas especificações técnicas escondidas de laboratório.")

# 1. Nosso Banco de Dados Interno (O catálogo de vinhos conhecidos pelo sistema)
BANCO_DE_DADOS_VINHOS = {
    "Pera Manca Tinto (Alentejo)": {
        "Uva Principal": "Trincadeira e Aragonez",
        "Teor Alcoólico": "14.5% vol",
        "Tipo de Solo": "Granítico com presença de quartzo",
        "Acidez Total": "5.8 g/L (Equilibrada)",
        "Extrato Seco": "31.2 g/L (Muito encorpado)",
        "IPT (Taninos)": "72 (Altíssima estrutura)",
        "Curiosidade": "Estagia 18 meses em tonéis de carvalho e mais 24 meses em garrafa antes de ir para o mercado."
    },
    "Château Margaux (Bordeaux)": {
        "Uva Principal": "Cabernet Sauvignon",
        "Teor Alcoólico": "13.5% vol",
        "Tipo de Solo": "Croupes de graves (Cascalho quartzoso profundo do Quaternário)",
        "Acidez Total": "6.2 g/L (Alta e refrescante)",
        "Extrato Seco": "29.5 g/L (Elegante e persistente)",
        "IPT (Taninos)": "78 (Taninos finos e massivos)",
        "Curiosidade": "É um Premier Grand Cru Classé desde a histórica Classificação de 1855."
    },
    "Almanaviva (Vale do Maipo)": {
        "Uva Principal": "Cabernet Sauvignon e Carménère",
        "Teor Alcoólico": "14.0% vol",
        "Tipo de Solo": "Aluvial pedregoso na base da Cordilheira dos Andes",
        "Acidez Total": "5.4 g/L (Macio)",
        "Extrato Seco": "30.8 g/L (Estruturado)",
        "IPT (Taninos)": "68 (Taninos maduros e sedosos)",
        "Curiosidade": "Uma parceria lendária entre a Viña Concha y Toro e a francesa Baron Philippe de Rothschild."
    },
    "Brunello di Montalcino (Toscana)": {
        "Uva Principal": "Sangiovese Grosso",
        "Teor Alcoólico": "14.0% vol",
        "Tipo de Solo": "Galestro (argila xistosa friável) e Albarese (calcário)",
        "Acidez Total": "6.5 g/L (Vibrante)",
        "Extrato Seco": "28.8 g/L (Vertical e profundo)",
        "IPT (Taninos)": "75 (Muita garra e potência tânica)",
        "Curiosidade": "Exige por lei um envelhecimento mínimo de 5 anos antes de ser vendido."
    }
}

# 2. Interface de Escolha para o Usuário
st.sidebar.header("🔍 Selecione o Vinho do Rótulo")
vinho_selecionado = st.sidebar.selectbox(
    "Qual garrafa está na sua mão?",
    list(BANCO_DE_DADOS_VINHOS.keys())
)

# 3. Exibição da Ficha Técnica na Tela
if vinho_selecionado:
    ficha = BANCO_DE_DADOS_VINHOS[vinho_selecionado]
    
    st.subheader(f"📋 Ficha Técnica Oculta: {vinho_selecionado}")
    st.write("---")
    
    # Criando colunas bonitas para exibir os dados
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"🍇 **Uva:** {ficha['Uva Principal']}")
        st.info(f"🧪 **Teor Alcoólico:** {ficha['Teor Alcoólico']}")
        st.info(f"💎 **Tipo de Solo:** {ficha['Tipo de Solo']}")
        
    with col2:
        st.warning(f"📉 **Acidez Total:** {ficha['Acidez Total']}")
        st.warning(f"🪵 **Extrato Seco:** {ficha['Extrato Seco']}")
        st.warning(f"🧬 **Índice de Taninos (IPT):** {ficha['IPT (Taninos)']}")
        
    st.success(f"💡 **História e Curiosidade:** {ficha['Curiosidade']}")
