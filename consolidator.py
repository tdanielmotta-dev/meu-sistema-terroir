WINE_FIELDS = [
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

def blank_record():
    return {field: "" for field in WINE_FIELDS}

def merge_record(target: dict, source: dict, source_name: str, source_priority: int, source_map: dict):
    if not source:
        return

    for field in WINE_FIELDS:
        val = source.get(field, "")
        if val is None:
            val = ""
        val = str(val).strip()

        if not val:
            continue

        current = (target.get(field) or "").strip()
        current_priority = source_map.get(field, {}).get("priority", -1)

        if not current or source_priority >= current_priority:
            target[field] = val
            source_map[field] = {
                "source": source_name,
                "priority": source_priority
            }

def consolidate(query: str, parsed_query: dict, local_wine: dict, kb_matches: list, parsed_sources: list):
    result = blank_record()
    source_map = {}

    # guarda query original
    result["notes"] = ""

    # 1) parser da query (baixa prioridade)
    query_record = {}
    if parsed_query.get("vintage"):
        query_record["vintage"] = parsed_query["vintage"]
    if parsed_query.get("grape"):
        query_record["grape"] = parsed_query["grape"]
    if parsed_query.get("country"):
        query_record["country"] = parsed_query["country"]
    if parsed_query.get("region"):
        query_record["region"] = parsed_query["region"]
    if parsed_query.get("denomination"):
        query_record["denomination"] = parsed_query["denomination"]

    merge_record(result, query_record, "QUERY_PARSER", 10, source_map)

    # 2) banco local
    if local_wine:
        merge_record(result, local_wine, "LOCAL_DB_WINE", 40, source_map)

    # 3) knowledge base
    for idx, item in enumerate(kb_matches[:3], start=1):
        merge_record(result, item, f"KNOWLEDGE_BASE_{idx}", 50, source_map)

    # 4) fontes online
    for item in parsed_sources:
        source_name = f"WEB:{item.get('_source_title', 'fonte')}"
        priority = 60

        parser_name = item.get("_parser")
        if parser_name == "generic":
            priority = 55
        elif parser_name == "wine_searcher":
            priority = 58
        elif parser_name == "vivino":
            priority = 57

        merge_record(result, item, source_name, priority, source_map)

    # fallback: se não preencheu nome do vinho, usa query
    if not result.get("wine_name"):
        result["wine_name"] = query

    return result, source_map

def count_filled_fields(record: dict):
    total = 21
    filled = 0
    for k, v in record.items():
        if k not in [
            "producer","wine_name","vintage","grape","country","region","subregion",
            "denomination","classification","wine_type","alcohol","aromas","palate",
            "acidity","body","soil","climate","terroir","aging","pairing","notes"
        ]:
            continue
        if str(v or "").strip():
            filled += 1
    return filled, total
