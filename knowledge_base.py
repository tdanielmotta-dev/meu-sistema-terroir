import json
from pathlib import Path
from difflib import SequenceMatcher

KB_PATH = Path("knowledge_base.json")


def ensure_kb():
    if not KB_PATH.exists():
        KB_PATH.write_text("[]", encoding="utf-8")


def load_knowledge_base():
    ensure_kb()
    try:
        return json.loads(KB_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_knowledge_base(data):
    KB_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()


def search_knowledge_base(query: str, limit: int = 5):
    kb = load_knowledge_base()
    scored = []

    for item in kb:
        hay = " ".join([
            str(item.get("producer", "")),
            str(item.get("wine_name", "")),
            str(item.get("vintage", "")),
            str(item.get("grape", "")),
            str(item.get("country", "")),
            str(item.get("region", "")),
            str(item.get("denomination", "")),
            " ".join(item.get("aliases", []) if isinstance(item.get("aliases"), list) else [])
        ])

        score = similarity(query, hay)
        if query.lower() in hay.lower():
            score += 0.35

        if score >= 0.30:
            item2 = dict(item)
            item2["_score"] = round(score, 4)
            scored.append(item2)

    scored.sort(key=lambda x: x["_score"], reverse=True)
    return scored[:limit]


def save_wine_to_knowledge(record: dict):
    kb = load_knowledge_base()

    producer = (record.get("producer") or "").strip().lower()
    wine_name = (record.get("wine_name") or "").strip().lower()
    vintage = (record.get("vintage") or "").strip().lower()

    for i, item in enumerate(kb):
        if (
            (item.get("producer", "").strip().lower() == producer) and
            (item.get("wine_name", "").strip().lower() == wine_name) and
            (item.get("vintage", "").strip().lower() == vintage)
        ):
            kb[i] = {**item, **record}
            save_knowledge_base(kb)
            return

    kb.append(record)
    save_knowledge_base(kb)
