#!/usr/bin/env python3
import argparse
import traceback
import re
import json
import subprocess
from shlex import split
import anitopy
from Logger import Logger
import codes
from utils import normalize_fragment, extract_episode, normalize_title

'''
This script is part of Anime Manager.
https://github.com/anma-dev/Anime-Manager
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
# reduce title when ampersand is present
# 'foo & bar with baz' => 'foo & bar'
match = re.match(
    "(?:[a-zA-Z0-9]*[^a-zA-Z ]*)*\s&\s(?:[a-zA-Z0-9]*[^a-zA-Z ]*)*", args.title)
if match:
    args.synonyms.append(match[0])
    args.synonyms.append(match[0].replace("&", "and"))
all_titles = [] + args.synonyms
all_titles.append(args.title)
# remove empty values
all_titles = [x for x in all_titles if len(x) != 0]

logger = Logger(file="file_extractor.log",
                debug=args.debug,
                log_name="file_extractor").log

webtorrent_timeout = 20
match = False
video_ext = (".webm", ".mkv", ".flv", ".avi", ".mov", ".wmv", ".mp4", ".m4p",
             ".m4v", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".m2v", ".3gp",
             ".3g2")
match_file_index = codes.CODE_FILE_SEL
video_res = []


def parseEpisode(ep: str):
    # remove non digit characters
    ep = re.sub("[^\d]", "", ep)
    ep = float(ep)
    return ep


def split_filename(f: str):
    return f.split(" - ")


def get_match_index():
    # select the first match by default
    match_index = 0
    """
    Try to find a title match and prioritize it.
    This is useful for example when some uploader bundles 
    stuff that a user did not request but is still a match
    by episode.
    It will not remove matches.
    """
    for index, match_file in enumerate(video_res):
        title = match_file["anime_title"]
        for x in all_titles:
            if re.findall(f"{normalize_title(x)}", normalize_title(title)):
                return index
    return match_index


def validateEpisode(parsed_title: object):
    if ("episode_number" in parsed_title):
        if type(parsed_title["episode_number"]) == list:
            ep_range_start = parseEpisode(
                parsed_title["episode_number"][0])
            ep_range_end = parseEpisode(
                parsed_title["episode_number"][1])
            if (args.episode >= ep_range_start
                    and args.episode <= ep_range_end):
                parsed_title["file_name"] = filename_og
                video_res.append(parsed_title)
                return True
        elif (args.episode == parseEpisode(
                parsed_title["episode_number"])):
            parsed_title["file_name"] = filename_og
            video_res.append(parsed_title)
            return True
    logger.error("Invalid parse.")
    return False


try:
    command = split(
        f"node lib/javascript/webtorrent-cli/bin/cmd.js download {args.magnet_link} -s -q"
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
        filename = normalize_fragment(filename)
        if args.type == "movie":
            video_res.append(anitopy.parse(filename_og))
        if args.type == "ova":
            if "ova" in normalize_title(filename):
                video_res.append(anitopy.parse(filename_og))
        else:
            """
            Match only the episode number because it might be the case
            that some uploader did not name the files with the anime 
            title or synonyms but would still be a match.
            """
            parsed_anime = extract_episode(filename)
            if not validateEpisode(parsed_anime):
                for fragment in split_filename(filename):
                    parsed_anime = extract_episode(fragment)
                    if not validateEpisode(fragment):
                        parsed_anime = extract_episode(
                            normalize_fragment(fragment))
                        if validateEpisode(fragment):
                            break
                    else:
                        break


except Exception as e:
    logger.error(traceback.format_exc())
    match_file_index = codes.RET_CODE_FATAL_ERROR
    res = f"None////None////{match_file_index}"
else:
    if len(video_res) == 0:
        msg = [
            f"No filename match for ",
            f"-     title: {args.title}",
            f"-     synonyms: {args.synonyms}",
            f"-     magnet link: {args.magnet_link}",
            f"-     episode: {args.episode}", f"-     type: {args.type}"
        ]
        logger.info("\n".join(msg))
        comp_res = '\\n'.join(video_res)
        match_file_index = codes.RET_CODE_CONTENT_MISMATCH
        res = f"None////None////{match_file_index}"
    else:
        video_res_index = get_match_index()
        match_file_index = int(re.findall(
            "^(\d+)\s+.*", video_res[video_res_index]["file_name"])[0])
        parsed_title_res = video_res[video_res_index]
        comp_res = '\\n'.join(p["file_name"] for p in video_res)
        res = f"{json.dumps(parsed_title_res, ensure_ascii=False)}////{comp_res}////{match_file_index}"
print(res)
