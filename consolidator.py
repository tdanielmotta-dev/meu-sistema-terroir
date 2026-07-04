FIELDS = [
    "producer", "wine_name", "vintage", "grape", "country", "region", "subregion",
    "denomination", "classification", "wine_type", "alcohol", "aromas", "palate",
    "acidity", "body", "soil", "climate", "terroir", "aging", "pairing", "notes"
]


def is_filled(v):
    return v is not None and str(v).strip() != ""


def merge_value(final_data, sources_map, field, value, source_name):
    if not is_filled(value):
        return

    if not is_filled(final_data.get(field)):
        final_data[field] = value
        sources_map.setdefault(field, []).append(source_name)
        return

    # se já existe, mas o novo texto é maior / mais rico, substitui
    old = str(final_data.get(field, "")).strip()
    new = str(value).strip()
    if len(new) > len(old):
        final_data[field] = new
        sources_map.setdefault(field, []).append(source_name)


def consolidate_report(query, parsed_query, local_wine, local_denom, kb_matches, online_sources, parsed_sources):
    final_data = {f: "" for f in FIELDS}
    source_map = {"query": ["USER_QUERY"]}

    # query parser
    if parsed_query.get("vintage"):
        merge_value(final_data, source_map, "vintage", parsed_query["vintage"], "QUERY_PARSER")
    if parsed_query.get("grape"):
        merge_value(final_data, source_map, "grape", parsed_query["grape"], "QUERY_PARSER")
    if parsed_query.get("country"):
        merge_value(final_data, source_map, "country", parsed_query["country"], "QUERY_PARSER")
    if parsed_query.get("region"):
        merge_value(final_data, source_map, "region", parsed_query["region"], "QUERY_PARSER")
    if parsed_query.get("denomination"):
        merge_value(final_data, source_map, "denomination", parsed_query["denomination"], "QUERY_PARSER")

    # local wine
    if local_wine:
        for f in FIELDS:
            merge_value(final_data, source_map, f, local_wine.get(f, ""), "LOCAL_DB_WINE")

    # local denomination
    if local_denom:
        merge_value(final_data, source_map, "country", local_denom.get("country", ""), "LOCAL_DB_DENOM")
        merge_value(final_data, source_map, "region", local_denom.get("region", ""), "LOCAL_DB_DENOM")
        merge_value(final_data, source_map, "denomination", local_denom.get("denomination", ""), "LOCAL_DB_DENOM")
        merge_value(final_data, source_map, "classification", local_denom.get("classification", ""), "LOCAL_DB_DENOM")
        merge_value(final_data, source_map, "grape", local_denom.get("allowed_grapes", ""), "LOCAL_DB_DENOM")
        merge_value(final_data, source_map, "alcohol", local_denom.get("min_alcohol", ""), "LOCAL_DB_DENOM")
        merge_value(final_data, source_map, "aging", local_denom.get("aging_rules", ""), "LOCAL_DB_DENOM")
        merge_value(final_data, source_map, "notes", local_denom.get("notes", ""), "LOCAL_DB_DENOM")

    # knowledge base
    for idx, kb in enumerate(kb_matches, start=1):
        source_name = f"KNOWLEDGE_BASE_{idx}"
        for f in FIELDS:
            merge_value(final_data, source_map, f, kb.get(f, ""), source_name)

    # online parsed
    for idx, parsed in enumerate(parsed_sources, start=1):
        source_name = f"WEB_SOURCE_{idx}"
        for f in FIELDS:
            merge_value(final_data, source_map, f, parsed.get(f, ""), source_name)

    # fallback: nome consultado
    if not final_data.get("wine_name"):
        final_data["wine_name"] = query

    filled = sum(1 for f in FIELDS if is_filled(final_data.get(f)))
    total_sources = sum(len(v) for v in source_map.values())

    return {
        "query": query,
        "final_data": final_data,
        "source_map": source_map,
        "filled_fields": filled,
        "total_fields": len(FIELDS),
        "total_source_attributions": total_sources,
        "local_wine": local_wine,
        "local_denomination": local_denom,
        "knowledge_matches": kb_matches,
        "online_sources": online_sources,
        "parsed_online_sources": parsed_sources,
        "parsed_query": parsed_query
            }
