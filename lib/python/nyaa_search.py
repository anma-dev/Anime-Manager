#!/usr/bin/env python3
import argparse
import traceback
import re
import json
import NyaaPy
from NyaaPy.nyaa import Nyaa
from NyaaPy import torrent
from NyaaPy import utils
from Logger import Logger
import requests
from http import HTTPStatus
import codes
from decorators import exp_back_off
from circuit_breaker import CBreaker
c_breaker = CBreaker()


if (NyaaPy.__version__ == "0.6.3"):
    # monkey patch fix the issue
    # https://github.com/JuanjoSalvador/NyaaPy/issues/68
    def mp_nyaa_search(self, keyword, **kwargs):
        url = self.URL

        user = kwargs.get('user', None)
        category = kwargs.get('category', 0)
        subcategory = kwargs.get('subcategory', 0)
        filters = kwargs.get('filters', 0)
        page = kwargs.get('page', 0)

        if user:
            user_uri = f"user/{user}"
        else:
            user_uri = ""

        if page > 0:
            r = requests.get("{}/{}?f={}&c={}_{}&q={}&p={}".format(
                url, user_uri, filters, category, subcategory, keyword,
                page))
        else:
            r = requests.get("{}/{}?f={}&c={}_{}&q={}".format(
                url, user_uri, filters, category, subcategory, keyword))

        r.raise_for_status()

        json_data = utils.parse_nyaa(
            request_text=r.content,  # ! change
            limit=None,
            site=self.SITE
        )

        return torrent.json_to_class(json_data)

    Nyaa.search = mp_nyaa_search


'''
This script is part of Anime Manager.
https://github.com/anma-dev/Anime-Manager
'''

help_msg = "Queries nyaa.si and returns the results."
parser = argparse.ArgumentParser(description=help_msg)

parser.add_argument("-d",
                    "--debug",
                    action='store_true',
                    help="enable debug output")
parser.add_argument("--title", type=str, help="filter by series title")
parser.add_argument("--episode", type=int, help="search for this episode")
parser.add_argument("--quality", type=int, help="filter by quality")
parser.add_argument("--show-type",
                    type=str,
                    help="show type (tv, ova, movie, etc)")

args = parser.parse_args()

logger = Logger(file="nyaa_search.log",
                debug=args.debug,
                log_name="nyaa_search").log
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
query_template_default = f"{args.title}"
query_template_ep = f"{args.title} {args.episode}"
allowed_eps = ["movie"]

query_template_batch_1 = f"\"{args.title}\" \"~\""
query_template_batch_2 = f"\"{args.title}\" batch"
query_last_resort = f"\"{args.title}\""
match_res = []  # aggregated search results from all the queries


@exp_back_off(c_breaker=c_breaker, logger=logger)
def search_nyaa(query: str, category: str, subcategory: str, filters: str):
    global query_res
    try:
        query_res = nyaa.search(keyword=query,
                                category=category,
                                subcategory=subcategory,
                                filters=filters)
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        if (err.response.status_code == HTTPStatus.TOO_MANY_REQUESTS):
            # transient fault, retry request
            raise requests.exceptions.HTTPError(response=err.response)
        else:
            # service unavailable
            raise Exception(
                f"Nyaa.si service is unavailable. Status code: {err.response.status_code}.")
    except requests.exceptions.RequestException as err:
        logger.error(err)
        raise Exception(
            f"Nyaa.si service is unavailable. (Request exception).")
    except Exception as err:
        logger.error(err)
        return
    else:
        if (len(query_res) > 0):
            for entry_raw in query_res:
                entry = entry_raw.__dict__
                if (int(entry["seeders"]) == 0):
                    continue
                else:
                    entry["name"] = f"{entry['name']} [S: {entry['seeders']} / L: {entry['leechers']}]"
                if entry["type"] == "default":
                    entry["name"] = f"?????? {entry['name']}"
                elif entry["type"] == "remake":
                    entry["name"] = f"???? {entry['name']}"
                elif entry["type"] == "trusted":
                    entry["name"] = f"???? {entry['name']}"
                global parsed_entry
                # filter out batches that don't contain the episode
                batch_reg = r"\(?(\d+)\s*\-\s*(\d+)\)?|(\d+)\s*~\s*(\d+)"
                global batch_interval
                batch_interval = re.findall(batch_reg, entry["name"],
                                            re.IGNORECASE)
                if (batch_interval):
                    filtered = list(filter(None, batch_interval[0]))
                    batch_range_start = int(filtered[0])
                    batch_range_end = int(filtered[1])
                    if (args.episode >= batch_range_start
                            and args.episode <= batch_range_end):
                        match_res.append(entry)
                else:
                    match_res.append(entry)


try:
    """
        Search for the episode itself
        Search for batches twice with different patterns
        Finally search anything that matches the series title
    """
    search_nyaa(query_template_batch_1, cat_anime, subcat_english_translated,
                filter_trusted)
    search_nyaa(query_template_batch_2, cat_anime, subcat_english_translated,
                filter_trusted)
    search_nyaa(query_template_default, cat_anime, subcat_english_translated,
                filter_trusted)
    if (args.show_type.casefold() in allowed_eps):
        search_nyaa(query_template_ep, cat_anime, subcat_english_translated,
                    filter_trusted)
    # remove duplicates
    match_res = [dict(t) for t in {tuple(d.items()) for d in match_res}]
    if (len(match_res) == 0):
        msg = [
            "----------------",
            f"ERROR: No query_res found or no match for file input: ",
            f"-     title: {args.title}",
            f"-     episode: {args.episode}",
            f"-     type: {args.show_type}",
            f"-     query 1: {query_template_batch_1}",
            f"-     query 2: {query_template_batch_2}",
            f"-     query 3: {query_template_default}",
            "----------------"
        ]
        "\n".join(msg)
        raise AssertionError("Search returned no results.")
except AssertionError as err:
    logger.error(err)
    print(f"{err}////{codes.RET_CODE_NO_RESULTS}")
except Exception as err:
    logger.error(traceback.format_exc())
    logger.error(err)
    print(f"{err}////{codes.RET_CODE_FATAL_ERROR}")
else:
    for entry in match_res:
        print(json.dumps(entry, ensure_ascii=False))
