from pathlib import Path
from typing import List
import re

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

# Palabras que ignoramos porque aparecen en todo
STOPWORDS = {
    "el", "la", "los", "las", "de", "del", "en", "es", "un", "una",
    "que", "se", "su", "por", "con", "para", "al", "como", "más",
    "pero", "sus", "le", "ya", "o", "fue", "este", "ha", "me", "si",
    "sin", "sobre", "ser", "hay", "quien", "cual", "qué", "cómo"
}

def search_knowledge(query: str, max_results: int = 2) -> str:
    keywords = [
        w.lower() for w in re.findall(r'\w+', query)
        if w.lower() not in STOPWORDS and len(w) > 2  # ← filtra stopwords y palabras muy cortas
    ]

    # Si no quedan keywords útiles, no busca nada
    if not keywords:
        return ""

    scored_results = []

    for md_file in KNOWLEDGE_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        content_lower = content.lower()
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > 0:
            scored_results.append((score, f"# {md_file.stem}\n" + content.strip()))

    scored_results.sort(reverse=True, key=lambda x: x[0])
    results = [r[1] for r in scored_results[:max_results]]
    return "\n\n---\n\n".join(results) if results else ""