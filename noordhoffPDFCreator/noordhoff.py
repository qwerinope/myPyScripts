#!/bin/env python
# Noordhoff now loads images from PDFs. Each chapter is split into multiple PDFs.
# Im gonna see if theres a simple file with references to all pdf blobs.
# If there is, than i just iterate over all PDFs and download them.
# Maybe give the user the option to not merge all files into one.

# The PDFs are still not secured. Anyone with the correct URL can access them.
# The format is the following: https://pdfsplitter.blob.core.windows.net/pdf/production/split-books/{UUID}_{PAGESTART}_{PAGEEND}.pdf
# An example is https://pdfsplitter.blob.core.windows.net/pdf/production/split-books/6fe3a785-4b5b-41d8-a167-f737d4e3c647_1_8.pdf 
# Here the UUID (v4 ofc) is "6fe3a785-4b5b-41d8-a167-f737d4e3c64"
# The first page of the PDF is page 1, and the last page is page 8
# The UUID is constant across an ebook
# For PDFs consisting of one page, the first and last page are identical
# Example: https://pdfsplitter.blob.core.windows.net/pdf/production/split-books/6fe3a785-4b5b-41d8-a167-f737d4e3c647_51_51.pdf

# There does not appear to be an easy json object with references to all PDFs, bummer
# I'll have to brute-force it.
# This new website does have a positive: The UUID is the only thing we need, and it can easily be found in the URL,
# The previous iteration of the website had it hidden in the network tab of the devtools, along with a unix timestamp
# It's a lot more user friendly now to use my tool LOL

# The way i will do this is the following:
# I know the first page is always page 1 (which is wrong and dumb, indexing starts at 0 and always should)
# Start at page 1, then request: {UUID}_1_1.pdf
# If it returns 404, try: {UUID}_1_2.pdf
# and repeat until found
# If a pdf is found within a certain amount, download it, then repeat with the the last page it downloaded + 1
# If no pdf is found, stop running the download function, and move onto the PDF merging function.

# This should work 99% of the time. The 1% of times it doesn't is when a PDF file contains more pages than hardcoded.
# The hardcoded value should be large enough to prevent it stopping early, but not too large to make it realize it's done really late.
# I have patience, and so a value of 100 for pageCheckRange should be plenty.

import argparse
import re
from pathlib import Path
import shutil
import requests
from pypdf import PdfWriter

BASEURL = "https://pdfsplitter.blob.core.windows.net/pdf/production/split-books/"
PAGECHECKRANGE = 100
UUIDPATTERN = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

def doParser():
    parser = argparse.ArgumentParser(description='Download books from Noordhoff as PDF', epilog='https://github.com/qweri0p/myPyScripts')
    parser.add_argument('-v', '--verbose', help='Display each request.', action='store_true', default=False)
    parser.add_argument('-o', '--output', help='Rename PDF after creation to specified name.', action='store', default='output')
    parser.add_argument('-k', '--keep', help='Keep partial PDF files.', action='store_true', default=False)
    parser.add_argument('link', metavar='link', help='URL of the book.', nargs=1)
    args = parser.parse_args()
    return args

def main(url:str, output:str, verbose:bool, keep=False):
    bookId = getBookUUID(url, verbose)
    dirSetup(bookId, verbose)
    files = getFiles(bookId, verbose)
    mergePdfs(files, output, verbose)
    if not keep:
        deletefiles(bookId, verbose)

def getBookUUID(bookURL:str, verbose:bool) -> str:
    regex = re.findall(UUIDPATTERN, bookURL)
    if len(regex) == 0:
        print("Incorrect link entered, please try again.")
        exit(1)
    elif len(regex) == 2:
        uuid = regex[1]
    else:
        uuid = regex[0]

    if verbose:
        print(f'Extracted {uuid} from provided URL')

    return uuid

def dirSetup(uuid:str, verbose:bool):
    saveDir = Path(uuid)
    saveDir.mkdir(exist_ok=True)
    if verbose:
        print(f'Succesfully Created directory "{uuid}"')

def getFiles(uuid:str, verbose:bool) -> list[str]:
    downloading = True
    pagestart = 1
    pageend = 1
    checkprogress = 0
    files = [] # This files.array makes merging the PDFs a lot easier
    while downloading:

        if verbose:
            print(f'Attempting download for pages {pagestart} - {pageend}')

        r = requests.get(BASEURL+uuid+f'_{pagestart}_{pageend}.pdf')

        if r.status_code != 200:
            pageend += 1
            checkprogress += 1
        else:
            if verbose:
                print(f'PDF for page {pagestart}-{pageend} found and downloaded')
            
            with open(f'{uuid}/{pagestart}.pdf', 'wb') as f:
                f.write(r.content)
                f.close()

            files.append(f'{uuid}/{pagestart}.pdf')

            pagestart = pageend + 1
            pageend += 1
            checkprogress = 0
        
        # This part stops the loop when it hasn't downloaded a file in a while.
        if checkprogress == PAGECHECKRANGE:
            downloading = False
            if verbose:
                print(f'Pages beyond page {pageend} not found, continuing to merge PDFs.')

    return files

def mergePdfs(files:list[str], output:str, verbose:bool):
    merger = PdfWriter()
    for file in files:
        merger.append(file)

    merger.write(f'{output}.pdf')
    merger.close()
    
    if verbose:
        print(f'Written complete PDF file to "{output}.pdf"')

def deletefiles(uuid:str, verbose:bool):
    shutil.rmtree(uuid)
    if verbose:
        print('Deleted temporary files')

if __name__ == "__main__":
    args = doParser()
    main(args.link[0], args.output, args.verbose, args.keep)
