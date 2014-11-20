torrent_extracter by Axel Larsson 20 nov 2014
===============================================
The torrent_extracter script is written in python3 and its purpose is to first analyse a given file path to determine what sort of media it points to, for example a film or a tv series episode or
season pack. The script then either copies this/these file/files to a suitable directory such as "films/Film name/film.file.mkv" if a film or "series/Series name/Season #/episode.mkv" if a 
tv series. The script relies on a carefully crafted regular expression to determine whether the given file path represents a film or a tv series. The currently supported file extensions are:
- .mkv
- .ts
- .avi
- .sub
- .srt

Installation
------------
First, you need to have the setuptools module installed, this can be installed with "apt-get install python3-setuptools". Then it's pretty straightforward, you just run 
"sudo python3 setup.py install", afterwards you can optionally run a clean-up command: "sudo python3 setup.py clean --all" which will clean up the directory a bit. But the important consequence of
the install command is that it should now be possible to just run "torrent_extracter" from anywhere in the system.

Usage
-----
usage: torrent_extracter_runner.py [-h] [-v | -q] [-t TV_PATH] [-f FILM_PATH]
                                   torrent

Extract or copy provided file path to either a TV show or Film directory.

positional arguments:
  torrent               the file path to the torrent to extract

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         set this flag to display more verbose output
  -q, --quiet           set this flag to display less verbose output.
  -t TV_PATH, --tv_path TV_PATH
                        path to destination folder for TV shows
  -f FILM_PATH, --film_path FILM_PATH
                        path to destination folder for films


Project file structure
----------------------
The project is structured according to `Distributing a python command line application`_.
In short this means that the project can be compiled into a single executable file (or rather eggsecutable) via the "setup.py install" command. It also means that the project cannot be run 
directly via the "torrent_extracter/torrent_extracter.py" file properly, instead a convenience wrapper "torrent_extracter_runner.py" is available for direct use in the source tree. 
:: _Distributing a python command line application: http://gehrcke.de/2014/02/distributing-a-python-command-line-application/

Common problems
---------------
If the "torrent_extracter" command does not launch the app properly it could be due to the fact that the executable /usr/local/bin/torrent_extracter actually points to an eggsecutable such as 
/usr/local/lib/python3.4/dist-packages/torrent_extracter-X.X-py3.4.egg and you need to make sure to have read permission to this file as well as executable permission to the 
/usr/local/bin/torrent_extracter file.
