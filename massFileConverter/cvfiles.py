#!/bin/env python
import subprocess
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Convert all files with a certain extension to a different extension', epilog='https://github.com/qweri0p/myPyScripts')
parser.add_argument('-q', '--quiet', help="Do not write anything to stdout.", action='store_true', default=False)
parser.add_argument('-c', '--clean', help="Remove input file when done converting.", action='store_true', default=False)
parser.add_argument('-d', '--dir', help="Runs the program in the specified directory.", default=".")
parser.add_argument('input', type=str, help="Files you wish to turn into different formats.")
parser.add_argument('output', type=str, help="Turn all files into this type of file")

args = parser.parse_args()

filepath = Path(args.dir)
files = sorted([str(file) for file in filepath.iterdir() if file.is_file()])

currentFileExtension = args.input
futureFileExtension = args.output

extra_arguments = '-hide_banner -loglevel error '

for file in files:
    if not file.endswith(currentFileExtension):
        continue
    match futureFileExtension:
        case 'mp3':
            extra_arguments += '-ab 320k '

    output = file[:-len(currentFileExtension):]+futureFileExtension

    cmd = ['ffmpeg', '-hide_banner', '-i', file, *extra_arguments.split(), output]
    run = subprocess.run(cmd)
    if run.returncode == 0:
        if not args.quiet:
            print(f'Successfully converted "{file}" into "{output}".')
        if args.clean:
            Path(file).unlink()
    else:
        exit()
