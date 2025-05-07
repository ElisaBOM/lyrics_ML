# pip install "bertopic[all]" sentence-transformers

import re
import string
import pandas as pd
from collections import Counter



spanish_punct = string.punctuation + "¡¿«»"

def remove_stuff(text):
    return re.sub(r"(?<!\w)-|-(?!\w)|[{}]".format(re.escape(spanish_punct.replace("-", ""))), "", text) 


if __name__ == '__main__':
    # Example Spanish documents
    df = pd.read_csv('c:/Users/rmessina/Eli/data/song_lyrics_es_1950_2020_lemmaNouns.csv', encoding='utf8')  # Load your dataset
    process_col = 'lemmatized_lyrics'

    # Remove NaN values from the 'lemmatized_lyrics' column
    initial_count = len(df)
    df = df.dropna(subset=[process_col])
    final_count = len(df)
    removed_count = initial_count - final_count
    print(f"Removed {removed_count} rows with NaN values from {process_col}.")

    initial_count = len(df)
    min_lemma = 10
    df['length'] = df['lemmatized_lyrics'].str.split().apply(len)
    df = df[df['length'] > min_lemma]  # Remove very short ones
    final_count = len(df)
    removed_count = initial_count - final_count
    print(f"Removed {removed_count} rows with less than {min_lemma} lemmas.")

    counter = Counter()
    for song in df[process_col].values:
        for word in song.split(' '):
            word = remove_stuff(word)
            counter[word] += 1
    with open("c:/Users/rmessina/Eli/data/song_lyrics_es_1950_2020_lemmaNouns_counters.csv", "wt", encoding="utf8") as fo:
        _ = fo.write("noun,count\n")
        for noun, m in sorted(counter.items(), key=lambda x: x[1], reverse=True):
            _ = fo.write(f"{noun},{m}\n")
        
