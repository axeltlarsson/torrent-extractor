# torrent_extracter by Axel Larsson

The torrent_extracter script is written in python3 and its purpose is to first analyse a given file path to determine what sort of media it points to, for example a film or a tv series episode or
season pack. The script then either copies this/these file/files to a suitable directory such as "films/Film name/film.file.mkv" if a film or "series/Series name/Season #/episode.mkv" if a 
tv series. The script relies on a carefully crafted regular expression to determine whether the given file path represents a film or a tv series. The currently supported file extensions are:
- .mkv
- .ts
- .avi
- .sub
- .srt

## Installation

First, you need to have the setuptools module installed, this can be installed with `apt-get install python3-setuptools`. Then it's pretty straightforward, you just run 
`sudo python3 setup.py install`, afterwards you can optionally run a clean-up command: `sudo python3 setup.py clean --all` which will clean up the directory a bit. But the important consequence of
the install command is that it should now be possible to just run `torrent_extracter` from anywhere in the system.

## Usage

	usage: torrent_extracter [-h] [-t TV_PATH] [-f FILM_PATH] [-d] [-l LOG_FILE]
	                         torrent

	Intelligently copies/extracts films and tv series to respective target
	directories

	positional arguments:
	  torrent               the file path to the torrent to extract

	optional arguments:
	  -h, --help            show this help message and exit
	  -t TV_PATH, --tv_path TV_PATH
	                        path to destination folder for TV shows, default is
	                        /tmp/films
	  -f FILM_PATH, --film_path FILM_PATH
	                        path to destination folder for films, default is
	                        /tmp/tv_series
	  -d, --debug           set this flag to prevent log files from being written
	                        and enable DEBUG-level output to console
	  -l LOG_FILE, --log_file LOG_FILE
	                        path to log file, default is ./torrent_extracter.log




## Project file structure

The project is structured according to [Distributing a python command line application](http://gehrcke.de/2014/02/distributing-a-python-command-line-application/).
In short this means that the project can be compiled into a single executable file (or rather eggsecutable) via the `setup.py install` command. It also means that the project cannot be run 
directly via the `torrent_extracter/torrent_extracter.py` file properly, instead a convenience wrapper `run_torrent_extracter.py` is available for direct use in the source tree. 

## Common problems

If the `torrent_extracter` command does not launch the app properly it could be due to the fact that the executable /usr/local/bin/torrent_extracter actually points to an eggsecutable such as 
/usr/local/lib/python3.4/dist-packages/torrent_extracter-X.X-py3.4.egg and you need to make sure to have read permission to this file as well as executable permission to the 
/usr/local/bin/torrent_extracter file.
