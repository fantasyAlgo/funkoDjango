import json

with open('funko_pop.json') as json_file:
    data = json.load(json_file)
print(data)

