#!/usr/bin/env python3
import io
from urllib import error as urllib_errors
import traceback
import json
import argparse
import feedparser
from Logger import Logger
import codes
import sys
from http import HTTPStatus
import time

'''
This script is part of Anime Manager.
https://github.com/anma-dev/Anime-Manager
'''

help_msg = "Queries a feed link and returns the result."
parser = argparse.ArgumentParser(description=help_msg)
parser.add_argument("-d",
                    "--debug",
                    action='store_true',
                    help="enable debug output")
parser.add_argument("--link", type=str, help="feed link")
parser.add_argument("--etag", type=str, help="etag")
parser.add_argument("--modified", type=str, help="last updated date")
parser.add_argument("--ttl", type=int, help="feed ttl in minutes")
parser.add_argument("--ttl-update", type=int, help="last feed ttl update time as epoch time")
args = parser.parse_args()

# feedparser.USER_AGENT = "Anime Manager/v0.6.9-alpha +https://github.com/anma-dev/Anime-Manager"

logger = Logger(file="get_feed.log",
                debug=args.debug,
                log_name="get_feed").log
try:
    if args.ttl != 0 and args.ttl_update != 0:
        ttl_delta_min = (time.time() - args.ttl_update) / 60
        if (ttl_delta_min < args.ttl):
            logger.info("Hit the TTL limit.")
            sys.exit(0)
    parsed_link = io.StringIO(args.link).getvalue()
    if args.etag != 0:
        feed_content = feedparser.parse(parsed_link, etag=args.etag)
    elif args.modified != 0:
        feed_content = feedparser.parse(parsed_link, modified=args.modified)
    else:
        feed_content = feedparser.parse(parsed_link)
    # in this order
    if feed_content.bozo:
        if hasattr(feed_content, 'bozo_exception'):
            raise feed_content.bozo_exception
        else:
            err_msg = "The feed contains non-well-formed content."
            raise AssertionError(err_msg)
    if feed_content.status == HTTPStatus.NOT_MODIFIED:
        logger.info("Not modified")
        sys.exit(0)

    # if not hasattr(feed_content, 'etag') and not hasattr(feed_content, 'updated'):
    #     err_msg = "Server replied with no etag and updated date."
    #     raise AssertionError(err_msg)
except AssertionError as err:
    err_msg = json.dumps({
        "am_ret_code": codes.BAD_FEED,
        "am_ret_msg": f"{err}"
    })
    logger.error(err_msg)
    print(err_msg)
    sys.exit(0)  # code 0 to not trigger the main script
except (urllib_errors.URLError, urllib_errors.HTTPError) as err:
    logger.error(traceback.format_exc())
    err_msg = json.dumps({
        "am_ret_code": codes.CONN_ISSUE,
        "am_ret_msg": f"An error occurred while requesting the feed."
    })
    print(err_msg)
    sys.exit(0)  # code 0 to not trigger the main script
except Exception as err:
    logger.error(traceback.format_exc())
    err_msg = json.dumps({
        "am_ret_code": codes.UNKNOWN,
        "am_ret_msg": f"An unknown error occurred."
    })
    print(err_msg)
    sys.exit(0)  # code 0 to not trigger the main script
else:
    print(json.dumps(feed_content, ensure_ascii=False))
