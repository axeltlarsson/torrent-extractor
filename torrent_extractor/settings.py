#!/usr/bin/python3
"""torrent_extactor.settings: settings module used to store settings"""


class Settings:
    class __Settings:
        def __init__(self):
            self.tv_path = ""
            self.film_path = ""
            self.verbosity = 0
            self.dry_run = False

        def __str__(self):
            return repr(self)

    # List with supported extensions
    ok_extensions = ['.mkv', '.ts', '.avi', '.iso', '.srt', '.sub', '.mp4']

    # Instance variable for Singleton use
    instance = None

    def __new__(cls):
        if not Settings.instance:
            Settings.instance = Settings.__Settings()
        return Settings.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
