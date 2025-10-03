# Implémentation de la similarité et distance de Jaccard en Python
from typing import Union

def jaccard_similarity(A: Union[set, str], B: Union[set, str]) -> float:
    """
    Calcule la similarité de Jaccard entre deux ensembles ou deux chaînes de caractères.
    Les deux entrées doivent être du même type.
    Retourne une valeur entre 0 et 1.
    """
    if type(A) is not type(B):
        raise TypeError("Les deux entrées doivent être du même type (set ou str).")

    if isinstance(A, str):
        set1 = set(A)
        set2 = set(B)
    elif isinstance(A, set):
        set1 = A
        set2 = B
    else:
        raise TypeError("Les entrées doivent être de type set ou str.")

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    if union == 0:
        return 1.0  # Les deux ensembles/chaînes sont vides, considérés comme identiques

    return intersection / union

def jaccard_distance(A: Union[set, str], B: Union[set, str]) -> float:
    """
    Calcule la distance de Jaccard = 1 - similarité.
    Fonctionne pour les ensembles et les chaînes de caractères.
    """
    return 1 - jaccard_similarity(A, B)

# Exemple d'utilisation
string1 = "chat"
string2 = "chien"

print("Chaîne 1 :", string1)
print("Chaîne 2 :", string2)
print("Similarité de Jaccard (strings) :", jaccard_similarity(string1, string2))
print("Distance de Jaccard (strings) :", jaccard_distance(string1, string2))
print("-" * 20)
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
print("Ensemble 1 :", set1)
print("Ensemble 2 :", set2)
print("Similarité de Jaccard (sets) :", jaccard_similarity(set1, set2))
print("Distance de Jaccard (sets) :", jaccard_distance(set1, set2))
