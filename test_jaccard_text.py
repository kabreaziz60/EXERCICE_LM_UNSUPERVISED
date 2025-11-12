"""Tests Pytest pour le module jaccard_text."""

import pytest

import jaccard_text as jt


def test_multiset_characters_matches_expected_ratio():
    """Validation de l'exemple multiset du cours (caractères)."""

    sim = jt.jaccard_index_text("Je mange", "Je suis une grande")
    assert sim == pytest.approx(6 / 16)


def test_positional_word_index_uses_max_length_union():
    """Lorsque l'ordre compte, l'union est max(len(A), len(B))."""

    sim = jt.jaccard_index_text(
        "banane mangue citron",
        "banane mangues citron",
        mode="word",
        respect_positions=True,
    )
    assert sim == pytest.approx(2 / 3)


def test_stop_words_and_synonyms_normalize_tokens():
    """Stop-words + synonymes doivent rapprocher les phrases."""

    sim = jt.jaccard_index_text(
        "La voiture est plus rapide que l'auto",
        "Cette automobile est très rapide",
        mode="word",
        strip_punctuation=True,
        use_default_stopwords=True,
        use_default_synonyms=True,
        normalize_plural=True,
    )
    assert sim == pytest.approx(2 / 3)


def test_custom_synonym_map_overrides_default():
    """On peut injecter sa propre table de synonymes."""

    synonym_map = {"chien": "canin", "dog": "canin"}
    sim = jt.jaccard_index_text(
        "chien fidèle",
        "dog loyal",
        mode="word",
        strip_punctuation=True,
        stop_words={"loyal"},
        synonyms_map=synonym_map,
    )
    assert sim == pytest.approx(1.0)


def test_ngram_generation_for_characters():
    """Les n-grammes doivent fonctionner sur les caractères."""

    tokens = jt.tokenize_text("abc", mode="char", ngram_size=2)
    assert tokens == ["ab", "bc"]
