__author__ = 'JOKAZ'

from ex1 import *

def readSpaceVectorsFromFile():
    i = 0
    space_vectors = []
    while i < 100:
        f = open('vectors/' + str(i), 'r')

        space_vectors.append(json.load(f))

        f.close()

        i += 1

    return space_vectors


def createSpaceVectors():
    i = 0
    space_vectors = []
    while i < 100:
        dic_A = dictAllDocs[dic_key[i]]

        f = open('vectors/' + str(i), 'w')

        words_A = []

        for word in dic_A:
            words_A.append(word[0])

        # bzero the space vector
        space_vector = [0] * len(lexicon)

        z = 0
        while z < len(lexicon):
            word = lexicon[z]
            if word in words_A:
                space_vector[z] = find_tupple(dic_A, word)

            z += 1

        space_vectors.append(space_vector)
        i += 1

        json.dump(space_vector, f)
        f.close()

    return space_vectors


# Calculates the cosine between two documents
def cosine(doc_1, doc_2):
    tam = len(doc_1)
    # Calculates first the product between vectors
    i = 0
    sum = 0
    while i < tam:
        values = (doc_1[i] * doc_2[i])
        sum += values
        i += 1

    # Calculates here the |doc_1|
    i = 0
    sum_2 = 0
    while i < tam:
        values = doc_1[i] * doc_1[i]
        sum_2 += values
        i += 1

    res_1 = sum_2 ** 0.5

    # Calculates here the |doc_2|
    i = 0
    sum_3 = 0
    while i < tam:
        values = doc_2[i] * doc_2[i]
        sum_3 += values
        i += 1

    res_2 = sum_3 ** 0.5  # pow

    if res_1 == 0:
        return 0

    if res_2 == 0:
        return 0

    cosine = sum / (res_1 * res_2)

    return cosine
