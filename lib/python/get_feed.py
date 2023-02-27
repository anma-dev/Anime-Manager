#!/usr/bin/env python3
import io
import json
import argparse
import feedparser
from Logger import Logger
import codes
import sys
from http import HTTPStatus

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
args = parser.parse_args()

# feedparser.USER_AGENT = "Anime Manager/v0.6.9-alpha +https://github.com/anma-dev/Anime-Manager"

logger = Logger(file="get_feed.log",
                debug=args.debug,
                log_name="get_feed").log
try:
    error = False
    parsed_link = io.StringIO(args.link).getvalue()

    if args.etag != 0:
        feed_content = feedparser.parse(parsed_link, etag=args.etag)
    elif args.modified != 0:
        feed_content = feedparser.parse(parsed_link, modified=args.modified)
    else:
        feed_content = feedparser.parse(parsed_link)

    if feed_content.status == HTTPStatus.NOT_MODIFIED:
        logger.info("Not modified")
        sys.exit(0)

    if feed_content.bozo:
        error = True
        err_msg = "The feed contains non-well-formed content."
        logger.error(err_msg)
    if feed_content.status != HTTPStatus.OK:
        error = True
        err_msg = f"Unable to get feed content. Status code {feed_content.status}."
    if not feed_content.etag and not feed_content.updated_parsed:
        error = True
        err_msg = "Unable to operate. Feed server returned no etag and last-modified date."
    if error:
        print(json.dumps({
            "am_ret_code": codes.BAD_FEED,
            "am_ret_msg": err_msg
        }))
        sys.exit(0)  # code 0 to not trigger the main script
except Exception as err:
    logger.error(err)
    sys.exit(1)
else:
    print(json.dumps(feed_content, ensure_ascii=False))
