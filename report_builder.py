from parser_engine import parse_wine_query
from local_search import search_local_wine
from knowledge_base import search_knowledge_base, upsert_knowledge_entry
from web_fetcher import search_wine_online
from source_parsers import parse_source_item
from consolidator import consolidate, count_filled_fields
from database import insert_wine_if_new

def build_wine_report(query: str):
    parsed_query = parse_wine_query(query)
    local_wine = search_local_wine(query)
    kb_matches = search_knowledge_base(query)

    online_sources = search_wine_online(query, parsed_query)
    parsed_sources = []

    for src in online_sources:
        try:
            parsed = parse_source_item(src, query)
            parsed_sources.append(parsed)
        except Exception:
            continue

    consolidated, source_map = consolidate(
        query=query,
        parsed_query=parsed_query,
        local_wine=local_wine,
        kb_matches=kb_matches,
        parsed_sources=parsed_sources
    )

    filled, total = count_filled_fields(consolidated)

    # auto-save se encontrou algo minimamente útil
    if filled >= 6:
        upsert_knowledge_entry(query, consolidated)
        insert_wine_if_new(consolidated)

    report = {
        "query": query,
        "parsed_query": parsed_query,
        "local_wine": local_wine,
        "kb_matches": kb_matches,
        "online_sources": online_sources,
        "parsed_sources": parsed_sources,
        "consolidated": consolidated,
        "source_map": source_map,
        "filled_fields": filled,
        "total_fields": total,
    }
    return report
