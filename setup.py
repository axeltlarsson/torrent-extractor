#!/usr/bin/python3

"""setup.py: setuptools control"""


import re
from setuptools import setup

version = re.search('^__version__\s*=\s*"(.*)"',
	open('torrent_extracter/torrent_extracter.py').read(),
	re.M
	).group(1)

with open("README.md", "rb") as f:
	long_descr = f.read().decode("utf-8")

setup(
	name="torrent_extracter",
	packages=["torrent_extracter"],
	entry_points =  {
		"console_scripts": ['torrent_extracter = torrent_extracter.torrent_extracter:main']
	},
	version = version,
	description = "Torrent extracting script.",
	long_description = long_descr,
	author = "Axel Larsson",
	author_email = "mail@axellarsson.nu",
	url = "http.//axellarsson.nu",
	install_requires=['colorlog']
	)