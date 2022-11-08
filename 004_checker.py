import csv
import requests
import time
import json
from urllib.parse import quote

PREFIX_URL = "http://www.wikidata.org/entity/"

def checkpoint(n, semweb_data):
    with open('semweb-data-005.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        for i in range(n):
            writer.writerow(semweb_data[i])

def main():
    semweb_data = []
    with open('semweb-data-004.csv') as csvfile:
        semweb_data = list(csv.reader(csvfile))
    all_university = set()

    with open('all_university.csv') as csvfile:
        tmp = list(csv.reader(csvfile))
        for j in range(1, len(tmp)):
            all_university.add(tmp[j][0])

    fixes = dict()
    with open('changer.csv') as csvfile:
        fixed = list(csv.reader(csvfile))
        for row in fixed:
            fixes[row[0]] = row[1]
    failed_id = set()
    n = len(semweb_data)
    failed = 0
    for i in range(1, n):
        id = semweb_data[i][-1]
        ujung = semweb_data[i][-1].split('/')[-1]
        if(id not in all_university):
            semweb_data[i][-1] = semweb_data[i][-1].replace(ujung, fixes[ujung])
        id = semweb_data[i][-1]
        if(id not in all_university):
            failed += 1
            print(semweb_data[i][0], semweb_data[i][-1])
    checkpoint(n, semweb_data)
    print(failed)

if __name__ == '__main__':
    main()
