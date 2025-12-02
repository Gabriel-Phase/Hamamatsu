import json

input = "4"

with open("saved_procedure.json", "r") as infile:
    data = json.load(infile)

    new_data = {}
    current_new_key = 2
    sorted_keys = sorted(data.keys(), key=int)

    KEY_TO_REMOVE = input

    for old_key in sorted_keys:
        if old_key == KEY_TO_REMOVE:
            continue
        
        value = data[old_key]

        new_key_str = str(current_new_key)
        
        new_data[new_key_str] = value
        
        current_new_key += 1

    with open("saved_procedure.json", "w") as outfile:
        json.dump(new_data, outfile, indent=4)
    