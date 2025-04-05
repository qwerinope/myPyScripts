#!/bin/env python
import requests, img2pdf, argparse, os, re, json, shutil

parser = argparse.ArgumentParser(description='Download books from Noordhoff (JSON definition version)', epilog="https://github.com/qwerinope/myPyScripts")
parser.add_argument('-v', '--verbose', help="display individual images downloaded", action='store_true', default=False)
args = parser.parse_args()

try:
    with open("noordhoff.json") as f:
        configobj = json.loads(f.read())
except:
    print("Your 'noordhoff.json' object is incorrectly formatted or entirely missing.\nPlease check the 'noordhoff.json' file for errors.")
    exit(1)

def main(input: str, output: str):
    # example link: https://cdp.contentdelivery.nu/f5c5e97e-5f64-4da4-a3dd-d99154e8338d/20221004094415/extract/assets/img/layout/1.jpg
    # I need to extract: f5c5e97e-5f64-4da4-a3dd-d99154e8338d/20221004094415
    # REGEX TIME!!! YAAAAAY!!
    # [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/[0-9]+
    # That should work fine
    try:
        bookID = re.search("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/[0-9]+", input)
        dirname = re.search("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", input).group()
    except:
        print("You provided an incorrect link. Please check the readme for instructions.")
        exit(1)
    #it works :)
    if not bookID:
        print("Cannot find data required from provided url. Make sure you follow the instructions.")
        exit(1)

    if args.verbose:
        print("Selected book Identifier: "+bookID.group()+".")

    try:
        os.mkdir(dirname)
    except:
        shutil.rmtree(dirname)
        os.mkdir(dirname)

    if args.verbose:
        print("Created '"+dirname+"' directory.")

    fulllink = "https://cdp.contentdelivery.nu/"+bookID.group()+"/extract/assets/img/layout/"
    print("Downloading "+output+".")
    running = True
    index = 1
    while running:
        r = requests.get(fulllink + str(index) + ".jpg")
        if r.status_code == 200:
            if args.verbose:
                print("Downloading "+r.url+".")
            with open(dirname+"/"+str(index)+".jpg", 'wb') as f:
                f.write(r.content)
        else:
            running = False
        index+=1
    print("Downloaded every page.")
    print("Creating PDF.")
    imgs = []
    imgpaths = []
    for fname in os.listdir(dirname):
        if not fname.endswith(".jpg"):
            continue
        path = os.path.join(dirname, fname)
        if os.path.isdir(path):
            continue
        imgs.append(fname)

    # THIS IS TERRIBLE!!!
    # NEVER CHANGE THIS
    # this is to turn the string representing each image into an integer
    # so that the sort function correctly sorts it and then turn it back into a string
    # thank you so much chatgpt i could never have written this abomination myself
    imgs = sorted([int(x[:-4]) for x in imgs]) 
    imgpaths = [dirname+"/"+str(x)+".jpg" for x in imgs]
    # 🤮🤮🤮🤮

    with open(output+".pdf","wb") as f:
        f.write(img2pdf.convert(imgpaths))
    print("Done.")
    shutil.rmtree(dirname)

if __name__ == "__main__":
    for item in configobj:
        main(item["link"], item["output"])
