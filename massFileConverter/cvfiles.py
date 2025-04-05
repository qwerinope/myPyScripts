#!/bin/env python
import subprocess, shutil, argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Convert all files with a certain extension to a different extension', epilog='https://github.com/qwerinope/myPyScripts')
parser.add_argument('-q', '--quiet', help="Do not write anything to stdout.", action='store_true', default=False)
parser.add_argument('-c', '--clean', help="Remove input file when done converting.", action='store_true', default=False)
parser.add_argument('-v', '--verbose', help="Print extra info about the file that's currently being converted.", action='store_true', default=False)
parser.add_argument('-d', '--dir', help="Runs the program in the specified directory.", default=".")
parser.add_argument('input', type=str, help="Files you wish to turn into different formats.")
parser.add_argument('output', type=str, help="Turn all files into this type of file")

args = parser.parse_args()

if not shutil.which("ffmpeg"):
    print("Please install 'ffmpeg'.")
    exit(1)

filepath = Path(args.dir)
files = sorted([str(file) for file in filepath.iterdir() if file.is_file()])

currentFileExtension = args.input
futureFileExtension = args.output

extra_arguments = '-hide_banner -loglevel error '

if args.verbose:
    extra_arguments += '-stats '

for file in files:
    if not file.endswith(currentFileExtension):
        continue
    match futureFileExtension:
        case 'mp3':
            extra_arguments += '-ab 320k '

    output = file[:-len(currentFileExtension):]+futureFileExtension

    cmd = ['ffmpeg', '-i', file, *extra_arguments.split(), output]
    run = subprocess.run(cmd)
    if run.returncode == 0:
        if not args.quiet:
            print(f'Successfully converted "{file}" into "{output}".')
        if args.clean:
            Path(file).unlink()
    else:
        raise OSError("File conversion failed, exiting...")
