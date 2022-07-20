# youtube2mp3 0.1.2

## About

Download complete playlist from youtube and convert downloaded webm to mp3 - for winamp compability ;)

* youtube2mp3_012.py - Run me with python3
* linksfile.txt - Add link to all the playlists to download, separated with newline.

Ofc read youtube license agreement before use.

Written in Python [3.10.5]

## Compability

Currently only working on linux. To run on windows, save paths need to be set to r'c:\\filepath\\'.

## Changelog
Added feature to use linkfile.txt

Fixed something I forgot, but Pytube works again...




## Requirements
* pip install pytube, pydub and re.
* ffmpeg.exe ffplay.exe ffprobe.exe from https://www.gyan.dev/ffmpeg/builds/

## Script overview
The script does this
1. Download webm file
2. Put in folder specified in top of py-file sorted by by artist->album
3. Convert to mp3
4. Remove webm
