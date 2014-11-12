#!/usr/bin/python3
from settings import Settings
import re, os, rarfile, shutil
from utils import debug

class TorrentFactory(object):
	""" 
	Generates object(s) representing films or tv series from a string.
	"""

	# Returns a tuple of (tv series name, season #) if *match_string* matches TV series pattern
	def __match_tv_series(self, match_string):
		tv_show = re.search(r'(^[\w\.\s]+)-*[\s\.](?:(?:(?:S|Season)(?:\w|\S)(\d{1,2}))|(?:(\d{1,2})x\d\d))', match_string, re.IGNORECASE)
		if tv_show and not re.search(r'.*sample.*', match_string, re.IGNORECASE):
			name = tv_show.group(1).replace(".", " ").replace("_", " ").strip()
			season = tv_show.group(2) or tv_show.group(3) # The season number is group 2, or 3 if season pack or form sxep
			return (name, 'Season ' + season.lstrip("0"))

	# Returns title of film if *match_string* matches film pattern
	def __match_film(self, match_string):
		film = re.search(r'^(?:((?:\w+[\s\.-]+)+)\d{4}[\.\s])', match_string, re.IGNORECASE)
		if film and not re.search(r'.*sample.*', match_string, re.IGNORECASE):
			return film.group(1).replace(".", " ").strip()

	""" 
	Returns either a TV series, Film or RarTorrent object depending on *match_string*
 
	@param match_string - the string to match regex against
	@param file_path - the file path of the presumptive torrent object
	@param rarinfo (optional) - RarInfo object of rar file
	@param rarfile (optional) - RarFile object containing the RarInfo *rarinfo* object
	@return a Torrent object, if applicable
	"""
	def __make_torrent(self, match_string, file_path, rarinfo=None, rarfile=None):
		torrent = None
		match_tv = self.__match_tv_series(match_string)
		if match_tv:
			debug(match_string + " is a TV series", Settings.VERBOSE)
			torrent = TvEpisode(match_tv, file_path)
		
		match_film = self.__match_film(match_string)
		if not match_tv and match_film:
			debug(match_string + " is a film", Settings.VERBOSE)
			torrent = Film(match_film, file_path)

		if torrent and rarinfo:
			return RarTorrent(torrent, file_path, rarinfo, rarfile)
		elif torrent:
			return torrent

	"""
	Starter method for __make_recursive,
	returns a list of applicable Torrents found in *file_path*
	
	@param file_path - the path to look for applicable, presumptive Torrent objects
	"""		
	def make(self, file_path):
		torrents = []
		self.__make_recursive(file_path, torrents)
		return torrents

	""" 
	Recursive method that recursively searches *file_path* for applicable, presumptive
	Torrent objects and saves them in the *torrents* list
	
	@param file_path - the file path to explore
	@param torrents - the list to store Torrent objects in
	"""
	def __make_recursive(self, file_path, torrents):
		file_path = os.path.abspath(file_path)
		if not os.path.exists(file_path):
			raise FileNotFoundError('The path: ' + file_path + ' does not exist.')

		basename = os.path.basename(file_path)
		dirname = os.path.dirname(file_path)

		if os.path.isfile(file_path):
			parent_folder = os.path.basename(dirname)

			if self.__has_ok_extension(basename): # base case
				torrent = self.__make_torrent(parent_folder, file_path)
				if torrent:
					torrents.append(torrent)
				else:
					debug(parent_folder + " is neither a film nor a TV series", Settings.VERBOSE)
					debug("Trying with basename instead: " + basename, Settings.VERBOSE)
					torrent = self.__make_torrent(basename, file_path)
					if torrent:
						torrents.append(torrent)
		
			elif self.__is_rarfile(file_path):
				try:
					rar = rarfile.RarFile(file_path)
					for rarinfo in rar.infolist():
						if self.__has_ok_extension(rarinfo.filename):
							torrent = self.__make_torrent(parent_folder, file_path, rarinfo, rar)
							if torrent:
								torrents.append(torrent)
				except rarfile.NeedFirstVolume as e: # Fall som r'.part\d\d.rar' där bara r'.part01.rar' fungerar.
					pass
				except Exception as e:
					debug(str(e), Settings.QUIET)

		elif os.path.isdir(file_path):
			filenames = os.listdir(file_path)
			for file_name in filenames:
				self.__make_recursive(os.path.join(dirname, basename, file_name), torrents)

	# Returns true if *file_path*'s extension is acceptable according to the ok_extensions list in Settings
	# and is not a sample file
	def __has_ok_extension(self, match_string):
		extension = os.path.splitext(match_string)[1]
		return extension in Settings.ok_extensions and not re.search(r'.*sample.*', match_string, re.IGNORECASE)

	# Returns true if *file_path* has extension '.rar' AND is a rar file according to rarfile.is_rarfile
	def __is_rarfile(self, file_path):
		return os.path.splitext(file_path)[1] == '.rar' and rarfile.is_rarfile(file_path)

class Torrent(object):
	"""
	Represents a file to be either copied or extracted to a destination as set in Settings
	"""
	def __init__(self, file_path):
		self.file_path = file_path

	def __eq__(self, other):
		return (isinstance(other, self.__class__) and self.__dict__ == other.__dict__)

	def __ne__(self, other):
		return not self.__eq__(other)

	def copy(self):
		if not os.path.exists(self.destination):
			os.makedirs(self.destination)
		if not os.path.exists(os.path.join(self.destination, os.path.basename(self.file_path))):
			debug("* {0:12} {1:110}{2:10}{3:<}".format("Copying:", os.path.basename(self.file_path), "==>", self.destination), Settings.NORMAL)
			try:
				shutil.copy(self.file_path, self.destination)
			except OSError as e:
				debug(str(e), Settings.QUIET)
		else:
			debug(os.path.join(self.destination, os.path.basename(self.file_path)) + " already exists, skipping.", Settings.VERBOSE)

class TvEpisode(Torrent):
	"""
	Represents a file from a Tv series, usually an episode
	"""

	def __init__(self, title_season, file_path):
		Torrent.__init__(self, file_path)
		self.title_season = title_season # (title, season)
		self.destination = os.path.join(Settings().tv_path, self.title_season[0], self.title_season[1])

	def __str__(self):
		return str(self.title_season) + " " + self.file_path

class Film(Torrent):
	"""
	Represents films.
	"""

	def __init__(self, title, file_path):
		Torrent.__init__(self, file_path)
		self.title = title
		self.destination = os.path.join(Settings().film_path, title)

	def __str__(self):
		return self.title + " " + self.file_path

class RarTorrent(Torrent):
	"""
	Represents Torrent objects archived within a rar file.
	"""

	def __init__(self, torrent, file_path, rarinfo, rarfile):
		self.torrent = torrent
		self.rarinfo = rarinfo
		self.rarfile = rarfile
		Torrent.__init__(self, file_path)

	def __str__(self):
		return str(self.torrent) + " " + str(self.rarinfo.filename)

	def copy(self):
		if not os.path.exists(self.torrent.destination):
			os.makedirs(self.torrent.destination)

		if not os.path.exists(os.path.join(self.torrent.destination, self.rarinfo.filename)):
			debug("* {0:12} {1:110}{2:10}{3:<}".format("Extracting:", self.rarinfo.filename, "==>", self.torrent.destination), Settings.NORMAL)
			self.rarfile.extract(self.rarinfo, self.torrent.destination)
		else:
			debug(os.path.join(self.torrent.file_path, self.torrent.destination) + " already exists, skipping.", Settings.VERBOSE)
