from parser_engine import parse_label_text
from local_search import search_local_wine, search_local_denomination
from web_fetch import search_web

def build_wine_report(label_text: str):
    parsed = parse_label_text(label_text)

    local_wine = search_local_wine(label_text)
    local_do = search_local_denomination(label_text)

    web_query = label_text
    web_data = search_web(web_query, max_results=5)

    report = {
        "input": label_text,
        "parsed": parsed,
        "local_wine_match": local_wine,
        "local_denomination_match": local_do,
        "web_results": web_data
    }

    return report
