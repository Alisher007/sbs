import json
import csv
dict_a = {}
list_a = []
with open('time.csv', 'r',newline='') as csvFile:    
    filereader = csv.reader(csvFile, delimiter=',')
    for row in filereader:
        list_a.append(
            {
                "model": "booking.timechoice",
                "pk": int(row[0]),
                "fields": {
                "name": row[1]
                }
            }
        )

filename = 'initial.json'
with open(filename, 'w') as file_object:
    json.dump(list_a, file_object)