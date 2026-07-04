from local_search import search_local_wine, search_local_denomination
from parser_engine import parse_wine_query
from knowledge_base import search_knowledge_base
from web_fetcher import search_wine_online, search_denomination_online


FIELDS = [
    "producer",
    "wine_name",
    "vintage",
    "grape",
    "country",
    "region",
    "subregion",
    "denomination",
    "classification",
    "wine_type",
    "alcohol",
    "aromas",
    "palate",
    "acidity",
    "body",
    "soil",
    "climate",
    "terroir",
    "aging",
    "pairing",
    "notes",
]


def normalize_empty(v):
    if v is None:
        return ""
    return str(v).strip()


def add_value(card, field, value, source):
    value = normalize_empty(value)
    if not value:
        return

    if not card[field]:
        card[field] = value
        card["_sources"][field].append(source)
        return

    existing = card[field].lower()
    incoming = value.lower()

    if incoming == existing:
        if source not in card["_sources"][field]:
            card["_sources"][field].append(source)
        return

    # se o valor atual é curto/vazio e o novo parece melhor, substitui
    if len(card[field]) < len(value):
        card[field] = value

    if source not in card["_sources"][field]:
        card["_sources"][field].append(source)


def build_empty_card(query: str):
    card = {field: "" for field in FIELDS}
    card["query"] = query
    card["_sources"] = {field: [] for field in FIELDS}
    return card


def apply_parser(card, parser_data):
    mapping = {
        "vintage": "QUERY_PARSER",
        "grape": "QUERY_PARSER",
        "country": "QUERY_PARSER",
        "region": "QUERY_PARSER",
        "subregion": "QUERY_PARSER",
        "denomination": "QUERY_PARSER",
    }
    for field, source in mapping.items():
        add_value(card, field, parser_data.get(field, ""), source)


def apply_local_wine(card, wine):
    if not wine:
        return
    for field in FIELDS:
        add_value(card, field, wine.get(field, ""), "LOCAL_DB_WINE")


def apply_local_denomination(card, denom):
    if not denom:
        return

    mapping = {
        "country": denom.get("country", ""),
        "region": denom.get("region", ""),
        "subregion": denom.get("subregion", ""),
        "denomination": denom.get("denomination", ""),
        "classification": denom.get("classification", ""),
        "soil": denom.get("soil", ""),
        "climate": denom.get("climate", ""),
        "terroir": denom.get("terroir", ""),
        "notes": denom.get("notes", ""),
    }

    for field, value in mapping.items():
        add_value(card, field, value, "LOCAL_DB_DENOMINATION")


def apply_knowledge(card, kb_matches):
    for idx, item in enumerate(kb_matches, start=1):
        src = f"KNOWLEDGE_BASE_{idx}"
        for field in FIELDS:
            add_value(card, field, item.get(field, ""), src)


def apply_online(card, online_sources):
    for src in online_sources:
        title = src.get("title", "WEB")
        parsed = src.get("parsed_data", {})
        source_name = f"WEB:{title}"

        for field in FIELDS:
            add_value(card, field, parsed.get(field, ""), source_name)


def build_summary(card, kb_matches):
    filled = 0
    total_sources = 0

    for field in FIELDS:
        if normalize_empty(card.get(field)):
            filled += 1
        total_sources += len(card["_sources"].get(field, []))

    summary = [
        f"Knowledge base encontrou {len(kb_matches)} correspondência(s).",
        f"Campos preenchidos na ficha: {filled}/{len(FIELDS)}.",
        f"Total de atribuições de fonte: {total_sources}."
    ]
    return summary


def build_wine_report(query: str):
    parser_data = parse_wine_query(query)

    wine = search_local_wine(query)
    denomination = search_local_denomination(query)
    kb_matches = search_knowledge_base(query)

    online_wine = search_wine_online(query)
    online_denom = search_denomination_online(query)

    online_sources = online_wine + online_denom

    card = build_empty_card(query)
    apply_parser(card, parser_data)
    apply_local_wine(card, wine)
    apply_local_denomination(card, denomination)
    apply_knowledge(card, kb_matches)
    apply_online(card, online_sources)

    report = {
        "query": query,
        "parser": parser_data,
        "wine_found": wine,
        "denomination_found": denomination,
        "knowledge_matches": kb_matches,
        "online_sources": online_sources,
        "card": card,
        "summary": build_summary(card, kb_matches)
    }

    return report
