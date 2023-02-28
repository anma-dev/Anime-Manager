#!/usr/bin/env python3
import sys
import argparse
import anitopy
import json
from Logger import Logger
from utils import normalize_fragment, extract_episode

'''
This script is part of Anime Manager.
https://github.com/anma-dev/Anime-Manager
'''

help_msg = "Extract and parse anime info from a string."
parser = argparse.ArgumentParser(description=help_msg)
parser.add_argument("-d",
                    "--debug",
                    action='store_true',
                    help="enable debug output")
parser.add_argument("--input", type=str,
                    help="a string containing information for an anime")
args = parser.parse_args()

logger = Logger(file="get_title.log",
                debug=args.debug,
                log_name="get_title").log

try:
    parsed_anime = anitopy.parse(normalize_fragment(args.input))
    if not "episode_number" in parsed_anime:
        parsed_anime = extract_episode(args.input)
except Exception as err:
    logger.error(err)
    sys.exit(0)
else:
    print(json.dumps(parsed_anime))
