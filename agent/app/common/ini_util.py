import configparser
from pathlib import Path


class IniUtilError(Exception):
    pass


class IniUtil:
    section = "HOST_INFO"

    def __init__(self, file_path: str):
        self.config = configparser.ConfigParser()
        self.file_path = file_path

    def load(self):
        try:
            self.config.read(self.file_path)
        except FileNotFoundError:
            Path(self.file_path).touch()
        except OSError as err:
            raise IniUtilError(f"ini file read err : {err}")

        if self.section not in self.config:
            self.config[self.section] = {}

    def read(self, key):
        if key not in self.config[self.section]:
            return 0

        return self.config[self.section][key]

    def add(self, key, value):
        if key is None or key == "":
            raise IniUtilError(f"key is invalid")

        self.config[self.section][key] = value

    def write(self):
        try:
            with open(self.file_path, 'w') as configfile:
                self.config.write(configfile)
        except OSError as err:
            IniUtilError(f"ini file write error : {err}")
