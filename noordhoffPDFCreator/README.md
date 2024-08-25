# noordhoff.py

Creates PDF files from Noordhoff ebooks.

Noordhoff is a dutch company that creates school books. They require you to use a terrible javascript infested website to read their books online. I don't want to do that, so I created a script that downloads each page and then merges them together.

You'll need the ['pypdf'](https://github.com/py-pdf/pypdf) and the ['requests'](https://github.com/psf/requests) libraries. Use the nix-shell environment included in the repo, a [python virtual environment](https://docs.python.org/3/library/venv.html) or the packages provided by your distro.

You will need to parse a single argument into the program. This `link` is the URL associated with the ebook.

## Optional Arguments
* `-v`/`--verbose` - Gives a lot of information about the program state.
* `-o`/`--output` - Renames the outputted PDF to the given name.
* `-k`/`--keep` - Do not delete temporary PDF files.

## How to get this link?
Go to the ebook, then copy the long code (the URL) on the top of your window. The code should look something like this:
```
https://apps.noordhoff.nl/se/content/book/4b9bf1e6-34c6-4eae-9d64-af4fe7fd3f6a/ebook/caa64911-13b3-4527-943d-5cf07af31d92
```
# noordhoff_json.py
For mass downloading files.

It requires `noordhoff.py` for use as a library.

It also requires a file called `noordhoff.json`. There's an example [here](noordhoff.json). If you're using this program, you should be able to figure out the rest.

# noordhoff-qt.py
QT6 GUI made using PySide6. Use pyinstaller to create a standalone executable.

Input the book URL in the top input, and select the download location with the 'Save as' button. Then press 'Download' and wait. 