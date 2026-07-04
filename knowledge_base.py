from difflib import SequenceMatcher

KNOWLEDGE_BASE = [
    {
        "aliases": ["gato negro malbec", "gato negro malbec 2019"],
        "producer": "Gato Negro",
        "wine_name": "Malbec",
        "vintage": "2019",
        "grape": "Malbec",
        "country": "Chile",
        "region": "Central Valley",
        "subregion": "",
        "denomination": "",
        "classification": "",
        "wine_type": "Tinto",
        "alcohol": "13%",
        "aromas": "frutas vermelhas maduras, ameixa, notas frutadas",
        "palate": "macio, frutado, taninos suaves",
        "acidity": "média",
        "body": "médio",
        "soil": "",
        "climate": "mediterrâneo",
        "terroir": "",
        "aging": "",
        "pairing": "massas, carnes leves, pizzas",
        "notes": "Entrada de conhecimento-base"
    },
    {
        "aliases": ["barolo classico", "barolo docg", "barolo 2018"],
        "producer": "",
        "wine_name": "Barolo",
        "vintage": "2018",
        "grape": "Nebbiolo",
        "country": "Itália",
        "region": "Piemonte",
        "subregion": "Barolo",
        "denomination": "Barolo DOCG",
        "classification": "DOCG",
        "wine_type": "Tinto",
        "alcohol": "",
        "aromas": "rosa, cereja, alcaçuz, alcatrão",
        "palate": "estruturado, tânico, longo",
        "acidity": "alta",
        "body": "encorpado",
        "soil": "marga calcária",
        "climate": "continental",
        "terroir": "encostas calcárias",
        "aging": "maturação longa conforme regra DOCG",
        "pairing": "carnes, caça, risoto",
        "notes": "Entrada de conhecimento-base"
    }
]


def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()


def search_knowledge_base(query: str):
    query = (query or "").strip()
    if not query:
        return []

    results = []
    q_lower = query.lower()

    for item in KNOWLEDGE_BASE:
        aliases = item.get("aliases", [])
        best = 0.0

        for alias in aliases:
            score = _sim(q_lower, alias.lower())
            if alias.lower() in q_lower or q_lower in alias.lower():
                score += 0.35
            if score > best:
                best = score

        if best >= 0.35:
            row = dict(item)
            row["_score"] = round(best, 4)
            results.append(row)

    results.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return results
