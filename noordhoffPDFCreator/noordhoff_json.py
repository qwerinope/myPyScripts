#!/bin/env python
import noordhoff
import json
import argparse

def doParser():
    parser = argparse.ArgumentParser(description='Download books from Noordhoff (JSON definition version)', epilog="https://github.com/qwerinope/myPyScripts")
    parser.add_argument('-v', '--verbose', help="Return more info regarding program state", action='store_true', default=False)
    args = parser.parse_args()
    return args

def main(verbose):
    cfg = loadcfg()
    for book in cfg:
        noordhoff.main(book["link"], book["output"], verbose)

def loadcfg():
    try:
        with open("noordhoff.json") as f:
            configobj = json.loads(f.read())
        return configobj
    except:
        print("Your 'noordhoff.json' object is incorrectly formatted or entirely missing.\nPlease check the 'noordhoff.json' file for errors.")
        exit(1)

if __name__ == "__main__":
    args = doParser()
    main(args.verbose)

