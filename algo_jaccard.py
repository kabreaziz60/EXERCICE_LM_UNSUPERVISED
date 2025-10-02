# Implémentation de la similarité et distance de Jaccard en Python

def jaccard_similarity(A: set, B: set) -> float:
    """
    Calcule la similarité de Jaccard entre deux ensembles.
    Retourne une valeur entre 0 et 1.
    """
    if not A and not B:
        return 1.0  # deux ensembles vides sont identiques
    intersection = len(A & B)
    union = len(A | B)
    return intersection / union

def jaccard_distance(A: set, B: set) -> float:
    """
    Calcule la distance de Jaccard = 1 - similarité
    """
    return 1 - jaccard_similarity(A, B)


# Exemple d'utilisation
A = {1, 2, 3}
B = {2, 3, 4, 5}

print("Ensemble A :", A)
print("Ensemble B :", B)
print("Similarité de Jaccard :", jaccard_similarity(A, B))
print("Distance de Jaccard :", jaccard_distance(A, B))
