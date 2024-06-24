# cvfiles.py

Iterates through all files in a given directory and utilizes [ffmpeg](https://ffmpeg.org) to transform all files into a different file format.

You'll need no additional libraries, every part of this script uses python3 built-ins.
You will however need ffmpeg. Make sure ffmpeg is in `$PATH`. If you're not sure, run `ffmpeg` from a new shell/terminal. If it responds `command not found` you have either not installed it properly or at all.

# Required Arguments
* `input` - The file format the files are currently in.
* `output` - The file format you wish to convert the files to.

# Optional Arguments
* `-q`/`--quiet` - Makes the script print nothing to the standard output.
* `-c`/`--clean` - After converting, makes it deletes the original file from disk.
* `-d`/`--dir` - Specify the directory with files to convert. It will run in that directory.
* `-v`/`--verbose` - Print extra info about the file that's currently being converted.

# Examples
```sh
$ python cvfiles.py -c -d 1992 flac mp3
# Successfully converted "1992/01 Long-Awaited.flac" into "1992/01 Long-Awaited.mp3".
# Successfully converted "1992/02 1992.flac" into "1992/02 1992.mp3".
# Successfully converted "1992/03 Realm.flac" into "1992/03 Realm.mp3".
# Successfully converted "1992/04 Pieces.flac" into "1992/04 Pieces.mp3".
# Successfully converted "1992/05 Low-Life.flac" into "1992/05 Low-Life.mp3".
# Successfully converted "1992/06 Hologram Rose.flac" into "1992/06 Hologram Rose.mp3".
# Successfully converted "1992/07 Be Mine.flac" into "1992/07 Be Mine.mp3".
# Successfully converted "1992/08 Distant.flac" into "1992/08 Distant.mp3".
# Successfully converted "1992/09 A Way.flac" into "1992/09 A Way.mp3".
# Successfully converted "1992/10 Endless Plains.flac" into "1992/10 Endless Plains.mp3".
# Successfully converted "1992/11 Transmitting Bridge.flac" into "1992/11 Transmitting Bridge.mp3".
# Successfully converted "1992/12 Modification.flac" into "1992/12 Modification.mp3".
# Successfully converted "1992/13 Спайсуха (Bonus).flac" into "1992/13 Спайсуха (Bonus).mp3".
# Successfully converted "1992/14 1991 (Bonus).flac" into "1992/14 1991 (Bonus).mp3".
```

In this example I change all flac music files from the album ['1992' by 'CMD094'](https://cmd094music.bandcamp.com/album/1992) into 320k bitrate mp3s.

When converting mp3 files, it will force the bitrate to a constant 320kbit, the maximum quality for mp3s.
