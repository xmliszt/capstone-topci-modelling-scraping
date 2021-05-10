import time
import sys
import requests
import json
import os
from formula import FORMULAS
from config import COOKIE
from tqdm import tqdm


def scrape(universe):

    formulas = FORMULAS.copy()

    if universe == "":
        print("Please provide company ID (universe)!")
        exit(1)

    if "@RIC" not in universe:
        universe += "@RIC"

    print("Start scraping for {}".format(universe))

    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.path.exists("json"):
        os.mkdir("json")

    formulas.extend([
        "AddSource=True",
        "Period=FY0:FY-6"
    ])

    request_payload = {
        "Entity": {
            "E": "ADC",
            "W": {
                "Formulas": formulas,
                "Output": "la, allcols",
                "ProductID": "ESG:UNITY",
                "Universe": [
                    universe
                ]
            }
        }
    }

    headers = {
        "Cookie": COOKIE,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Upgrade-Insecure-Requests": "1",
        "Sec-GPC": "1",
        "DNT": "1",
        "Referer": "https://apac1.apps.cp.thomsonreuters.com/Apps/EnvtSocGov/3.6.12/",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Content-Type": "application/json; charset=UTF-8",
        "Connection": "keep-alive",
        "X-Tr-ApplicationId": "EnvtSocGov",
        "X-Tr-ShowBackendError": "true",
        "X-Tr-TransactionId": "bbb67640-1ed5-45fe-9b43-8d2d37495038",
        "X-Tr-UseCache": "true",
        "Host": "apac1.apps.cp.thomsonreuters.com"
    }

    start_time = time.time()

    if os.path.exists("json/{}.json".format(universe)):
        with open("json/{}.json".format(universe), "r", encoding="utf-8") as fp:
            data = json.load(fp)
    else:
        response = requests.post(
            "https://apac1.apps.cp.thomsonreuters.com/apps/udf/msf/", data=json.dumps(request_payload), headers=headers)

        if response.status_code != 200:
            print("ERROR: ", response.content)

        try:
            data = response.json()
        except Exception:
            print("ERROR: unable to fetch data! Please login and grab the latest cookie!")
            exit(1)

        with open("json/{}.json".format(universe), "w", encoding="utf-8") as fp:
            json.dump(data, fp)

    results = data['r']

    if len(results) <= 1:
        print("NO DATA FOR {}".format(universe))
        print(data)
        pass

    else:
        prev_year = None
        offset = 0  # account for duplicated year data
        for idx in tqdm(range(1, len(results)), desc="Processing formulas..."):
            v = results[idx]["v"]
            year = v[5].get("___MSFVALUE", 0)
            if year == 0:
                continue
            if prev_year is not None and year == prev_year:
                offset += 1
                continue
            prev_year = year
            if len(v) <= 18:
                continue
            abstract = v[17].get("___MSFVALUE", None)
            if abstract is None or abstract == "English":
                abstract = v[18].get("___MSFVALUE", None)
            if abstract is None or abstract == "False":
                continue
            if len(abstract) < 2:
                continue
            abstract = abstract.replace(
                "\n", " ")

            topic_idx = (idx - offset - 1) // 7
            topic_name = formulas[:-2][topic_idx].split(".")[-1]
            topic_path = os.path.join(
                "data", topic_name)
            if not os.path.exists(topic_path):
                os.mkdir(topic_path)
            print(topic_name, idx, "offset:", offset)
            with open(topic_path+"/{}-{}.txt".format(year, universe), "w", encoding="utf-8") as fh:
                fh.write(abstract)

    print("Done scraping for {}".format(universe))

    elapsed = time.time() - start_time
    print("Took {} ms".format(elapsed*1000))

    formula = []


if __name__ == "__main__":
    universe = sys.argv[1]
    scrape(universe)
