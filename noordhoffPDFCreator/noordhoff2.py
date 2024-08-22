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