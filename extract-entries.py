'''
Author: Jake Bradford
Licence: See LICENSE in https://github.com/jakeb1996/bibtex-utils

This script takes a list of bibtex files and extracts entries for those keys
that you provide.

This is useful when you have a massive Bibtex file but only some of it is
actually being used. For example, when you export your Mendeley library
in Bibtex format, but only a subset of the references are used in your paper.
'''

import bibtexparser, glob
from bibtexparser.bibdatabase import BibDatabase

# the bibtex files to parse.
# provide a list, or use glob
BIBTEX_FILES = [
    r"C:\git\thesis\citations.bib"
]

OUTPUT_FILE = r"extract-entries.txt"

# the entry tags to extract from the bibtex files
ENTRIES_TO_EXTRACT = [

]






entriesById = {}

outBib = BibDatabase()

for fpBibtex in BIBTEX_FILES:
    with open(fpBibtex, encoding="utf8") as bibtex_file:
        bib = bibtexparser.load(bibtex_file)

        for entry in bib.entries:
            if entry['ID'] not in entriesById:
                entriesById[entry['ID']] = [entry]
            else:
                entriesById[entry['ID']].append(entry)

for entryToExtract in ENTRIES_TO_EXTRACT:
    if entryToExtract in entriesById:
        for ref in entriesById[entryToExtract]:
            outBib.entries.append(
                ref
            )

with open(OUTPUT_FILE, 'w+') as fp:           
    fp.write(bibtexparser.dumps(outBib))

    