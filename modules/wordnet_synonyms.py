"""Génération optionnelle de synonymes via WordNet (NLTK)."""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, Iterable

try:
    import nltk
    from nltk.corpus import wordnet as wn
except Exception as exc:  # pragma: no cover
    raise RuntimeError(
        "wordnet_synonyms nécessite nltk et les données WordNet. "
        "Installez-les via `pip install nltk` puis `nltk.download(\"wordnet\")`."
    ) from exc


@lru_cache(maxsize=1)
def ensure_wordnet_loaded() -> None:
    """Télécharge WordNet si nécessaire et valide son chargement."""

    try:
        wn.ensure_loaded()
    except LookupError:
        nltk.download("wordnet")
        wn.ensure_loaded()


def build_synonym_map(words: Iterable[str], max_synonyms: int = 5) -> Dict[str, str]:
    """Renvoie un mapping token -> synonyme principal basé sur WordNet."""

    ensure_wordnet_loaded()
    mapping: Dict[str, str] = {}

    for word in words:
        synsets = wn.synsets(word)
        if not synsets:
            continue
        lemmas = synsets[0].lemmas()
        if not lemmas:
            continue
        canonical = lemmas[0].name().lower()
        mapping[word] = canonical
        for lemma in lemmas[1:max_synonyms]:
            mapping[lemma.name().lower()] = canonical

    return mapping
