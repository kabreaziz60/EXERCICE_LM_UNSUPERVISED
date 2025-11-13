"""Calcul du Jaccard pondéré via TF-IDF."""

from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, Sequence

import math


def compute_tf(tokens: Sequence[str]) -> Dict[str, float]:
    """Calcule TF (fréquence relative) pour une séquence de tokens."""

    counter = Counter(tokens)
    total = sum(counter.values()) or 1
    return {token: count / total for token, count in counter.items()}


def compute_idf(corpus: Iterable[Sequence[str]]) -> Dict[str, float]:
    """Calcule IDF = log((1 + N)/(1 + df)) + 1 pour chaque token."""

    doc_freq: Counter[str] = Counter()
    total_docs = 0
    for doc in corpus:
        total_docs += 1
        for token in set(doc):
            doc_freq[token] += 1
    return {
        token: math.log((1 + total_docs) / (1 + df)) + 1
        for token, df in doc_freq.items()
    }


def weighted_jaccard(tokens_a: Sequence[str], tokens_b: Sequence[str], *, idf_weights: Dict[str, float]) -> float:
    """Calcule l'indice de Jaccard pondéré (TF-IDF)."""

    tf_a = compute_tf(tokens_a)
    tf_b = compute_tf(tokens_b)
    all_tokens = set(tf_a) | set(tf_b)

    numerator = 0.0
    denominator = 0.0

    for token in all_tokens:
        weight = idf_weights.get(token, 1.0)
        a = tf_a.get(token, 0.0)
        b = tf_b.get(token, 0.0)
        numerator += weight * min(a, b)
        denominator += weight * max(a, b)

    if denominator == 0:
        return 1.0
    return numerator / denominator
