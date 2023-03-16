import re
import sys

from nltk import RegexpTokenizer
from pymorphy2 import MorphAnalyzer


def tokenize(s):
    tknzr = RegexpTokenizer(r'[А-Яа-яёЁ&(\|)~\)\(]+')
    clean_words = tknzr.tokenize(s)
    clean_words = [w.lower() for w in clean_words if w != '']
    return list(clean_words)


def lemmatize(tokens):
    pymorphy2_analyzer = MorphAnalyzer()
    lemmas = []
    for token in tokens:
        if re.match(r'[А-Яа-яёЁ]', token):
            lemma = pymorphy2_analyzer.parse(token)[0].normal_form
            lemmas.append(lemma)
        else:
            lemmas.append(token)
    return lemmas


def operands(oper):
    if oper == '&':
        return 2
    elif oper == '|':
        return 1
    return -1


if __name__ == '__main__':
    pass
