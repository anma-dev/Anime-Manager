import sys
import os
import argparse
import logging
import traceback
import re
import json
from time import sleep
from NyaaPy.nyaa import Nyaa

help_msg = "Queries nyaa.si and returns the results."
parser = argparse.ArgumentParser(description=help_msg)

parser.add_argument("-d", "--debug", action='store_true',
                    help="enable debug output")
parser.add_argument("--title", type=str, help="filter by series title")
parser.add_argument("--episode", "--episode", type=int,
                    help="search for this episode")
parser.add_argument("--quality", type=int, help="filter by quality")
parser.add_argument("--show-type", type=str,
                    help="show type (tv, ova, movie, etc)")

args = parser.parse_args()
# print(vars(args))
# exit()

logfile = os.path.expanduser("~/.config/anime-manager/nyaa_search.log")
f = open(logfile, "a")
logger = logging.getLogger('nyaa_search')
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

# globals
nyaa = Nyaa()
# categories and subcategories
cat_anime = 1
subcat_music_video = 1
subcat_english_translated = 2
subcat_non_english_translated = 3
subcat_raw = 3

# filters
no_filter = 0
no_remakes = 1
trusted_only = 2

episode_format = f"0{args.episode}" if args.episode < 10 else args.episode
filter_trusted = no_filter
query_template_single_ep = f"{args.title}"
allowed_eps = ["tv", "ova"]

if (args.show_type.casefold() in allowed_eps):
    query_template_single_ep += f" {episode_format}"

query_template_batch_1 = f"\"{args.title}\" \"~\""
query_template_batch_2 = f"\"{args.title}\" batch"
query_last_resort = f"\"{args.title}\""
output_res = []
req_delay = 1


def search_nyaa(query: str, category: str, subcategory: str, filters: str):
    # print(query)
    global results
    results = nyaa.search(keyword=query, category=category,
                          subcategory=subcategory, filters=filters, sort="seeders")
    # print(results)
    if (len(results) > 0):
        for entry_raw in results:
            # print("found results")
            entry = entry_raw.__dict__
            # print(entry)
            if (int(entry["seeders"]) == 0):
                continue
            else:
                entry["name"] = f"{entry['name']} [S: {entry['seeders']} / L: {entry['leechers']}]"

            if entry["type"] == "default":
                entry["name"] = f"⚪️ {entry['name']}"
            elif entry["type"] == "remake":
                entry["name"] = f"🔴 {entry['name']}"
            elif entry["type"] == "trusted":
                entry["name"] = f"🟢 {entry['name']}"

            global parsed_entry
            # filter out batches that don't contain the episode
            batch_reg = rf"\(?(\d+)\s*\-\s*(\d+)\)?|(\d+)\s*~\s*(\d+)"
            global batch_interval
            batch_interval = re.findall(
                batch_reg, entry["name"], re.IGNORECASE)
            if (batch_interval):
                filtered = list(filter(None, batch_interval[0]))
                batch_range_start = int(filtered[0])
                batch_range_end = int(filtered[1])
                if (args.episode >= batch_range_start and args.episode <= batch_range_end):
                    output_res.append(entry)
            else:
                output_res.append(entry)


try:
    """
        First search for the episode itself
        Then search for batches twice with different patterns
        If we got no results from the previous requests, search
            anything that matches the series title
    """
    search_nyaa(
        query_template_batch_1, cat_anime, subcat_english_translated, filter_trusted)
    sleep(req_delay)
    search_nyaa(
        query_template_batch_2, cat_anime, subcat_english_translated, filter_trusted)
    sleep(req_delay)
    search_nyaa(
        query_template_single_ep, cat_anime, subcat_english_translated, filter_trusted)
    output_res = [dict(t) for t in {tuple(d.items()) for d in output_res}]
except Exception as e:
    logger.error(traceback.format_exc())
    print("-2")
else:
    if (len(output_res) == 0):
        search_nyaa(query_last_resort, cat_anime,
                    subcat_english_translated, filter_trusted)
    if (len(output_res) == 0):
        msg = [
            "----------------",
            f"ERROR: No results found or no match for file input: ",
            f"-     args.title: {args.title}",
            f"-     args.episode: {args.episode}",
            f"-     type: {args.show_type}",
            f"-     query 1: {query_template_batch_1}",
            f"-     query 2: {query_template_batch_2}",
            f"-     query 3: {query_template_single_ep}",
            f"-     results: {results}"
            "----------------"
        ]
        logger.error("\n".join(msg))
        print("-1")
        exit()
    for entry in output_res:
        print(json.dumps(entry, ensure_ascii=False))
