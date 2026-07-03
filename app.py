import streamlit as st

st.set_page_config(page_title="Master Terroir & Enologia", page_icon="🍷", layout="wide")

st.title("🍇 Terroir & Enologia Intelligence System")
st.write("Configuração global ativada. Altere qualquer variável de campo ou de vinícola para debulhar o perfil técnico completo.")

# ==========================================
# PAINEL LATERAL: ENTRADA DE DADOS GLOBAL
# ==========================================
st.sidebar.header("🌍 1. Origem e Clima (Terroir)")

pais = st.sidebar.selectbox("País de Origem", [
    "França", "Itália", "Portugal", "Espanha", "Alemanha", 
    "Brasil", "Argentina", "Chile", "EUA", "África do Sul", 
    "Nova Zelândia", "Grécia"
])

# Seleção Dinâmica de Regiões Globais
if pais == "França":
    regiao = st.sidebar.selectbox("Região Protegida", ["Bordeaux (Margem Esquerda)", "Bordeaux (Margem Direita)", "Champagne", "Borgonha"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Cabernet Sauvignon", "Merlot", "Chardonnay", "Pinot Noir"])
elif pais == "Itália":
    regiao = st.sidebar.selectbox("Região Protegida", ["Chianti Classico UGA", "Brunello di Montalcino", "Barolo DOCG"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Sangiovese", "Nebbiolo"])
elif pais == "Portugal":
    regiao = st.sidebar.selectbox("Região Protegida", ["Douro DOP", "Alentejo DOP", "Vinho Verde Alvarelhão"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Touriga Nacional", "Aragonez", "Alvarinho"])
elif pais == "Espanha":
    regiao = st.sidebar.selectbox("Região Protegida", ["Rioja DOCa", "Ribera del Duero", "Priorat DOQ"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Tempranillo", "Garnacha"])
elif pais == "Alemanha":
    regiao = st.sidebar.selectbox("Região Protegida", ["Mosel g.U.", "Rheingau vdp"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Riesling"])
elif pais == "Brasil":
    regiao = st.sidebar.selectbox("Região Protegida", ["Vale dos Vinhedos D.O.", "Campanha Gaúcha"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Merlot", "Tannat", "Chardonnay"])
elif pais == "Argentina":
    regiao = st.sidebar.selectbox("Região Protegida", ["Vale do Uco (Mendoza)", "Luján de Cuyo D.O."])
    uva = st.sidebar.selectbox("Casta Dominante", ["Malbec", "Cabernet Franc"])
elif pais == "Chile":
    regiao = st.sidebar.selectbox("Região Protegida", ["Vale do Maipo (Andes)", "Vale de Casablanca (Costa)"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Cabernet Sauvignon", "Carménère", "Sauvignon Blanc"])
elif pais == "EUA":
    regiao = st.sidebar.selectbox("Região Protegida", ["Napa Valley (Solo Vulcânico)", "Napa Valley (Aluvial)"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Cabernet Sauvignon", "Chardonnay"])
elif pais == "África do Sul":
    regiao = st.sidebar.selectbox("Região Protegida", ["Stellenbosch WO", "Swartland Old Vines"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Chenin Blanc", "Pinotage", "Syrah"])
elif pais == "Nova Zelândia":
    regiao = st.sidebar.selectbox("Região Protegida", ["Marlborough GI", "Central Otago Schist"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Sauvignon Blanc", "Pinot Noir"])
elif pais == "Grécia":
    regiao = st.sidebar.selectbox("Região Protegida", ["Santorini PDO", "Naoussa PDO"])
    uva = st.sidebar.selectbox("Casta Dominante", ["Assyrtiko", "Xinomavro"])

alcool = st.sidebar.slider("Teor Alcoólico do Rótulo (% vol)", 10.5, 16.0, 13.5)

st.sidebar.header("🪵 2. Processo de Produção (Enologia)")
levedura = st.sidebar.radio("Tipo de Levedura", ["Indígenas (Selvagens do Vinhedo)", "Selecionadas (Laboratório)"])
macencao = st.sidebar.slider("Tempo de Maceração com as Cascas (Dias)", 2, 30, 14)
temperatura = st.sidebar.slider("Temperatura de Fermentação (°C)", 15, 32, 26)
barrica = st.sidebar.selectbox("Estágio em Carvalho", ["Sem passagem por madeira", "Carvalho Francês Novo", "Carvalho Francês Usado", "Carvalho Americano Novo"])
tempo_barrica = st.sidebar.slider("Tempo de Barrica (Meses)", 0, 36, 12 if "Sem" not in barrica else 0)

# ==========================================
# MOTOR DE INFERÊNCIA: COMPILAÇÃO DE DADOS
# ==========================================
p_solo, p_clima, p_aroma, p_acidez, p_tanino, p_corpo = "", "", "", "", "", ""

# Deduções Geográficas Baseadas no Terroir Selecionado
if regiao == "Bordeaux (Margem Esquerda)":
    p_solo = "Croupes de graves (cascalho quartzoso profundo sobre matriz argilo-arenosa)."
    p_clima = "Oceânico marítimo moderado pela floresta de Landes e o estuário da Gironde."
    p_aroma = "Groselha preta (cassis), caixa de charuto, cedro, grafite e terra molhada."
    p_acidez = "Alta e linear, conferindo enorme potencial de guarda secular."
elif regiao == "Bordeaux (Margem Direita)":
    p_solo = "Calcário argiloso profundo e bolsões de argila azul rica em ferro (Smectite)."
    p_clima = "Oceânico temperado com menor influência marítima direta."
    p_aroma = "Ameixas pretas, chocolate amargo, notas florais sutis e especiarias secas."
    p_acidez = "Moderada a firme, textura incrivelmente aveludada."
elif regiao == "Champagne":
    p_solo = "Solos de giz puro e calcário belemnita de origem marinha fóssil."
    p_clima = "Continental fresco de limite norte de cultivo, alta amplitude térmica."
    p_aroma = "Brioche, maçã verde, amêndoas torradas, giz e notas salinas."
    p_acidez = "Cortante, elétrica e extremamente refrescante."
elif regiao == "Borgonha":
    p_solo = "Marly-limestone (mistura fina de argila e calcário do Jurássico)."
    p_clima = "Continental fresco com riscos severos de geadas na primavera."
    p_aroma = "Frutas vermelhas azedas (cereja, framboesa), sub-bosque, cogumelos e traços minerais."
    p_acidez = "Alta, vertical e integrada à fineza da fruta."
elif regiao == "Chianti Classico UGA":
    p_solo = "Galestro (argila xistosa friável) e Albarese (calcário compacto marinho)."
    p_clima = "Continental modificado com verões quentes e noites de montanha frias."
    p_aroma = "Cerejas azedas, ervas secas italianas (alecrim, tomilho), couro e sangue."
    p_acidez = "Vibrante, gastronômica e salivante."
elif regiao == "Brunello di Montalcino":
    p_solo = "Solos esqueléticos de Galestro em encostas de alta altitude."
    p_clima = "Mais quente e seco que Chianti, protegido pelo Monte Amiata."
    p_aroma = "Frutas negras densas, tabaco, alcatrão, especiarias exóticas e couro velho."
    p_acidez = "Firme com coluna vertebral tânica massiva."
elif regiao == "Barolo DOCG":
    p_solo = "Solos tortonianos de marga azul-acinzentada (argila, calcário e areia)."
    p_clima = "Continental alpino com névoas outonais marcantes (Nebbia)."
    p_aroma = "Alcatrão, rosas secas, trufas brancas, folhas secas e canela."
    p_acidez = "Altíssima, trabalhando junto com taninos severos de maturação lenta."
elif regiao == "Douro DOP":
    p_solo = "Encostas verticais fraturadas de xisto puro (pedra folheada vertical)."
    p_clima = "Continental mediterrâneo extremo, verões escaldantes e invernos rigorosos."
    p_aroma = "Frutas pretas concentradas, esteva (resina silvestre), violetas e grafite."
    p_acidez = "Equilibrada a firme, mineralidade de pedra quebrada."
elif regiao == "Alentejo DOP":
    p_solo = "Planícies de solos graníticos e quartzosos de baixa retenção hídrica."
    p_clima = "Mediterrâneo quente e ensolarado com maturação precoce."
    p_aroma = "Geléia de amora, especiarias doces, baunilha e notas quentes defumadas."
    p_acidez = "Baixa a moderada, vinho gordo, redondo e macio."
elif regiao == "Vinho Verde Alvarelhão":
    p_solo = "Solos graníticos arenosos de decomposição ácida profunda."
    p_clima = "Atlântico muito úmido, frio e com ventos marítimos constantes."
    p_aroma = "Frutas cítricas cortantes, pimenta branca, notas florais e salinidade ativa."
    p_acidez = "Altíssima, picante e refrescante."
elif regiao == "Rioja DOCa":
    p_solo = "Solos argilo-calcários nas encostas altas e argilo-ferrosos nas baixas."
    p_clima = "Continental moderado protegido pela Cordilheira Cantábrica."
    p_aroma = "Baunilha, coco, endro (do carvalho americano), cerejas maduras e couro."
    p_acidez = "Firme e sedosa, com taninos polidos pelo longo envelhecimento."
elif regiao == "Ribera del Duero":
    p_solo = "Camadas alternadas de calcário calcificado, giz e argilas aluviais."
    p_clima = "Continental extremo, verões curtos e tórridos, noites congelantes."
    p_aroma = "Frutas pretas massivas, alcaçuz, tostado intenso, café e especiarias."
    p_acidez = "Firme com taninos mastigáveis de grande potência."
elif regiao == "Priorat DOQ":
    p_solo = "Solo único de Licorella (xisto escuro misturado com partículas de mica reluzente)."
    p_clima = "Mediterrâneo continental árido, isolado e montanhoso."
    p_aroma = "Fruta preta licorosa, alcatrão, fumo, mineralidade mineral ardósia e grafite."
    p_acidez = "Equilibrada com taninos muito concentrados e potentes."
elif regiao == "Mosel g.U.":
    p_solo = "Xisto azul (Blauschiefer) e xisto vermelho (Rotschiefer) em encostas de até 68°."
    p_clima = "Continental frio regulado pelo reflexo de luz do espelho d'água do rio Mosel."
    p_aroma = "Petróleo (querosene em vinhos velhos), pêssego branco, jasmim e pedra lascada."
    p_acidez = "Elétrica, afiada como uma lâmina, equilibrando o açúcar natural."
elif regiao == "Rheingau vdp":
    p_solo = "Solos de quartzo misturados com loess e argilas sedimentares de encosta."
    p_clima = "Continental frio protegido pelas montanhas Taunus."
    p_aroma = "Damasco seco, raspas de limão siciliano, mel e mineralidade robusta."
    p_acidez = "Alta, encorpada e de grande volume estrutural."
elif regiao == "Vale dos Vinhedos D.O.":
    p_solo = "Basalto fraturado rico em ferro da Formação Serra Geral, encostas declivosas."
    p_clima = "Subtropical úmido de altitude (Cfb), alta pluviosidade na colheita."
    p_aroma = "Frutas vermelhas frescas (cereja, morango), especiarias finas, menta e couro fresco."
