#!/usr/bin/env python3
import argparse
import anitopy

'''
This script is part of Anime Manager.
https://github.com/anma-dev/Anime-Manager
'''

help_msg = "Finds an anime title in a string."
parser = argparse.ArgumentParser(description=help_msg)
parser.add_argument("--title", type=str, help="anime title")
args = parser.parse_args()

print(anitopy.parse(args.title))
