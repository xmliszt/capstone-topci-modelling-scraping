'''
Take in a list of company universie (ID) in a txt file (one line one universe) and perform scraping for each of the universe
'''

from scrape import scrape
from error import write_error
import sys

CATS = ["environment", "social", "governance", "controversies"]

if len(sys.argv) <= 1:
    print("Please provide category: {} and src path".format(CATS))
    exit(1)

category = sys.argv[1]
src_path = sys.argv[2]

if category not in CATS:
    print("Please input valid category: {}".format(CATS))
    exit(1)

with open(src_path, 'r', encoding='utf-8') as fh:
    lines = fh.readlines()
    for line in lines:
        universe = line.strip().strip("\n")
        try:
            scrape(universe, category=category)
        except Exception as e:
            write_error(category, universe, str(e))
