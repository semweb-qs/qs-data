import csv
import requests
import time
import json
from urllib.parse import quote

PREFIX_URL = "http://www.wikidata.org/entity/"

memoization = dict()

def get_search_url(query):
    query=quote(query)
    return f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={query}&format=json&errorformat=plaintext&language=en&uselang=en&type=item"

def checkpoint(n, semweb_data):
    with open('semweb-data-003.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        for i in range(n):
            writer.writerow(semweb_data[i])

    with open("002_memoization.json", "w") as outfile:
        json.dump(memoization, outfile)

def main():
    semweb_data = []
    with open('semweb-data-002.csv') as csvfile:
        semweb_data = list(csv.reader(csvfile))
    n = len(semweb_data)
    semweb_data[0].append('wikidata_entity')
    tot_failed = 943
    failed = 0
    ok = 0
    for i in range(1, n):
        id = semweb_data[i][-1]
        qs_id = semweb_data[i][4].split('/')[-1]
        if(id == ""):

            try:
                semweb_data[i][-1] = memoization[qs_id][0]
                print("skipped")
                print(f"Processing {ok}/{tot_failed}")
                ok += 1
                continue
            except:
                pass

            tmp_data = semweb_data[i][0].split(' ')
            while(True):
                try:
                    api_url = get_search_url(' '.join(tmp_data))
                    response = requests.get(api_url).json()
                    first_result = response['search'][0]
                    semweb_data[i][-1] = f"{PREFIX_URL}{first_result['id']}"
                    ok += 1
                    # print(f"Got {first_result} as {semweb_data[i][0]}")
                    print(f"Processing {ok}/{tot_failed}")
                    memoization[qs_id] = [semweb_data[i][-1], first_result]
                    checkpoint(n, semweb_data)
                    time.sleep(1)
                    break
                except:
                    semweb_data[i][-1] = ""
                    tmp_data = tmp_data[0:-1]
                    if(len(tmp_data) == 0):
                        print("failed ", semweb_data[i])
                        failed += 1
                        break
    print(f"{failed}/{n}")
    checkpoint(n, semweb_data)
    with open("002_memoization.json", "w") as outfile:
        json.dump(memoization, outfile)


if __name__ == '__main__':
    main()
