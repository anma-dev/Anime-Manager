from os import path, makedirs, environ
import sys
import logging

config_dir = path.expanduser("~/.config/anime-manager/log")


class Logger:
    '''
    Logging class for Anime Manager.
    https://github.com/anma-dev/Anime-Manager
    '''

    def __init__(self,
                 file='nyaa_default.log',
                 debug=False,
                 log_name='default'):
        # let environment override debug argument value
        if not debug:
            if environ.get("NYAA_DEBUG") and int(environ.get("NYAA_DEBUG")) == 1:
                debug = True
        if not path.isdir(config_dir):
            makedirs(config_dir)
        logfile = f"{config_dir}/{file}"
        self.log = logging.getLogger(log_name)
        self.log.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)
        if debug:
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setFormatter(formatter)
            self.log.addHandler(stderr_handler)
