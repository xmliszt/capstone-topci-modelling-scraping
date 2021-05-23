# capstone-topci-modelling-scraping

Simple Scraping Tool in Refinitiv for Topic Modelling - Capstone S21

## How To Run

Install dependencies

```
pip install -r requirements.txt
```

Replace **cookie** in `config.py`

### Scraping Universes

You need a text file containing the company's label ID (i.e. "universe") per line. We have a script that is used to scrape the universes given the company's names in a CSV file. Use `universe_scraper.py` to scrape the universes. Change `companies_csv_path` to your file that contains a list of company names.

```bash
python universe_scraper.py
```

The output files are defined in the python script as well, you can change it to your own preferred filename.

```python
found_file = "processed.txt"
not_found_file = "unprocessed.txt"
```

### Single Universe

Assume the company handle is "AAPL.O"

Choose a category first from "environment", "social", "governance" for the first argument

```
python scrape.py environment AAPL.O
```

This will create topics under `data/` folder and put pure text abstract inside

### Multiple Universes

Second argument will be the path to a txt file in which each line is a universe

```
python main.py social src/file.txt
```

`file.txt` containing company universe (ID) line by line like this:

```
AMRK.OQ
AAK.ST
AALB.AS
AAON.O
...
```

## Error

Companies result in error will all be put under `error.csv` file under `meta/` folder.
