from __future__ import annotations

from math import sqrt
from .types import Episode


def _cosine(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a))
    nb = sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


class EpisodicMemory:
    """In-memory similarity baseline.

    Replace with FAISS/vector DB plus persistent metadata once the baseline is
    validated. This implementation keeps the retrieval behavior testable and
    dependency-light.
    """

    def __init__(self) -> None:
        self._episodes: list[Episode] = []

    def add(self, episode: Episode) -> None:
        self._episodes.append(episode)

    def search(self, embedding: tuple[float, ...], top_k: int = 3) -> list[tuple[Episode, float]]:
        scored = [(ep, _cosine(embedding, ep.embedding)) for ep in self._episodes]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[: max(int(top_k), 0)]

    def __len__(self) -> int:
        return len(self._episodes)
