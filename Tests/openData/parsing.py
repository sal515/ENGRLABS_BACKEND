import csv
import json

csvFilePath = "labSchedulesRevised.csv"
jsonFilePath = "openDataParsing.json"

data = {}
with open(csvFilePath) as csv_file:
    csv_reader = csv.DictReader(csv_file)


    for csvRow in csv_reader:
        classNbr = csvRow["Class Nbr"]
        data[classNbr] = csvRow
        print(data)

root = {}
root["Class Number"] = data

with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(root, indent=4, sort_keys=True))




