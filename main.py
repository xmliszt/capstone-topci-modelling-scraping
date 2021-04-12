'''
Take in a list of company universie (ID) in a txt file (one line one universe) and perform scraping for each of the universe
'''

from scrape import scrape
import sys

if len(sys.argv) <= 1:
    print("Please provide src path")
    exit(1)

src_path = sys.argv[1]


with open(src_path, 'r', encoding='utf-8') as fh:
    lines = fh.readlines()
    for line in lines:
        universe = line.strip().strip("\n")
        scrape(universe)
