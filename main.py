import os

import nbt_to_json
import json_to_arrays
import arrays_to_path
import paths_to_instructions
import instructions_to_lua

if __name__ == "__main__":

    fileName = "data/asianBuilding.nbt"
    jsonFileName = fileName.replace(".nbt", ".json")

    # Convert the NBT file to a JSON file
    # nbt_to_json.nbt_to_json(fileName, jsonFileName)

    # Convert the JSON file to a 3D array of blocks
    blocks = json_to_arrays.json_to_arrays(jsonFileName)
    matrix = blocks.get_matrix()

    # Create an image
    # blocks.pretty_print_layer(1)

    # Find the paths for the turtle
    max_fuel = 10000
    paths = []
    starting_pos = (-1, 0)

    min_layer = 50 
    max_layer = 87 
    current_layer = 0

    for layer in matrix:   

        current_layer += 1

        if current_layer > min_layer and current_layer < max_layer:
            # path = arrays_to_path.turtle_path(layer, max_fuel)
            path, starting_pos = arrays_to_path.array_to_path(layer, max_fuel, starting_pos)
            paths.append(path)
        
    # Convert the paths to instructions for the turtle
    instructions = paths_to_instructions.paths_to_instructions(paths)

    # Convert the instructions to a Lua file

    # make out directory if it doesn't exist    
    if not os.path.exists("out"):
        os.makedirs("out")
    instructions_to_lua.instructions_to_lua(instructions, "out/build.lua")