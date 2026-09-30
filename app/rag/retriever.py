from __future__ import annotations

from typing import Any


def retrieve_relevant_documents(documents: list[str], query: str, top_k: int = 3) -> list[str]:
    if not documents:
        return []
    query_lower = query.lower()
    scored: list[tuple[int, str]] = []
    for document in documents:
        score = 0
        for token in query_lower.split():
            if token in document.lower():
                score += 1
        scored.append((score, document))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k] if doc]
