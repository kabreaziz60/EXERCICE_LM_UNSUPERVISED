"""Utilities pour calculer l'indice et la distance de Jaccard sur du texte.

Le module est pense pour traiter le texte comme un multiensemble (bag of tokens)
ou chaque occurrence compte. Par defaut on travaille au niveau caractere afin de
reproduire les exemples du cours, mais on peut facilement passer au niveau mot
ou meme fournir un tokeniseur custom.
"""

from __future__ import annotations

from collections import Counter
from typing import Callable, Collection, Iterable, List, Sequence, Tuple
import string

Tokens = List[str]
Tokenizer = Callable[[str], Tokens]

# Petite liste mixte de stop-words FR/EN pour démarrer.
DEFAULT_STOP_WORDS = {
    "je",
    "tu",
    "il",
    "elle",
    "nous",
    "vous",
    "ils",
    "elles",
    "le",
    "la",
    "les",
    "de",
    "des",
    "du",
    "un",
    "une",
    "et",
    "the",
    "a",
    "an",
    "of",
    "to",
    "is",
    "are",
    "be",
}

_PUNCTUATION_TABLE = str.maketrans("", "", string.punctuation)


def tokenize_text(
    text: str,
    mode: str = "char",
    lowercase: bool = True,
    keep_whitespace: bool = False,
    strip_punctuation: bool = False,
    stop_words: Collection[str] | None = None,
    normalize_plural: bool = False,
    ngram_size: int = 1,
) -> Tokens:
    """Transforme une chaine en liste de tokens pour char ou word.

    Args:
        text: texte brut a transformer.
        mode: "char" pour lettres, "word" pour mots separes par des espaces.
        lowercase: si True, convertit en minuscules pour ignorer la casse.
        keep_whitespace: seulement utile pour mode "char". Lorsque False les espaces
            et retours a la ligne sont retires avant comptage.
        strip_punctuation: supprime ponctuation de base avant tokenisation.
        stop_words: collection de tokens a ignorer (utile pour mode "word").
        normalize_plural: tentative simple pour ramener les pluriels a leur singulier.
        ngram_size: produit des n-grammes glissants si > 1.
    """

    if lowercase:
        text = text.lower()

    if strip_punctuation:
        text = text.translate(_PUNCTUATION_TABLE)

    if mode == "char":
        chars = list(text)
        if not keep_whitespace:
            chars = [ch for ch in chars if not ch.isspace()]
        tokens = chars
    elif mode == "word":
        tokens = text.split()
    else:
        raise ValueError("mode doit valoir 'char' ou 'word'")

    if stop_words:
        tokens = [tok for tok in tokens if tok not in stop_words]

    if normalize_plural and mode == "word":
        tokens = [_normalize_plural(tok) for tok in tokens]

    if ngram_size > 1:
        tokens = _generate_ngrams(tokens, ngram_size)

    return tokens


def _ensure_tokens(
    text: str,
    tokenizer: Tokenizer | None,
    mode: str,
    lowercase: bool,
    keep_whitespace: bool,
    strip_punctuation: bool,
    stop_words: Collection[str] | None,
    normalize_plural: bool,
    ngram_size: int,
) -> Tokens:
    if tokenizer is not None:
        return tokenizer(text)
    return tokenize_text(
        text,
        mode=mode,
        lowercase=lowercase,
        keep_whitespace=keep_whitespace,
        strip_punctuation=strip_punctuation,
        stop_words=stop_words,
        normalize_plural=normalize_plural,
        ngram_size=ngram_size,
    )


def _normalize_plural(token: str) -> str:
    """Simplifie la gestion des pluriels (troncature naive du 's' final)."""

    if token.endswith("s") and len(token) > 3:
        return token[:-1]
    return token


def _generate_ngrams(tokens: Sequence[str], size: int) -> Tokens:
    """Cree des n-grammes glissants (char ou word) de longueur 'size'."""

    if size <= 1:
        return list(tokens)
    if len(tokens) < size:
        return []
    joiner = "" if all(len(tok) == 1 for tok in tokens) else " "
    return [
        joiner.join(tokens[i : i + size])
        for i in range(len(tokens) - size + 1)
    ]


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


def jaccard_components_positional(
    tokens_a: Sequence[str], tokens_b: Sequence[str]
) -> Tuple[int, int]:
    """Retourne (intersection, union) en respectant les positions.

    Intersection: nombre de positions où les tokens sont identiques.
    Union: nombre total de positions couvertes (max(len(A), len(B))).
    """

    len_a = len(tokens_a)
    len_b = len(tokens_b)
    if len_a == 0 and len_b == 0:
        return 0, 0

    limit = min(len_a, len_b)
    intersection = sum(1 for i in range(limit) if tokens_a[i] == tokens_b[i])
    union = max(len_a, len_b)
    return intersection, union


def jaccard_index_from_tokens(tokens_a: Iterable[str], tokens_b: Iterable[str]) -> float:
    """Indice de Jaccard pour deux sequences deja tokenisees."""

    intersection, union = jaccard_components_from_tokens(tokens_a, tokens_b)

    if union == 0:
        return 1.0

    return intersection / union


def jaccard_index_positional(tokens_a: Sequence[str], tokens_b: Sequence[str]) -> float:
    """Indice de Jaccard lorsque les positions comptent."""

    intersection, union = jaccard_components_positional(tokens_a, tokens_b)

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
    strip_punctuation: bool = False,
    stop_words: Collection[str] | None = None,
    normalize_plural: bool = False,
    ngram_size: int = 1,
    respect_positions: bool = False,
) -> float:
    """Indice de Jaccard pour deux textes.

    On peut:
        - laisser mode="char" pour compter les lettres (doublons conservent leur poids),
        - utiliser mode="word" pour travailler sur les mots,
        - activer la normalisation (ponctuation, stop-words, pluriels, n-grammes),
        - mettre `respect_positions=True` pour n'autoriser les correspondances qu'au même index
          (formule utilisée dans le cours: union = max(len(A), len(B))).
        - ou bien fournir un tokenizer custom via l'argument tokenizer.
    """

    tokens_a = _ensure_tokens(
        text_a,
        tokenizer,
        mode,
        lowercase,
        keep_whitespace,
        strip_punctuation,
        stop_words,
        normalize_plural,
        ngram_size,
    )
    tokens_b = _ensure_tokens(
        text_b,
        tokenizer,
        mode,
        lowercase,
        keep_whitespace,
        strip_punctuation,
        stop_words,
        normalize_plural,
        ngram_size,
    )
    if respect_positions:
        return jaccard_index_positional(tokens_a, tokens_b)
    return jaccard_index_from_tokens(tokens_a, tokens_b)


def jaccard_components_text(
    text_a: str,
    text_b: str,
    *,
    tokenizer: Tokenizer | None = None,
    mode: str = "char",
    lowercase: bool = True,
    keep_whitespace: bool = False,
    strip_punctuation: bool = False,
    stop_words: Collection[str] | None = None,
    normalize_plural: bool = False,
    ngram_size: int = 1,
    respect_positions: bool = False,
) -> Tuple[int, int]:
    """Composants (intersection, union) de Jaccard pour deux textes.

    Lorsque `respect_positions=True`, on applique la version positionnelle:
    intersection = nombre de positions identiques, union = max(len(A), len(B)).
    """

    tokens_a = _ensure_tokens(
        text_a,
        tokenizer,
        mode,
        lowercase,
        keep_whitespace,
        strip_punctuation,
        stop_words,
        normalize_plural,
        ngram_size,
    )
    tokens_b = _ensure_tokens(
        text_b,
        tokenizer,
        mode,
        lowercase,
        keep_whitespace,
        strip_punctuation,
        stop_words,
        normalize_plural,
        ngram_size,
    )
    if respect_positions:
        return jaccard_components_positional(tokens_a, tokens_b)
    return jaccard_components_from_tokens(tokens_a, tokens_b)


def jaccard_distance_text(
    text_a: str,
    text_b: str,
    *,
    tokenizer: Tokenizer | None = None,
    mode: str = "char",
    lowercase: bool = True,
    keep_whitespace: bool = False,
    strip_punctuation: bool = False,
    stop_words: Collection[str] | None = None,
    normalize_plural: bool = False,
    ngram_size: int = 1,
    respect_positions: bool = False,
) -> float:
    """Distance de Jaccard entre deux textes (wrapper pratique)."""

    return 1.0 - jaccard_index_text(
        text_a,
        text_b,
        tokenizer=tokenizer,
        mode=mode,
        lowercase=lowercase,
        keep_whitespace=keep_whitespace,
        strip_punctuation=strip_punctuation,
        stop_words=stop_words,
        normalize_plural=normalize_plural,
        ngram_size=ngram_size,
        respect_positions=respect_positions,
    )


def _pretty_counter(label: str, values: Sequence[str]) -> None:
    counter = Counter(values)
    detail = ", ".join(f"{token}:{count}" for token, count in sorted(counter.items()))
    print(f"{label}: {detail}")


if __name__ == "__main__":
    text_a = "Je mange"
    text_b = "Je suis une grande"

    print("=== Exemple caractere par caractere (ordre libre) ===")
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

    print("=== Exemple caractere avec positions alignees ===")
    pos_intersection, pos_union = jaccard_components_text(
        text_a,
        text_b,
        respect_positions=True,
    )
    sim_char_pos = jaccard_index_text(
        text_a,
        text_b,
        respect_positions=True,
    )
    print(f"Intersection (numerateur): {pos_intersection}")
    print(f"Union (denominateur): {pos_union}")
    print(f"Indice de Jaccard positionnel (char): {sim_char_pos:.3f}")
    print(f"Distance positionnelle (char): {1 - sim_char_pos:.3f}\n")

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

    print("\n=== Exemple mot a mot avec positions ===")
    word_pos_intersection, word_pos_union = jaccard_components_text(
        phrase_a,
        phrase_b,
        mode="word",
        respect_positions=True,
    )
    sim_word_pos = jaccard_index_text(
        phrase_a,
        phrase_b,
        mode="word",
        respect_positions=True,
    )
    print(f"Intersection (numerateur): {word_pos_intersection}")
    print(f"Union (denominateur): {word_pos_union}")
    print(f"Indice de Jaccard positionnel (word): {sim_word_pos:.3f}")
    print(f"Distance positionnelle (word): {1 - sim_word_pos:.3f}")
