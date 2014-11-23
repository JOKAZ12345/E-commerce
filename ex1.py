# coding=utf-8
from ex1HTML import *

__author__ = 'Jorge Cruz' + 'Adrien Aguado'

import json
import urllib
import urllib2
import cookielib
import re
import lxml.html
import BeautifulSoup
import numpy
from nltk.corpus import stopwords
from operator import itemgetter
from operator import add
import scipy.spatial.distance
import nltk
#import gensim
from random import randint

google_s = 'google_search.html'

stop = stopwords.words('english')
sentence = "this is a foobar test"
print [i for i in sentence.split() if i not in stop]
#nltk.download()

s = numpy.array((1,2,3) * 3)

debug = 1  # change this to 0 to download each page/parse again (I put this at 1 because i already have them downloaded)
stop_words = []
punctuation = []
allWords = []
dictAllWords = {} # array of dicts containing each occurrence of words
dictAllDocs = {} # array of dicts containing for each document each occurrence of words
tosave = "results/page_%d"  # Sets where it should save the parsing results of each page visited

#  EXERCISE 2
lexicon = []

def find_tupple(dic, word):
    for d in dic:
        if d[0] == word:
            return d[1]

    return 0

def printDictionary(dic):
    e = open('results.txt', 'w')
    for k in dic:
        print k[0] + " " + str(k[1])
        # UNCOMMENT ONE OF THIS LINES AT A TIME.. FIRST RUN WITH LINE 30 AND THEN RUN WITH JUST LINE 31
        # EACH TIME COPY THE VALUES TO EXCELL AND CREATE GRAPHS
        #e.write(str(k[1]) + "\n")  # This has each word.. Copy this to an excell grid
        #e.write(str(k[0]) + "\n")  # The other time copy this number of occurences for each word to excell grid

    e.close()


def addKeyToAllWords(key):
    if key in dictAllWords:
        value = dictAllWords[key]
        value += 1
        dictAllWords[key] = value
    else:
        dictAllWords[key] = 1


# This procedure counts how many times a word repeats itself for each document
def countWords():
    i = 0
    while i < 100:
        dict_words = {}  # empty dict
        f = open(tosave.replace('%d', str(i)))
        lines = f.readlines()

        #words = []
        for line in lines:
            w = re.split(r'[;,\s]\s*', line)  # matches and whitespace character (\r\n\t\f) (Parses each line of the document)
            for char in w: # w is an array of words of each line
                if char is not '':
                    if char in dict_words:  # already exists so we just increment its value
                        value = dict_words.get(char)
                        value += 1
                        dict_words[char] = value
                        addKeyToAllWords(char)
                    else:  # doesn't exist so add's it
                        dict_words[char] = 1
                        addKeyToAllWords(char)

        # ADDED THIS CODE TO SORT THE ARRAY BEFORE USING IT ON EXERCISE 2
        dict_words = sorted(dict_words.items(), key=itemgetter(1), reverse=True)  # and we have all how many times the words repeat themselves
        dictAllDocs[tosave.replace('%d', str(i))] = dict_words
        i += 1
    # at this point we have access to how many times in each document a word repeats itself (or not)


# Checks if a stopword is present in the middle of the text (uses boundary)..
def replace_all(text, dic):
    for i in dic:
        text = re.sub(r'\b(' + i + r')\b', '', text, 0, flags=re.IGNORECASE)
    return text

cj = cookielib.CookieJar()  # cookies are needed if not sometimes it doesn't preserve the web session

# Reads the file which contains the stopping words and puts them in memory for faster access
# http://www.webconfs.com/stop-words.php
def readStopWordsFile():
    file = open('stop_words.txt', 'r')

    lines = file.readlines()

    for line in lines:
        stop_words.append(line.replace("\n", ""))

# Sometimes the text changes it's own location.. Either on 'article', 'div', etc..
pages = 'page_%d'
xpath1 = '//*[@id="rso"]/div[2]'

# Opens the file with BeautifulSoup
# Then calls parseGoogle that gives us each URL of the search
a = parseGoogle(BeautifulSoup.BeautifulSoup(open(google_s)))

# Converting to a set doesn't produce duplicate search results (so it doesn't download the same page again)
# Caution: Doesn't preserve the order of the elements
if debug is 0:
    a = list(set(a))

    print "---Downloading all the single webpages!---\n"
    downloadpages(a)  # Downloads all the individual webpages
    print "---Download completed!---\n"

print "---Reading stop words from file...---"
readStopWordsFile()
print "---Completed---"

# Iterate each file.. (just change this after to a more generic approach)
z = 100

if debug is 0:
    e = 0
else:
    e = 100

while e != z:
    try:
        if e is not 4000:
            fileName = 'page_' + str(e)
            root = lxml.html.fromstring(decode_html(fileName))
            soup = BeautifulSoup.BeautifulSoup(open(fileName))
            childrenSoup = soup.findAll('p')
            inv_tags = ['p']
            i = 0
            f = open("results/" + fileName, 'w')

            ret = checkSoupHeaders(root, e)

            if ret is not -1:
                error = u'Spain: Joy For £2bn El Gordo Lottery Winners'
                if ret == error:
                    ret = u'spain: joy for 2 bn el gordo lottery winners'

                f.write(ret.lower() + "\n")
                for child in childrenSoup:
                    if i > 2:
                        if i < len(childrenSoup) - 1:
                            textChild = unicode.join(u'', map(unicode, child))  # convert child to string
                            textChild = re.sub('<[^>]*>', '', textChild)  # remove the tags from the text | matches all the text between < and >
                            textChild = ReplaceEntityNamesByCharacter(textChild.encode('utf-8'))
                            textChild = replace_all(textChild, stop_words)  # Remove stop words
                            textChild = re.sub("[^_a-zA-Z0-9]", ' ', textChild)  # remove punctuation | matches a single char that's not a '_' or a 'a-z' or 'A-Z' or '0-9'
                            textChild = " ".join(textChild.split())  # Split in an array by ' '
                            f.write(textChild.lower() + "\n")
                    i += 1
            f.close()
            e += 1
        else:
            e += 1
    except Exception as e:
        raise

countWords()  # Reads the words from /results/..

_s = sorted(dictAllWords.items(), key=itemgetter(1), reverse=True)  # and we have all how many times the words repeat themselves
# dictAllWord has ours Vectors Space Models

dic_key = dictAllDocs.keys()
lexicon = dictAllWords.keys()


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

space_vectors = []


# GETS THE SPACE VECTORS FOR EACH DOCUMENT ACCORDING TO THE LEXICON
if debug == 0:
    space_vectors = createSpaceVectors()
else:
    space_vectors = readSpaceVectorsFromFile()

u = space_vectors[0]
v = space_vectors[1]
cos = cosine(u, v)  # example.. this calculates the similarity between doc_1 and doc_2
similar_docs = {}
randomDocs = []


# CHOOSES HERE 5 RANDOM DOCUMENTS AND THEN GENERATES SUGGESTIONS
i = 0
lex = []
while i < 5:
    randNumber = randint(0, 99)
    if randNumber not in randomDocs:
        print 'rand=' + str(randNumber)
        randomDocs.append(randNumber)

        #lexDoc = dictAllDocs[tosave.replace('%d', str(randNumber))]
        #lex.append(lexDoc)
        i += 1

# Sum the space vectors of each document
# It's code prettier using numpy to sum the vectors instead of summing each element by each element
a = numpy.array(space_vectors[randomDocs[0]])
b = numpy.array(space_vectors[randomDocs[1]])
c = numpy.array(space_vectors[randomDocs[2]])
d = numpy.array(space_vectors[randomDocs[3]])
e = numpy.array(space_vectors[randomDocs[4]])

sum = a + b + c + d + e
u = sum.tolist()



i = 1
max = 0
doc = 0

while i < 100:
    #if i not in randomDocs:
        cos = cosine(u, space_vectors[i])

        similar_docs[i] = cos

        i += 1

maxAux = sorted(similar_docs.items(), key=itemgetter(1), reverse=True)

i = 0

for item in maxAux:
    if i >= 5:
        break
    print "Doc " + str(item[0]) + " - Cos " + str(item[1])
    i += 1

cos2 = 1 - scipy.spatial.distance.cosine(u, v)
d = scipy.spatial.distance.cityblock(u, v)
d2 = scipy.spatial.distance.euclidean(u, v)
correlation = scipy.spatial.distance.correlation(u, v)

#printAllWordValues(dictAllDocs)  # print all words and their own values
#printAllDocWordValues(dictAllDocs)  # print all words for each document and their own values
#printDictionary(_s)  # Prints the sorted results to a .txt file (CHECK THE FUNCTION FOR MORE DETAILS)

print 'finished'

