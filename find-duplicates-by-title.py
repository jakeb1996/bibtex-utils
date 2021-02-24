'''
Author: Jake Bradford
Licence: See LICENSE in https://github.com/jakeb1996/bibtex-utils

This script takes a list of bibtex files and identifies entries with very
similar titles. The Levenshtein distance is used to calculate similarity
for all paired combinations of titles. The threshold can be set.
'''

import bibtexparser, glob, itertools
from bibtexparser.bibdatabase import BibDatabase

# The bibtex files to parse
# provide a list, or use glob
BIBTEX_FILES = [
    r"C:\git\thesis\citations.bib"
]

# Levenshtein distance is used to calculate similarity.
# If the L. distance is less than this value, it is deemed to be the same.
SIMILARITY_THRESHOLD = 20






# https://stackoverflow.com/a/32558749
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


entriesById = {}

for fpBibtex in BIBTEX_FILES:
    with open(fpBibtex, encoding="utf8") as bibtex_file:
        bib = bibtexparser.load(bibtex_file)

        for entry in bib.entries:

            if entry['ID'] not in entriesById:
                entriesById[entry['ID']] = entry['title']
            else:
                print('Found duplicate ID')

for combo in itertools.combinations(entriesById.keys(), 2):
    entryIdA = combo[0]
    entryIdB = combo[1]

    score = levenshteinDistance(
        entriesById[entryIdA],
        entriesById[entryIdB]
    ) 
    if score < 10:
        print(entryIdA, entryIdB, score)
    
