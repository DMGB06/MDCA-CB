from pathlib import Path
from typing import List
import re

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

def search_knowledge(query: str, max_results: int = 2) -> str:
    """
    Busca información relevante en los archivos markdown de la base local.
    Devuelve un string con los fragmentos más relevantes, priorizando coincidencias exactas y por cantidad de palabras clave.
    """
    keywords = [w.lower() for w in re.findall(r'\w+', query)]
    scored_results = []

    for md_file in KNOWLEDGE_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        content_lower = content.lower()
        # Cuenta cuántas palabras clave aparecen en el archivo
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > 0:
            scored_results.append((score, f"# {md_file.stem}\n" + content.strip()))

    # Ordena por score descendente (más coincidencias primero)
    scored_results.sort(reverse=True, key=lambda x: x[0])
    results = [r[1] for r in scored_results[:max_results]]
    return "\n\n---\n\n".join(results) if results else ""
