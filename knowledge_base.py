"""
Base local complementar para enriquecer a resposta com informação técnica fixa
quando a consulta bater com certas regiões/denominações.
"""

KNOWLEDGE_BASE = {
    "bordeaux": {
        "country": "França",
        "classification": "AOC / AOP",
        "style": "Tintos de corte bordalês, brancos secos e doces botrytizados conforme sub-região",
        "grapes": [
            "Merlot", "Cabernet Sauvignon", "Cabernet Franc",
            "Sémillon", "Sauvignon Blanc", "Muscadelle"
        ],
        "notes": (
            "Bordeaux é uma macro-região histórica do sudoeste da França, fortemente "
            "marcada por blends, influência atlântica e grande diversidade de subzonas."
        )
    },
    "barolo docg": {
        "country": "Itália",
        "classification": "DOCG",
        "style": "Tinto estruturado de Nebbiolo, alto potencial de guarda",
        "grapes": ["Nebbiolo"],
        "notes": (
            "Barolo é uma das denominações mais emblemáticas do Piemonte, "
            "com regras rígidas e longa tradição de envelhecimento."
        )
    },
    "rioja doca": {
        "country": "Espanha",
        "classification": "DOCa",
        "style": "Tintos de Tempranillo e blends tradicionais, além de rosados e brancos",
        "grapes": ["Tempranillo", "Garnacha", "Graciano", "Mazuelo"],
        "notes": (
            "Rioja é uma das regiões mais tradicionais da Espanha, com forte cultura "
            "de envelhecimento em barrica e segmentação entre Rioja Alta, Alavesa e Oriental."
        )
    }
}


def get_knowledge_matches(parsed_query: dict):
    if not isinstance(parsed_query, dict):
        return []

    candidates = []

    denomination = (parsed_query.get("denomination") or "").lower().strip()
    region = (parsed_query.get("region") or "").lower().strip()

    if denomination and denomination in KNOWLEDGE_BASE:
        candidates.append({
            "match_type": "denomination",
            "key": denomination,
            "data": KNOWLEDGE_BASE[denomination]
        })

    if region and region in KNOWLEDGE_BASE:
        candidates.append({
            "match_type": "region",
            "key": region,
            "data": KNOWLEDGE_BASE[region]
        })

    return candidates
