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

La fonction principale `jaccard_index_text` accepte plusieurs paramètres :
- `mode="char"` (defaut) ou `mode="word"` pour choisir le type de tokens ;
- `lowercase=True` pour ignorer la casse ;
- `keep_whitespace=False` pour ignorer les espaces en mode caractere ;
- `tokenizer` pour brancher votre propre fonction de tokenisation (ex: n-grammes, nettoyage du texte, etc.).

Des variantes `jaccard_distance_text` et `jaccard_components_text` sont egalement exposes pour recuperer respectivement la distance ou le duo (intersection, union).

## Travaux a suivre

- Ajouter des tests unitaires (ex: pytest) pour valider les cas limites.
- Documenter des exemples supplementaires (synonymes, normalisation, stopwords...).
- Eventuellement proposer une version Notebook pour les demonstrations en cours.
