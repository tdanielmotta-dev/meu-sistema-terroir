from parser_engine import parse_wine_query
from local_search import search_local_wine, search_local_denomination
from knowledge_base import search_knowledge_base
from web_fetcher import (
    search_wine_online,
    search_denomination_online,
    parse_online_source
)
from database import init_db, seed_if_empty


FIELDS = [
    "producer", "wine_name", "vintage", "grape", "country", "region", "subregion",
    "denomination", "classification", "wine_type", "alcohol", "aromas", "palate",
    "acidity", "body", "soil", "climate", "terroir", "aging", "pairing", "notes"
]


def normalize_value(v):
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip()
        return v if v else None
    return v


def set_if_empty(record, field_sources, field, value, source):
    value = normalize_value(value)
    if value is None:
        return
    if normalize_value(record.get(field)) in [None, ""]:
        record[field] = value
        field_sources.setdefault(field, []).append(source)


def append_source_if_value(record, field_sources, field, value, source):
    value = normalize_value(value)
    if value is None:
        return
    current = normalize_value(record.get(field))
    if current == value:
        if source not in field_sources.setdefault(field, []):
            field_sources[field].append(source)


def build_wine_report(query: str):
    init_db()
    seed_if_empty()

    parsed = parse_wine_query(query)
    wine = search_local_wine(query)
    denomination = search_local_denomination(query)
    knowledge_hits = search_knowledge_base(query)

    web_wine = search_wine_online(query)
    web_denom = search_denomination_online(query)

    web_results = web_wine + web_denom

    extracted_web = []
    for item in web_results:
        parsed_data = parse_online_source(item)
        extracted_web.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "parsed_data": parsed_data
        })

    final_record = {
        "query_name": query
    }
    field_sources = {"query_name": ["USER_QUERY"]}

    # 1) parser da query
    for f in ["vintage", "grape", "country", "region", "subregion", "denomination"]:
        if parsed.get(f):
            final_record[f] = parsed.get(f)
            field_sources.setdefault(f, []).append("QUERY_PARSER")

    # 2) banco local - vinho
    if wine:
        mapping = {
            "producer": "producer",
            "wine_name": "wine_name",
            "vintage": "vintage",
            "grape": "grape",
            "country": "country",
            "region": "region",
            "subregion": "subregion",
            "denomination": "denomination",
            "classification": "classification",
            "wine_type": "wine_type",
            "alcohol": "alcohol",
            "aromas": "aromas",
            "palate": "palate",
            "acidity": "acidity",
            "body": "body",
            "soil": "soil",
            "climate": "climate",
            "terroir": "terroir",
            "aging": "aging",
            "pairing": "pairing",
            "notes": "notes"
        }
        for dest, src in mapping.items():
            set_if_empty(final_record, field_sources, dest, wine.get(src), "LOCAL_DB_WINE")

    # 3) banco local - denominação
    if denomination:
        denom_map = {
            "country": "country",
            "region": "region",
            "subregion": "subregion",
            "denomination": "denomination",
            "classification": "classification",
            "soil": "soil",
            "climate": "climate",
            "terroir": "terroir",
            "notes": "notes"
        }
        for dest, src in denom_map.items():
            set_if_empty(final_record, field_sources, dest, denomination.get(src), "LOCAL_DB_DENOM")

    # 4) knowledge base
    for idx, kb in enumerate(knowledge_hits, start=1):
        source = f"KNOWLEDGE_BASE_{idx}"
        for f in FIELDS:
            set_if_empty(final_record, field_sources, f, kb.get(f), source)

    # 5) web extraída
    for item in extracted_web:
        source = f"WEB:{item.get('title', 'fonte')}"
        pdata = item.get("parsed_data", {})

        for f in ["vintage", "grape", "country", "region", "denomination", "aromas", "palate", "acidity", "soil", "climate", "terroir", "aging", "pairing", "alcohol"]:
            set_if_empty(final_record, field_sources, f, pdata.get(f), source)

    # 6) pós-ajuste: se local já tinha valor e web confirma, adiciona a fonte também
    if wine:
        for f in ["producer", "wine_name", "country", "region", "grape", "vintage"]:
            append_source_if_value(final_record, field_sources, f, wine.get(f), "LOCAL_DB_WINE")

    # preencher vazios restantes
    for f in FIELDS:
        final_record.setdefault(f, None)

    filled_count = 0
    for k, v in final_record.items():
        if k == "query_name":
            continue
        if normalize_value(v) not in [None, ""]:
            filled_count += 1

    total_sources = sum(len(v) for v in field_sources.values())

    summary = []
    summary.append(f"Knowledge base encontrou {len(knowledge_hits)} correspondência(s).")
    summary.append(f"Campos preenchidos na ficha: {filled_count}/{len(FIELDS)}.")
    summary.append(f"Total de atribuições de fonte: {total_sources}.")

    return {
        "query": query,
        "parsed_query": parsed,
        "wine_found": wine,
        "denomination_found": denomination,
        "knowledge_hits": knowledge_hits,
        "web_results": web_results,
        "web_extracted": extracted_web,
        "final_record": final_record,
        "field_sources": field_sources,
        "summary": summary
    }
