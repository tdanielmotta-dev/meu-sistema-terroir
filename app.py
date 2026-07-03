import streamlit as st
import matplotlib.pyplot as plt

# Configuração da página web
st.set_page_config(page_title="Terroir Intelligence", page_icon="🍷")

st.title("🍷 Terroir Intelligence System")
st.write("Bem-vindo ao painel online de certificação de Denominações de Origem.")

# 1. Regras do jogo (Limites da D.O.)
LIMITES_DO = {
    "acidez_volatil_max": 15.0,
    "alcool_min": 12.0,
    "extrato_seco_min": 27.0,
    "ipt_min": 60
}

st.sidebar.header("🧪 Testar Seu Próprio Vinho")
nome_vinho = st.sidebar.text_input("Nome do Vinho", "Meu Merlot Artesanal")
acidez = st.sidebar.slider("Acidez Volátil (meq/L)", 5.0, 20.0, 11.2)
alcool = st.sidebar.slider("Teor Alcoólico (% v/v)", 9.0, 16.0, 13.5)
extrato = st.sidebar.slider("Extrato Seco (g/L)", 15.0, 40.0, 29.4)
ipt = st.sidebar.slider("Índice de Polifenóis (IPT)", 30, 90, 64)

# Lista de vinhos padrão + o vinho que você mexer nos botões
lotes = [
    {"nome": "Vinho Reserva Premium", "acidez_volatil": 11.2, "alcool": 13.5, "extrato_seco": 29.4, "ipt": 64},
    {"nome": "Vinho de Mesa Comum", "acidez_volatil": 16.2, "alcool": 11.1, "extrato_seco": 24.0, "ipt": 45},
    {"nome": "Vinho Gran Terroir", "acidez_volatil": 10.5, "alcool": 14.0, "extrato_seco": 31.0, "ipt": 70},
    {"nome": nome_vinho, "acidez_volatil": acidez, "alcool": alcool, "extrato_seco": extrato, "ipt": ipt}
]

aprovados = 0
reprovados = 0

st.subheader("📋 Relatório de Análise dos Lotes")

for lote in lotes:
    erros = []
    if lote["acidez_volatil"] > LIMITES_DO["acidez_volatil_max"]:
        erros.append(f"Acidez alta ({lote['acidez_volatil']} > {LIMITES_DO['acidez_volatil_max']})")
    if lote["alcool"] < LIMITES_DO["alcool_min"]:
        erros.append(f"Álcool baixo ({lote['alcool']}% < {LIMITES_DO['alcool_min']}%)")
    if lote["extrato_seco"] < LIMITES_DO["extrato_seco_min"]:
        erros.append(f"Muito ralo ({lote['extrato_seco']}g/L < {LIMITES_DO['extrato_seco_min']}g/L)")
    if lote["ipt"] < LIMITES_DO["ipt_min"]:
        erros.append(f"Pouca cor/tanino (IPT {lote['ipt']} < {LIMITES_DO['ipt_min']})")
        
    if erros:
        reprovados += 1
        st.error(f"❌ **{lote['nome']}** - REPROVADO")
        for e in erros:
            st.write(f"  ↳ {e}")
    else:
        aprovados += 1
        st.success(f"✅ **{lote['nome']}** - APROVADO! Selo D.O. Concedido.")

# Mostrar gráfico na tela
st.subheader("📊 Estatísticas Consolidadas")
fig, ax = plt.subplots(figsize=(5, 3))
ax.bar(['Aprovados', 'Reprovados'], [aprovados, reprovados], color=['#2ca02c', '#d62728'], width=0.4)
ax.set_ylabel('Quantidade')
st.pyplot(fig)
