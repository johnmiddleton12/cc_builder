import python_nbt.nbt as nbt

import json

def nbt_to_json(nbt_path, json_path):
    print("Converting NBT file to JSON file...")
    nbtfile = nbt.read_from_nbt_file(nbt_path)
    json_from_nbt = nbtfile.json_obj(full_json=False)
    with open(json_path, 'w') as f:
        json.dump(json_from_nbt, f)