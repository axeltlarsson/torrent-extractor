#!/usr/bin/python3
"""setup.py: setuptools control"""

import re
from setuptools import setup

version = re.search('^__version__\s*=\s*"(.*)"',
                    open('torrent_extractor/torrent_extractor.py').read(),
                    re.M).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="torrent-extractor",
    packages=["torrent_extractor"],
    entry_points={
        "console_scripts":
        ['torrent-extractor = torrent_extractor.torrent_extractor:main']
    },
    version=version,
    description="Torrent extracting script.",
    long_description=long_descr,
    author="Axel Larsson",
    author_email="mail@axellarsson.nu",
    url="http.//axellarsson.nu",
    install_requires=['colorlog'])
