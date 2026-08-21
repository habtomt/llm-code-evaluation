import json
import os
import re
INPUT_FILE = "initial_reference_codes.json"
OUTPUT_DIR = "reference_codes"

# load data
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

def safe_name(name):
    #clean scenario name for folder usage
    name = name.replace(" ", "_")
    name = name.replace("&", "and")
    name = re.sub(r"[^\w\-_.]", "", name)
    return name

def parse_group_key(group_key):
    #   split scenario and task id
    parts = group_key.split("__task_")
    scenario = parts[0]
    task_id = parts[1]
    return scenario, task_id

os.makedirs(OUTPUT_DIR, exist_ok=True)
for group_key, codes in data.items():

    scenario, task_id = parse_group_key(group_key)

    # clean folder name
    scenario_folder = safe_name(scenario)

    folder_path = os.path.join(OUTPUT_DIR, scenario_folder)
    os.makedirs(folder_path, exist_ok=True)

    # save files
    for i, code in enumerate(codes):
        filename = f"task_{task_id}_code_{i+1}.py"
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

total_files = sum(len(v) for v in data.values())

print("Files saved successfully!")
print(f"Total scenarios: {len(set(k.split('__task_')[0] for k in data.keys()))}")
print(f"Total files created: {total_files}")