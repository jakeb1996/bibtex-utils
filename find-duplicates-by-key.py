'''
Author: Jake Bradford
Licence: See LICENSE in https://github.com/jakeb1996/bibtex-utils

This script takes a list of bibtex files and identifies entries with identical
keys. 
'''

import bibtexparser, glob
from bibtexparser.bibdatabase import BibDatabase

# the bibtex files to parse.
# attempt to merge these into one
# provide a list, or use glob
BIBTEX_FILES = [
    r"C:\git\thesis\citations.bib"
]

# Write results to files?
# If True: ensure you check the OUT_ variables below
WRITE_RESULTS_TO_FILE = True

# the file to write unique entries into
OUT_SINGLE = r"citations.singles.bib"

# the file to write duplicate entries into
OUT_DUPLICATES = r"citations.duplicates.bib"





entriesById = {}

outBibSingles = BibDatabase()
outBibDuplicates = BibDatabase()

for fpBibtex in BIBTEX_FILES:
    with open(fpBibtex, encoding="utf8") as bibtex_file:
        bib = bibtexparser.load(bibtex_file)

        for entry in bib.entries:
        
            # remove some fields
            for field in [
                'file',
                'mendeley-groups',
                'abstract'
            ]:
                if field in entry:
                    del entry[field]
        
            if entry['ID'] not in entriesById:
                entriesById[entry['ID']] = [entry]
            else:
                isTrueDuplicate = False
                for existingEntry in entriesById[entry['ID']]:
                    isTrueDuplicate |= (existingEntry == entry)
                        
                if not isTrueDuplicate:
                    entriesById[entry['ID']].append(
                        entry
                    )

for entryId in entriesById:
    if len(entriesById[entryId]) == 1:
        # singles
        outBibSingles.entries.append(
            entriesById[entryId][0]
        )
        
    else:
        # duplicates
        for i in entriesById[entryId]:
            outBibDuplicates.entries.append(
                i
            )

if WRITE_RESULTS_TO_FILE:            
    with open(OUT_SINGLE, 'w+', encoding="utf8") as fp:
        fp.write(bibtexparser.dumps(outBibSingles))

                    
    with open(OUT_DUPLICATES, 'w+', encoding="utf8") as fp:
        fp.write(bibtexparser.dumps(outBibDuplicates))

else:
    print('-------------------- Entries with keys that exist only once')
    print(bibtexparser.dumps(outBibSingles))
    
    print('-------------------- Entries with keys that exist as duplicates')
    print(bibtexparser.dumps(outBibDuplicates))
    