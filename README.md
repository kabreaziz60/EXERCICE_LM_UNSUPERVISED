# Indice et distance de Jaccard pour le texte

Ce dossier contient un script Python (`jaccard_text.py`) concu pour manipuler le texte comme un multiensemble (bag of tokens) et calculer :

- l'indice de Jaccard (similarite) entre deux textes, en preservant les doublons;
- la distance de Jaccard (1 - indice) ;
- les composantes numerateur (intersection) et denominateur (union) pour mieux comprendre le calcul.

## Utilisation rapide

```bash
python3 jaccard_text.py
```

Le script affiche deux exemples :
1. comparaison caractere par caractere de `"Je mange"` et `"Je suis une grande"`;
2. comparaison mot a mot de `"banane mangue citron"` et `"banane mangues citron"`.

Chaque exemple detaille :
- le comptage des tokens,
- la valeur de l'intersection (numerateur),
- la valeur de l'union (denominateur),
- l'indice et la distance de Jaccard.

## Personnalisation

La fonction principale `jaccard_index_text` accepte désormais une série d'options pour façonner la tokenisation :

| Option | Description |
| --- | --- |
| `mode` | `"char"` (défaut) ou `"word"` selon que l'on travaille au niveau lettre ou mot. |
| `lowercase` | Normalise en minuscules pour ignorer la casse. |
| `keep_whitespace` | Utile en mode caractère si l'on souhaite garder les espaces. |
| `strip_punctuation` | Supprime la ponctuation de base (`string.punctuation`) avant tokenisation. |
| `use_default_stopwords` | Active instantanément un set mixte FR/EN déjà fourni. |
| `stop_words` | Ajoute/override votre propre liste (cumulable avec `use_default_stopwords`). |
| `normalize_plural` | Simplifie la gestion des pluriels en enlevant un `s` final (solution rapide pour commencer). |
| `lemmatizer` | Permet de brancher une fonction de lemmatisation/stemming maison (ex: `lambda t: stemmer.stem(t)`). |
| `ngram_size` | Produit des n-grammes glissants (ex: bigrammes de caractères pour capter les lettres adjacentes). |
| `respect_positions` | Active la version *positionnelle* : seuls les tokens alignés (même index) peuvent correspondre, l'union vaut `max(len(A), len(B))`. |
| `tokenizer` | Toujours possible d'injecter une fonction maison si l'on veut une logique totalement custom (nettoyage, synonymes...). |

> **Doublons / multiensembles** : les tokens sont comptés via `collections.Counter`, donc `"good good day"` ≠ `"good day"` (le multiset retient bien les répétitions).

Des variantes `jaccard_distance_text` et `jaccard_components_text` sont egalement exposes pour recuperer respectivement la distance ou le duo (intersection, union).

## Travaux a suivre

- Ajouter des tests unitaires (ex: pytest) pour valider les cas limites.
- Documenter des exemples supplementaires (synonymes, normalisation, stopwords...).
- Eventuellement proposer une version Notebook pour les demonstrations en cours.
