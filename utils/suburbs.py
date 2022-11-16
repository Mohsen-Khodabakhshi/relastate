import json

file_name = 'csvjson.json'


with open(file_name, 'r', encoding='utf-8') as f:
    my_list = json.load(f)

    for idx, obj in enumerate(my_list):
        obj.pop('index', None)
        obj.pop('metro', None)
        obj.pop('date_time', None)
        obj.pop('region', None)
        obj.pop('distance', None)
        obj.pop('duration', None)
        obj.pop('sa3', None)
        obj.pop('sa3name', None)
        obj.pop('region_new', None)

new_file_name = 'new-file.json'

with open(new_file_name, 'w', encoding='utf-8') as f:
    f.write(json.dumps(my_list, indent=2))
