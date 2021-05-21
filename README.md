# capstone-topci-modelling-scraping

Simple Scraping Tool in Refinitiv for Topic Modelling - Capstone S21

## How To Run

Install dependencies

```
pip install -r requirements.txt
```

Replace **cookie** in `config.py`

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
