import re

KNOWN_APPELLATIONS = [
    "Sauternes", "Barsac", "Barolo", "Barbaresco", "Rioja"
]

KNOWN_REGIONS = [
    "Bordeaux", "Piemonte", "Rioja", "Mendoza"
]

def parse_label_text(label_text: str):
    raw = label_text.strip()
    lower = raw.lower()

    # safra
    vintage_match = re.search(r"\b(19\d{2}|20\d{2})\b", raw)
    vintage = vintage_match.group(1) if vintage_match else None

    appellation = None
    for item in KNOWN_APPELLATIONS:
        if item.lower() in lower:
            appellation = item
            break

    region = None
    for item in KNOWN_REGIONS:
        if item.lower() in lower:
            region = item
            break

    return {
        "raw_text": raw,
        "vintage": vintage,
        "appellation_hint": appellation,
        "region_hint": region
    }
