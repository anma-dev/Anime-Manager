import sys
import os
import argparse
import logging
import traceback
import re
import json
import subprocess
from shlex import split
import anitopy
import csv
from contextlib import suppress

help_msg = "Looks up a file in a magnet link and returns its index."
parser = argparse.ArgumentParser(description=help_msg)

parser.add_argument("-d",
                    "--debug",
                    action='store_true',
                    help="enable debug output")
parser.add_argument("--magnet-link", type=str, help="magnet link")
parser.add_argument("--title", type=str, help="show title")
parser.add_argument("--episode", type=int, help="a series episode number")
parser.add_argument("--show-type",
                    type=str,
                    help="show type (tv, ova, movie, etc)")

args = parser.parse_args()
args.episode = float(args.episode)
args.title = args.title.split(", ")

logfile = os.path.expanduser("~/.config/anime-manager/get_torrent_fid.log")
f = open(logfile, "a")
logger = logging.getLogger('get_torrent_fid')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s')
file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
if args.debug:
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

sniffer = csv.Sniffer()
valid_delim = ' _.&+,|'
webtorrent_timeout = 60
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
    reg = rf"[^a-zA-Z0-9-_ \/!='+.$&%\"]"
    title = re.sub(reg, "", title, re.IGNORECASE)
    return title.casefold()


try:
    command = split(f"node lib/webtorrent-cli/bin/cmd.js download {args.magnet_link} -s -q")
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
        parsed_title = anitopy.parse(filename)
        # print(filename)
        if args.show_type == "movie":
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
                    if (not args.episode >= ep_range_start
                            and not args.episode <= ep_range_end):
                        continue
                elif (not args.episode == parseEpisode(
                        parsed_title["episode_number"])):
                    continue
                if any(
                        normalize_title(x) in normalize_title(filename)
                        for x in args.title):
                    video_res.append(filename_og)

except Exception as e:
    logger.error(traceback.format_exc())
    index = -2
    res = f"None////None////{index}"
else:
    if len(video_res) == 0:
        msg = [
            f"No filename match for ",
            f"-     magnet link: {args.magnet_link}",
            f"-     episode: {args.episode}", f"-     type: {args.show_type}"
        ]
        logger.info("\n".join(msg))
        comp_res = '\\n'.join(video_res)
        index = -1
        res = f"None////None////{index}"
    else:
        # return index from first match
        index = int(re.findall("^(\d+)\s+.*", video_res[0])[0])
        comp_res = '\\n'.join(video_res)
        parsed_title_res = anitopy.parse(video_res[0])
        res = f"{json.dumps(parsed_title_res, ensure_ascii=False)}////{comp_res}////{index}"
print(res)
