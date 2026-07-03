import streamlit as st

st.set_page_config(page_title="Master Terroir Intelligence", page_icon="🌐", layout="wide")

st.title("🌐 Terroir & Enological Intelligence System")
st.write("O simulador definitivo de perfis de vinho. Altere os fatores geográficos e todas as variáveis de produção para debulhar o resultado molecular e sensorial do vinho.")

# ===================================================================
# PAINEL DE CONTROLE LATERAL: TODAS AS VARIÁVEIS DO PLANETA
# ===================================================================
st.sidebar.header("🌍 1. LOCALIZAÇÃO E GEOGRAFIA GLOBAL")

continente = st.sidebar.selectbox("Continente", ["Europa (Velho Mundo)", "Américas (Novo Mundo)", "Hemisfério Sul & Fronteiras"])

if continente == "Europa (Velho Mundo)":
    pais = st.sidebar.selectbox("País", ["França", "Itália", "Portugal", "Alemanha", "Grécia"])
    if pais == "França":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Bordeaux (Margem Esquerda)", "Bordeaux (Margem Direita)", "Champagne", "Borgonha (Côte d'Or)"])
        uva = st.sidebar.selectbox("Uva Principal", ["Cabernet Sauvignon", "Merlot", "Pinot Noir", "Chardonnay"])
    elif pais == "Itália":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Chianti Classico (UGA Radda)", "Chianti Classico (UGA Panzano)", "Brunello di Montalcino", "Barolo DOCG"])
        uva = st.sidebar.selectbox("Uva Principal", ["Sangiovese", "Nebbiolo"])
    elif pais == "Portugal":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Douro", "Alentejo", "Vinho Verde (Monção e Melgaço)"])
        uva = st.sidebar.selectbox("Uva Principal", ["Touriga Nacional", "Aragonez", "Alvarinho"])
    elif pais == "Alemanha":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Mosel (Encostas Íngremes)", "Rheingau"])
        uva = st.sidebar.selectbox("Uva Principal", ["Riesling"])
    elif pais == "Grécia":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Santorini PDO (Solo Vulcânico)", "Naoussa"])
        uva = st.sidebar.selectbox("Uva Principal", ["Assyrtiko", "Xinomavro"])

elif continente == "Américas (Novo Mundo)":
    pais = st.sidebar.selectbox("País", ["Brasil", "Estados Unidos", "Argentina", "Chile"])
    if pais == "Brasil":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Vale dos Vinhedos (D.O.)", "Campanha Gaúcha", "Vale do São Francisco (Semiárido)"])
        uva = st.sidebar.selectbox("Uva Principal", ["Merlot", "Tannat", "Syrah"])
    elif pais == "Estados Unidos":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Napa Valley (Solo Vulcânico de Altitude)", "Napa Valley (Solo Aluvial do Vale)", "Russian River Valley"])
        uva = st.sidebar.selectbox("Uva Principal", ["Cabernet Sauvignon", "Pinot Noir", "Chardonnay"])
    elif pais == "Argentina":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Vale do Uco (Mendoza - Calcário)", "Luján de Cuyo", "Salta (Cafayate - Altitude Extrema)"])
        uva = st.sidebar.selectbox("Uva Principal", ["Malbec", "Torrontés", "Cabernet Franc"])
    elif pais == "Chile":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Vale do Maipo (Andes)", "Vale de Casablanca (Costa Fria)", "Vale do Colchagua"])
        uva = st.sidebar.selectbox("Uva Principal", ["Carménère", "Cabernet Sauvignon", "Sauvignon Blanc"])

elif continente == "Hemisfério Sul & Fronteiras":
    pais = st.sidebar.selectbox("País", ["África do Sul", "Nova Zelândia", "Austrália"])
    if pais == "África do Sul":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Stellenbosch (Granito Antigo)", "Swartland (Solo Seco sem Irrigação)"])
        uva = st.sidebar.selectbox("Uva Principal", ["Chenin Blanc", "Pinotage", "Syrah"])
    elif pais == "Nova Zelândia":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Marlborough", "Central Otago (Xisto Glacial)"])
        uva = st.sidebar.selectbox("Uva Principal", ["Sauvignon Blanc", "Pinot Noir"])
    elif pais == "Austrália":
        regiao = st.sidebar.selectbox("Região / D.O.", ["Barossa Valley (Vinhas Velhas)", "Coonawarra (Solo de Terra Rossa)"])
        uva = st.sidebar.selectbox("Uva Principal", ["Shiraz", "Cabernet Sauvignon"])

# VARIÁVEIS DO RÓTULO
alcool = st.sidebar.slider("Teor Alcoólico do Rótulo (% vol)", 8.5, 16.0, 13.5, step=0.1)
safra = st.sidebar.number_input("Ano da Safra", min_value=1950, max_value=2026, value=2023)

st.sidebar.write("---")
st.sidebar.header("🧪 2. ENGENHARIA DE VITICULTURA E PRODUÇÃO")

tipo_colheita = st.sidebar.radio("Método de Colheita", ["Manual Selecionada (Preserva bagos)", "Mecânica Noturna (Evita oxidação)", "Mecânica Padrão"])
levedura = st.sidebar.selectbox("Tipo de Fermentação / Levedura", ["Nativa / Selvagem (Traz complexidade do vinhedo)", "Selecionada de Laboratório (Previsível e limpa)"])
controle_termico = st.sidebar.checkbox("Controle de Temperatura Rigoroso na Fermentação", value=True)

st.sidebar.write("---")
st.sidebar.header("🪵 3. ENVELHECIMENTO E CARVALHO")
passagem_madeira = st.sidebar.radio("O Vinho passa por Madeira?", ["Não (Foco total na fruta pura)", "Sim (Barricas Novas de Carvalho Francês)", "Sim (Barricas Usadas de Carvalho Americano)", "Sim (Grandes Tonéis de Madeira Antiga)"])

if passagem_madeira != "Não (Foco total na fruta pura)":
    tempo_madeira = st.sidebar.slider("Tempo de estágio em madeira (Meses)", 3, 36, 12)
else:
    tempo_madeira = 0

# ===================================================================
# MOTOR DE INFERÊNCIA E DEDUÇÃO MOLECULAR (DEBULHANDO TUDO)
# ===================================================================

# Variáveis Base de Análise
solo_desc = ""
clima_desc = ""
acidez_analise = "Equilibrada"
tanino_analise = "Médio"
perfil_aromatico = []
estilo_corpo = "Médio Corpo"
potencial_guarda = "3 a 5 anos"

# 1. CÁLCULO DO CORPO E ESTRUTURA BASEADO NO ÁLCOOL
if alcool >= 14.5:
    estilo_corpo = "Muito Encorpado, denso, pesado no palato e alcóolico"
elif alcool >= 13.5:
    estilo_corpo = "Encorpado e estruturado"
elif alcool >= 12.0:
    estilo_corpo = "Corpo Médio, equilibrado e fluido"
else:
    estilo_corpo = "Corpo Leve, vertical, magro e muito fácil de beber"

# 2. MICRO-MAPEAMENTO GEOLÓGICO E CLIMÁTICO GLOBAL
if regiao == "Bordeaux (Margem Esquerda)":
    solo_desc = "Croupes de Graves: Terraços profundos de cascalhos e seixos rolados do Quaternário. Altíssima drenagem e reflexão de calor."
    clima_desc = "Oceânico temperado marítimo, protegido pela floresta de Landes e regulado pelo Estuário da Gironde."
    acidez_analise = "Alta, linear e firme."
    tanino_analise = "Alto, potente e mastigável."
    perfil_aromatico += ["Groselha preta (Cassis)", "Folha de tabaco", "Cedro / Caixa de Charuto", "Grafite"]
elif regiao == "Bordeaux (Margem Direita)":
    solo_desc = "Solos argilo-calcários profundos sobre platô de calcário de Fronsac e manchas de argila azul rica em ferro (Smectite)."
    clima_desc = "Oceânico com sutil transição continental, menor influência direta do mar."
    acidez_analise = "Moderada a alta, redonda."
    tanino_analise = "Médio-Alto, aveludado e sedoso."
    perfil_aromatico += ["Ameixa preta madura", "Cacau", "Trufas / Solo de floresta", "Especiarias doces"]
elif regiao == "Chianti Classico (UGA Radda)":
    solo_desc = "Predomínio severo de Galestro (argila xistosa friável) e rochas esqueléticas de Albarese."
    clima_desc = "Continental de altitude fria, cercado por florestas. Altíssima amplitude térmica diária."
    acidez_analise = "Altíssima, vibrante e cortante."
    tanino_analise = "Alto, nervoso, giz e poeira de pedra."
    perfil_aromatico += ["Cereja azeda", "Violetas secas", "Ervas aromáticas (Tomilho/Alecrim)", "Sangue/Ferrugem"]
elif regiao == "Chianti Classico (UGA Panzano)":
    solo_desc = "Anfiteatro da Conca d'Oro. Solos ricos de Galestro profundo intercalados com argilas férteis."
    clima_desc = "Clima perfeitamente ensolarado, exposição total ao Sul, capturando máxima radiação térmica."
    acidez_analise = "Alta, porém integrada ao volume de fruta."
    tanino_analise = "Alto, robusto, maduro e amplo."
    perfil_aromatico += ["Cereja preta madura", "Couro curtido", "Alcaçuz", "Toque balsâmico"]
elif regiao == "Vale dos Vinhedos (D.O.)":
    solo_desc = "Planalto basáltico fracionado derivado de derrames vulcânicos antigos (Serra Geral). Riquíssimo em ferro."
    clima_desc = "Subtropical úmido de altitude. Alta pluviosidade corrigida por fortes declividades que escoam a água."
    acidez_analise = "Vibrante, gastronômica e muito salivante."
    tanino_analise = "Médio-Alto, firme e reto."
    perfil_aromatico += ["Morango e cereja frescos", "Goiaba", "Toque sutil de couro úmido", "Mentol fresco"]
elif regiao == "Vale do Uco (Mendoza - Calcário)":
    solo_desc = "Cones aluviais andinos severos. Seixos rolados cobertos por uma crosta branca de carbonato de cálcio puro (Calcário Ativo)."
    clima_desc = "Desértico de altitude extrema (até 1.600m). Radiação ultravioleta brutal e noites congelantes."
    acidez_analise = "Altíssima, elétrica e refrescante (impulsionada pelo frio da montanha)."
    tanino_analise = "Alto, textura granulada que lembra poeira de giz ou cimento."
    perfil_aromatico += ["Mirtilo", "Lápis de cor / Mineral de pedra", "Violetas intensas", "Pimenta preta moida"]
elif regiao == "Mosel (Encostas Íngremes)":
    solo_desc = "Xisto Azul (Blauschiefer) e Xisto Vermelho (Rotschiefer) puro em encostas com inclinação vertical de até 68°."
    clima_desc = "Continental frio limitante. O rio Mosel funciona como espelho parabólico refletindo raios de sol para as videiras."
    acidez_analise = "Cítrica, cortante, quase uma agulha de acidez cristalina."
    tanino_analise = "Baixo (Quase nulo em brancos, focado na extração mineral)."
    perfil_aromatico += ["Petróleo / Querosene (Típico de Riesling velha)", "Limão siciliano", "Pêssego verde", "Pedra de Isqueiro/Pólvora"]
elif regiao == "Santorini PDO (Solo Vulcânico)":
