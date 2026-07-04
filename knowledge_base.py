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
        "aliases": ["barolo classico 2018", "barolo docg 2018"],
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
        "aromas": "rosas, cereja ácida, alcaçuz, alcatrão",
        "palate": "estruturado, tânico, longo",
        "acidity": "alta",
        "body": "encorpado",
        "soil": "margas calcárias",
        "climate": "continental",
        "terroir": "colinas do Piemonte",
        "aging": "envelhecimento prolongado",
        "pairing": "carnes, trufas, risoto",
        "notes": "Entrada de conhecimento-base"
    }
]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def search_knowledge_base(query: str, threshold: float = 0.45):
    query = (query or "").strip()
    if not query:
        return []

    hits = []

    for item in KNOWLEDGE_BASE:
        haystacks = item.get("aliases", []) + [
            f"{item.get('producer', '')} {item.get('wine_name', '')} {item.get('vintage', '')}".strip()
        ]

        best_score = 0.0
        for h in haystacks:
            score = similarity(query, h)
            if query.lower() in h.lower():
                score += 0.35
            if score > best_score:
                best_score = score

        if best_score >= threshold:
            copy_item = dict(item)
            copy_item["_score"] = round(best_score, 4)
            hits.append(copy_item)

    hits.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return hits
