import os

import lib.nbt_to_json as nbt_to_json
import lib.json_to_arrays as json_to_arrays
import lib.arrays_to_path as arrays_to_path
import lib.paths_to_instructions as paths_to_instructions
import lib.instructions_to_lua as instructions_to_lua

if __name__ == "__main__":

    # fileName = "data/dome.nbt"

    # Convert the NBT file to a JSON file
    # jsonFileName = fileName.replace(".nbt", ".json")
    # nbt_to_json.nbt_to_json(fileName, jsonFileName)

    # Convert the JSON file to a 3D array of blocks
    # blocks = json_to_arrays.json_to_arrays(jsonFileName)
    # matrix = blocks.get_matrix()

    # layer0 = [(0,0,0),(0,0,1),(0,0,0)]
    layer0 = [(1,1,1,1,1), (1,1,1,1,1), (1,1,1,1,1), (1,1,1,1,1), (1,1,1,1,1)]
    layer1 = [(0,0,0,0,0),(0,0,0,0,0),(0,0,0,0,0),(0,0,0,0,0),(0,0,0,0,1)]
    # layer2 = [(0,0,0,0,0),(0,0,0,0,0),(0,0,1,0,0),(0,0,0,0,0),(0,0,0,0,0)]
    # matrix = [layer0, layer1, layer2]
    matrix = [layer0, layer1]

    # Find the paths for the turtle
    fuel = 19
    maxFuel = 22
    starting_pos = (-1, 0)

    paths = []
    for i in range(len(matrix)):
        path, fuel, starting_pos = arrays_to_path.array_to_path(matrix[i], fuel, maxFuel, starting_pos, i)
        print(path)
        paths.append(path)
        
    # Convert the paths to instructions for the turtle
    instructions = paths_to_instructions.paths_to_instructions(paths)

    # Convert the instructions to a Lua file
    if not os.path.exists("out"):
        os.makedirs("out")
    instructions_to_lua.instructions_to_lua(instructions, "out/build.lua")