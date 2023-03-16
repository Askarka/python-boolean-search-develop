import os
import re

import nltk
import pymorphy2
from nltk.corpus import stopwords

# nltk.download('stopwords')

folder = 'data'
lemmas_folder = 'data lemmatized'
lemmas_file = open('lemmas.txt', 'r')
stopWords = stopwords.words("english")
sw = stopwords.words('russian') + stopwords.words('english')
morph = pymorphy2.MorphAnalyzer()


def lineWithoutStopWords(line):
    return [word for word in line if word not in stopWords]


def text_to_lemmas():
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.html'):
                text = open(folder + '/' + file, 'r')
                text = [line.lower() for line in text]
                text = [re.sub(r'[^\w\s]', ' ', line, flags=re.UNICODE) for line in text]
                tokenizedText = [nltk.word_tokenize(line) for line in text]
                withoutStopWords = [lineWithoutStopWords(line) for line in tokenizedText]

                def normalForm(line):
                    return [morph.parse(word)[0].normal_form for word in line if len(word) > 2]

                normalForm = [normalForm(line) for line in withoutStopWords]
                lemmatized_file = open(lemmas_folder + '/' + file.replace('.html', '_lemmas.txt'), "w+")
                for line in normalForm:
                    for word in line:
                        lemmatized_file.write(word + '\n')
                lemmatized_file.close()


if __name__ == '__main__':
    # text_to_lemmas()

    indexes = {}
    lemmas = []
    for line in lemmas_file:
        lemmas.append(line.split()[0])

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.html'):
                text = open(lemmas_folder + '/' + file.replace('.html', '_lemmas.txt'), 'r')
                text = text.read()
                for word in lemmas:
                    if text.split().__contains__(word):
                        if indexes.keys().__contains__(word):
                            indexes[word] = indexes[word] + ' ' + file.split('_')[1].replace('.html', '')
                        else:
                            indexes[word] = file.split('_')[1].replace('.html', '')

    # print(lemmas)
    # print(indexes)

    indexes_file = open('inverted_index.txt', "w+")
    for ind in indexes:
        indexes_file.write(ind + ' ' + indexes[ind] + '\n')
    # indexes_file.write()
    indexes_file.close()
    # print(len(lemmas))
