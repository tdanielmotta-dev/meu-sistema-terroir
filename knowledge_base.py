import json
from pathlib import Path
from difflib import SequenceMatcher

KB_PATH = Path("knowledge_base.json")

DEFAULT_KB = [
    {
        "aliases": ["dom perignon", "dom pérignon"],
        "producer": "Moët & Chandon",
        "wine_name": "Dom Pérignon",
        "vintage": "",
        "grape": "Chardonnay, Pinot Noir",
        "country": "França",
        "region": "Champagne",
        "subregion": "",
        "denomination": "Champagne AOC",
        "classification": "Prestige Cuvée",
        "wine_type": "Espumante",
        "alcohol": "12.5%",
        "aromas": "cítricos, brioche, flores, frutas brancas, tostado",
        "palate": "fino, cremoso, mineral, complexo",
        "acidity": "alta",
        "body": "médio a encorpado",
        "soil": "calcário, giz",
        "climate": "frio continental",
        "terroir": "Champagne de solos calcários e clima marginal",
        "aging": "longo amadurecimento sobre borras",
        "pairing": "ostras, caviar, frutos do mar, aves nobres",
        "notes": "KB seed"
    },
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
        "notes": "KB seed"
    },
    {
        "aliases": ["barolo", "barolo docg"],
        "producer": "",
        "wine_name": "Barolo",
        "vintage": "",
        "grape": "Nebbiolo",
        "country": "Itália",
        "region": "Piemonte",
        "subregion": "Barolo",
        "denomination": "Barolo DOCG",
        "classification": "DOCG",
        "wine_type": "Tinto",
        "alcohol": "14%",
        "aromas": "rosa, alcatrão, cereja, especiarias",
        "palate": "estruturado, taninos firmes, final longo",
        "acidity": "alta",
        "body": "encorpado",
        "soil": "margas calcárias",
        "climate": "continental",
        "terroir": "Langhe",
        "aging": "envelhecimento obrigatório conforme DOCG",
        "pairing": "carnes assadas, caça, trufas",
        "notes": "KB seed"
    }
]

def load_knowledge_base():
    if not KB_PATH.exists():
        save_knowledge_base(DEFAULT_KB)
        return DEFAULT_KB.copy()

    try:
        with open(KB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass

    save_knowledge_base(DEFAULT_KB)
    return DEFAULT_KB.copy()

def save_knowledge_base(data):
    with open(KB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()

def search_knowledge_base(query: str, threshold: float = 0.45, top_n: int = 5):
    kb = load_knowledge_base()
    q = (query or "").strip()
    if not q:
        return []

    scored = []

    for item in kb:
        aliases = item.get("aliases", []) or []
        haystack_parts = aliases + [
            item.get("producer", ""),
            item.get("wine_name", ""),
            item.get("denomination", ""),
            item.get("region", ""),
            item.get("country", ""),
            item.get("grape", ""),
        ]
        haystack = " | ".join([str(x) for x in haystack_parts if x])

        score = similarity(q, haystack)

        for alias in aliases:
            if q.lower() == alias.lower():
                score += 0.7
            elif q.lower() in alias.lower():
                score += 0.45

        if q.lower() in haystack.lower():
            score += 0.2

        if score >= threshold:
            clone = dict(item)
            clone["_score"] = round(score, 4)
            scored.append(clone)

    scored.sort(key=lambda x: x["_score"], reverse=True)
    return scored[:top_n]

def upsert_knowledge_entry(query: str, record: dict):
    """
    Salva/atualiza automaticamente um vinho descoberto.
    """
    if not isinstance(record, dict):
        return False

    producer = (record.get("producer") or "").strip()
    wine_name = (record.get("wine_name") or "").strip()
    denomination = (record.get("denomination") or "").strip()

    if not producer and not wine_name and not denomination:
        return False

    kb = load_knowledge_base()

    aliases = set()
    if query:
        aliases.add(query.strip().lower())
    if producer and wine_name:
        aliases.add(f"{producer} {wine_name}".strip().lower())
    if wine_name:
        aliases.add(wine_name.strip().lower())
    if denomination:
        aliases.add(denomination.strip().lower())

    # procura entrada já existente
    best_idx = None
    best_score = 0.0

    for idx, item in enumerate(kb):
        item_aliases = item.get("aliases", []) or []
        hay = " | ".join(item_aliases + [
            item.get("producer", ""),
            item.get("wine_name", ""),
            item.get("denomination", "")
        ])

        score = similarity(" ".join(sorted(aliases)), hay)
        if score > best_score:
            best_score = score
            best_idx = idx

    if best_idx is not None and best_score >= 0.65:
        existing = kb[best_idx]
        existing_aliases = set(existing.get("aliases", []) or [])
        existing_aliases.update(aliases)
        existing["aliases"] = sorted(existing_aliases)

        for k, v in record.items():
            if k == "_sources":
                continue
            if v and not existing.get(k):
                existing[k] = v

        kb[best_idx] = existing
        save_knowledge_base(kb)
        return True

    new_entry = {
        "aliases": sorted(aliases),
        "producer": record.get("producer", ""),
        "wine_name": record.get("wine_name", ""),
        "vintage": record.get("vintage", ""),
        "grape": record.get("grape", ""),
        "country": record.get("country", ""),
        "region": record.get("region", ""),
        "subregion": record.get("subregion", ""),
        "denomination": record.get("denomination", ""),
        "classification": record.get("classification", ""),
        "wine_type": record.get("wine_type", ""),
        "alcohol": record.get("alcohol", ""),
        "aromas": record.get("aromas", ""),
        "palate": record.get("palate", ""),
        "acidity": record.get("acidity", ""),
        "body": record.get("body", ""),
        "soil": record.get("soil", ""),
        "climate": record.get("climate", ""),
        "terroir": record.get("terroir", ""),
        "aging": record.get("aging", ""),
        "pairing": record.get("pairing", ""),
        "notes": record.get("notes", ""),
    }
    kb.append(new_entry)
    save_knowledge_base(kb)
    return True
