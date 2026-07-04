from parser_engine import parse_wine_query
from local_search import search_local_wine, search_local_denomination
from knowledge_base import search_knowledge_base, save_wine_to_knowledge
from web_fetcher import search_wine_online, search_denomination_online
from source_parsers import parse_source_result
from consolidator import consolidate_report
from database import insert_or_update_wine


def build_wine_report(query: str):
    parsed_query = parse_wine_query(query)

    local_wine = search_local_wine(query)
    local_denom = search_local_denomination(query)
    kb_matches = search_knowledge_base(query, limit=5)

    wine_sources = search_wine_online(query)
    denom_sources = search_denomination_online(query)

    all_sources = []
    seen_urls = set()

    for s in wine_sources + denom_sources:
        url = s.get("url", "")
        if url and url not in seen_urls:
            all_sources.append(s)
            seen_urls.add(url)

    parsed_sources = []
    for s in all_sources[:8]:
        try:
            parsed = parse_source_result(s)
            parsed_sources.append(parsed)
        except Exception:
            continue

    report = consolidate_report(
        query=query,
        parsed_query=parsed_query,
        local_wine=local_wine,
        local_denom=local_denom,
        kb_matches=kb_matches,
        online_sources=all_sources,
        parsed_sources=parsed_sources
    )

    # auto-save se a ficha estiver minimamente útil
    if report["filled_fields"] >= 6:
        final_data = dict(report["final_data"])

        aliases = [query.strip()]
        if final_data.get("producer") and final_data.get("wine_name"):
            aliases.append(f"{final_data['producer']} {final_data['wine_name']}".strip())

        kb_record = {
            "aliases": list(dict.fromkeys([a for a in aliases if a])),
            **final_data
        }

        save_wine_to_knowledge(kb_record)
        insert_or_update_wine(final_data)

    return report
