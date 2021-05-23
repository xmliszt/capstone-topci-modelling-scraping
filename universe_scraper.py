import requests
import bs4

# paths
# file containing the full list of company names
companies_csv_path = "ListEsgCompaniesName.txt"
# split_company_csv = "original_"  # prefix for grouping companies into smaller sizes

found_file = "processed.txt"
not_found_file = "unprocessed.txt"

# arrays
COMPANIES = []
CANNOT_FIND = []
STOCK_TICKS_TEMP = []
STOCK_TICKS = []

# global variables
SEARCH_URL = "https://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&sortBy=&dateRange=&search="
LIMIT = 1000


def write_txt(path_to_file, arr):
    with open(path_to_file, "w") as f:
        while True:
            comp = arr.pop(0)
            if len(arr) == 0:
                f.write(comp)
                break
            else:
                f.write(comp + "\n")


def read_unprocessed_and_edit(path_to_file):
    with open(path_to_file, "r", encoding="utf-8-sig") as f:
        while True:
            row = f.readline().rstrip().split()
            if row == []:
                break
            if len(row) == 1:
                COMPANIES.append(" ".join(row))
            elif row.__contains__("DEAD"):
                index = row.index("DEAD")
                line = row[:index]
                COMPANIES.append(" ".join(line))
            else:
                COMPANIES.append(" ".join(row))


# 1 read the given company list
read_unprocessed_and_edit(companies_csv_path)

counter = -1
found_seq = 1
not_found_seq = 1

# 2 make queries
for i in COMPANIES:
    print(i)
    search_url = SEARCH_URL + i
    res = requests.get(search_url)

    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    results = soup.find(id='content')
    elems = results.find_all(
        'table', class_='search-table-data')  # 0 if nothing

    counter += 1

    # nothing found
    if len(elems) == 0:
        CANNOT_FIND.append(i)
        print("counter: {}, type: {}".format(counter, "failed"))
        continue

    for ele in elems:  # find 1 table
        counts = 2
        for j in ele:
            if j == '\n':
                continue
            lst = list(j.strings)
            STOCK_TICKS_TEMP.append(lst[3])
            counts -= 1
            if counts == 0:
                break
    print("counter: {}, type: {}".format(counter, "passed"))

# 3 process all stock ticks
for i in STOCK_TICKS_TEMP:
    if i != "Symbol":
        STOCK_TICKS.append(i)

# 4 save to files
write_txt(found_file, STOCK_TICKS)
write_txt(not_found_file, CANNOT_FIND)

print("done")
