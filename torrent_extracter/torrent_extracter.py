#!/usr/bin/python3
"""torrent_extracter.torrent_extracter: provides entry point main()."""

__version__ = "0.1"

import re, sys, argparse, os
from .utils import debug
from .settings import Settings
from .torrent import TorrentFactory

# Handles the command line parsing and starts the process of extracting/copying
def main():
	#-----------------------------------
	#	Dealing with args and settings
	#-----------------------------------
	parser = argparse.ArgumentParser(description="Extract or copy provided file path to either a TV show or Film directory.")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-v", "--verbose", action="store_true", help="set this flag to display more verbose output")
	group.add_argument("-q", "--quiet", action="store_true", help="set this flag to display less verbose output.")
	parser.add_argument("-t", "--tv_path", help="path to destination folder for TV shows")
	parser.add_argument("-f", "--film_path", help="path to destination folder for films")
	parser.add_argument("torrent", help="the file path to the torrent to extract")
	args = parser.parse_args()

	settings = Settings()
	settings.tv_path = os.path.normpath(args.tv_path or "/tmp/tv_series")
	settings.film_path = os.path.normpath(args.film_path or "/tmp/films")
	if args.quiet:
		settings.verbosity = 0
	elif args.verbose:
		settings.verbosity = 2
	else:
		settings.verbosity = 1		
	
	if not os.path.exists(args.torrent):
		print(args.torrent + " does not exist.")
		sys.exit(1)

	#-----------------------------------
	#	Processing request
	#-----------------------------------
	torrentFactory = TorrentFactory()
	torrents = torrentFactory.make(os.path.normpath(args.torrent))
	for torrent in torrents:
		torrent.copy()

if __name__ == "__main__":
	main()
