import json

data = {
    "name": "Alice",
    "age": 30,
    "is_student": False,
    "courses": ["Math", "Science", "History"]
}

with open('output.json', 'w') as f:
        json.dump(data, f, indent=4) # indent=4 for pretty-printing