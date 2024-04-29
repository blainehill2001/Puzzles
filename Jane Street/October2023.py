import re

import nltk
from nltk.corpus import words

nltk.download("words")


def has_vowels_in_order(word):
    pattern = "^.*e.*u.*a.*i.*o.*$"
    return all(word.count(vowel) == 1 for vowel in "aeiou") and re.search(
        pattern, word
    )


english_words = words.words()
filtered_words = [word for word in english_words if has_vowels_in_order(word)]

for word in filtered_words:
    print(word)
