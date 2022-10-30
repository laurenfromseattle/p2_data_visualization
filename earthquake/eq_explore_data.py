import json

# Explore the structure of the data.
filename = "data/eq_data_1_day_m1.json"
with open(filename) as f:
    data = json.load(f)

readable_file = "data/readable_eq_data_1_day_m1.json"
with open(readable_file, "w") as f:
    json.dump(data, f, indent=4)
