"""Interface Streamlit pour explorer l'indice et la distance de Jaccard."""

import streamlit as st

import jaccard_text as jt


st.set_page_config(page_title="Indice de Jaccard", layout="wide")
st.title("Explorateur d'indice de Jaccard")


with st.sidebar:
    st.header("Paramètres de tokenisation")
    mode = st.selectbox("Mode", options=["char", "word"], index=1)
    respect_positions = st.checkbox("Respecter l'ordre / positions", value=False)
    lowercase = st.checkbox("Passer en minuscules", value=True)
    strip_punctuation = st.checkbox("Supprimer la ponctuation", value=True)
    keep_whitespace = st.checkbox("Conserver les espaces (mode char)", value=False)
    use_default_stopwords = st.checkbox("Stop-words par défaut", value=True)
    custom_stop = st.text_area(
        "Stop-words personnalisés (séparés par des espaces)",
        help="Ex: et le la of the",
    )
    normalize_plural = st.checkbox("Normaliser les pluriels", value=True)
    use_default_synonyms = st.checkbox("Synonymes par défaut (auto/car...)", value=True)
    custom_synonyms = st.text_area(
        "Synonymes personnalisés (clé=valeur, un par ligne)",
        help="Ex: voiture=automobile",
    )
    ngram_size = st.number_input("Taille n-gramme", min_value=1, max_value=5, value=1)
    count_duplicates = st.checkbox("Compter les doublons (multiset)", value=True)


text_a = st.text_area("Texte A", value="banane mangue citron")
text_b = st.text_area("Texte B", value="banane mangues citron")


stop_words = set(custom_stop.split()) if custom_stop else None
syn_map = None
if custom_synonyms:
    syn_map = {}
    for line in custom_synonyms.splitlines():
        if "=" in line:
            src, tgt = line.split("=", 1)
            syn_map[src.strip().lower()] = tgt.strip().lower()


params = dict(
    mode=mode,
    lowercase=lowercase,
    keep_whitespace=keep_whitespace,
    strip_punctuation=strip_punctuation,
    stop_words=stop_words,
    use_default_stopwords=use_default_stopwords,
    normalize_plural=normalize_plural,
    use_default_synonyms=use_default_synonyms,
    synonyms_map=syn_map,
    ngram_size=ngram_size,
)

token_list_a = jt.tokenize_text(text_a, **params)
token_list_b = jt.tokenize_text(text_b, **params)

index_params = dict(
    params,
    respect_positions=respect_positions,
    count_duplicates=count_duplicates,
)
index = jt.jaccard_index_text(text_a, text_b, **index_params)
distance = jt.jaccard_distance_text(text_a, text_b, **index_params)
inter, union = jt.jaccard_components_text(text_a, text_b, **index_params)


col1, col2, col3 = st.columns(3)
col1.metric("Intersection", inter)
col2.metric("Union", union)
col3.metric("Indice", f"{index:.3f}", delta=f"Distance {distance:.3f}")


st.subheader("Tokens utilisés (après normalisation)")
col_a, col_b = st.columns(2)
col_a.write(token_list_a)
col_b.write(token_list_b)

st.caption(
    "• Décochez 'Compter les doublons' pour reproduire l'exemple du cours "
    "`banane`/`citron` (union = 9).\n"
    "• Activez 'Respecter l'ordre / positions' pour appliquer la formule "
    "positionnelle (union = max(len(A), len(B)))."
)
