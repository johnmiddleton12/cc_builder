import nbt_to_json
import json_to_arrays
import arrays_to_path
import paths_to_instructions
import instructions_to_lua

if __name__ == "__main__":

    jsonFileName = "data/buildVanilla.json"

    # Convert the NBT file to a JSON file
    nbt_to_json.nbt_to_json("data/buildVanilla.nbt", jsonFileName)

    # Convert the JSON file to a 3D array of blocks
    blocks = json_to_arrays.json_to_arrays(jsonFileName)
    matrix = blocks.get_matrix()

    # Create an image
    # blocks.pretty_print_layer(1)

    # Find the paths for the turtle
    max_fuel = 100000
    paths = []
    for layer in matrix:   
        path = arrays_to_path.turtle_path(layer, max_fuel)
        paths.append(path)

    # Convert the paths to instructions for the turtle
    instructions = paths_to_instructions.paths_to_instructions(paths)

    # Convert the instructions to a Lua file
    instructions_to_lua.instructions_to_lua(instructions, "buildVanilla.lua")