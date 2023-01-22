#!/usr/bin/env python3
import argparse
import traceback
import re
import json
import subprocess
from shlex import split
import anitopy
import csv
from contextlib import suppress
from Logger import Logger
import return_codes as codes

'''
This script is part of Anime Manager.
https://github.com/anma-dev/Anime-Manage
'''

help_msg = "Looks up a file in a magnet link and returns its index."
parser = argparse.ArgumentParser(description=help_msg)

parser.add_argument("-d",
                    "--debug",
                    action='store_true',
                    help="enable debug output")
parser.add_argument("--magnet-link", type=str, help="magnet link")
parser.add_argument("--title", type=str, help="anime title")
parser.add_argument("--synonyms", type=str, help="anime synonyms")
parser.add_argument("--episode", type=int, help="an episode number")
parser.add_argument("--type",
                    type=str,
                    help="anime type (tv, ova, movie, etc)")

args = parser.parse_args()
args.episode = float(args.episode)
args.synonyms = args.synonyms.split(", ")
# generate more title synonyms for better matching
# replace ampersand symbols with their word
args.synonyms.append(args.title.replace("&", "and"))
all_titles = [] + args.synonyms
all_titles.append(args.title)

logger = Logger(file="get_torrent_fid.log",
                debug=args.debug,
                log_name="get_torrent_fid").log

sniffer = csv.Sniffer()
valid_delim = ' _.&+,|'
webtorrent_timeout = 20
match = False
video_ext = (".webm", ".mkv", ".flv", ".avi", ".mov", ".wmv", ".mp4", ".m4p",
             ".m4v", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".m2v", ".3gp",
             ".3g2")
error_code = -2
file_sel_code = -1
index = file_sel_code
video_res = []


def parseEpisode(ep: str):
    # remove non digit characters
    ep = re.sub("[^\d]", "", ep)
    ep = float(ep)
    return ep


def normalize_title(title: str):
    title = re.sub("[^a-zA-Z0-9]+", " ", title)
    return title.casefold()


try:
    command = split(
        f"node lib/webtorrent-cli/bin/cmd.js download {args.magnet_link} -s -q"
    )
    magnet_content = subprocess.run(command,
                                    stdout=subprocess.PIPE,
                                    shell=False,
                                    timeout=webtorrent_timeout,
                                    check=True)
    result = magnet_content.stdout.decode("utf-8").splitlines()
    result = [x for x in result if len(x) != 0]
    del result[0]
    del result[-3:]
    if len(result) == 0:
        raise AssertionError("Magnet link has no content.")
    for filename in result:
        filename_og = filename
        # removes the index number and data beyond the file extension
        filename = re.sub(r'(\.\w{3,4})\s+\(.*\)$', '\\1', filename)
        filename = re.sub(r'^\d+\s*', '', filename)
        if (not filename.endswith(video_ext)):
            continue
        if not any(normalize_title(x) in normalize_title(filename) for x in all_titles):
            continue
        parsed_title = anitopy.parse(filename)
        # print(normalize_title(filename))
        if args.type == "movie":
            if any(
                    normalize_title(x) in normalize_title(filename)
                    for x in args.title):
                video_res.append(filename_og)
        else:
            if not "episode_number" in parsed_title:
                tmp_delim = valid_delim
                # try to detect separator
                while not "episode_number" in parsed_title and len(
                        tmp_delim) > 0:
                    # the csv parser complains when it can't find a delimiter
                    with suppress(Exception):
                        dialect = sniffer.sniff(filename, delimiters=tmp_delim)
                    parsed_title = anitopy.parse(
                        filename, {'allowed_delimiters': dialect.delimiter})
                    # narrow down the valid delimiters
                    tmp_delim = tmp_delim[1:]
            if ("episode_number" in parsed_title
                    and "anime_title" in parsed_title):
                if type(parsed_title["episode_number"]) == list:
                    ep_range_start = parseEpisode(
                        parsed_title["episode_number"][0])
                    ep_range_end = parseEpisode(
                        parsed_title["episode_number"][1])
                    if (args.episode >= ep_range_start
                            and args.episode <= ep_range_end):
                        video_res.append(filename_og)
                elif (args.episode == parseEpisode(
                        parsed_title["episode_number"])):
                    video_res.append(filename_og)

except Exception as e:
    logger.error(traceback.format_exc())
    index = codes.RET_CODE_FATAL_ERROR
    res = f"None////None////{index}"
else:
    if len(video_res) == 0:
        msg = [
            f"No filename match for ",
            f"-     magnet link: {args.magnet_link}",
            f"-     episode: {args.episode}", f"-     type: {args.type}"
        ]
        logger.info("\n".join(msg))
        comp_res = '\\n'.join(video_res)
        index = codes.RET_CODE_CONTENT_MISMATCH
        res = f"None////None////{index}"
    else:
        # return index from first match
        index = int(re.findall("^(\d+)\s+.*", video_res[0])[0])
        comp_res = '\\n'.join(video_res)
        parsed_title_res = anitopy.parse(video_res[0])
        res = f"{json.dumps(parsed_title_res, ensure_ascii=False)}////{comp_res}////{index}"
print(res)
