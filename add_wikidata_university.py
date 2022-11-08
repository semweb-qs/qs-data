import csv


def main():
    semweb_data = []
    university_data = dict()
    with open('university.csv') as csvFile:
        tmp = list(csv.reader(csvFile))
        n = len(tmp)
        for i in range(1, n):
            # print(tmp[i][1], tmp[i][0])
            university_data[tmp[i][1]] = tmp[i][0]
    with open('semweb-data-000.csv') as csvfile:
        semweb_data = list(csv.reader(csvfile))
    n = len(semweb_data)
    semweb_data[0].append('wikidata_entity')
    failed = 0
    for i in range(1, n):
        id = semweb_data[i][4].split('/')[-1]

        try:
            wikidata = university_data[id]
            semweb_data[i].append(wikidata)
        except:
            failed += 1
            semweb_data[i].append("")

        # old = id
        # ok = 0
        # lewat = 0
        # while (True):
        #     try:
                # wikidata = university_data[id]
                # semweb_data[i].append(wikidata)
                # ok = 1
                # if(lewat != 0):
                #     print(f"{old} => {id}")
                # break
            # except:
            #     pass
            # lewat += 1
            # id = id[:-1]
            # if (id == ""): break
        # if(ok == 0): failed += 1


    print(f"{failed}/{n}")
    with open('semweb-data-001.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        for i in range(n):
            writer.writerow(semweb_data[i])


if __name__ == '__main__':
    main()
