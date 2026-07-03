def get_knowledge_base():
    return {
        "barolo": {
            "country": "Itália",
            "region": "Piemonte",
            "denomination": "Barolo DOCG",
            "classification": "DOCG",
            "grapes": ["Nebbiolo"],
            "min_alcohol": 13.0,
            "aging_rules": "Barolo DOCG exige maturação mínima; Riserva exige período maior.",
            "terroir": "Colinas calcárias e argilo-calcárias, altitudes moderadas, forte influência continental.",
            "climate": "Continental, com invernos frios e verões quentes, boa amplitude térmica.",
            "style": "Tinto de alta estrutura, tanino elevado, acidez presente, guarda longa.",
            "aromas": ["rosa", "alcatrão", "cereja ácida", "ervas secas", "especiarias", "trufa com evolução"],
            "notes": "Denominação histórica do Piemonte; foco absoluto em Nebbiolo."
        },
        "barbaresco": {
            "country": "Itália",
            "region": "Piemonte",
            "denomination": "Barbaresco DOCG",
            "classification": "DOCG",
            "grapes": ["Nebbiolo"],
            "min_alcohol": 12.5,
            "aging_rules": "Maturação obrigatória conforme regulamento da DOCG.",
            "terroir": "Colinas de solo calcário-argiloso, geralmente com expressão um pouco mais elegante que Barolo.",
            "climate": "Continental.",
            "style": "Tinto de alta classe aromática, taninos firmes porém muitas vezes mais polidos que Barolo.",
            "aromas": ["violeta", "rosa", "frutas vermelhas ácidas", "chá", "especiarias", "terra"],
            "notes": "Grande DOCG piemontesa baseada em Nebbiolo."
        },
        "bordeaux": {
            "country": "França",
            "region": "Bordeaux",
            "denomination": "Bordeaux AOC",
            "classification": "AOC",
            "grapes": [
                "Merlot", "Cabernet Sauvignon", "Cabernet Franc",
                "Sauvignon Blanc", "Semillon", "Muscadelle"
            ],
            "min_alcohol": 10.5,
            "aging_rules": "Variável conforme a AOC e sub-região.",
            "terroir": "Cascalho, argilo-calcário, areia e aluvião; enorme diversidade de terroirs.",
            "climate": "Marítimo temperado com influência atlântica.",
            "style": "Tintos de lote bordalês, brancos secos e doces botrytizados conforme subzona.",
            "aromas": ["cassis", "ameixa", "cedro", "tabaco", "erva seca", "baunilha em vinhos com barrica"],
            "notes": "Macro universo de sub-regiões como Médoc, Graves, Saint-Émilion, Pomerol, Sauternes e Barsac."
        },
        "sauternes": {
            "country": "França",
            "region": "Bordeaux",
            "denomination": "Sauternes AOC",
            "classification": "AOC",
            "grapes": ["Semillon", "Sauvignon Blanc", "Muscadelle"],
            "min_alcohol": 12.0,
            "aging_rules": "Regras específicas para vinhos doces botrytizados.",
            "terroir": "Cascalho, argila, calcário e influência de neblinas locais favoráveis à Botrytis cinerea.",
            "climate": "Marítimo com condições específicas de umidade e neblina.",
            "style": "Branco doce botrytizado, untuoso, concentrado e de longa guarda.",
            "aromas": ["damasco seco", "mel", "marmelada", "açafrão", "laranja cristalizada", "cera"],
            "notes": "Ícone mundial de vinhos doces de podridão nobre."
        },
        "rioja": {
            "country": "Espanha",
            "region": "Rioja",
            "denomination": "DOCa Rioja",
            "classification": "DOCa",
            "grapes": ["Tempranillo", "Garnacha", "Graciano", "Mazuelo", "Viura"],
            "min_alcohol": None,
            "aging_rules": "Sistema clássico com Crianza, Reserva e Gran Reserva.",
            "terroir": "Mistura de solos argilo-calcários, ferrosos e aluviais.",
            "climate": "Transição atlântica-continental-mediterrânea conforme subzona.",
            "style": "Tintos de Tempranillo com ou sem madeira, perfil que pode variar do clássico ao moderno.",
            "aromas": ["cereja", "ameixa", "baunilha", "coco", "tabaco", "especiarias"],
            "notes": "Rioja Alta, Rioja Alavesa e Rioja Oriental compõem o mosaico regional."
        },
        "chianti classico": {
            "country": "Itália",
            "region": "Toscana",
            "denomination": "Chianti Classico DOCG",
            "classification": "DOCG",
            "grapes": ["Sangiovese"],
            "min_alcohol": None,
            "aging_rules": "Categorias Annata, Riserva e Gran Selezione conforme disciplinares.",
            "terroir": "Colinas toscanas com forte presença de galestro, alberese e argila.",
            "climate": "Mediterrâneo com influência continental local.",
            "style": "Tinto de acidez alta, cereja ácida, ervas, taninos médios a firmes.",
            "aromas": ["cereja", "violeta", "ervas secas", "terra", "chá", "especiarias"],
            "notes": "Zona histórica entre Florença e Siena."
        }
    }


def infer_from_query(query: str):
    q = (query or "").lower()
    kb = get_knowledge_base()

    matches = []
    for key, data in kb.items():
        if key in q:
            matches.append({"key": key, **data})

    return matches
