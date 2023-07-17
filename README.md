# adjective ordering

## Collection of Multi-Adjective Phrases

1. Sentences are sourced from Universal Dependencies (UD) treebank 
1. We identify words with a `upos` tag of "NOUN".
1. For each noun, we identify all of its dependents that have a `upos` tag of "ADJ" and a `deprel` tag of  "amod". 
1. We filter for nouns that have at least 2 adjective dependents.
1. We filter for sentences that have the adjectives either all pre-nominal or post-nominal (removing cases where adjectives occur both before and after a noun).
1. We lemmatize adjectives and nouns to flatten differences in morphological affix, gender, number, etc. 

## Format of Multi-Adjective Phrase Data Files

* Data files are located in `data/{lang}/adjective_phrases.txt`, where `{lang}` represents the 2-letter language code used to represent the language in UD. 
* `phrase`: the multi-adjective phrase (including noun) in lemmatized form
* `order`: one of "adj_noun" or "noun_adj", depending on whether the noun comes before or after the adjectives in the sentence
* `sentence_id`: the ID of the sentence in the UD dataset to recover the full original sentence
* `language`: 2-letter language code