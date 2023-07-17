from collections import defaultdict
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from tqdm import tqdm
import pyconll
import json

LANG_LOOKUP = {
    "en": "../data/UD/UD_English/en-ud-train.conllu",
    "ja": "../data/UD/UD_Japanese/ja-ud-train.conllu",
    "ru": "../data/UD/UD_Russian/ru-ud-train.conllu",
    "fr": "../data/UD/UD_French/fr-ud-train.conllu",
    "es": "../data/UD/UD_Spanish/es-ud-train.conllu",
    "it": "../data/UD/UD_Italian/it-ud-train.conllu",
}


def extract_one(sentence):

    # for word in sentence:
    #     if "\\n" in word.misc.get("SpacesAfter", set()) and int(word.id) < len(
    #         sentence
    #     ):
    #         return None

    sentence_list = list(sentence)

    mapping = defaultdict(list)

    for word in sentence_list:
        # print(word.id, word.form, word.upos, word.head, word.deprel)
        mapping[word.head].append(word)

    phrases = []
    orders = []

    for head in mapping.keys():
        if head == "0" or head is None:
            continue
        if sentence[head].upos not in {"NOUN"}:
            continue

        filtered = list(
            filter(lambda x: x.upos == "ADJ" and x.deprel == "amod", mapping[head])
        )
        if len(filtered) < 2:
            continue

        sentence_idxs = [int(x.id) for x in filtered]

        # make sure there are no duplicate entries
        if len(set(sentence_idxs)) != len(sentence_idxs):
            continue

        # make sure the adjectives are consecutive
        # if max(sentence_idxs) - min(sentence_idxs) != (len(sentence_idxs) - 1):
        #     continue

        adjs = [x.lemma for x in filtered]

        if int(head) > max(sentence_idxs):
            phrases.append(" ".join([*adjs, sentence[head].lemma]))
            orders.append("adj_noun")
        elif int(head) < min(sentence_idxs):
            phrases.append(" ".join([sentence[head].lemma, *adjs]))
            orders.append("noun_adj")
        else:
            # the noun is in between the adjectives (weird)
            continue

    df = pd.DataFrame({"phrase": phrases, "order": orders})
    df.phrase = df.phrase.astype(str).apply(lambda x: x.lower())
    df["sentence_id"] = sentence.id
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang")
    parser.add_argument("--output_file")
    parser.add_argument("--num_sents", type=int)

    args = parser.parse_args()

    sentences = pyconll.load_from_file(LANG_LOOKUP.get(args.lang))

    dfs = []

    for i, sentence in zip(itertools.count(args.num_sents), sentences):
        df = extract_one(sentence)
        dfs.append(df)
    df = pd.concat(dfs)
    df["language"] = args.lang
    df.to_csv(args.output_file, index=False)
