from difflib import SequenceMatcher

KNOWLEDGE_BASE = {
    "gato_negro_merlot": {
        "aliases": [
            "Gato Negro Merlot",
            "Gato Negro Merlot 2020",
            "Gato Negro",
        ],
        "producer": "Viña San Pedro",
        "country": "Chile",
        "region": "Valle Central",
        "denomination": None,
        "classification": None,
        "wine_type": "Tinto",
        "grape": "Merlot",
        "alcohol": None,
        "body": "Médio",
        "acidity": "Média",
        "tannin": "Macios",
        "oak": None,
        "aroma": "Frutas vermelhas maduras, ameixa, toques herbais suaves",
        "flavor": "Frutado, macio, acessível, taninos suaves",
        "soil": None,
        "climate": "Mediterrâneo / quente a moderado conforme zona do Valle Central",
        "aging_rules": None,
        "grapes": "Merlot",
        "notes": "Entrada base de referência para Gato Negro Merlot."
    },
    "casillero_del_diablo_cabernet": {
        "aliases": [
            "Casillero del Diablo Cabernet Sauvignon",
            "Casillero del Diablo Cabernet",
        ],
        "producer": "Concha y Toro",
        "country": "Chile",
        "region": "Valle Central",
        "denomination": None,
        "classification": None,
        "wine_type": "Tinto",
        "grape": "Cabernet Sauvignon",
        "alcohol": None,
        "body": "Médio a encorpado",
        "acidity": "Média",
        "tannin": "Médios",
        "oak": "Pode haver uso de carvalho conforme edição/linha",
        "aroma": "Cassis, cereja preta, especiarias, leve baunilha",
        "flavor": "Fruta negra, especiarias, estrutura média",
        "soil": None,
        "climate": None,
        "aging_rules": None,
        "grapes": "Cabernet Sauvignon",
        "notes": "Entrada base de referência para Casillero del Diablo Cabernet Sauvignon."
    },
    "barolo_docg": {
        "aliases": [
            "Barolo", "Barolo DOCG"
        ],
        "producer": None,
        "country": "Itália",
        "region": "Piemonte",
        "denomination": "Barolo DOCG",
        "classification": "DOCG",
        "wine_type": "Tinto",
        "grape": "Nebbiolo",
        "alcohol": "mínimo legal depende do disciplinare vigente",
        "body": "Encorpado",
        "acidity": "Alta",
        "tannin": "Firmes",
        "oak": "frequente, mas varia por produtor e estilo",
        "aroma": "Rosa, alcatrão, cereja, ervas, especiarias",
        "flavor": "Estruturado, longevo, taninos marcantes",
        "soil": "Margas calcárias e argilosas, com variações locais",
        "climate": "Continental, influência de altitude e neblina",
        "aging_rules": "Barolo DOCG possui exigências legais de envelhecimento previstas no disciplinare",
        "grapes": "Nebbiolo",
        "notes": "Base geral da denominação Barolo DOCG."
    },
    "bordeaux_aoc": {
        "aliases": [
            "Bordeaux", "Bordeaux AOC"
        ],
        "producer": None,
        "country": "França",
        "region": "Bordeaux",
        "denomination": "Bordeaux AOC",
        "classification": "AOC",
        "wine_type": None,
        "grape": None,
        "alcohol": None,
        "body": None,
        "acidity": None,
        "tannin": None,
        "oak": None,
        "aroma": None,
        "flavor": None,
        "soil": "Diversos, incluindo cascalho, argilo-calcário e areia, conforme subzona",
        "climate": "Marítimo / atlântico temperado",
        "aging_rules": None,
        "grapes": "Merlot, Cabernet Sauvignon, Cabernet Franc e outras conforme denominação/subzona",
        "notes": "Base geral da região Bordeaux."
    }
}


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()


def get_knowledge_matches(query: str, parsed: dict = None):
    query = (query or "").strip()
    if not query:
        return []

    results = []

    for key, data in KNOWLEDGE_BASE.items():
        aliases = data.get("aliases", [])
        best_score = 0.0

        for alias in aliases:
            score = similarity(query, alias)
            if alias.lower() in query.lower() or query.lower() in alias.lower():
                score += 0.35
            if score > best_score:
                best_score = score

        if best_score >= 0.35:
            results.append({
                "key": key,
                "score": round(best_score, 4),
                "data": data
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
