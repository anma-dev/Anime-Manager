from os import path, makedirs
import sys
import logging

config_dir = path.expanduser("~/.config/anime-manager")


class Logger:
    '''
    Logging class for Anime Manager.
    https://github.com/anma-dev/Anime-Manager
    '''

    def __init__(self,
                 file='nyaa_default.log',
                 debug=False,
                 log_name='default'):
        if not path.isdir(config_dir):
            makedirs(config_dir)
        logfile = f"{config_dir}/{file}"
        f = open(logfile, "a")
        self.log = logging.getLogger(log_name)
        self.log.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)
        if debug:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.DEBUG)
            stdout_handler.setFormatter(formatter)
            self.log.addHandler(stdout_handler)
