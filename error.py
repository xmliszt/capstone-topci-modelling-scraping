import csv
import os

# Record error companies in CSV for re-run


def write_error(category, error_universe, error_reason):
    if not os.path.exists("meta"):
        os.mkdir("meta")

    if not os.path.exists(os.path.join("meta", category)):
        os.mkdir(os.path.join("meta", category))

    with open("meta/{}/error.csv".format(category), "a", encoding="utf-8", newline="") as fh:
        csv_writer = csv.writer(fh)
        csv_writer.writerow([error_universe, error_reason])
