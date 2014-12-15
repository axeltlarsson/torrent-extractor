#!/usr/bin/python3
"""torrent_extracter.torrent_extracter: provides entry point main()."""

__version__ = "0.3"

import re
import sys
import argparse
import os
from .settings import Settings
from .torrent import TorrentFactory
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from colorlog import ColoredFormatter

# Handles the command line parsing and starts the process of extracting/copying
def main():
	#-----------------------------------
	#	Deal with args and settings
	#-----------------------------------
	parser = argparse.ArgumentParser(description="Intelligently copies/extracts films and tv series to respective target directories")
	parser.add_argument("-t", "--tv_path", help="path to destination folder for TV shows, default is /tmp/films")
	parser.add_argument("-f", "--film_path", help="path to destination folder for films, default is /tmp/tv_series")
	parser.add_argument("-d", "--debug", action="store_true", help="set this flag to prevent log files from being written and enable DEBUG-level output to console")
	parser.add_argument("-l", "--log_file", help="path to log file, default is ./torrent_extracter.log")
	parser.add_argument("torrent", help="the file path to the torrent to extract")
	args = parser.parse_args()

	settings = Settings()
	settings.tv_path = os.path.normpath(args.tv_path or "/tmp/tv_series")
	settings.film_path = os.path.normpath(args.film_path or "/tmp/films")
	log_file = os.path.normpath(args.log_file or "./torrent_extracter.log")

	#-----------------------------------
	#	Set up logging
	#-----------------------------------
	log = logging.getLogger("t_e")
	log.setLevel(logging.DEBUG) # let the handlers filter instead

	# Set up a console handler
	console_handler = StreamHandler(stream=sys.stdout)
	console_handler.setLevel(logging.DEBUG if args.debug else logging.INFO)
	#console_formatter = logging.Formatter(fmt='[{levelname:8}] {message}', 
	#	datefmt='%b %d %H:%M:%S', style="{")

	console_formatter = ColoredFormatter(
		"{log_color}[{levelname:8}]{reset} {message}", 
		datefmt='%b %d %H:%M:%S', 
		style="{",
		log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
    	}
	)
	console_handler.setFormatter(console_formatter)
	log.addHandler(console_handler)

	# Set up a file handler that also rotates the logs, unless of course debug mode is set, then we only log to console
	if not args.debug and os.access(os.path.dirname(os.path.abspath(log_file)), os.W_OK):
		file_handler = RotatingFileHandler(log_file, 
			maxBytes=30000, # gives about 220 lines before rotating
			backupCount=5, # keep 5 backups
			delay=True) # do not write the log file until first log message
		file_handler.setLevel(logging.DEBUG) # will log everything
		file_formatter = ColoredFormatter(
				'{log_color}{asctime} [{levelname:8}]{reset} {message}',
				datefmt='%b %d %H:%M:%S',
				style='{',
				log_colors={
		            'DEBUG':    'cyan',
		            'INFO':     'green',
		            'WARNING':  'yellow',
		            'ERROR':    'red',
		            'CRITICAL': 'red',
		    	}
		)
		file_handler.setFormatter(file_formatter)
		log.addHandler(file_handler)

	# Some extra checks on the arguments		
	if not os.path.exists(os.path.normpath(args.torrent)):
		log.critical(os.path.normpath(args.torrent) + " does not exist, exiting.")
		sys.exit(1)
	if not os.access(os.path.dirname(os.path.abspath(log_file)), os.W_OK):
		log.warning("No write permission to " + log_file + ", no log file will be written.")
	if not os.access(os.path.dirname(os.path.abspath(settings.tv_path)), os.W_OK):
		log.critical("No write permission to " + os.path.abspath(settings.tv_path) + ", exiting.")
		sys.exit(1)
	if not os.access(os.path.dirname(os.path.abspath(settings.film_path)), os.W_OK):
		log.critical("No write permission to " + os.path.abspath(settings.film_path) + ", exiting.")
		sys.exit(1)

	#-----------------------------------
	#	Processing request
	#-----------------------------------
	torrentFactory = TorrentFactory()
	torrents = torrentFactory.make(os.path.normpath(args.torrent))
	if not torrents:
		log.info("No torrents to unpack or extract found in " + os.path.normpath(args.torrent))
	for torrent in torrents:
		torrent.copy()

if __name__ == "__main__":
	main()
