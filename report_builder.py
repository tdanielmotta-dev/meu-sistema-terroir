from parser_engine import parse_wine_query
from local_search import search_local_wine, search_local_denomination, search_knowledge_base
from web_search import search_wine_sources
from source_parsers import parse_source


ALL_FIELDS = [
    "producer", "wine_name", "vintage", "grape", "country", "region", "subregion",
    "denomination", "classification", "wine_type", "alcohol", "aromas", "palate",
    "acidity", "body", "soil", "climate", "terroir", "aging", "pairing", "notes"
]


def empty_profile(query: str):
    return {
        "query": query,
        "producer": "",
        "wine_name": "",
        "vintage": "",
        "grape": "",
        "country": "",
        "region": "",
        "subregion": "",
        "denomination": "",
        "classification": "",
        "wine_type": "",
        "alcohol": "",
        "aromas": "",
        "palate": "",
        "acidity": "",
        "body": "",
        "soil": "",
        "climate": "",
        "terroir": "",
        "aging": "",
        "pairing": "",
        "notes": ""
    }


def apply_value(profile: dict, field_sources: dict, field: str, value, source_label: str):
    if value is None:
        return
    value = str(value).strip()
    if not value:
        return

    current = str(profile.get(field, "")).strip()
    if not current:
        profile[field] = value
        field_sources.setdefault(field, []).append(source_label)
        return

    # se o valor novo é maior e mais informativo, substitui
    if len(value) > len(current) + 8:
        profile[field] = value
        field_sources.setdefault(field, []).append(source_label)


def merge_from_record(profile: dict, field_sources: dict, record: dict, source_label: str):
    if not record:
        return

    mapping = {
        "producer": record.get("producer"),
        "wine_name": record.get("wine_name"),
        "vintage": record.get("vintage"),
        "grape": record.get("grape"),
        "country": record.get("country"),
        "region": record.get("region"),
        "subregion": record.get("subregion"),
        "denomination": record.get("denomination"),
        "classification": record.get("classification"),
        "wine_type": record.get("wine_type"),
        "alcohol": record.get("alcohol"),
        "aromas": record.get("aromas"),
        "palate": record.get("palate"),
        "acidity": record.get("acidity"),
        "body": record.get("body"),
        "soil": record.get("soil"),
        "climate": record.get("climate"),
        "terroir": record.get("terroir"),
        "aging": record.get("aging"),
        "pairing": record.get("pairing"),
        "notes": record.get("notes"),
    }

    for field, value in mapping.items():
        apply_value(profile, field_sources, field, value, source_label)


def merge_from_denomination(profile: dict, field_sources: dict, denom: dict, source_label: str):
    if not denom:
        return

    mapping = {
        "country": denom.get("country"),
        "region": denom.get("region"),
        "subregion": denom.get("subregion"),
        "denomination": denom.get("denomination"),
        "classification": denom.get("classification"),
        "soil": denom.get("soil"),
        "climate": denom.get("climate"),
        "terroir": denom.get("terroir"),
        "notes": denom.get("notes"),
    }

    for field, value in mapping.items():
        apply_value(profile, field_sources, field, value, source_label)


def merge_from_web(profile: dict, field_sources: dict, parsed_source: dict, query: str):
    if not parsed_source:
        return

    extracted = parsed_source.get("extracted", {})
    source_title = parsed_source.get("source_title", "") or parsed_source.get("source_url", "web")

    # heurística para nome do vinho/produtor a partir do título
    if source_title and not profile.get("wine_name"):
        apply_value(profile, field_sources, "wine_name", query, f"WEB:{source_title}")

    for field in [
        "vintage", "grape", "country", "region", "denomination",
        "alcohol", "aromas", "palate", "acidity", "soil",
        "climate", "terroir", "aging", "pairing"
    ]:
        apply_value(profile, field_sources, field, extracted.get(field), f"WEB:{source_title}")


def fill_from_query_parser(profile: dict, field_sources: dict, parser: dict):
    apply_value(profile, field_sources, "vintage", parser.get("vintage"), "QUERY_PARSER")
    apply_value(profile, field_sources, "grape", parser.get("grape"), "QUERY_PARSER")
    apply_value(profile, field_sources, "country", parser.get("country"), "QUERY_PARSER")
    apply_value(profile, field_sources, "denomination", parser.get("denomination"), "QUERY_PARSER")


def build_wine_report(query: str):
    parser = parse_wine_query(query)
    profile = empty_profile(query)
    field_sources = {}

    # 1) parser da query
    fill_from_query_parser(profile, field_sources, parser)

    # 2) banco local
    local_wine = search_local_wine(query)
    local_denom = search_local_denomination(query)

    if local_wine:
        merge_from_record(profile, field_sources, local_wine, "LOCAL_DB_WINE")
    if local_denom:
        merge_from_denomination(profile, field_sources, local_denom, "LOCAL_DB_DENOM")

    # 3) knowledge base
    kb_matches = search_knowledge_base(query)
    for i, kb in enumerate(kb_matches[:3], start=1):
        merge_from_record(profile, field_sources, kb, f"KNOWLEDGE_BASE_{i}")

    # 4) web search
    sources = search_wine_sources(query, parser)
    parsed_sources = []

    for src in sources[:8]:
        parsed = parse_source(
            url=src.get("url", ""),
            title=src.get("title", ""),
            snippet=src.get("snippet", "")
        )
        parsed_sources.append(parsed)
        merge_from_web(profile, field_sources, parsed, query)

    # 5) heurística final: se não tem wine_name, usa query
    if not profile["wine_name"]:
        profile["wine_name"] = query

    # 6) resumo
    filled_count = sum(1 for f in ALL_FIELDS if str(profile.get(f, "")).strip())
    total_source_attributions = sum(len(v) for v in field_sources.values())

    summary = []
    summary.append(f"Knowledge base encontrou {len(kb_matches)} correspondência(s).")
    summary.append(f"Campos preenchidos na ficha: {filled_count}/{len(ALL_FIELDS)}.")
    summary.append(f"Total de atribuições de fonte: {total_source_attributions}.")

    return {
        "query": query,
        "parser": parser,
        "wine_found": local_wine,
        "denomination_found": local_denom,
        "knowledge_matches": kb_matches,
        "online_sources": sources,
        "parsed_sources": parsed_sources,
        "field_sources": field_sources,
        "profile": profile,
        "summary": summary
    }
