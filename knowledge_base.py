KNOWLEDGE_BASE = {
    "gato negro merlot": {
        "producer": "Viña San Pedro",
        "country": "Chile",
        "region": "Valle Central",
        "denomination": "Indicação geográfica / origem chilena",
        "classification": "IG",
        "wine_type": "Tinto",
        "grape": "Merlot",
        "alcohol": "13.0% vol (pode variar por safra/lote/mercado)",
        "aroma": "Frutas vermelhas maduras, ameixa, leve toque herbáceo, notas simples e frutadas",
        "flavor": "Frutado, macio, corpo médio, taninos suaves, final simples",
        "body": "Médio",
        "acidity": "Média",
        "tannin": "Baixos a médios / macios",
        "oak": "Geralmente discreta ou ausente no perfil base",
        "soil": "Composição variável; em macrovisão do Valle Central aparecem solos aluviais e coluviais",
        "climate": "Mediterrâneo, com boa insolação e forte importância da amplitude térmica em algumas áreas",
        "aging_rules": "Não há regra de envelhecimento equivalente a DOCG/AOC para o rótulo comercial em si",
        "notes": "Perfil de mercado focado em fruta, maciez e facilidade de consumo"
    },
    "bordeaux": {
        "country": "França",
        "classification": "AOC / AOP",
        "style": "Tintos de corte bordalês, brancos secos e doces botrytizados conforme sub-região",
        "grapes": "Merlot, Cabernet Sauvignon, Cabernet Franc, Sémillon, Sauvignon Blanc, Muscadelle",
        "soil": "Cascalho, argila, calcário, areia",
        "climate": "Oceânico / marítimo",
        "notes": "Macro-região histórica com enorme diversidade de subzonas"
    },
    "barolo docg": {
        "country": "Itália",
        "classification": "DOCG",
        "style": "Nebbiolo de alto potencial de guarda",
        "grapes": "Nebbiolo",
        "soil": "Margas calcárias, argila e calcário em várias comunas",
        "climate": "Continental com forte influência de colinas",
        "notes": "Uma das denominações mais emblemáticas do Piemonte"
    },
    "rioja doca": {
        "country": "Espanha",
        "classification": "DOCa",
        "style": "Tintos tradicionais de Tempranillo e blends, além de rosados e brancos",
        "grapes": "Tempranillo, Garnacha, Graciano, Mazuelo e outras autorizadas",
        "soil": "Muito variável conforme Rioja Alta, Alavesa e Oriental",
        "climate": "Mistura de influências atlântica, continental e mediterrânea",
        "notes": "Região clássica com forte tradição de barrica"
    }
}


def get_knowledge_matches(query: str, parsed_query: dict):
    matches = []

    q = (query or "").lower().strip()
    if q in KNOWLEDGE_BASE:
        matches.append({"key": q, "data": KNOWLEDGE_BASE[q]})

    normalized = (parsed_query or {}).get("normalized_query", "").lower().strip()
    for key, data in KNOWLEDGE_BASE.items():
        if key in normalized or normalized in key:
            if {"key": key, "data": data} not in matches:
                matches.append({"key": key, "data": data})

    region = (parsed_query or {}).get("region", "")
    if region:
        region = region.lower().strip()
        if region in KNOWLEDGE_BASE:
            item = {"key": region, "data": KNOWLEDGE_BASE[region]}
            if item not in matches:
                matches.append(item)

    denomination = (parsed_query or {}).get("denomination", "")
    if denomination:
        denomination = denomination.lower().strip()
        if denomination in KNOWLEDGE_BASE:
            item = {"key": denomination, "data": KNOWLEDGE_BASE[denomination]}
            if item not in matches:
                matches.append(item)

    return matches
