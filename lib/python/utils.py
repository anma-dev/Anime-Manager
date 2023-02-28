import re
from contextlib import suppress
import anitopy
import csv
sniffer = csv.Sniffer()

# for title to title comparison, not to use for parsing data
def normalize_title(fragment: str):
    fragment = re.sub("[^a-zA-Z0-9&]+", " ", fragment)
    fragment = fragment.casefold()
    return fragment

# used to parse data
def normalize_fragment(fragment: str):
    fragment = re.sub("(\d)-(\D)", "\\1 \\2", fragment)
    fragment = re.sub("(\d)\.(\d)", "\\1-\\2", fragment)
    return fragment

def extract_episode(fragment: str):
    valid_delimiters = ' _.&+,|'
    parsed_title = anitopy.parse(fragment)
    tmp_delim = valid_delimiters
    # try to detect separator
    while not "episode_number" in parsed_title and len(tmp_delim):
        # the csv parser complains when it can't find a delimiter
        with suppress(Exception):
            dialect = sniffer.sniff(
                fragment, delimiters=tmp_delim)
            parsed_title = anitopy.parse(
                fragment, {'allowed_delimiters': dialect.delimiter})
        # narrow down the valid delimiters
        tmp_delim = tmp_delim[1:]
    return parsed_title
