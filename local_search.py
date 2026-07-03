from rapidfuzz import fuzz
from database import fetch_all_wines, fetch_all_denominations

def search_local_wine(label_text: str):
    rows = fetch_all_wines()
    best = None
    best_score = 0

    label_lower = label_text.lower()

    for row in rows:
        wine_name, producer, country, macro_region, sub_region, appellation_name, vintage, grapes, style, notes = row

        haystack = " | ".join([
            wine_name or "",
            producer or "",
            country or "",
            macro_region or "",
            sub_region or "",
            appellation_name or "",
            vintage or "",
            grapes or ""
        ]).lower()

        score = fuzz.token_set_ratio(label_lower, haystack)
        if score > best_score:
            best_score = score
            best = {
                "wine_name": wine_name,
                "producer": producer,
                "country": country,
                "macro_region": macro_region,
                "sub_region": sub_region,
                "appellation_name": appellation_name,
                "vintage": vintage,
                "grapes": grapes,
                "style": style,
                "notes": notes,
                "score": score
            }

    return best

def search_local_denomination(label_text: str):
    rows = fetch_all_denominations()
    best = None
    best_score = 0

    label_lower = label_text.lower()

    for row in rows:
        universal_id, country, macro_region, sub_region, appellation_name, legal_level, wine_color_scope, alcohol_min, allowed_grapes, notes = row

        haystack = " | ".join([
            universal_id or "",
            country or "",
            macro_region or "",
            sub_region or "",
            appellation_name or "",
            legal_level or "",
            allowed_grapes or ""
        ]).lower()

        score = fuzz.token_set_ratio(label_lower, haystack)
        if score > best_score:
            best_score = score
            best = {
                "universal_id": universal_id,
                "country": country,
                "macro_region": macro_region,
                "sub_region": sub_region,
                "appellation_name": appellation_name,
                "legal_level": legal_level,
                "wine_color_scope": wine_color_scope,
                "alcohol_min": alcohol_min,
                "allowed_grapes": allowed_grapes,
                "notes": notes,
                "score": score
            }

    return best
