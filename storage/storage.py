import json


def from_json_as_list():
    db = open(r"D:\GitHub\NLP_FAQ_Assistant\storage\FAQ.json", 'r')
    json_data = json.load(db)
    return json_data
