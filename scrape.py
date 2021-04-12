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

    idx = 0
    for formula in tqdm(formulas[:-2], desc="Processing formulas..."):
        topic_name = formula.split(".")[-1]
        topic_path = os.path.join("data", topic_name)
        if not os.path.exists(topic_path):
            os.mkdir(topic_path)
        start = idx * 7 + 1
        end = start + 7
        for i in range(start, end):
            if len(results) <= i:
                continue

            abstract = results[i]["v"]
            year = results[i]["v"][5].get("___MSFVALUE", 0)
            if len(abstract) <= 17:
                continue
            abstract = abstract[17].get("___MSFVALUE", None)
            if abstract is None:
                continue
            if len(abstract) < 2:
                continue
            abstract = abstract.replace("\n", " ")

            with open(topic_path+"/{}-{}.txt".format(year, universe), "w", encoding="utf-8") as fh:
                fh.write(abstract)
        idx += 1

    print("Done scraping for {}".format(universe))

    elapsed = time.time() - start_time
    print("Took {} ms".format(elapsed*1000))

    formula = []


if __name__ == "__main__":
    universie = sys.argv[1]
    scrape(universe)
