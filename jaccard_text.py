"""Utilities pour calculer l'indice et la distance de Jaccard sur du texte.

Le module est pense pour traiter le texte comme un multiensemble (bag of tokens)
ou chaque occurrence compte. Par defaut on travaille au niveau caractere afin de
reproduire les exemples du cours, mais on peut facilement passer au niveau mot
ou meme fournir un tokeniseur custom.
"""

from __future__ import annotations

from collections import Counter
from typing import Callable, Iterable, List, Sequence, Tuple

Tokens = List[str]
Tokenizer = Callable[[str], Tokens]


def tokenize_text(
    text: str,
    mode: str = "char",
    lowercase: bool = True,
    keep_whitespace: bool = False,
) -> Tokens:
    """Transforme une chaine en liste de tokens pour char ou word.

    Args:
        text: texte brut a transformer.
        mode: "char" pour lettres individuelles, "word" pour mots separes par des espaces.
        lowercase: si True, convertit en minuscules pour ignorer la casse.
        keep_whitespace: seulement utile pour mode "char". Lorsque False les espaces
            et retours a la ligne sont retires avant comptage.
    """

    if lowercase:
        text = text.lower()

    if mode == "char":
        chars = list(text)
        if not keep_whitespace:
            chars = [ch for ch in chars if not ch.isspace()]
        return chars

    if mode == "word":
        return text.split()

    raise ValueError("mode doit valoir 'char' ou 'word'")


def _ensure_tokens(
    text: str,
    tokenizer: Tokenizer | None,
    mode: str,
    lowercase: bool,
    keep_whitespace: bool,
) -> Tokens:
    if tokenizer is not None:
        return tokenizer(text)
    return tokenize_text(
        text,
        mode=mode,
        lowercase=lowercase,
        keep_whitespace=keep_whitespace,
    )


def jaccard_components_from_tokens(
    tokens_a: Iterable[str], tokens_b: Iterable[str]
) -> Tuple[int, int]:
    """Retourne (intersection, union) pour deux sequences tokenisees."""

    counter_a = Counter(tokens_a)
    counter_b = Counter(tokens_b)

    if not counter_a and not counter_b:
        return 0, 0

    intersection = sum(
        min(counter_a[token], counter_b[token])
        for token in counter_a.keys() & counter_b.keys()
    )
    union = counter_a.total() + counter_b.total() - intersection
    return intersection, union


def jaccard_index_from_tokens(tokens_a: Iterable[str], tokens_b: Iterable[str]) -> float:
    """Indice de Jaccard pour deux sequences deja tokenisees."""

    intersection, union = jaccard_components_from_tokens(tokens_a, tokens_b)

    if union == 0:
        return 1.0

    return intersection / union


def jaccard_distance_from_tokens(tokens_a: Iterable[str], tokens_b: Iterable[str]) -> float:
    """Distance de Jaccard (= 1 - indice)."""

    return 1.0 - jaccard_index_from_tokens(tokens_a, tokens_b)


def jaccard_index_text(
    text_a: str,
    text_b: str,
    *,
    tokenizer: Tokenizer | None = None,
    mode: str = "char",
    lowercase: bool = True,
    keep_whitespace: bool = False,
) -> float:
    """Indice de Jaccard pour deux textes.

    On peut:
        - laisser mode="char" pour compter les lettres (doublons conservent leur poids),
        - utiliser mode="word" pour travailler sur les mots,
        - ou bien fournir un tokenizer custom via l'argument tokenizer.
    """

    tokens_a = _ensure_tokens(text_a, tokenizer, mode, lowercase, keep_whitespace)
    tokens_b = _ensure_tokens(text_b, tokenizer, mode, lowercase, keep_whitespace)
    return jaccard_index_from_tokens(tokens_a, tokens_b)


def jaccard_components_text(
    text_a: str,
    text_b: str,
    *,
    tokenizer: Tokenizer | None = None,
    mode: str = "char",
    lowercase: bool = True,
    keep_whitespace: bool = False,
) -> Tuple[int, int]:
    """Composants (intersection, union) de Jaccard pour deux textes."""

    tokens_a = _ensure_tokens(text_a, tokenizer, mode, lowercase, keep_whitespace)
    tokens_b = _ensure_tokens(text_b, tokenizer, mode, lowercase, keep_whitespace)
    return jaccard_components_from_tokens(tokens_a, tokens_b)


def jaccard_distance_text(
    text_a: str,
    text_b: str,
    **kwargs,
) -> float:
    """Distance de Jaccard entre deux textes (wrapper pratique)."""

    return 1.0 - jaccard_index_text(text_a, text_b, **kwargs)


def _pretty_counter(label: str, values: Sequence[str]) -> None:
    counter = Counter(values)
    detail = ", ".join(f"{token}:{count}" for token, count in sorted(counter.items()))
    print(f"{label}: {detail}")


if __name__ == "__main__":
    text_a = "Je mange"
    text_b = "Je suis une grande"

    print("=== Exemple caractere par caractere ===")
    tokens_a = tokenize_text(text_a)
    tokens_b = tokenize_text(text_b)
    _pretty_counter("Comptage A", tokens_a)
    _pretty_counter("Comptage B", tokens_b)
    char_intersection, char_union = jaccard_components_from_tokens(tokens_a, tokens_b)
    sim_char = jaccard_index_from_tokens(tokens_a, tokens_b)
    print(f"Intersection (numerateur): {char_intersection}")
    print(f"Union (denominateur): {char_union}")
    print(f"Indice de Jaccard (char): {sim_char:.3f}")
    print(f"Distance de Jaccard (char): {1 - sim_char:.3f}\n")

    print("=== Exemple mot a mot ===")
    phrase_a = "banane mangue citron"
    phrase_b = "banane mangues citron"
    word_intersection, word_union = jaccard_components_text(phrase_a, phrase_b, mode="word")
    sim_word = jaccard_index_text(phrase_a, phrase_b, mode="word")
    print(f"Phrases: '{phrase_a}' vs '{phrase_b}'")
    print(f"Intersection (numerateur): {word_intersection}")
    print(f"Union (denominateur): {word_union}")
    print(f"Indice de Jaccard (word): {sim_word:.3f}")
    print(f"Distance de Jaccard (word): {1 - sim_word:.3f}")
