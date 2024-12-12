# bandc.py

Extracts zips downloaded from [bandcamp](https://bandcamp.com).
Usually the naming is very annoying, but this tool renames them to something acceptable.
Instead of `artist - album/artist - album - tracknumber trackname`
it's `album/tracknumber trackname`.
You'll need the ['music-tag' library from PyPi](https://pypi.org/project/music-tag/).
Use the nix-shell environment included in the repo, a [python virtual environment](https://docs.python.org/3/library/venv.html)
or the [AUR package](https://aur.archlinux.org/packages/python-music-tag).

***NOTE: `.wav` can't and won't be extracted.
This is because bandcamp doesn't add tags to .wav files.
I have absolutely no idea why.***

## Optional Arguments

* `-v`/`--verbose` - Lists each track being extracted individually.
* `-q`/`--quiet` - Do not display any information at all apart from crashes.
* `-c`/`--clean` - Removes zipfile when finished.
* `-k`/`--keep` - Do not delete temporary files when finished.
* `-d`/`--dir` - Runs the program in the specified directory.
