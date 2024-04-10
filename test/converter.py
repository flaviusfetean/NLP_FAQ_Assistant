import json
import csv
import os

json_path = r"D:\GitHub\NLP_FAQ_Assistant\storage\FAQ.json"
csv_path = r"D:\GitHub\NLP_FAQ_Assistant\storage\FAQ.csv"


def convert_json_to_csv():
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        count = 0
        for item in data:
            if count == 0:
                header = item.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(item.values())


if __name__ == "__main__":
    convert_json_to_csv()
    print("Conversion successful.")