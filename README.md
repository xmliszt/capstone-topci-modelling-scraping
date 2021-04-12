# capstone-topci-modelling-scraping

Scaping for Topic Modelling - Capstone S21

## How To Run

Replace **cookie**

Assume the company handle is "AAPL.O"

```
python scrape.py AAPL.O
```

This will create topics under `data/` folder and put pure text abstract inside

## Multiple universes

```
python main.py src/file.txt
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
