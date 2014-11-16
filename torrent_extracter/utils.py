#!/usr/bin/python3

from .settings import Settings
# Prints *msg* if current verbosity setting is higher than *level*
def debug(msg, level=Settings.NORMAL):
	settings = Settings()
	if settings.verbosity >= level:
		print(msg)
