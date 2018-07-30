import json

with open('env\config.json') as json_data_file:
    data = json.load(json_data_file)


def get(key):
    return data[key]

