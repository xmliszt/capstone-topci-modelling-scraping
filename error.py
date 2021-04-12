import csv
import os

# Record error companies in CSV for re-run


def write_error(error_universe, error_reason):
    if not os.path.exists("meta"):
        os.mkdir("meta")

    with open("meta/error.csv", "a", encoding="utf-8", newline="") as fh:
        csv_writer = csv.writer(fh)
        csv_writer.writerow([error_universe, error_reason])
