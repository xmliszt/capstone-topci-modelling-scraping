import sys
import requests
import json
import os
from formula import FORMULAS
from tqdm import tqdm

if len(sys.argv) <= 1:
    print("Please provide company ID (universe)!")
    exit(1)
universe = sys.argv[1]

if "@RIC" not in universe:
    universe += "@RIC"

FORMULAS.extend([
    "AddSource=True",
    "Period=FY0:FY-6"
])

request_payload = {
    "Entity": {
        "E": "ADC",
        "W": {
            "Formulas": FORMULAS,
            "Output": "la, allcols",
            "ProductID": "ESG:UNITY",
            "Universe": [
                universe
            ]
        }
    }
}

cookie = "traacRef={%22initial-referring-domain%22:%22apac1.apps.cp.thomsonreuters.com%22%2C%22initial-referrer%22:%22https://apac1.apps.cp.thomsonreuters.com/web/Apps/Homepage/?locale=en-US%22}; tid=817a1c17-afab-44c7-c4cc-bd0928c48f56; BIGipServerDACT-ERPCPRP-80=2811341066.20480.0000; userId=GESG1-97598; enableFeature=; disableFeature=; CSS=auto; trace=; BIGipServerHDCP-DATACLOUD-VIP-1080=1236400394.45845.0000; SAFFINITY=FE85A0BBB80E85289056D118FC889165; signBackUrl=https%3A%2F%2Fapac1.apps.cp.thomsonreuters.com%2Fweb%2FApps%2FCorp; iPlanetDirectoryPro=AQIC5wM2LY4SfcxNxyaUrMck0PXDW506chh3JX%2FTynw3W%2B0%3D%40AAJTSQACMzAAAlNLABQtMjc2MDg0MTQ3NTE4MzAzMjA4NAACUzEAAjI0%23; sessionId=f5a8b6f2-4b2b-4a69-88f8-d55d8f134914; sharedSessionStartTime=1617959907217"

headers = {
    "Cookie": cookie,
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


response = requests.post(
    "https://apac1.apps.cp.thomsonreuters.com/apps/udf/msf/", data=json.dumps(request_payload), headers=headers)

data = response.json()

if response.status_code != 200:
    print("ERROR: ", response.content)

# with open(os.path.join("json", json_filename), "w") as f:
#     json.dump(data, f)

results = data['r']

idx = 0
for formula in tqdm(FORMULAS[:-2], desc="Processing formulas..."):
    topic_name = formula.split(".")[-1]
    topic_path = os.path.join("data", topic_name)
    if not os.path.exists(topic_path):
        os.mkdir(topic_path)
    start = idx * 8 if idx > 0 else 1
    end = start + 7
    count = 1
    for i in range(start, end+1):
        if len(results) <= i:
            continue
        abstract = results[i]["v"]
        if len(abstract) <= 17:
            continue
        abstract = abstract[17].get("___MSFVALUE", None)
        if abstract is None:
            continue
        if len(abstract) < 2:
            continue
        abstract = abstract.replace("\n", " ")

        with open(topic_path+"/{}.txt".format(count), "w", encoding="utf-8") as fh:
            fh.write(abstract)
        count += 1
    idx += 1

print("Done scraping for {}".format(universe))
