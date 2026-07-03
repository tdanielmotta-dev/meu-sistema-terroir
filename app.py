import streamlit as st

st.set_page_config(page_title="Terroir Intelligence Engine", page_icon="🍷", layout="wide")

st.title("🍷 Terroir Intelligence System — Global Engine")
st.write("Insira as informações do rótulo para debulhar o perfil completo de terroir e produção do vinho.")

# ==========================================
# ⚙️ 1. BANCO DE DADOS GLOBAL DE ADIVINHAÇÃO (TERROIR ANCHORS)
# ==========================================
BASE_TERROIR = {
    "Portugal": {
        "Alentejo": {
            "solo": "Matriz de planícies graníticas e xistosas, solos rasos e de baixíssima retenção hídrica.",
            "clima": "Clima mediterrâneo continental severo, com verões escaldantes e noites secas.",
            "acidez": "Acidez natural moderada a baixa. O calor reduz o ácido málico nas uvas, exigindo colheitas antecipadas.",
            "perfil": "Vinhos volumosos, redondos, com notas intensas de geleia de amora, ameixa preta madura e especiarias doces."
        },
        "Douro": {
            "solo": "Encostas verticais e terraços esculpidos em xisto puro e duro (fraturamento vertical de rocha metamórfica).",
            "clima": "Clima de extremos, protegido pelas montanhas do Marão. Verões secos e invernos rigorosos.",
            "acidez": "Acidez firme e gastronômica, sustentada por uma estrutura tânica massiva e rústica.",
            "perfil": "Concentração brutal de frutas pretas, notas de esteva (erva local), violetas, chocolate amargo e mineralidade de pedra."
        }
    },
    "França": {
        "Bordeaux": {
            "solo": "Croupes de graves (terraços de cascalhos, quartzo e seixos rolados profundos sobre base argilosa).",
            "clima": "Oceânico temperado marítimo, regulado pelo estuário da Gironde e protegido pela floresta de Landes.",
            "acidez": "Acidez elegante, linear e de sustentação. Perfil projetado para suportar décadas de envelhecimento.",
            "perfil": "Notas clássicas de groselha preta (cassis), caixa de charuto, cedro, grafite e discretos toques de pimentão assado."
        },
        "Champagne": {
            "solo": "Solo calcário puro de cré (giz belemnita do período Cretáceo), altamente poroso e reflexivo.",
            "clima": "Clima continental frio, no limite norte absoluto da viticultura mundial estável.",
            "acidez": "Acidez cortante, elétrica e cristalina. O frio extremo preserva os ácidos mesmo na maturação completa.",
            "perfil": "Notas de brioche, fermento de pão, maçã verde, giz úmido, avelãs e uma textura efervescente ultra-fina."
        }
    },
    "Brasil": {
        "Vale dos Vinhedos": {
            "solo": "Planalto de derrames basálticos ricos em ferro. Encostas com forte declividade e excelente escoamento.",
            "clima": "Subtropical úmido de altitude. Alta pluviosidade anual que exige manejo cirúrgico da copa.",
            "acidez": "Acidez vibrante, refrescante e alta, conferindo leveza e excelente aptidão gastronômica.",
            "perfil": "Frutas vermelhas frescas (cereja, morango), notas de especiarias finas, terra úmida e couro leve."
        },
        "Campanha Gaúcha": {
            "solo": "Campos levemente ondulados (coxilhas), solos arenosos, profundos e muito antigos estruturalmente.",
            "clima": "Subtropical temperado com verões secos e alta insolação diária na fronteira com o Uruguai.",
            "acidez": "Acidez moderada a macia, entregando vinhos redondos e fáceis de tomar desde jovens.",
            "perfil": "Frutas escuras maduras, toque sutil de baunilha, folha seca e taninos muito dóceis no palato."
        }
    },
    "Argentina": {
        "Vale do Uco (Mendoza)": {
            "solo": "Cones aluviais de alta altitude com seixos rolados recobertos por ricas crostas de carbonato de cálcio.",
            "clima": "Clima desértico continental de altitude. Radiação ultravioleta extrema com noites congelantes.",
            "acidez": "Acidez linear e cortante, impulsionada pelo gradiente térmico da Cordilheira dos Andes.",
            "perfil": "Aromas explosivos de violetas, mirtilo fresco, toque mineral que remete a giz de lousa e taninos de textura de poeira."
        }
    },
    "Grécia": {
        "Santorini PDO": {
            "solo": "Asppa vulcânica pura: cinzas, pedra-pome pulverizada e lava solidificada. Zero argila (imune à filoxera).",
            "clima": "Clima mediterrâneo semiárido e extremo. Ventos violentos (Meltemi) curados pela névoa marítima noturna.",
            "acidez": "Acidez cítrica avassaladora e pungente, que desafia o calor da ilha.",
            "perfil": "Notas de limão siciliano, sal marinho, pólvora, fumaça e uma secura extrema na ponta da língua."
        }
    }
}

# ==========================================
# 📝 2. ENTRADA DE DADOS NO CANTO ESQUERDO (DADOS DO RÓTULO)
# ==========================================
st.sidebar.header("📝 Dados Contidos no Rótulo")

paises_disponiveis = list(BASE_TERROIR.keys())
pais = st.sidebar.selectbox("1. Escolha o País do Rótulo", paises_disponiveis)

regioes_disponiveis = list(BASE_TERROIR[pais].keys())
regiao = st.sidebar.selectbox("2. Escolha a Região/D.O.", regioes_disponiveis)

safra = st.sidebar.number_input("3. Ano da Safra indicado", min_value=1900, max_value=2026, value=2023)
alcool = st.sidebar.slider("4. Teor Alcoólico (% vol)", 8.0, 16.5, 13.5, step=0.1)

# Botão de Execução Total
gerar_perfil = st.sidebar.button("🚀 Debulhar Perfil Técnico", use_container_width=True)

# ==========================================
# 🧠 3. MOTOR DE INFERÊNCIA REVERSA DE PRODUÇÃO
# ==========================================
if gerar_perfil:
    # Coleta os dados de terroir estáticos da região
    dados_regiao = BASE_TERROIR[pais][regiao]
    
    st.subheader(f"🔍 Relatório Técnico de Engenharia Reversa: {regiao} (Safra {safra})")
    st.write("---")
    
    # --- BLOCO 1: O TERROIR ORIGINAL DO SOLO E CLIMA ---
    st.markdown("### 🗺️ Camada 1: Características do Terroir Original")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"💎 **Geologia e Pedologia do Solo:**\n\n{dados_regiao['solo']}")
    with col2:
        st.info(f"🌤️ **Dinâmica Macroclimática Regional:**\n\n{dados_regiao['clima']}")
        
    st.write("")
    
    # --- BLOCO 2: DEDUÇÃO COMPORTAMENTAL DO PRODUTOR (CÁLCULO AUTOMÁTICO) ---
    st.markdown("### 🧪 Camada 2: Decisões Ocultas de Produção e Adega")
    
    # Adivinhação baseada no Álcool do Rótulo
    if alcool >= 14.0:
        decisao_colheita = "O enólogo optou por uma **Colheita Tardia/Supermaturação**. Deixou as uvas na videira por mais tempo para concentrar açúcares, sacrificando parte da acidez natural em troca de potência e volume de boca."
        manejo_adega = "Para aguentar esse nível alcoólico sem desandar, o vinho provavelmente passou por **Envelhecimento Prolongado em Barricas de Carvalho Novo** para domar a potência e adicionar notas de baunilha/tostado."
    elif alcool < 12.5:
        decisao_colheita = "O enólogo optou por uma **Colheita Antecipada/Fresca**. As uvas foram colhidas assim que atingiram a maturação técnica básica, priorizando a retenção de acidez e evitando que o vinho ficasse pesado."
        manejo_adega = "A vinificação provavelmente priorizou **Tanques de Aço Inoxidável com Controle de Temperatura** (sem madeira nova) para preservar o frescor puro da fruta e a delicadeza dos aromas originais."
    else:
        decisao_colheita = "A colheita ocorreu na **Janela de Equilíbrio Clássico**. Buscou-se a intersecção exata entre a maturação dos taninos (fenólica) e a concentração ideal de açúcar sem perder o frescor."
        manejo_adega = "O manejo utilizou provavelmente **Barricas de Carvalho Usadas ou Grandes Tonéis**, aplicando uma micro-oxigenação sutil para amaciar os taninos sem mascarar a tipicidade da fruta."

    # Adivinhação baseada no Clima da Safra (Anos Ímpares vs Pares para simulação)
    if safra % 2 == 0:
        efeito_safra = f"A safra de {safra} foi marcada por um **Ano Seco e Quente** na região de {regiao}. Isso gerou bagas menores, cascas mais grossas e alta concentração natural de cor e taninos. Vinhos desse ano tendem a ser mais potentes."
    else:
        efeito_safra = f"A safra de {safra} registrou um **Ano Mais Frio e Chuvoso** em {regiao}. Isso exigiu uma seleção rigorosa de cachos na esteira para evitar podridão. O perfil do ano entrega maior acidez e vinhos mais verticais."

    col3, col4 = st.columns(2)
    with col3:
        st.warning(f"🍇 **Momento da Colheita na Videira:**\n\n{decisao_colheita}")
        st.warning(f"🪵 **Manejo e Estágio na Adega:**\n\n{manejo_adega}")
    with col4:
        st.error(f"📉 **Comportamento da Acidez no Copo:**\n\n{dados_regiao['acidez']}")
        st.error(f"🌤️ **Impacto Climático do Ano ({safra}):**\n\n{efeito_safra}")

    st.write("")
    
    # --- BLOCO 3: O PERFIL SENSORIAL PROVÁVEL NO SEU COPO ---
    st.markdown("### 👅 Camada 3: Perfil Sensorial e Análise Organoléptica Provável")
    st.success(f"🍷 **Aromas e Sabores no Seu Copo:**\n\n{dados_regiao['perfil']}")

else:
    st.warning("👈 Insira os dados do rótulo na barra lateral esquerda e clique no botão 'Debulhar Perfil Técnico' para ver os resultados.")
