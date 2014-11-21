__author__ = 'JOKAZ'

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