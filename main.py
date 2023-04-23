import nbt_to_json
import json_to_arrays
import arrays_to_path
import path_to_lua

if __name__ == "__main__":

    # jsonFile = "buildVanilla.json"

    # Convert the NBT file to a JSON file
    # nbt_to_json.nbt_to_json("buildVanilla.nbt", jsonFile)

    # Convert the JSON file to a 3D array of blocks
    # blocks = json_to_arrays.json_to_arrays(jsonFile)

    # Create the image
    # blocks.pretty_print_layer(1)

    # Find the path for the turtle
    matrix = [(0,0,0,0,0),(0,1,1,1,0),(0,1,1,1,0),(0,1,1,1,0),(0,0,0,0,0)]
    # max_fuel = 11
    max_fuel = 100000

    print(arrays_to_path.turtle_path(matrix, max_fuel))

