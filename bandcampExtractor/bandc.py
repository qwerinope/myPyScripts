#!/bin/env python
import zipfile, argparse, shutil, sys
from pathlib import Path

MUSICFILETYPES = ['.mp3', '.flac', '.ogg', '.aiff', '.m4a'] # for some reason, bandcamp doesn't include tagging data on .wav files...

try: 
    import music_tag
except ImportError:
    print("Please install the 'music-tag' python package. Check the README for more details.")
    exit(1)

parser = argparse.ArgumentParser(description='Unzip zipfiles downloaded from Bandcamp.com into directories labelled by album.', epilog="https://github.com/qweri0p/myPyScripts")
parser.add_argument('-v', '--verbose', help="Display individual items being extracted.", action='store_true', default=False)
parser.add_argument('-q', '--quiet', help="Do not display any information at all.", action='store_true', default=False)
parser.add_argument('-c', '--clean', help="Removes zipfile once completed", action='store_true', default=False)
parser.add_argument('-k', '--keep', help="Keep the temporary extracted files.", action='store_true', default=False)
parser.add_argument('-d', '--dir', help="Runs the program in the specified directory.", default=".")
parser.add_argument('zips', metavar="zipfiles", help="Only unzips specified zipfiles.", nargs='*')
args = parser.parse_args()

albums = []

# if the zips argument is parsed, don't do the fs scanning
if args.zips:
    for i in args.zips:
        albums.append(i.split(".zip")[0])
else:
    filepath = Path(args.dir)
    files = sorted([str(file) for file in filepath.iterdir() if file.is_file() and file.suffix == '.zip'])
    for i in files:
        albums.append(i.split(".zip")[0])

if albums == []:
    print('No zipfiles found', file=sys.stderr)
    exit(1)

# start actual process
for i in albums:
    currentzip = Path(f'{i}.zip')
    try:
        zip_ref = zipfile.ZipFile(currentzip, "r")
    except zipfile.BadZipFile:
        print(f'ERROR: Zipfile \'{currentzip.name}\' is corrupt. Please redownload the music from bandcamp', file=sys.stderr)
        exit(1)

    if args.quiet == False:
        print(f'Extracting: \'{currentzip.name}\'')

    # from the name of the zipfile, try to get the name of the album & artist
    # not possible if the user renamed it so there's a fallback
    # zipfiles from bandcamp have the following structure: "{ARTIST} - {ALBUM}.zip"
    try:
        artistname, albumname = i.split(' - ')
    except ValueError:
        artistname = ''
        albumname = i

    # create tempdir, if it already exists delete it and retry
    tempdir = Path(f'{albumname}-temp')
    if tempdir.exists():
        shutil.rmtree(tempdir)
    tempdir.mkdir()

    zip_ref.extractall(tempdir)

    if args.verbose == True:
        print(f'Extracted: \'{currentzip.name}\'')

    zip_ref.close()

    if args.clean == True:
        currentzip.unlink()
        if args.verbose == True:
            print(f'Deleted \'{currentzip.name}\'')

    finaldir = Path(f'{args.dir}/{albumname}')
    if finaldir.exists():
        print(f'ERROR: Cannot create directory \'{albumname}\' as directory already exists', file=sys.stderr)
        if args.keep == False:
            shutil.rmtree(tempdir)
        exit(1)
    else:
        finaldir.mkdir()

    for file in tempdir.iterdir():
        if file.suffix in MUSICFILETYPES:
            tagger = music_tag.load_file(file)
            tracknumber = str(tagger['tracknumber']).zfill(2)
            tracktitle = str(tagger['tracktitle'])
            newname = f'{tracknumber} {tracktitle}{file.suffix}'
            # i have no fucking clue why but STFU PYRIGHT
        else:
            nameelements = file.name.split(' - ')
            newname = nameelements[-1]

        newfile = finaldir / newname
        shutil.copy(tempdir / file.name, newfile)

        if args.verbose == True:
            print(f'Copied \'{file}\' to \'{newfile}\'.')

    if args.quiet == False:
        print(f'Extracted and renamed all files from \'{currentzip.name}\'')

    if args.keep == False:
        shutil.rmtree(tempdir)
        if args.verbose == True:
            print(f'Deleted \'{tempdir}\'')
